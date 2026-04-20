from groq import Groq
from groq.types.chat import ChatCompletionUserMessageParam
from dotenv import load_dotenv
import sys
import glob
import os
import requests

load_dotenv()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = os.environ.get("REPO_NAME")
PR_NUMBER = os.environ.get("PR_NUMBER")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("\nERROR: No API key found in environment variables.")
    sys.exit(1)

client = Groq(api_key=GROQ_API_KEY)


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

        prompt = (f"Act as a DevSecOps CI/CD expert.\n"
                  f"Review this GitHub Action YAML and evaluate based on these rules:\n\n"
                  f"1. SECRETS: Look for hardcoded credentials, API keys, or tokens. ONLY `${{{{ secrets.XYZ }}}}` is allowed. Any hardcoded secret, even if unused, must be REJECTED.\n"
                  f"2. ACTIONS: Flag outdated actions (e.g. prefer v4 over v4.0.0).\n"
                  f"3. BEST PRACTICES: Ensure explicit timeouts and appropriate permissions happen.\n"
                  f"4. DANGEROUS PRACTICES: Flag risky scripts, but '-auto-approve' in terraform apply is ALLOWED.\n\n"
                  f"If it violates any rule, start your response with 'REJECTED'.\n"
                  f"If perfectly secure, start with 'APPROVED'. Explain your findings concisely.\n\n"
                  f"YAML Code:\n{yaml_content}")

    messages: list[ChatCompletionUserMessageParam] = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.1
    )

    response_text = response.choices[0].message.content
    print(response_text)
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