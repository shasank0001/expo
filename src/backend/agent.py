"""Agentic retrieval: model sees file tree, picks search terms, can re-search once."""
import requests
from .retriever import retrieve, file_tree

PICKER_SYSTEM = (
    "You pick search terms for a notes filesystem. Reply with ONLY one line: "
    "SEARCH: term1, term2  (2-4 short keywords from the question + file tree). "
    "Or reply ENOUGH if the context already answers the question."
)


def _picker(ollama_host: str, model: str, query: str, tree: str, context_paths: list,
            think: bool, temperature: float = 0.2) -> str:
    user = (f"Question: {query}\n\nFile tree:\n{tree}\n\n"
            f"Already retrieved: {context_paths or '(none)'}\n"
            "Pick search terms or reply ENOUGH.")
    payload = {"model": model, "messages": [
        {"role": "system", "content": PICKER_SYSTEM}, {"role": "user", "content": user}],
        "stream": False, "think": think,
        "options": {"temperature": temperature, "num_ctx": 2048, "num_predict": 256}}
    r = requests.post(f"{ollama_host}/api/chat", json=payload, timeout=120)
    r.raise_for_status()
    import re
    content = r.json()["message"].get("content") or ""
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)
    return re.sub(r"<think>.*$", "", content, flags=re.DOTALL).strip()


def agent_retrieve(ollama_host: str, model: str, subject: str, query: str, top_k: int = 3,
                   think: bool = False, temperature: float = 0.2, max_rounds: int = 2):
    """Returns (chunks, rounds_log, tree). Model drives search terms; BM25 executes."""
    tree = file_tree(subject)
    seen, rounds = {}, []
    # Picker always runs think=False: it must emit SEARCH terms, not essays.
    # Round 1: model picks terms (fallback: raw query)
    try:
        pick = _picker(ollama_host, model, query, tree, [], False, temperature)
    except Exception as e:
        pick = ""
        rounds.append({"round": 1, "picker": f"picker-error: {e}", "terms": [query]})
    if "ENOUGH" in pick.upper() and not seen:
        terms = [query]
    elif pick.upper().startswith("SEARCH:"):
        terms = [t.strip("- ") for t in pick.split(":", 1)[1].split(",") if t.strip()]
        terms = terms or [query]
    else:
        terms = [query]
    if not rounds:
        rounds.append({"round": 1, "picker": pick[:200], "terms": terms})
    for t in terms:
        for c in retrieve(subject, t, top_k):
            seen.setdefault(c["path"], c)
    # round 2: model may refine once
    if max_rounds >= 2:
        try:
            pick2 = _picker(ollama_host, model, query, tree, list(seen)[:6], False, temperature)
        except Exception as e:
            pick2 = ""
            rounds.append({"round": 2, "picker": f"picker-error: {e}", "terms": []})
        else:
            if pick2.upper().startswith("SEARCH:"):
                terms2 = [t.strip("- ") for t in pick2.split(":", 1)[1].split(",") if t.strip()]
                rounds.append({"round": 2, "picker": pick2[:200], "terms": terms2})
                for t in terms2:
                    for c in retrieve(subject, t, top_k):
                        seen.setdefault(c["path"], c)
            else:
                rounds.append({"round": 2, "picker": pick2[:200], "terms": []})
    chunks = sorted(seen.values(), key=lambda c: c["score"], reverse=True)[:top_k]
    return chunks, rounds, tree
