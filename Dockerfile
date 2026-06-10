# 1. 파이썬 가벼운 버전으로 베이스 이미지 선택
FROM python:3.13-slim

# 2. 로컬 구조 재현: /project/clover/ → main.py의 _PROJECT_ROOT = /project
WORKDIR /project

# 3. 종속성 파일 복사 및 설치 (캐싱 활용을 위해 먼저 복사)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 소스 코드를 clover/ 하위에 복사 (from clover.core.* import 경로 일치)
COPY . clover/

# 5. FastAPI 실행 (8000 포트 개방)
EXPOSE 8000
CMD ["uvicorn", "clover.main:app", "--host", "0.0.0.0", "--port", "8000"]
