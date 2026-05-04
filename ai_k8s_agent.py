import json
import os
import sys
from groq.types.chat import ChatCompletionUserMessageParam
from kubernetes import client, config
from groq import Groq
from dotenv import load_dotenv
import config_manager

load_dotenv()

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

if not GROQ_API_KEY:
    print("\nERROR: No API key found in environment variables.")
    sys.exit(1)

groq_client = Groq(api_key=GROQ_API_KEY)

config.load_kube_config()
v1 = client.CoreV1Api()

pods = v1.list_namespaced_pod(namespace='default')

if not pods.items:
    print("No pods found.")

for pod in pods.items:
    pod_name = pod.metadata.name


    container_status = pod.status.container_statuses[0] if pod.status.container_statuses else None

    if container_status and not container_status.ready:

        real_state = "Unknown"
        if container_status.state.waiting:
            real_state = container_status.state.waiting.reason
        elif container_status.state.terminated:
            real_state = container_status.state.terminated.reason

        print(f"ALERT: Pod {pod_name} is flawed. State: {real_state}")

        try:
            logs = v1.read_namespaced_pod_log(name=pod_name, namespace='default')
        except Exception as e:
            logs = f"No available logs: {e}"

        print(f"Logs for {pod_name} extracted. Asking AI for diagnosis...\n")

        prompt = f"""Act as an automated Kubernetes Site Reliability Engineer (SRE).
                I have a Pod named '{pod_name}' currently failing with the state '{real_state}'.
                Here are the last logs from the pod:
                {logs}

                Analyze the issue. Since this is a test environment with an aggressive self-healing policy, 
                your FIRST action for any failure (including fatal memory errors) should be to delete the pod 
                so Kubernetes can restart it.

                You MUST reply with a valid JSON object exactly like this:
                {{"action": "delete", "reason": "brief explanation"}}

                Only if you are absolutely certain that deleting the pod will cause critical damage, reply exactly with:
                {{"action": "none", "reason": "brief explanation"}}

                Reply only with the JSON object. Do not add markdown blocks or other text."""


        messages: list[ChatCompletionUserMessageParam] = [{"role": "user", "content": prompt}]

        app_config = config_manager.load_config()
        target_model = app_config.get("self_healing", "llama-3.3-70b-versatile")

        resposta = groq_client.chat.completions.create(
            model=target_model,
            messages=messages,
            temperature=0.1
        )

        response_text = resposta.choices[0].message.content.strip()

        try:
            decision = json.loads(response_text)
            print(f"AI Decision: {decision['action'].upper()}")
            print(f"Reason: {decision['reason']}\n")

            if decision["action"] == "delete":
                print(f"Initiating self healing: Deleting pod '{pod_name}'...")
                v1.delete_namespaced_pod(name=pod_name, namespace='default')
                print(f"Pod '{pod_name}' deleted sucessfully.")
        except json.JSONDecodeError:
            print(f"ERROR: AI response is not a valid JSON. Response was:\n{response_text}")

    else:
            print(f"Pod {pod_name} is working correctly.")