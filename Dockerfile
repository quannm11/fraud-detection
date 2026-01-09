# 1. Base Image
FROM python:3.9-slim

# 2. Setup: Create working directory
WORKDIR /app

# 3. System Dependencies (Required for XGBoost/LightGBM compilation)
# We use a single RUN command to keep the layer size small
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements first (Layer Caching)
COPY requirements.txt .

# 5. Install Python dependencies with BuildKit Cache (Package Caching)
# This is the "Pro" move you identified
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# 6. Copy Code
# We copy explicitly to avoid accidentally copying junk files
COPY src/ ./src
# Create the data directory (empty) so the code doesn't crash before mounting
RUN mkdir data

# 7. Default Command
CMD ["python", "src/train.py"]