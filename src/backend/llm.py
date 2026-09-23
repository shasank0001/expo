"""Ollama chat client. Structured short prompt + optional thinking."""
import re
import requests

SYSTEM_STRUCTURED = (
    "You are a CSE basics tutor. Use ONLY the context files. Simple English. "
    "Format: 1) Basics (3-5 lines) 2) Example 3) Common mistake (1 line) 4) Exam 2-mark (2 lines). "
    "Cite files as [path] after each part. "
    "If context lacks the answer, say 'Not in my v0 notes' + name the missing topic file. "
    "Never bluff. Max 10 lines total."
)

# Thinking models loop forever on rigid format demands (tested: 14k chars thinking,
# zero content). Think mode gets a minimal instruction and it answers.
SYSTEM_SIMPLE = (
    "You are a CSE basics tutor. Answer using the context. "
    "Simple English. Cite files like [path]. "
    "If the context lacks the answer, say 'Not in my v0 notes'."
)

THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
THINK_OPEN_RE = re.compile(r"<think>.*$", re.DOTALL | re.IGNORECASE)


def strip_think(text: str) -> str:
    text = THINK_RE.sub("", text)
    return THINK_OPEN_RE.sub("", text).strip()  # unclosed tag: drop everything after it


def build_prompt(query: str, chunks: list, tree: str = "", simple: bool = False) -> list:
    context = "\n\n".join(f"FILE: {c['path']}\n{c['body']}" for c in chunks)
    tree_block = f"\nFile tree for this subject:\n{tree}\n" if tree else ""
    user = (
        f"Question: {query}\n{tree_block}\nContext:\n{context if context else '(no-hit)'}\n\n"
        + ("Answer." if simple else "Follow the Format exactly. Cite every factual part.")
    )
    return [{"role": "system", "content": SYSTEM_SIMPLE if simple else SYSTEM_STRUCTURED},
            {"role": "user", "content": user}]


def chat(ollama_host: str, model: str, query: str, chunks: list, temperature: float = 0.2,
         num_ctx: int = 2048, think: bool = False, tree: str = "",
         num_predict: int | None = None) -> tuple:
    """Returns (answer, thinking). Thinking logged, never shown as answer.

    Thinking models spend 1300-1600 tokens in <think> before answering; the default
    num_predict budget gets eaten entirely -> empty content. So think mode needs
    num_predict>=2048 AND num_ctx>=8192 (prompt ~900 + thinking ~1600 + answer ~300).
    """
    if num_predict is None:
        num_predict = 4096 if think else 1024
    if think and num_ctx < 8192:
        num_ctx = 8192
    payload = {
        "model": model,
        "messages": build_prompt(query, chunks, tree, simple=think),
        "stream": False,
        "think": think,
        "options": {"temperature": temperature, "num_ctx": num_ctx, "num_predict": num_predict},
    }
    r = requests.post(f"{ollama_host}/api/chat", json=payload, timeout=180)
    r.raise_for_status()
    msg = r.json().get("message", {})
    thinking = (msg.get("thinking") or "").strip()
    answer = strip_think(msg.get("content") or "")
    return answer, thinking
