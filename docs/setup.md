# Setup

## 사전 준비 (Docker 미설치 시)

```bash
bash setup_docker.sh
```

설치 후 그룹 변경 적용을 위해 터미널을 재접속하거나 `newgrp docker` 실행.

## 환경 변수

```bash
cp .env.example .env
```

`AIRFLOW_UID`는 기본값(1000)을 대부분의 리눅스 단일 사용자 환경에서 그대로 써도 됨. 다르면 `id -u` 값으로 교체.

## 실행

```bash
docker compose up airflow-init   # DB 마이그레이션 + 계정 생성 (최초 1회)
docker compose up -d             # 전체 서비스 기동
```

## 접속

- UI: http://localhost:8080
- 계정: `airflow` / `airflow`

## DAG 추가

`dags/` 폴더에 `.py` 파일 추가. 기본적으로 5분마다 스캔하며, 즉시 반영하려면:

```bash
docker compose restart airflow-dag-processor
```

## 종료

```bash
docker compose down          # 컨테이너만 정리 (DB 데이터는 volume에 유지)
docker compose down -v       # 볼륨까지 완전 삭제 (초기화)
```
