# mitmdump 記憶體消耗優化策略

`mitmdump` 因其預設將所有網路流量 (flows) 保留在記憶體的行為，可能導致記憶體用量持續增長。以下提供三種有效降低其記憶體消耗的方法。

## 1. 處理大型流量 (Streaming)

如果您的流量中包含許多大型檔案（如影片、圖片、軟體更新等），這些檔案的 body 會被完整讀入記憶體。您可以啟用串流模式，讓 `mitmdump` 將大型的 body 直接寫入暫存檔案，而不是保存在記憶體中。

在啟動 `mitmdump` 時加入以下參數：

```bash
mitmdump --set stream_large_bodies=1m
```

這會將所有大於 1MB 的 request/response body 串流到磁碟。您可以根據需求調整大小（例如 `100k`, `5m`）。

## 2. 在腳本中主動釋放流量 (Flows)

這是最有效的方法。如果您使用自訂腳本 (`-s your_script.py`) 來處理流量，您可以在處理完畢後，明確地將流量從 `mitmdump` 的視野中移除，從而讓記憶體回收機制可以釋放它。

在您的 Python 腳本中，您可以這樣做：

```python
from mitmproxy import http
from mitmproxy import ctx

def response(flow: http.HTTPFlow) -> None:
    # 在這裡對 flow 進行您需要的處理
    # 例如：分析、紀錄、修改等
    # ...

    # 處理完畢後，設定 live 為 False，mitmdump 就會將它從 view 中移除
    # 這能有效釋放記憶體
    flow.live = False
```

將 `flow.live = False` 這一行加到您的處理函數（如 `response` 或 `request`）的結尾，是官方和社群推薦的最佳實踐。

## 3. 定期重啟

雖然這不是最優雅的解決方案，但如果上述方法因故無法實施，定期重啟 `mitmdump` 服務也是一個簡單粗暴但有效的辦法，可以避免記憶體無限增長。

---

### 總結建議

強烈建議您優先嘗試**方法 2**，在您的腳本中加入 `flow.live = False`。如果您的流量中確實有大檔案，可以再搭配**方法 1** (`--set stream_large_bodies=1m`) 一起使用。這樣應該能將 `mitmdump` 的記憶體用量控制在一個相對穩定且合理的範圍內。
