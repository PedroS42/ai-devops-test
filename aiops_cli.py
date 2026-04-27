import os
import sys
import subprocess

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header():
    header = f"""
{CYAN}====================================================
{BOLD}             DevScope AIOps Toolkit
{RESET}{CYAN}===================================================={RESET}
"""
    print(header)

def run_script(script_name):
    print(f"\n{YELLOW}Running {script_name}...{RESET}\n")
    try:
        subprocess.run([sys.executable, script_name], check=True)
        print(f"\n{GREEN}✔ {script_name} executed successfully.{RESET}\n")
    except subprocess.CalledProcessError:
        print(f"\n{RED}✖ {script_name} encountered an error.{RESET}\n")
    except FileNotFoundError:
        print(f"\n{RED}✖ Could not find {script_name}. Ensure you are in the correct directory.{RESET}\n")

def main():
    while True:
        print_header()
        print("Please choose an action:")
        print(f"  {BOLD}1.{RESET} Inspect and Validate CI/CD Pipelines (ai_pipeline_reviewer.py)")
        print(f"  {BOLD}2.{RESET} Security Gatekeeper for Terraform (ai_reviewer.py)")
        print(f"  {BOLD}3.{RESET} Kubernetes Monitoring and Self-Healing (ai_k8s_agent.py)")
        print(f"  {BOLD}4.{RESET} AI PR Code Reviewer (ai_pr_reviewer.py)")
        print(f"  {BOLD}5.{RESET} Cost Estimate Functionality (cost_estimate.py)")
        print(f"  {BOLD}6.{RESET} IaC Generator with AI (iac_generator.py)")
        print(f"  {BOLD}7.{RESET} Exit")
        
        choice = input(f"\n{CYAN}Enter your choice (1-7): {RESET}")
        
        if choice == '1':
            run_script("ai_pipeline_reviewer.py")
        elif choice == '2':
            run_script("ai_reviewer.py")
        elif choice == '3':
            run_script("ai_k8s_agent.py")
        elif choice == '4':
            run_script("ai_pr_reviewer.py")
        elif choice == '5':
            run_script("cost_estimate.py")
        elif choice == '6':
            run_script("iac_generator.py")
        elif choice == '7':
            print(f"\n{GREEN}Exiting DevScope AIOps Toolkit. Goodbye!{RESET}")
            sys.exit(0)
        else:
            print(f"\n{RED}Invalid choice. Please enter a number between 1 and 7.{RESET}\n")
        
        input(f"{YELLOW}Press Enter to continue...{RESET}")
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()