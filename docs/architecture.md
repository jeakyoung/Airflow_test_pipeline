# Architecture

Apache Airflow 3.3.1, CeleryExecutor 기반. `docker-compose.yaml`은 Airflow 공식 템플릿을 사용.

## 컨테이너 구성

| 서비스 | 역할 |
|---|---|
| postgres | 메타데이터 DB (DAG 상태, 실행 기록, 커넥션/변수) |
| redis | Celery 메시지 브로커 (스케줄러 → 워커로 태스크 전달) |
| airflow-scheduler | DAG를 평가해서 실행할 태스크를 큐에 올림 |
| airflow-dag-processor | `dags/` 폴더의 파이썬 파일을 파싱 (스케줄러와 분리된 전용 프로세스) |
| airflow-worker | 큐에서 태스크를 꺼내 실제 실행 |
| airflow-triggerer | deferrable(비동기 대기) 오퍼레이터 처리 |
| airflow-apiserver | REST API + 웹 UI (`localhost:8080`) |

## 볼륨 마운트

- `dags/` → DAG 정의 파일. 여기에 `.py` 추가하면 자동 인식 (기본 5분 주기 스캔)
- `plugins/` → 커스텀 오퍼레이터/훅/센서
- `logs/` → 태스크별 실행 로그 (git 추적 안 함)
- `config/` → `airflow.cfg` 등 런타임 설정 (git 추적 안 함)

## 설정

- `LOAD_EXAMPLES: false` — 예제 DAG 비활성화, 직접 만든 DAG만 표시
- `.env`의 `AIRFLOW_UID` — 컨테이너와 호스트 파일 권한 매칭용 (git 추적 안 함, `.env.example` 참고)
