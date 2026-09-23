"""Filesystem BM25 retriever with title-boost + synonyms. No vectorDB for v0."""
from pathlib import Path
from rank_bm25 import BM25Okapi

DATA_ROOT = Path(__file__).resolve().parents[2] / "data"

# NOTE: 'for' removed from STOP — it is a keyword (for-loop). 1-char tokens dropped instead.
STOP = {"explain", "describe", "tell", "give", "what", "why", "how", "is", "are", "the", "a", "an",
        "in", "of", "with", "to", "me", "lines", "line", "words", "simple", "example", "please", "short",
        "detail", "details", "note", "notes", "my", "v0"}

SYNONYMS = {
    "subquery": ["nested", "queries", "nested-queries", "subqueries"],
    "subqueries": ["nested", "queries"],
    "for-loop": ["for", "loop"],
    "dml": ["dml-basics", "insert", "update", "delete"],
    "ddl": ["ddl-basics", "create", "alter", "drop"],
    "3nf": ["third-normal-form", "normal"],
    "bcnf": ["bcnf-basics", "normal"],
    "joins": ["join", "joins-sql"],
    "arrays": ["array", "arrays"],
}


def _tokenize(text: str):
    toks = []
    for t in text.lower().replace("/", " ").replace("-", " ").replace("_", " ").split():
        t = "".join(ch for ch in t if ch.isalnum())
        if not t or len(t) < 2 or t in STOP:
            continue
        toks.append(t)
        toks.extend(SYNONYMS.get(t, []))
    return toks


def _parse_md(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    if text.startswith("---"):
        parts = text.split("---", 2)
        body = parts[2] if len(parts) > 2 else text
    else:
        body = text
    return body.strip()


def _load_subject_docs(subject: str, title_boost: bool = True):
    subdir = DATA_ROOT / subject
    files = sorted(subdir.rglob("*.md")) if subdir.exists() else []
    docs = []
    for f in files:
        body = _parse_md(f)
        slug = f.stem  # topic filename = strong signal
        boosted = f"{slug} {slug} {slug} {body}" if title_boost else body
        docs.append({
            "path": str(f.relative_to(DATA_ROOT.parents[0])),
            "body": body,
            "slug": slug,
            "tokens": _tokenize(boosted),
        })
    return docs


def file_tree(subject: str) -> str:
    subdir = DATA_ROOT / subject
    files = sorted(subdir.rglob("*.md")) if subdir.exists() else []
    return "\n".join(f"- {f.relative_to(DATA_ROOT.parents[0])}" for f in files)


def retrieve(subject: str, query: str, top_k: int = 3, title_boost: bool = True):
    docs = _load_subject_docs(subject, title_boost)
    if not docs:
        return []
    bm25 = BM25Okapi([d["tokens"] for d in docs])
    scores = bm25.get_scores(_tokenize(query))
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)[:top_k]
    return [{"path": d["path"], "score": float(s), "body": d["body"][:1200]} for d, s in ranked]
