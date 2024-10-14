import argparse
import subprocess
from colorama import Fore, Style
import json


explanations = {
    "C0301": "Line too long: This line exceeds the maximum allowed line length.",
    "C0114": "Missing module docstring: This module should have a docstring explaining its purpose.",
    "C0116": "Missing function or method docstring: All functions should have docstrings describing their behavior.",
    "R0913": "Too many arguments: A function should not have too many arguments, as this can complicate its usage.",
    "R0917": "Too many positional arguments: Avoid having too many positional arguments for better readability.",
    "W0611": "Unused import: Remove this import as it is not used anywhere in the code.",
    "B605": "Starting a process with a shell, possible injection detected: This can lead to security vulnerabilities."
}


def load_config():
    with open('config.json') as config_file:
        return json.load(config_file)


config = load_config()


# Function to run pylint and capture output

def run_pylint(file_path):
    result = subprocess.run(['pylint', file_path], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"{Fore.GREEN}Pylint: No issues found in {file_path}\n{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Pylint Results: \n{Style.RESET_ALL}", format_pylint_output(result.stdout))

# Function to run flake8 and capture output


def run_flake8(file_path):
    result = subprocess.run(['flake8', file_path], capture_output=True, text=True)
    if result.stdout.strip() == "":
        print(f"{Fore.GREEN}Flake8: No issues found in {file_path}\n{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Flake8 Results: \n{Style.RESET_ALL}", format_flake8_output(result.stdout))

# Function to run bandit and capture output


def run_bandit(file_path):
    result = subprocess.run(['bandit', '-r', file_path], capture_output=True, text=True)
    if "No issues identified" in result.stdout:
        print(f"{Fore.GREEN}Bandit: No security issues found in {file_path}\n{Style.RESET_ALL}")

    else:
        print(f"{Fore.YELLOW}Bandit Results: \n{Style.RESET_ALL}", format_bandit_output(result.stdout))

# Format Pylint output


def format_pylint_output(output):
    lines = output.splitlines()
    formatted_output = ""
    for line in lines:
        if ": " in line:
            parts = line.split(":")
            if len(parts) > 3:
                error_code = parts[3].strip().split()[0]  # Get the error code (third part of the split)
                explanation = get_pylint_explanation(error_code)
                formatted_output += f"{line}\nExplanation: {explanation}\n\n"
        else:
            formatted_output += line + "\n"
    return formatted_output


# Format Flake8 output

def format_flake8_output(output):
    lines = output.splitlines()
    formatted_output = ""
    for line in lines:
        if ":" in line:
            formatted_output += f"{line}\n"
            parts = line.split(":")
            if len(parts) > 3:
                error_code = parts[3].strip().split()[0]  # Adjusted extraction of error code
                explanation = get_flake8_explanation(error_code)
                formatted_output += f"Explanation: {explanation}\n\n"
    return formatted_output

# Format Bandit output


def format_bandit_output(output):
    lines = output.splitlines()
    formatted_output = ""
    for line in lines:
        if "Issue:" in line:
            issue_code = line.split("[")[1].split(":")[
                0].strip()  # Extracts code before the colon inside square brackets
            explanation = get_bandit_explanation(issue_code)
            formatted_output += f"{line}\nExplanation: {explanation}\n\n"
        else:
            formatted_output += line + "\n"
    return formatted_output


# Get explanations for common pylint issues


def get_pylint_explanation(error_code):
    pylint_explanations = {
        "C0301": "This line exceeds the maximum allowed line length. Try breaking the line into multiple shorter lines.",
        "C0114": "This module is missing a docstring. Add a docstring at the top of the module to describe its purpose.",
        "C0116": "This function or method is missing a docstring. Add a docstring to describe what the function does.",
        "R0913": "This function has too many arguments. Refactor it to reduce the number of arguments.",
        "R0917": "Too many positional arguments are being used. Consider refactoring the function call.",
        "C0103": "The constant name should be in UPPER_CASE format. Change the name to conform to this convention.",
        "W0611": "This import statement is not used. Remove the unused import to clean up the code."
        # Add more explanations for other codes...
    }
    return pylint_explanations.get(error_code, "No explanation available for this issue.")

# Get explanations for common flake8 issues


def get_flake8_explanation(error_code):
    flake8_explanations = {
        "F401": "This module contains an unused import. Consider removing it to clean up the code.",
        "E501": "This line exceeds the maximum allowed line length. Keep your lines shorter for better readability."
        # Add more explanations for other codes...
    }
    return flake8_explanations.get(error_code, "No explanation available for this issue.")


def get_bandit_explanation(issue_code):
    bandit_explanations = {
        "B605": "Starting a process with a shell can lead to command injection vulnerabilities. Avoid using 'os.system' with untrusted input. Use 'subprocess.run' or similar instead."
        # Add more explanations for other Bandit codes...
    }
    return bandit_explanations.get(issue_code, "No explanation available for this issue.")


def main():
    parser = argparse.ArgumentParser(description="AI-Powered Code Review Assistant")
    parser.add_argument('file', help='Path to the Python file to review')
    args = parser.parse_args()

    file_path = args.file

    print(f"Running code review for {file_path}...\n")

    # Run each tool and print the results with explanations
    run_pylint(file_path)
    run_flake8(file_path)
    run_bandit(file_path)


if __name__ == "__main__":
    main()

