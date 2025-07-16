# 如何在 Windows 中設定 PROXY 環境變數

本文將引導您如何在 Windows 系統中設定 `HTTP_PROXY`、`HTTPS_PROXY` 和 `NO_PROXY` 環境變數。這些變數常用於設定應用程式透過代理伺服器 (Proxy Server) 連線到網際網路。

## 變數說明

-   `HTTP_PROXY`: 用於 HTTP 請求的代理伺服器位址。
-   `HTTPS_PROXY`: 用於 HTTPS 請求的代理伺服器位址。
-   `NO_PROXY`: 指定哪些主機名稱或 IP 位址 **不應** 透過代理伺服器連線，而是直接連線。

**變數格式範例:**
-   `HTTP_PROXY`: `http://proxy.example.com:8080`
-   `HTTPS_PROXY`: `http://proxy.example.com:8080` (注意：即使是 HTTPS 的代理，其協定本身通常也是 http)
-   `NO_PROXY`: `localhost,127.0.0.1,.example.com,192.168.0.1` (以逗號分隔的多個項目)

---

## 方法一：使用圖形化使用者介面 (GUI)

這是最常見且直觀的方法，適合大多數使用者。

1.  **開啟「系統內容」**:
    -   按下 `Win` + `R` 鍵開啟「執行」對話方塊。
    -   輸入 `sysdm.cpl` 並按下 Enter。

2.  **進入「環境變數」設定**:
    -   在「系統內容」視窗中，切換到「進階」分頁。
    -   點擊右下角的「環境變數...」按鈕。

3.  **新增或編輯環境變數**:
    -   在「環境變數」視窗中，您可以看到「使用者變數」和「系統變數」兩個區塊。
        -   **使用者變數**: 只對目前登入的使用者生效。
        -   **系統變數**: 對系統上所有使用者生效 (需要系統管理員權限)。
    -   點擊「新增...」按鈕 (在您想設定的變數區塊下)。
    -   **變數名稱**: 輸入 `HTTP_PROXY`、`HTTPS_PROXY` 或 `NO_PROXY`。
    -   **變數值**: 輸入您的代理伺服器位址或不需要代理的主機列表。
    -   點擊「確定」儲存變數。

4.  **完成設定**:
    -   重複步驟 3 以新增所有需要的變數。
    -   完成後，點擊所有開啟視窗的「確定」按鈕。

**注意**: 變更完成後，需要重新啟動命令提示字元、PowerShell 或應用程式，新的環境變數才會生效。

---

## 方法二：使用命令提示字元 (Command Prompt)

### 1. 臨時設定 (僅對目前視窗有效)

這種設定方式只在當前的命令提示字元視窗中有效，關閉後即失效。

```cmd
set HTTP_PROXY=http://your-proxy-server:port
set HTTPS_PROXY=http://your-proxy-server:port
set NO_PROXY=localhost,127.0.0.1
```

### 2. 永久設定 (使用 `setx`)

使用 `setx` 指令可以永久設定環境變數。

-   **設定使用者變數**:
    ```cmd
    setx HTTP_PROXY "http://your-proxy-server:port"
    ```

-   **設定系統變數** (需要以系統管理員身分執行命令提示字元):
    ```cmd
    setx /m HTTP_PROXY "http://your-proxy-server:port"
    ```

**注意**: 使用 `setx` 設定的變數只會在 **新開啟** 的命令提示字元視窗中生效，對目前視窗無效。

---

## 方法三：使用 PowerShell

### 1. 臨時設定 (僅對目前工作階段有效)

這種設定方式只在當前的 PowerShell 工作階段中有效。

```powershell
$env:HTTP_PROXY="http://your-proxy-server:port"
$env:HTTPS_PROXY="http://your-proxy-server:port"
$env:NO_PROXY="localhost,127.0.0.1"
```

### 2. 永久設定

使用 .NET 的 `Environment` 類別可以永久設定環境變數。

-   **設定使用者變數**:
    ```powershell
    [System.Environment]::SetEnvironmentVariable('HTTP_PROXY', 'http://your-proxy-server:port', 'User')
    ```

-   **設定系統變數** (需要以系統管理員身分執行 PowerShell):
    ```powershell
    [System.Environment]::SetEnvironmentVariable('HTTP_PROXY', 'http://your-proxy-server:port', 'Machine')
    ```

**注意**: 與 `setx` 類似，永久設定的變數需要開啟新的 PowerShell 工作階段才會生效。
