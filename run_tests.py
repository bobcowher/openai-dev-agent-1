import subprocess

def run_pytest():
    # Command to execute Pytest
    command = ["pytest", "-v", "./output/test.py"]

    try:
        # Run the command and capture output
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE,  # Capture error output
            text=True                # Decode output as text
        )

        return result.returncode, result.stderr + result.stdout

    except FileNotFoundError:
        print("Error: Pytest command not found. Make sure Pytest is installed.")
        return 1