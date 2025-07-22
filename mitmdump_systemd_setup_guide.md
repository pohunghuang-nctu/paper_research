# 將 mitmdump 設定為 Systemd 服務的指南

將 `mitmdump` 設定為一個 `systemd` 服務是確保其在背景長期穩定運行的最佳實踐。相較於 `nohup` 或 `screen`，使用 `systemd` 可以帶來自動重啟、開機自啟以及標準化的服務管理等優點。

以下是詳細的設定步驟。

## 步驟一：建立 Systemd 服務檔案

首先，您需要建立一個服務定義檔。使用 `sudo` 和您偏好的文字編輯器（例如 `nano` 或 `vim`）來建立此檔案：

```bash
sudo nano /etc/systemd/system/mitmdump.service
```

接著，將以下內容複製並貼到檔案中。這是一個通用的範本，請務必根據您的實際環境修改 `User` 和 `ExecStart` 的值。

```ini
[Unit]
Description=mitmproxy in dump mode
# 確保服務在網路連線建立後才啟動
After=network.target

[Service]
# 【請修改】指定執行 mitmdump 的使用者，建議不要使用 root
User=your_username

# 【請修改】指定 mitmdump 的完整路徑以及您需要的任何參數
# 您可以使用 `which mitmdump` 來找到其完整路徑
# 範例: ExecStart=/home/your_username/.local/bin/mitmdump -s /path/to/your/script.py --set flow_detail=0
ExecStart=/usr/local/bin/mitmdump --set flow_detail=0

# (可選) 如果您的腳本需要讀取相對路徑的檔案，請設定工作目錄
# WorkingDirectory=/path/to/your/working/dir

# 設定服務失敗時的自動重啟策略
Restart=always
RestartSec=5

# 將標準輸出與錯誤都導向 systemd journal，這是推薦的作法
StandardOutput=journal
StandardError=journal
# 設定日誌在 journal 中的識別符
SyslogIdentifier=mitmdump

[Install]
# 設定服務在哪個 target 下啟用
WantedBy=multi-user.target
```

## 步驟二：(可選) 設定 rsyslog 將日誌導向獨立檔案

`systemd` 預設會將所有日誌記錄到 `journal`。您可以使用 `journalctl -u mitmdump.service -f` 來查看日誌。如果您偏好將日誌輸出到一個獨立的檔案（例如 `/var/log/mitmdump.log`），可以設定 `rsyslog`。

1.  **建立 rsyslog 設定檔**：
    ```bash
    sudo nano /etc/rsyslog.d/mitmdump.conf
    ```

2.  **貼上以下內容**：
    ```
    if $programname == 'mitmdump' then /var/log/mitmdump.log
    & stop
    ```

3.  **重啟 rsyslog 服務**：
    ```bash
    sudo systemctl restart rsyslog
    ```

## 步驟三：管理 mitmdump 服務

完成設定後，您就可以使用 `systemctl` 指令來管理您的 `mitmdump` 服務了。

1.  **重新載入 Systemd 設定** (讓新服務生效)：
    ```bash
    sudo systemctl daemon-reload
    ```

2.  **啟動服務**：
    ```bash
    sudo systemctl start mitmdump.service
    ```

3.  **查看服務狀態** (確認是否成功執行)：
    ```bash
    sudo systemctl status mitmdump.service
    ```

4.  **設定開機時自動啟動**：
    ```bash
    sudo systemctl enable mitmdump.service
    ```

5.  **停止服務**：
    ```bash
    sudo systemctl stop mitmdump.service
    ```
