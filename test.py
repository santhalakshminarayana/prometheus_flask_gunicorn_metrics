import requests
from dataclasses import dataclass
from random import choices
import time
import threading

@dataclass
class URL:
    method: str
    url: str
    data: dict = None

urls = [
    URL("get", "/fetch"),
    URL("get", "/select/10"),
    URL("get", "/select/20"),
    URL("put", "/update_item/10/type_no/30"),
    URL("put", "/update_item/20/type_no/40"),
    URL("put", "/update_item/20/type_no/40"),
    URL("post", "/update_item/10/type_no/30", {"data": ["1", "2", "3"]}),
    URL("post", "/update_item/20/type_no/40", {"data": ["4", "5", "6"]}),
    URL("post", "/update_item/20/type_no/40", {"data": ["7", "8", "9"]}),
    URL("delete", "/update_item/20/type_no/40"),
    URL("delete", "/update_item/20/type_no/30"),
]

base_path = "http://127.0.0.1:4001"
times = [0, 1, 1.5, 2, 2.5, 3, 2, 2.5, 1]
select_k = 10
requests_count = {}

def make_request(url: URL):
    try:
        if url.method == "put":
            requests.request(url.method, base_path + url.url, params={"a": 1, "b": 2})
        elif url.method == "post":
            requests.request(url.method, base_path + url.url, data=url.data)
        else:
            requests.request(url.method, base_path + url.url)
    except Exception as e:
        print(e)

def parallel_requests():
    global requests_count

    cs = choices(urls, k=select_k)
    threads = []
    for url in cs:
        p = threading.Thread(target=make_request, args=(url,), daemon=True)
        req_key = url.method + "_" + url.url
        if requests_count.get(req_key):
            requests_count[req_key] += 1
        else:
            requests_count[req_key] = 1

        threads.append(p)
        p.start()
    
    return threads

def run():
    global requests_count
    requests_count = {}

    threads = []
    print("started running")
    for i in times:
        time.sleep(i)
        threads.extend(parallel_requests())
    
    print("all requests made")

    for thread in threads:
        thread.join()

    print()
    print(f"total requests: {len(times) * select_k}")
    print(requests_count)

if __name__ == "__main__":
    run()