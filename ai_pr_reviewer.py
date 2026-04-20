import os
import sys
import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = os.environ.get("REPO_NAME")
PR_NUMBER = os.environ.get("PR_NUMBER")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("ERROR: No GRoQ API key found.")
    sys.exit(1)

client = Groq(api_key=GROQ_API_KEY)

def get_pr_diff():
    if not PR_NUMBER or not GITHUB_TOKEN or not REPO_NAME:
        print("Missing GitHub credentials. Cannot fetch PR diff.")
        return None

    url = f"https://api.github.com/repos/{REPO_NAME}/pulls/{PR_NUMBER}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch PR diff: {response.text}")
        return None

def publish_github_comment(comment):
    if not PR_NUMBER or not GITHUB_TOKEN or not REPO_NAME:
        print("Missing GitHub credentials. Printing comment:")
        print(comment)
        return

    url = f"https://api.github.com/repos/{REPO_NAME}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": comment}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print("Comment published successfully!")
    else:
        print(f"Failed to publish comment: {response.text}")

def main():
    diff_content = get_pr_diff()
    if not diff_content:
        print("No diff content found or not running in a Pull Request.")
        sys.exit(0)

    # In case of large diffs, truncate to avoid token limits
    if len(diff_content) > 10000:
        diff_content = diff_content[:10000] + "\n\n... Diff truncated due to size limit."

    prompt = (f"Act as an expert Code Reviewer. Review the following pull request diff. "
              f"Look for any bugs, security vulnerabilities, architectural flaws, or bad practices. "
              f"If the code looks good, briefly praise the author. "
              f"Format your response neatly in markdown.\n\n"
              f"PR Diff:\n```diff\n{diff_content}\n```")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    review_comment = "### AI Code Review (PR Diff)\n\n" + response.choices[0].message.content

    print(review_comment)
    publish_github_comment(review_comment)

if __name__ == "__main__":
    main()

