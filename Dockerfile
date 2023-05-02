FROM python:3.8-slim-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    curl \
    gnupg \
    unzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /src/*.deb

# set display port to avoid crash
ENV DISPLAY=:99

RUN pip install Flask selenium beautifulsoup4

COPY app.py /app.py

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]
