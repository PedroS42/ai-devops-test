import sys
import os
from dotenv import load_dotenv
from groq import Groq
from groq.types.chat import ChatCompletionUserMessageParam

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("\nERROR: No API key found in environment variables.")
    sys.exit(1)

client = Groq(api_key=GROQ_API_KEY)

with open("main.tf", "r") as file:
    code_to_review = file.read()

prompt = f"Act as a Cloud security and terraform expert. Check if this code has any errors (it is meant for Azure), security vulnerabilities, invalid syntax, or bad practices. If it has, you MUST start your response with the exact word 'REJECTED'. Only reject the code if there are undeniable, critical security vulnerabilities or actual syntax errors. Do not reject for stylistic choices or implicit Terraform dependencies. If the code is fine and safe, start with the exact word 'APPROVED'. Then provide a brief explanation. \nTerraform Code: \n{code_to_review}"

messages: list[ChatCompletionUserMessageParam] = [{"role": "user", "content": prompt}]

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    temperature=0.1
)

response_text = response.choices[0].message.content

print("AI Review of the Code:")
print(response_text)
print("\n")

if response_text.strip().upper().startswith("REJECTED"):
    print("\nCRITICAL ERROR: AI has rejected this code! The pipeline will now stop.")
    sys.exit(1) # this tells GitHub: stop pipeline
else:
    print("\nSUCCESS: AI has approved this code.")
    sys.exit(0)