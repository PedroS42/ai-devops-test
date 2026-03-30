import ollama
import sys

with open("main.tf", "r") as file:
    code_to_review = file.read()

prompt = f"Act as a Cloud security and terraform expert. Check if this code has any errors (it is meant for Azure), security vulnerabilities, invalid syntax, or bad practices. If it has, you MUST start your response with the exact word 'REJECTED'. Only reject the code if there are undeniable, critical security vulnerabilities or actual syntax errors. Do not reject for stylistic choices or implicit Terraform dependencies. If the code is fine and safe, start with the exact word 'APPROVED'. Then provide a brief explanation. \nTerraform Code: \n{code_to_review}"

# Send the prompt to the Gemini API and get the response
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

print("AI Review of the Code:")
for chunk in response:
    content = chunk['message']['content']
    print(content, end='', flush=True)
    response_text += content

print("\n")

if response_text.strip().upper().startswith("REJECTED"):
    print("\nCRITICAL ERROR: AI has rejected this code! The pipeline will now stop.")
    sys.exit(1) # this tells GitHub: stop pipeline
else:
    print("\nSUCCESS: AI has approved this code.")
    sys.exit(0)