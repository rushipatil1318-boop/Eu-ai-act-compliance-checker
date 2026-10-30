FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
# Render and similar platforms give the port in $PORT; 8501 is the local default
CMD streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0
