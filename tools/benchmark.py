import time
import csv
import requests

API = "http://127.0.0.1:8000/api/dummy"

def run_rounds(rounds=5, count=50000, delay_min=2.0, delay_max=3.0, cpu_work=200000):
    results = []
    for i in range(rounds):
        params = {
            'count': count,
            'delay_min': delay_min,
            'delay_max': delay_max,
            'cpu_work': cpu_work,
        }
        t0 = time.time()
        r = requests.get(API, params=params, stream=True)
        # consume content to ensure full download time
        _ = r.content
        t1 = time.time()
        duration = t1 - t0
        results.append((i+1, duration, len(r.json())))
        print(f"Round {i+1}: {duration:.3f}s, items={len(r.json())}")

    # save csv
    with open('benchmark_results.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['round','duration_s','items'])
        w.writerows(results)

if __name__ == '__main__':
    run_rounds()
