FROM python:3.12-slim

# matplotlib/pandas need a C toolchain on some platforms to build wheels
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install deps first so this layer is cached unless requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project (app code, templates, static, graph.py, main.py)
COPY . .

# Writable dirs used at runtime for generated charts + matplotlib's font cache
RUN mkdir -p image_dashboards /tmp/matplotlib
ENV MPLCONFIGDIR=/tmp/matplotlib

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
