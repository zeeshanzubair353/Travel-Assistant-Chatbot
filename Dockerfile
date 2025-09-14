FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN mkdir -p /app/.files /app/.chainlit && \
    touch /app/chainlit.md && \
    chmod -R 777 /app/.files /app/.chainlit /app/chainlit.md

# Set Chainlit environment variables
ENV CHAINLIT_UI=True
ENV CHAINLIT_BROWSER_AUTO_OPEN=false

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]

