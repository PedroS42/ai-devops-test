import os
import sys
import subprocess
import config_manager

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

def settings_menu():
    AVAILABLE_MODELS = [
        "llama-3.3-70b-versatile",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
        "deepseek-r1-distill-llama-70b"
    ]

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{CYAN}===================================================={RESET}")
        print(f"{BOLD}             Settings - AI Models{RESET}")
        print(f"{CYAN}===================================================={RESET}")
        
        config = config_manager.load_config()
        if not config:
            print(f"{RED}No configuration found.{RESET}")
            return

        features = list(config.keys())
        for idx, feature in enumerate(features, 1):
            print(f"  {BOLD}{idx}.{RESET} {feature.replace('_', ' ').title()}: {YELLOW}{config[feature]}{RESET}")
        print(f"  {BOLD}{len(features) + 1}.{RESET} Back to Main Menu")

        choice = input(f"\n{CYAN}Select a feature to change (1-{len(features) + 1}): {RESET}")

        try:
            choice_idx = int(choice)
            if choice_idx == len(features) + 1:
                break
            if 1 <= choice_idx <= len(features):
                feature_to_change = features[choice_idx - 1]
                print(f"\n{CYAN}Available Models:{RESET}")
                for m_idx, model_name in enumerate(AVAILABLE_MODELS, 1):
                    print(f"  {BOLD}{m_idx}.{RESET} {model_name}")
                
                model_choice = input(f"\n{CYAN}Select a new model (1-{len(AVAILABLE_MODELS)}): {RESET}")
                
                try:
                    m_choice_idx = int(model_choice)
                    if 1 <= m_choice_idx <= len(AVAILABLE_MODELS):
                        new_model = AVAILABLE_MODELS[m_choice_idx - 1]
                        config_manager.update_config(feature_to_change, new_model)
                        print(f"\n{GREEN}✔ Model updated successfully to {new_model}!{RESET}\n")
                    else:
                        print(f"{RED}Invalid model choice.{RESET}")
                except ValueError:
                    print(f"{RED}Please enter a valid number for model selection.{RESET}")
                    
                input(f"{YELLOW}Press Enter to continue...{RESET}")
            else:
                print(f"{RED}Invalid choice.{RESET}")
                input(f"{YELLOW}Press Enter to continue...{RESET}")
        except ValueError:
            print(f"{RED}Please enter a valid number.{RESET}")
            input(f"{YELLOW}Press Enter to continue...{RESET}")

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
        print(f"  {BOLD}7.{RESET} Settings (Configure AI Models)")
        print(f"  {BOLD}8.{RESET} Exit")
        
        choice = input(f"\n{CYAN}Enter your choice (1-8): {RESET}")
        
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
            settings_menu()
            continue
        elif choice == '8':
            print(f"\n{GREEN}Exiting DevScope AIOps Toolkit. Goodbye!{RESET}")
            sys.exit(0)
        else:
            print(f"\n{RED}Invalid choice. Please enter a number between 1 and 8.{RESET}\n")
        
        input(f"{YELLOW}Press Enter to continue...{RESET}")
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()