import ollama
import sys
import glob


workflows_folders = [".github/workflows/*.yml", ".github/workflows/*.yaml"]
pipelines_files = []

for folder in workflows_folders:
    pipelines_files.extend(glob.glob(folder))

if not pipelines_files:
    print("\nERROR: No pipelines found in this directory.")
    sys.exit(0)

has_failures = False

for file in pipelines_files:
    print("Analyzing: " + file)

    with open(file, "r") as f:
        yaml_content = f.read()

    prompt = (f"Act as a DevSecOps Engineer and CI/CD specialist.\n"
              f"Review the following GitHub Action YAML file.\n"
              f"Look for:\n"
              f"1 - Hardcoded secrets or tokens (IGNORE standard GitHub Secrets syntax like ${{{{ secrets.XYZ }}}}).\n"
              f"2 - Outdated actions (e.g., recommend v4 instead of v4.0.0).\n"
              f"3 - Missing Best practices (missing timeouts on jobs, lack of specific permissions).\n"
              f"4 - Dangerous practices (but allow -auto-approve for Terraform if it is a standard automated CI/CD flow).\n"
              f"If you find any undeniable, critical security flaws, start your response exactly with 'REJECTED'.\n"
              f"If the YAML is generally secure, start with 'APPROVED'. Do not reject for minor stylistic issues.\n"
              f"Provide a concise explanation.\n\n"
              f"YAML Code:\n{yaml_content}")

    response = ollama.chat(
        model="llama3.1",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        stream=True,
        options={
            "temperature": 0.0
        }
    )

    response_text = ""

    for chunk in response:
        content = chunk["message"]["content"]
        print(content, end="", flush=True)
        response_text += content

    print("\n")

    if response_text.strip().upper().startswith("REJECTED"):
        print(f"❌ CRITICAL ERROR: AI has rejected the code in {file}!")
        has_failures = True
    else:
        print(f"\nSUCCESS: AI has approved {file}.")

if has_failures:
    print("\nERROR: Pipeline failed because one or more workflows were rejected")
    sys.exit(1)
else:
    print("\nSUCCESS: All pipelines succeeded")
    sys.exit(0)