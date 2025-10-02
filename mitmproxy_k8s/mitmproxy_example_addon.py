"""
mitmproxy 自訂腳本範例

此腳本展示如何攔截、記錄和修改 HTTP/HTTPS 流量
同時實作記憶體優化最佳實踐
"""

from mitmproxy import http, ctx
import json
import re
from datetime import datetime


class TrafficInterceptor:
    """流量攔截器類別"""
    
    def __init__(self):
        self.request_count = 0
        self.response_count = 0
        
    def request(self, flow: http.HTTPFlow) -> None:
        """
        處理 HTTP 請求
        在請求送出前執行
        """
        self.request_count += 1
        
        # 記錄請求資訊
        ctx.log.info(f"[Request #{self.request_count}] {flow.request.method} {flow.request.pretty_url}")
        
        # 範例 1: 修改請求標頭
        # flow.request.headers["X-Custom-Header"] = "MyValue"
        
        # 範例 2: 攔截特定 URL
        if "api.example.com" in flow.request.pretty_url:
            ctx.log.warn(f"攔截到 API 請求: {flow.request.pretty_url}")
            # 可以在這裡修改請求內容
            # flow.request.query["debug"] = "true"
        
        # 範例 3: 記錄 POST 資料
        if flow.request.method == "POST":
            content_type = flow.request.headers.get("content-type", "")
            if "application/json" in content_type:
                try:
                    body = flow.request.content.decode("utf-8")
                    json_data = json.loads(body)
                    ctx.log.info(f"POST JSON: {json.dumps(json_data, indent=2, ensure_ascii=False)}")
                except Exception as e:
                    ctx.log.error(f"解析 JSON 失敗: {e}")

    def response(self, flow: http.HTTPFlow) -> None:
        """
        處理 HTTP 回應
        在回應送回客戶端前執行
        """
        self.response_count += 1
        
        # 記錄回應資訊
        status_emoji = "✅" if 200 <= flow.response.status_code < 300 else "❌"
        ctx.log.info(
            f"[Response #{self.response_count}] {status_emoji} "
            f"{flow.response.status_code} "
            f"{flow.request.method} {flow.request.pretty_url}"
        )
        
        # 記錄回應大小
        content_length = len(flow.response.content) if flow.response.content else 0
        ctx.log.info(f"  └─ Size: {content_length} bytes")
        
        # 範例 1: 修改回應標頭
        # flow.response.headers["X-Modified-By"] = "mitmproxy"
        
        # 範例 2: 記錄 JSON 回應
        content_type = flow.response.headers.get("content-type", "")
        if "application/json" in content_type:
            try:
                body = flow.response.content.decode("utf-8")
                json_data = json.loads(body)
                # 只記錄部分資料以避免日誌過大
                ctx.log.info(f"Response JSON keys: {list(json_data.keys())}")
            except Exception as e:
                ctx.log.error(f"解析回應 JSON 失敗: {e}")
        
        # 範例 3: 攔截錯誤回應
        if flow.response.status_code >= 400:
            ctx.log.error(
                f"HTTP Error {flow.response.status_code}: "
                f"{flow.request.method} {flow.request.pretty_url}"
            )
        
        # 範例 4: 修改回應內容 (謹慎使用)
        # if "text/html" in content_type:
        #     html = flow.response.content.decode("utf-8", errors="ignore")
        #     modified_html = html.replace("Original", "Modified")
        #     flow.response.content = modified_html.encode("utf-8")
        
        # ⚠️ 重要：處理完畢後釋放記憶體
        # 這是防止記憶體洩漏的關鍵步驟
        flow.live = False

    def error(self, flow: http.HTTPFlow) -> None:
        """
        處理錯誤
        當請求或回應發生錯誤時執行
        """
        if flow.error:
            ctx.log.error(f"Flow Error: {flow.error.msg}")
            ctx.log.error(f"  └─ URL: {flow.request.pretty_url}")


# 實例化攔截器
addons = [TrafficInterceptor()]


