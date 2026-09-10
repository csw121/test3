# 실시간 접속자 대시보드 (스트레스 테스트)

로컬에서 모바일/브라우저 렌더링 성능을 테스트하기 위한 간단한 FastAPI 앱입니다.

구성요소
- `main.py`: FastAPI 서버 및 `/api/dummy` 엔드포인트 (더미 데이터 50,000건, 2~3초 인위적 지연 포함)
- `static/index.html`: 프론트엔드 페이지 — 페이징 없이 한 번에 50,000건을 DOM에 렌더링합니다.

실행 방법
1. 가상환경을 만들고 활성화합니다.

```bash
python -m venv .venv
.
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

3. 서버 실행
```bash
python main.py
```

4. 모바일 또는 데스크톱 브라우저에서 `http://localhost:8000/` 에 접속합니다.

주의
- 이 앱은 의도적으로 많은 DOM을 생성하고 서버 응답을 지연시킵니다. 실제 운영 환경에서는 사용하지 마세요.

추가 기능
- API 파라미터: `/api/dummy?count=10000&delay_min=1&delay_max=2&cpu_work=100000` 형태로 요청하면 응답 크기와 지연/CPU 모방량을 조절할 수 있습니다.
- 클라이언트 메트릭 수집: 프론트엔드는 `sendBeacon`으로 `/api/metrics`에 렌더링/페치 시간 등의 메트릭을 전송합니다. 로그는 `metrics.log`에 누적됩니다.
- 벤치마크 스크립트: `tools/benchmark.py` 는 API를 여러 번 호출해 응답시간을 CSV로 기록합니다.

벤치마크 사용 예
```bash
python -m pip install -r requirements.txt
python tools/benchmark.py
```
