# Airflow Test Pipeline

Airflow 테스트/실습용 파이프라인 프로젝트.

## 구조

```
dags/       DAG 정의 파일
plugins/    커스텀 오퍼레이터 / 훅 / 센서
include/    DAG에서 참조하는 SQL, 설정, 헬퍼 스크립트
tests/      DAG 무결성 및 단위 테스트
```

## 환경 구성

(추후 결정: Docker Compose 또는 Python venv)
