FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install compliancehub package in editable mode
RUN pip install -e .

ENTRYPOINT ["compliancehub"]
