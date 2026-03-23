from groq import Groq
from groq.types.chat import ChatCompletionUserMessageParam
import os, sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.environ.get("GROQ_API_KEY")

if not API_KEY:
    print("Please set GROQ_API_KEY environment variable")
    exit(1)


client = Groq(api_key=API_KEY)

with open("codigo_com_erro.py", "r") as file:
    code_to_review = file.read()

prompt = f"Act as a DevOps engineer. Check if this code has any errors, security vulnerabilities, or bad practices. If it has, you MUST start your response with the exact word 'REJECTED'. If the code is fine and safe, start with the exact word 'APPROVED'. Then provide a brief explanation. \nCode: \n{code_to_review}"


messages: list[ChatCompletionUserMessageParam] = [
    {
        "role": "user",
        "content": prompt,
    }
]
# Send the prompt to the Gemini API and get the response
response = client.chat.completions.create(
    messages=messages,
    model="llama-3.3-70b-versatile"
)

print("AI Review of the Code:")
print(response.choices[0].message.content)
response2 = response.choices[0].message.content

if response2.strip().upper().startswith("REJECTED"):
    print("\nCRITICAL ERROR: AI has rejected this code! The pipeline will now stop.")
    sys.exit(1) # this tells github: stop pipeline 
else:
    print("\nSUCCESS: AI has approved this code.")
    sys.exit(0)