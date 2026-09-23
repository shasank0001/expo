# Run v0 (local laptop)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ollama list  # confirm model tags match config/models.yaml
uvicorn backend.main:app --port 8000
# new terminal:
streamlit run app.py --server.port 8501
