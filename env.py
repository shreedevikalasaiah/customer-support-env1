import random
from typing import Optional

TICKETS = {
    "classify_ticket": [
        {"ticket": "My invoice shows a charge I did not authorise.", "answer": "billing", "options": ["billing", "technical", "general"]},
        {"ticket": "The app keeps crashing when I upload a file.", "answer": "technical", "options": ["billing", "technical", "general"]},
        {"ticket": "What are your business hours?", "answer": "general", "options": ["billing", "technical", "general"]},
    ],
    "draft_response": [
        {"ticket": "I was double charged last month!", "keywords": ["apologise", "refund", "investigate", "resolve"]},
        {"ticket": "I cannot log in even after resetting my password.", "keywords": ["sorry", "steps", "support", "account", "help"]},
        {"ticket": "How do I upgrade my plan?", "keywords": ["upgrade", "plan", "settings", "billing", "steps"]},
    ],
    "resolve_escalation": [
        {"ticket": "I contacted support 5 times and nobody fixed it. I want a refund and to cancel!", "keywords": ["sincerely apologise", "escalate", "immediate", "refund", "manager", "resolve", "personal"], "min_length": 80},
    ],
}

class CustomerSupportEnv:
    TASKS = ["classify_ticket", "draft_response", "resolve_escalation"]
    def __init__(self):
        self._task_id = None; self._sample = None; self._done = True; self._step_count = 0

    def reset(self, task_id=None):
        self._task_id = task_id or random.choice(self.TASKS)
        if self._task_id not in TICKETS:
            raise ValueError(f"Unknown task_id: {self._task_id}")
        self._sample = random.choice(TICKETS[self._task_id])
        self._done = False; self._step_count = 0
        return self._observation()

    def step(self, action):
        if self._done:
            raise RuntimeError("Call reset() before step().")
        self._step_count += 1
        reward = self._grade(action)
        self._done = True
        return {"observation": self._observation(), "reward": reward, "done": self._done, "info": {"task": self._task_id, "steps": self._step_count}}

    def state(self):
        return {"task_id": self._task_id, "done": self._done, "step_count": self._step_count, "sample": self._sample}

    def list_tasks(self):
        return [{"id": "classify_ticket", "difficulty": "easy"}, {"id": "draft_response", "difficulty": "medium"}, {"id": "resolve_escalation", "difficulty": "hard"}]

    def _observation(self):
        if self._sample is None:
            return {"ticket": None, "task": None}
        obs = {"task": self._task_id, "ticket": self._sample["ticket"]}
        if self._task_id == "classify_ticket":
            obs["options"] = self._sample["options"]
        return obs

    def _grade(self, action):
        t = self._task_id
        if t == "classify_ticket":
            return 1.0 if action.get("category", "").strip().lower() == self._sample["answer"] else 0.0
        if t == "draft_response":
            resp = action.get("response", "").lower()
            if not resp: return 0.0
            hits = sum(1 for kw in self._sample["keywords"] if kw in resp)
            score = hits / len(self._sample["keywords"])
            if len(resp.split()) >= 20: score = min(1.0, score + 0.1)
            return round(score, 4)
        if t == "resolve_escalation":
            resp = action.get("response", "").lower()
            if not resp: return 0.0
            kws = self._sample["keywords"]
            hits = sum(1 for kw in kws if kw in resp)
            length_score = min(1.0, len(resp.split()) / self._sample.get("min_length", 50))
            return round(0.6 * hits/len(kws) + 0.4 * length_score, 4)
        return 0.0
