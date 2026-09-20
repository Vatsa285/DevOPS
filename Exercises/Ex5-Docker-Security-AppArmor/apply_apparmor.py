"""
Script to apply AppArmor profile and run Docker container with security restrictions.
Uses Docker SDK for Python.
"""
import subprocess
import sys

def load_apparmor_profile(profile_path):
    """Load AppArmor profile using apparmor_parser"""
    try:
        result = subprocess.run(
            ['sudo', 'apparmor_parser', '-r', '-W', profile_path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"[SUCCESS] AppArmor profile loaded from {profile_path}")
        else:
            print(f"[ERROR] Failed to load AppArmor profile: {result.stderr}")
            sys.exit(1)
    except FileNotFoundError:
        print("[ERROR] apparmor_parser not found. Install with: sudo apt-get install apparmor-utils")
        sys.exit(1)

def run_container_with_apparmor(image_name, profile_name):
    """Run Docker container with AppArmor profile applied"""
    cmd = [
        'docker', 'run', '-d',
        '--name', 'secure-flask-app',
        '--security-opt', f'apparmor={profile_name}',
        '-p', '5000:5000',
        image_name
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        container_id = result.stdout.strip()
        print(f"[SUCCESS] Container started with ID: {container_id}")
        return container_id
    else:
        print(f"[ERROR] Failed to start container: {result.stderr}")
        return None

def test_restricted_actions(container_name):
    """Test that restricted actions are blocked by AppArmor"""
    print("\n--- Testing Restricted Actions ---\n")

    # Test 1: Try to read /etc/shadow
    print("[TEST 1] Attempting to read /etc/shadow...")
    result = subprocess.run(
        ['docker', 'exec', container_name, 'cat', '/etc/shadow'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("  [PASS] Access to /etc/shadow denied (as expected)")
    else:
        print("  [FAIL] Access to /etc/shadow was allowed!")

    # Test 2: Try to execute curl
    print("[TEST 2] Attempting to execute curl...")
    result = subprocess.run(
        ['docker', 'exec', container_name, 'curl', 'http://localhost'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("  [PASS] Execution of curl denied (as expected)")
    else:
        print("  [FAIL] Execution of curl was allowed!")

    # Test 3: Try to write to /usr directory
    print("[TEST 3] Attempting to write to /usr...")
    result = subprocess.run(
        ['docker', 'exec', container_name, 'touch', '/usr/testfile'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("  [PASS] Write to /usr denied (as expected)")
    else:
        print("  [FAIL] Write to /usr was allowed!")

    # Test 4: Verify Flask app is accessible
    print("[TEST 4] Testing Flask app accessibility...")
    result = subprocess.run(
        ['curl', '-s', 'http://localhost:5000/'],
        capture_output=True, text=True
    )
    if "secure Flask application" in result.stdout:
        print("  [PASS] Flask app is running and accessible")
    else:
        print("  [INFO] Flask app response:", result.stdout[:100] if result.stdout else "No response")


if __name__ == "__main__":
    PROFILE_PATH = "/etc/apparmor.d/my-apparmor-profile"
    IMAGE_NAME = "flask-apparmor"
    PROFILE_NAME = "my-apparmor-profile"

    print("=== Docker Security with AppArmor ===\n")

    # Step 1: Load AppArmor profile
    load_apparmor_profile(PROFILE_PATH)

    # Step 2: Run container with AppArmor
    container_id = run_container_with_apparmor(IMAGE_NAME, PROFILE_NAME)

    if container_id:
        # Step 3: Test restricted actions
        import time
        print("\nWaiting 5 seconds for container to start...")
        time.sleep(5)
        test_restricted_actions("secure-flask-app")

    print("\n=== Exercise Complete ===")
    print("To clean up: docker stop secure-flask-app && docker rm secure-flask-app")
