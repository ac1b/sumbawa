FROM python:3.12-slim-bookworm

# System deps for Chromium (Playwright/Patchright)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libdbus-1-3 libxcb1 libxkbcommon0 libx11-6 \
    libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 \
    libgbm1 libpango-1.0-0 libcairo2 libasound2 libatspi2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install scrapling with fetchers (includes Chromium)
RUN pip install --no-cache-dir "scrapling[fetchers]" && scrapling install

COPY app.py /app/app.py
WORKDIR /app

EXPOSE 8100
CMD ["python", "app.py"]
