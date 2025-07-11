# 在 Debian/Ubuntu 上安裝 Windsurf IDE

這份指南將引導您透過 `apt` 套件管理器，在 Debian、Ubuntu 或其他 deb-based Linux 發行版上安裝 Windsurf IDE。

## 步驟一：加入 Windsurf 的 GPG 金鑰與軟體來源

首先，我們需要讓您的系統信任 Windsurf 的軟體來源，並將其加入到您的套件管理器設定中。

1.  **安裝必要工具**：
    確保您已安裝 `wget` 和 `gpg`。

    ```bash
    sudo apt-get update
    sudo apt-get install wget gpg
    ```

2.  **加入 GPG 金鑰與軟體來源**：
    執行以下指令來下載 Windsurf 的 GPG 金鑰，並設定軟體來源。

    ```bash
    # 下載並安裝 GPG 金鑰
    wget -qO- "https://windsurf-stable.codeiumdata.com/wVxQEIWkwPUEAGf3/windsurf.gpg" | gpg --dearmor | sudo tee /etc/apt/keyrings/windsurf-stable.gpg > /dev/null

    # 將 Windsurf 的軟體來源加入設定檔
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/windsurf-stable.gpg] https://windsurf-stable.codeiumdata.com/wVxQEIWkwPUEAGf3/apt stable main" | sudo tee /etc/apt/sources.list.d/windsurf.list > /dev/null
    ```

## 步驟二：更新套件列表

加入新的軟體來源後，需要更新本地的套件列表，以取得最新的套件資訊。

```bash
# 安裝 apt-transport-https 以確保可以透過 https 下載
sudo apt-get install apt-transport-https

# 更新您的套件列表
sudo apt-get update
```

## 步驟三：安裝 Windsurf IDE

現在，您可以直接透過 `apt` 指令來安裝 Windsurf。

```bash
sudo apt-get install windsurf
```

安裝完成後，您應該可以在您的應用程式選單中找到並啟動 Windsurf IDE。
