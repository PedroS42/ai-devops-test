from dotenv import load_dotenv
from groq import Groq
import os
import re
import sys

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("\nERROR: No API key found in environment variables.")
    sys.exit(1)

client = Groq(api_key=GROQ_API_KEY)

# Color codes for terminal
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def get_user_inputs():
    print(f"\n{BOLD} IAC Generator with AI {RESET}\n")

    dir = input("Enter the directory where you want to generate the IaC files (e.g., './iac_output'): ") or "./iac_output"
    cloud = input("Enter the cloud provider (e.g., 'AWS', 'Azure', 'GCP'): ") or "azure"

    desc = input("Enter a brief description of the infrastructure you want to generate: ")
    if not desc:
        print(f"\n{RED} ERROR: No description provided. {RESET}")
        sys.exit(1)

    print("\nAnswer the following questions (ENTER for default values): ")
    proj_name = input("Project name [myproject]: ") or "myproject"
    envs = input("Environments (comma-separated) [staging, prod]: ") or "staging, prod"

    return dir, cloud, desc, proj_name, envs


def generate_iac(dir, cloud, desc, proj_name, envs):

    print(f"\n{YELLOW} Generating iac for: {desc}... {RESET}\n")

    prompt = f"""Act as a Senior Cloud and DevOps Engineer expert in Terraform.
    Your task is to write production-ready Terraform code for {cloud.upper()}.
    
    Project Details:
    - Project Name: {proj_name}
    - Environments needed: {envs}
    - Architecture Requirements: {desc}
    
    CRITICAL INSTRUCTIONS FOR OUTPUT FORMAT:
    You must output multiple files. For EACH file, use EXACTLY this format:
    
    ### [relative/path/to/file.tf]
    ```hcl
    # File content here
    ```
    
    Make sure to include necessary files like:
    - providers.tf
    - variables.tf
    - main.tf (or split by resource like network.tf, compute.tf, databases.tf)
    - outputs.tf
    - envs/ (folder with .tfvars files for the requested environments)
    
    Do not add extra explanations outside of the file blocks. Just output the files."""


    answer = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return answer.choices[0].message.content


def extract_files_and_save(ia_text, base_dir):
    # Use REGEX expressions to find all blocks in the requested format
    standard = re.compile(r"###\s*\[?(.+?)\]?\n.*?```(?:hcl|terraform|tf|json|yaml)?\n(.*?)```", re.DOTALL)
    matches = standard.findall(ia_text)

    if not matches:
        print(f"\n{RED} ERROR: No files found in the AI response. {RESET}")
        return

    print(f"\n{len(matches)} generated files. Review each one before confirming:\n")

    for path, content in matches:
        print(f"{GREEN}[NEW]{RESET} {path.strip()}")

    confirm = input("\nDo you want to save these files? (y/n): ").lower()

    if confirm != 'y':
        print(f"\n{RED} Aborting file save. {RESET}")
        return

    for path, content in matches:
        clean_path = path.strip().strip("/") # clean spaces and initial "/"
        full_path = os.path.join(base_dir, clean_path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

    print(f"\n{GREEN} All files saved successfully in {base_dir}! {RESET}\n")

def main():
    dir, cloud, desc, proj_name, envs = get_user_inputs()
    ia_text = generate_iac(dir, cloud, desc, proj_name, envs)
    extract_files_and_save(ia_text, dir)

if __name__ == "__main__":
    main()