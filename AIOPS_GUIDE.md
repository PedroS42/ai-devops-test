# DevScope AIOps Toolkit - Project Architecture & Guidelines

Below is a quick, direct guide to how this project is structured, the AI mechanics behind it, and how to operate it.

---

## 🤖 AI Configuration (The What, Where, and How)

**Q: What AI model is used?**
**A:** By default, all features use `llama-3.3-70b-versatile` for an excellent balance of speed and deep reasoning. However, the system also supports:
* `mixtral-8x7b-32768` (for massive file inputs/PR diffs)
* `deepseek-r1-distill-llama-70b` (for complex, advanced reasoning)
* `llama3-8b-8192` (for blazing-fast responses)
* `gemma2-9b-it` (Google's lightweight model)

**Q: Where is the AI model running?**
**A:** The models run on the **Groq cloud platform**. Our scripts interact with them via the Groq API (`groq` python library). This provides ultra-fast inference speeds without requiring local hardware.

**Q: How can I easily change the AI model?**
**A:** You absolutely **do not** need to edit Python code!
1. Launch the CLI toolkit: `python aiops_cli.py`
2. Select option **7. Settings**.
3. Choose the specific workflow you want to change (e.g., *IaC Generation* or *PR Review*).
4. Select your desired model from the interactive list.
5. The changes are instantly saved to `config.yml` and will be respected by both local executions and GitHub Actions pipelines.

---

## ⚙️ Features Overview

**How does the IaC Generator work?**
Takes user prompts and outputs fully structured, production-ready Terraform code (Azure by default) split into proper files (`main.tf`, `variables.tf`, etc.), powered by the AI's understanding of Infrastructure as Code.

**How does the PR Reviewer work?**
Triggered automatically on GitHub. It intercepts the `git diff` of any Pull Request, reads the code changes, and writes an automated comment approving or rejecting the PR. If rejected, it halts the pipeline.

**How does the Pipeline Validator work?**
Scans `.yaml` and `.yml` GitHub Action files to enforce DevSecOps rules—like rejecting hardcoded secrets, spotting outdated actions, and warning about risky scripts.

**How does the Terraform Security Gatekeeper work?**
Reviews `.tf` files for security flaws, bad practices, and syntax errors. It acts as an intelligent shield, blocking the CI/CD pipeline if critical infrastructure vulnerabilities are detected.

**What is the Auto-Merge Functionality?**
If the AI completely approves your Pull Request or pipeline changes without finding errors, it automatically squashes and merges the PR, enabling a seamless, automated DevSecOps workflow.

**How is the Infrastructure Cost Estimated?**
Using a combination of the `infracost` CLI tool (which calculates precise Azure costs based on the `.tf` files) and our AI FinOps agent, which analyzes the generated JSON breakdown to provide top actionable saving recommendations.

**How does Kubernetes Self-Healing work?**
A Python script continuously surveys a Minikube cluster via the `kubernetes` Python API. If a Pod is found failing, its logs are extracted and sent to the AI. The AI analyzes the log and makes an autonomous decision to safely restart/heal the pod, if possible.

---

## 🚀 Execution Environments

**1. Local (CLI)**
Everything can be run locally via `aiops_cli.py` (The Interactive Terminal Application). This is best for generating IaC, checking costs, and testing Kubernetes loops.

**2. GitHub Actions (CI/CD)**
The protective operations happen automatically in the Cloud:
* `pipeline_validator.yml`: Guards against bad pipeline creation.
* `pr_reviewer.yml`: Reads code diffs upon Pull Request creation.
* `ai-review.yml`: Audits Terraform code and applies it securely. 
If the AI encounters critical errors, it explicitly fails the CI/CD job using `sys.exit(1)`, functioning as an intelligent security gatekeeper!
* If the above scripts pass, the `terraform apply` step is executed, which updates the infrastructure in Azure.

