# 1. Ubuntu 이미지 사용
FROM ubuntu:22.04

# 2. 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. requirements.txt 복사 후 패키지 설치
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 5. 전체 코드 복사
COPY . .

# 6. FastAPI 앱 실행
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]