# === 進階範例：過濾特定流量 ===

class APIMonitor:
    """
    API 監控器
    只記錄特定 API 的流量
    """
    
    def __init__(self):
        # 定義要監控的 API 模式
        self.patterns = [
            r"api\.github\.com",
            r"api\.openai\.com",
            r".*\.googleapis\.com",
        ]
        
    def _should_monitor(self, url: str) -> bool:
        """檢查 URL 是否符合監控條件"""
        return any(re.search(pattern, url) for pattern in self.patterns)
    
    def response(self, flow: http.HTTPFlow) -> None:
        if self._should_monitor(flow.request.pretty_url):
            # 記錄 API 呼叫詳情
            ctx.log.info(f"[API Monitor] {flow.request.method} {flow.request.pretty_url}")
            ctx.log.info(f"  └─ Status: {flow.response.status_code}")
            ctx.log.info(f"  └─ Time: {flow.response.timestamp_end - flow.request.timestamp_start:.2f}s")
        
        # 釋放記憶體
        flow.live = False


# === 進階範例：效能分析 ===

class PerformanceAnalyzer:
    """
    效能分析器
    記錄慢速請求
    """
    
    def __init__(self):
        self.slow_threshold = 2.0  # 秒
        
    def response(self, flow: http.HTTPFlow) -> None:
        if flow.response and flow.request.timestamp_start:
            duration = flow.response.timestamp_end - flow.request.timestamp_start
            
            if duration > self.slow_threshold:
                ctx.log.warn(
                    f"⚠️  Slow Request ({duration:.2f}s): "
                    f"{flow.request.method} {flow.request.pretty_url}"
                )
        
        # 釋放記憶體
        flow.live = False


# === 進階範例：請求重寫 ===

class RequestRewriter:
    """
    請求重寫器
    將請求重導向到不同的伺服器（例如從生產環境導向測試環境）
    """
    
    def request(self, flow: http.HTTPFlow) -> None:
        # 範例：將 production API 重導向到 staging
        if "api.production.com" in flow.request.pretty_host:
            flow.request.host = "api.staging.com"
            ctx.log.info(f"重導向請求到 staging: {flow.request.pretty_url}")


# === 進階範例：快取模擬 ===

class CacheSimulator:
    """
    快取模擬器
    對特定請求回傳快取的回應（可用於離線測試）
    """
    
    def __init__(self):
        self.cache = {}
        
    def request(self, flow: http.HTTPFlow) -> None:
        cache_key = f"{flow.request.method}:{flow.request.pretty_url}"
        
        if cache_key in self.cache:
            ctx.log.info(f"從快取回傳: {cache_key}")
            flow.response = self.cache[cache_key]
            
    def response(self, flow: http.HTTPFlow) -> None:
        # 只快取 GET 請求
        if flow.request.method == "GET" and flow.response.status_code == 200:
            cache_key = f"{flow.request.method}:{flow.request.pretty_url}"
            self.cache[cache_key] = flow.response
            
        # 釋放記憶體
        flow.live = False


# === 選擇要啟用的 addon ===
# 取消註解以啟用對應的功能

# addons = [TrafficInterceptor()]
# addons = [APIMonitor()]
# addons = [PerformanceAnalyzer()]
# addons = [RequestRewriter()]
# addons = [CacheSimulator()]

# 也可以同時啟用多個
# addons = [
#     TrafficInterceptor(),
#     APIMonitor(),
#     PerformanceAnalyzer(),
# ]


def load(loader):
    """
    載入配置
    在 mitmproxy 啟動時執行
    """
    ctx.log.info("=" * 50)
    ctx.log.info("mitmproxy 自訂腳本已載入")
    ctx.log.info(f"啟用的 addons: {[type(addon).__name__ for addon in addons]}")
    ctx.log.info("=" * 50)


def done():
    """
    清理資源
    在 mitmproxy 關閉時執行
    """
    ctx.log.info("mitmproxy 腳本已卸載")
