import time
import random
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.get("/api/dummy")
def get_dummy(count: int = 50000, delay_min: float = 2.0, delay_max: float = 3.0, cpu_work: int = 200000):
    """
    더미 데이터 생성 API
    - count: 반환할 항목 수 (기본 50,000)
    - delay_min, delay_max: 블로킹 sleep 범위 (초)
    - cpu_work: 반복문으로 모방할 CPU 작업량
    """
    # 인위적 지연: 블로킹 sleep
    time.sleep(random.uniform(delay_min, delay_max))
    # 가벼운 계산 반복으로 CPU 부하 모방
    for _ in range(max(0, int(cpu_work))):
        pass

    # 더미 데이터 생성
    data = [
        {"id": i, "name": f"Item {i}", "value": random.random()}
        for i in range(max(0, int(count)))
    ]
    return JSONResponse(content=data)


@app.post("/api/metrics")
async def post_metrics(request: Request, background_tasks: BackgroundTasks):
    """클라이언트 측 성능 메트릭을 수집하여 파일에 기록합니다."""
    try:
        payload = await request.json()
    except Exception:
        payload = {"error": "invalid json"}

    def write_log(p):
        with open("metrics.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    background_tasks.add_task(write_log, payload)
    return JSONResponse(content={"status": "ok"})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
