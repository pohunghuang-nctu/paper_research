from mitmproxy import http
from mitmproxy import ctx

def request(flow: http.HTTPFlow) -> None:
    """
    這個函數會被 mitmproxy 對每個通過的 HTTP/HTTPS 請求呼叫。
    """
    # 檢查請求的目標主機是否為 github.com
    # 並且請求的路徑是否包含 'git-receive-pack'，這是 git push 的關鍵特徵
    if flow.request.host == "github.com" and "git-receive-pack" in flow.request.path:
        
        # 在 mitmproxy 的事件日誌中印出一條訊息，方便除錯
        ctx.log.info(f"[*] Blocking git push request to: {flow.request.pretty_url}")
        
        # 建立一個 HTTP 403 Forbidden 回應並將其發送回客戶端 (Git)
        # 這樣 Git 就會收到一個明確的錯誤，而不是單純的連線中斷
        flow.response = http.HTTPResponse.make(
            403,  # HTTP 狀態碼：禁止
            b"Git push to github.com has been blocked by mitmproxy.",  # 回應內容
            {"Content-Type": "text/plain"}  # 回應標頭
        )
