import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置
URL = "http://bgp1984.eicp.net/sangao/Question/select"
NUM_CLIENTS = 60          # 模拟 60 台终端
REQUESTS_PER_CLIENT = 5   # 每台终端发 5 次请求
TIMEOUT = 30              # 超时时间（秒）

# 线程安全的列表，用于收集结果
results = []
results_lock = threading.Lock()

def send_request(client_id, request_num):
    start_time = time.time()
    try:
        response = requests.get(URL, timeout=TIMEOUT)
        elapsed = time.time() - start_time
        success = response.status_code == 200
        status_code = response.status_code
    except Exception as e:
        elapsed = time.time() - start_time
        success = False
        status_code = None
        error = str(e)
    else:
        error = None

    result = {
        "client_id": client_id,
        "request_num": request_num,
        "elapsed": elapsed,
        "success": success,
        "status_code": status_code,
        "error": error
    }

    with results_lock:
        results.append(result)

    # 可选：打印每条请求日志（调试用，正式运行可注释掉）
    # print(f"[Client {client_id:2d}-{request_num}] {'OK' if success else 'FAIL'} "
    #       f"({elapsed:.2f}s, code={status_code})")

    return result

def main():
    print(f"开始压力测试：{NUM_CLIENTS} 个并发客户端，每个发送 {REQUESTS_PER_CLIENT} 次请求")
    print(f"目标 URL: {URL}\n")

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=NUM_CLIENTS) as executor:
        futures = []
        for client_id in range(1, NUM_CLIENTS + 1):
            for req in range(1, REQUESTS_PER_CLIENT + 1):
                futures.append(executor.submit(send_request, client_id, req))

        # 等待所有任务完成
        for future in as_completed(futures):
            pass  # 结果已通过回调收集

    total_time = time.time() - start_time
    total_requests = len(results)
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    # 统计
    if successful:
        avg_response_time = sum(r["elapsed"] for r in successful) / len(successful)
        max_time = max(r["elapsed"] for r in successful)
        min_time = min(r["elapsed"] for r in successful)
    else:
        avg_response_time = max_time = min_time = 0

    print("\n" + "="*60)
    print("压力测试结果汇总")
    print("="*60)
    print(f"总请求数:       {total_requests}")
    print(f"成功请求数:     {len(successful)}")
    print(f"失败请求数:     {len(failed)}")
    print(f"成功率:         {len(successful)/total_requests*100:.1f}%")
    print(f"总耗时:         {total_time:.2f} 秒")
    print(f"平均响应时间:   {avg_response_time:.3f} 秒")
    print(f"最快响应:       {min_time:.3f} 秒")
    print(f"最慢响应:       {max_time:.3f} 秒")

    if failed:
        print("\n部分错误示例（最多显示5条）:")
        for err in failed[:5]:
            print(f"  Client {err['client_id']}-{err['request_num']}: {err['error']}")

if __name__ == "__main__":
    main()