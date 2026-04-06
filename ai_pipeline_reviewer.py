import ollama
import sys
import glob
import os
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = os.environ.get("REPO_NAME")
PR_NUMBER = os.environ.get("PR_NUMBER")


def publicar_comentario_github(comentario):
    if not PR_NUMBER or not GITHUB_TOKEN or not REPO_NAME:
        print(
            "Aviso: Não estou a correr numa Pull Request ou faltam credenciais do GitHub. A imprimir apenas no terminal:")
        print(comentario)
        return

    url = f"https://api.github.com/repos/{REPO_NAME}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": comentario}

    resposta = requests.post(url, headers=headers, json=data)
    if resposta.status_code == 201:
        print("✅ Comentário publicado na Pull Request com sucesso!")
    else:
        print(f"❌ Erro ao publicar comentário: {resposta.status_code} - {resposta.text}")

workflows_folders = [".github/workflows/*.yml", ".github/workflows/*.yaml"]
pipelines_files = []

for folder in workflows_folders:
    pipelines_files.extend(glob.glob(folder))

if not pipelines_files:
    print("\nERROR: No pipelines found in this directory.")
    sys.exit(0)

has_failures = False


pr_comment = "AIOps Pipeline Review\n\nI am the AI Agent responsible for reviewing the YAML files. Here are the results:\n\n"


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

    # Append the AI's response for this file to the overall PR comment
    pr_comment += f"### 📄 File: `{file}`\n{response_text}\n\n---\n"


    if response_text.strip().upper().startswith("REJECTED"):
        print(f"❌ CRITICAL ERROR: AI has rejected the code in {file}!")
        has_failures = True
    else:
        print(f"\nSUCCESS: AI has approved {file}.")

if has_failures:
    print("\nERROR: Pipeline failed because one or more workflows were rejected")
    publicar_comentario_github(pr_comment)
    sys.exit(1)
else:
    print("\nSUCCESS: All pipelines succeeded")
    sys.exit(0)