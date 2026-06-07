import os
import sys
import requests
import subprocess
from groq import Groq
from groq.types.chat import ChatCompletionUserMessageParam
from dotenv import load_dotenv
import config_manager

load_dotenv()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = os.environ.get("REPO_NAME")
PR_NUMBER = os.environ.get("PR_NUMBER")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("ERROR: No GRoQ API key found.")
    sys.exit(1)

client = Groq(api_key=GROQ_API_KEY)


def _read_git_diff(*git_args):
    result = subprocess.run(
        ["git", *git_args],
        capture_output=True,
        check=True,
    )
    return result.stdout.decode("utf-8", errors="replace").strip()

def get_pr_diff():
    if not PR_NUMBER or not GITHUB_TOKEN or not REPO_NAME:
        print("Missing GitHub credentials. Attempting to fetch local git diff...")
        for git_args in (("diff", "--no-color", "main"), ("diff", "--no-color", "HEAD"), ("diff", "--no-color", "--cached")):
            try:
                diff_text = _read_git_diff(*git_args)
                if diff_text:
                    return diff_text
            except (subprocess.CalledProcessError, FileNotFoundError, UnicodeDecodeError) as e:
                print(f"Local git diff attempt {' '.join(git_args)} failed: {e}")
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
              f"If it has critical issues, you MUST start your response with the exact word 'REJECTED'. "
              f"If the code looks good and safe, start your response with the exact word 'APPROVED'. "
              f"Format your response neatly in markdown.\n\n"
              f"PR Diff:\n```diff\n{diff_content}\n```")

    app_config = config_manager.load_config()
    target_model = app_config.get("pr_review", "llama-3.3-70b-versatile")

    messages: list[ChatCompletionUserMessageParam] = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model=target_model,
        messages=messages,
        temperature=0.1
    )

    review_comment = "### AI Code Review (PR Diff)\n\n" + response.choices[0].message.content

    print(review_comment)
    publish_github_comment(review_comment)

    if response.choices[0].message.content.strip().upper().startswith("REJECTED"):
        print("\nCRITICAL ERROR: AI has rejected this pull request! The pipeline will now stop.")
        sys.exit(1)
    else:
        print("\nSUCCESS: AI has approved this pull request.")
        sys.exit(0)

if __name__ == "__main__":
    main()
