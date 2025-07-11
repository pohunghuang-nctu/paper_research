# 在 Linux 上設定 Chrome 政策以允許 Proxy 整合式驗證

本文件說明如何在 Linux 系統上為 Google Chrome 設定 `AuthServerAllowlist` 政策，以允許瀏覽器自動向指定的 Proxy 伺服器進行整合式驗證（例如 Kerberos 或 NTLM），實現單一登入（SSO）並避免重複跳出要求輸入帳號密碼的視窗。

## 步驟

### 1. 建立政策目錄

Chrome 會在特定目錄中尋找給所有使用者套用的託管政策 (Managed Policies)。您需要使用 `sudo` 權限來建立這些目錄。

打開終端機並執行以下指令：

```bash
sudo mkdir -p /etc/opt/chrome/policies/managed
```

*   `/etc/opt/chrome/policies/managed`：這個路徑是給 Google Chrome 瀏覽器讀取託管政策設定的。

### 2. 建立政策 JSON 檔案

在剛剛建立的 `managed` 目錄中，建立一個 JSON 檔案來定義您的政策。檔案名稱可以自訂，但必須以 `.json` 結尾。我們這裡使用 `auth_policy.json` 作為範例。

使用您偏好的文字編輯器（例如 `nano` 或 `vim`）建立此檔案：

```bash
sudo nano /etc/opt/chrome/policies/managed/auth_policy.json
```

### 3. 撰寫 JSON 內容

在 `auth_policy.json` 檔案中，貼上以下內容。請務必將 `proxy.mycompany.com` 換成您實際的 Proxy 伺服器主機名稱。

```json
{
  "AuthServerAllowlist": "proxy.mycompany.com,*.mycompany.com"
}
```

**說明：**
*   `AuthServerAllowlist`：這是政策的名稱。
*   `"proxy.mycompany.com,*.mycompany.com"`：這是允許清單。
    *   您可以填寫一個或多個主機名稱，用逗號 `,` 分隔。
    *   支援使用萬用字元 `*`。例如 `*.mycompany.com` 會允許所有 `mycompany.com` 子網域下的伺服器。
    *   **注意**：請勿在最後一個主機名稱後面加上逗號。

編輯完成後，儲存並關閉檔案。

### 4. 重新啟動 Chrome 並驗證

政策設定完成後，必須完全關閉並重新啟動 Google Chrome 瀏覽器，新的政策才會生效。

驗證步驟：
1.  重新啟動 Chrome。
2.  在網址列輸入 `chrome://policy` 並按下 Enter。
3.  在政策頁面中，您應該能找到名為 `AuthServerAllowlist` 的政策，其「狀態」應為「確定」，且「值」為您剛剛設定的主機名稱。

如果政策成功顯示，代表您已設定完成。Chrome 現在會自動對清單中的 Proxy 伺服器進行整合式驗證。
