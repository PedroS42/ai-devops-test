import sys
import os
from dotenv import load_dotenv
from groq import Groq
from groq.types.chat import ChatCompletionUserMessageParam
import glob
import config_manager

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("\nERROR: No API key found in environment variables.")
    sys.exit(1)

client = Groq(api_key=GROQ_API_KEY)

tf_files = glob.glob("**/*.tf", recursive=True)
if not tf_files:
    print("No Terraform files found.")
    sys.exit(0)

has_failures = False

for file_path in tf_files:
    print(f"\nAnalyzing: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        code_to_review = file.read()

    if not code_to_review.strip():
        print("Skipping empty file.")
        continue

    prompt = f"Act as a Cloud security and terraform expert. Check if this code has any errors (it is meant for Azure), security vulnerabilities, invalid syntax, or bad practices. If it has, you MUST start your response with the exact word 'REJECTED'. Only reject the code if there are undeniable, critical security vulnerabilities or actual syntax errors. Do not reject for stylistic choices or implicit Terraform dependencies. If the code is fine and safe, start with the exact word 'APPROVED'. Then provide a brief explanation. \nTerraform Code: \n{code_to_review}"

    messages: list[ChatCompletionUserMessageParam] = [{"role": "user", "content": prompt}]

    app_config = config_manager.load_config()
    target_model = app_config.get("iac_validation", "llama-3.3-70b-versatile")

    response = client.chat.completions.create(
        model=target_model,
        messages=messages,
        temperature=0.1
    )

    response_text = response.choices[0].message.content

    print("AI Review of the Code:")
    print(response_text)
    print("\n")

    if response_text.strip().upper().startswith("REJECTED"):
        print(f"❌ CRITICAL ERROR: AI has rejected this code in {file_path}!")
        has_failures = True
    else:
        print(f"✅ SUCCESS: AI has approved this code in {file_path}.")

if has_failures:
    print("\nCRITICAL ERROR: AI has rejected one or more Terraform files! The pipeline will now stop.")
    sys.exit(1) # this tells GitHub: stop pipeline
else:
    print("\nSUCCESS: AI has approved all Terraform code.")
    sys.exit(0)