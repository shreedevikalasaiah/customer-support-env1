import os, json, time, httpx
from openai import OpenAI

API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME   = os.environ.get("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN     = os.environ.get("HF_TOKEN", "")
ENV_URL      = os.environ.get("ENV_URL", "http://localhost:7860")

client = OpenAI(api_key=HF_TOKEN, base_url=API_BASE_URL)
TASKS = ["classify_ticket", "draft_response", "resolve_escalation"]

def call_env(method, path, body=None):
    url = f"{ENV_URL}{path}"
    r = httpx.post(url, json=body or {}, timeout=60) if method == "POST" else httpx.get(url, timeout=60)
    r.raise_for_status()
    return r.json()

def get_agent_action(task_id, observation):
    ticket = observation.get("ticket", "")
    options = observation.get("options", [])
    if task_id == "classify_ticket":
        prompt = f"Classify this support ticket into one of {options}.\nTicket: {ticket}\nReply with ONLY the category word."
        resp = client.chat.completions.create(model=MODEL_NAME, messages=[{"role":"user","content":prompt}], max_tokens=10)
        return {"category": resp.choices[0].message.content.strip().lower()}
    else:
        tone = "sincerely apologetic, offering immediate refund and manager escalation" if task_id == "resolve_escalation" else "empathetic and professional"
        prompt = f"You are a customer support agent. Respond to this ticket in a {tone} tone (min 3 sentences).\nTicket: {ticket}\nWrite ONLY the reply."
        resp = client.chat.completions.create(model=MODEL_NAME, messages=[{"role":"user","content":prompt}], max_tokens=300)
        return {"response": resp.choices[0].message.content.strip()}

def run_task(task_id):
    obs = call_env("POST", "/reset", {"task_id": task_id})
    print(json.dumps({"type": "[START]", "task": task_id, "observation": obs}))
    action = get_agent_action(task_id, obs)
    result = call_env("POST", "/step", {"action": action})
    reward = result.get("reward", 0.0)
    print(json.dumps({"type": "[STEP]", "task": task_id, "action": action, "reward": reward, "done": result.get("done")}))
    print(json.dumps({"type": "[END]", "task": task_id, "total_reward": reward}))
    return reward

if __name__ == "__main__":
    scores = {}
    for task in TASKS:
        try:
            scores[task] = run_task(task)
        except Exception as e:
            print(json.dumps({"type": "[END]", "task": task, "error": str(e)}))
            scores[task] = 0.0
        time.sleep(1)
    print("\n=== Final Scores ===")
    for task, score in scores.items():
        print(f"  {task}: {score:.4f}")
    print(f"  Average: {sum(scores.values())/len(scores):.4f}")
