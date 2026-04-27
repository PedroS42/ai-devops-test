import os
import sys
import json
import subprocess

from dotenv import load_dotenv
from groq import Groq

GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("ERROR: No GRoQ API key found.")
    sys.exit(1)

client = Groq(api_key=GROQ_API_KEY)

def run_infracost(dir):
    print(f"\n{CYAN}Calling infracost to calculate costs...{RESET}")
    try:
        result = subprocess.run(["infracost", "breakdown", "--path", dir, "--format", "json"], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except FileNotFoundError:
        print(f"{RED}ERROR: Infracost is not installed, or not found in PATH.{RESET}")
        print("Run: 'winget install infracost' and after 'infracost auth login")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error running Infracost:{RESET}\n{e.stderr}")
        sys.exit(1)

def finops_ai_analysis(client, infracost_data):
    total_cost = infracost_data.get("totalMonthlyCost", "0.00")

    resource_summary = []
    for project in infracost_data.get("projects", []):
        for resource in project.get("breakdown", {}).get("resources", []):
            resource_summary.append({
                "resource": resource.get("name"),
                "montly_cost": resource.get("monthlyCost")
            })

    print(f"{YELLOW}Calling AI for analysis...{RESET}")

    prompt = f"""Act as a Senior Cloud FinOps Expert for Microsoft Azure.
        I have a Terraform infrastructure with an exact estimated total monthly cost of ${total_cost}.
        Here is the breakdown by resource:
        {json.dumps(resource_summary, indent=2)}

        Please provide:
        1. A concise analysis of where the budget is going.
        2. Top 3 actionable recommendations to optimize and reduce this cost in Azure (e.g., Reserved Instances, auto-scaling, cheaper SKUs).

        Keep it professional, objective and well-formatted.
        """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    return total_cost, response.choices[0].message.content

def main():
    print(f"\n{BOLD}Cost Estimate Funcionality{RESET}")

    dir = input("Enter the directory path of your Terraform code [./iac_output]: ") or "./iac_output"

    if not os.path.exists(dir):
        print(f"{RED}ERROR: Directory '{dir}' does not exist or was not found.{RESET}")
        sys.exit(1)

    infracost_data = run_infracost(dir)
    total_cost, ai_analysis = finops_ai_analysis(client, infracost_data)

    print("\n" + "="*60)
    print(f"Estimated Total Cost:{BOLD}{GREEN}{total_cost} / month{RESET}")
    print("="*60)
    print(f"\n{BOLD}AI analysis and saving opportunities:{RESET}\n")
    print(ai_analysis)
    print("="*60 + "\n")

if __name__ == "__main__":
    main()