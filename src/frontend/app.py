"""Streamlit frontend. No retrieval / no Ollama here. Calls FastAPI only."""
import requests
import streamlit as st

BACKEND = "http://localhost:8000"

st.set_page_config(page_title="CSE Assistant v0", layout="wide")
st.title("CSE Assistant v0 — C / ML / DBMS (thin-notes demo)")

subs = requests.get(f"{BACKEND}/subjects").json() if True else ["c", "ml", "dbms"]
try:
    models_cfg = requests.get(f"{BACKEND}/models").json()
    model_names = [m["ollama"] for m in models_cfg]
except Exception:
    model_names = ["lfm2.5-2.6b", "gemma3:4b"]

with st.sidebar:
    subject = st.selectbox("Subject", subs)
    model = st.selectbox("Model (Ollama tag)", model_names)
    top_k = st.slider("top_k files", 1, 5, 3)

if "history" not in st.session_state:
    st.session_state.history = []

q = st.text_input("Ask a basics question")
if st.button("Ask") and q:
    with st.spinner("Retrieving + generating..."):
        r = requests.post(f"{BACKEND}/query", json={
            "subject": subject, "model": model, "query": q, "top_k": top_k,
        }, timeout=180)
        if r.status_code != 200:
            st.error(r.text)
        else:
            data = r.json()
            st.session_state.history.append((q, data))
            # feedback hooks
            c1, c2 = st.columns(2)
            if c1.button("👍", key=f"up-{data['query_id']}"):
                requests.post(f"{BACKEND}/feedback", json={"query_id": data["query_id"], "thumbs": 1, "missing": False})
            if c2.button("Missing info", key=f"miss-{data['query_id']}"):
                requests.post(f"{BACKEND}/feedback", json={"query_id": data["query_id"], "missing": True})

for q, data in reversed(st.session_state.history):
    st.markdown(f"**Q:** {q}")
    st.markdown(data["answer"])
    st.caption(f"Sources: {', '.join(s['path'] for s in data['sources'])} | {data['latency_ms']}ms | {data['model']}")
    with st.expander("Debug: retrieved chunks + scores"):
        st.json(data["sources"])
    st.divider()
