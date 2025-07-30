# 透過擴充功能與 MCP 伺服器取得 VS Code 狀態：實作指南

本文件將引導您建立一個簡單的系統，讓外部應用程式（例如 AI 代理）可以透過模型內容協定（MCP）來取得 Visual Studio Code 當前開啟的工作區（Workspace）資訊。

此架構包含兩個核心元件：
1.  **VS Code 擴充功能 (Reporter)**：讀取 VS Code 內部的工作區狀態，並在狀態變更時，主動將資訊匯報給本地伺服器。
2.  **本地 MCP 伺服器 (Provider)**：一個輕量級的後端服務，接收來自擴充功能的更新，並依照 MCP 規範提供資料給外部查詢。

---

## Part 1: 建立 VS Code 擴充功能 (The Reporter)

首先，我們需要一個能與 VS Code API 互動的擴充功能。

### 步驟 1: 產生擴充功能專案

如果您尚未安裝，請先安裝 Yeoman 和 VS Code Extension Generator。

```bash
npm install -g yo generator-code
```

接著，產生一個新的 TypeScript 或 JavaScript 擴充功能專案。

```bash
yo code
```

在互動式問答中，選擇 'New Extension (JavaScript)' 並填寫基本資訊。

### 步驟 2: 撰寫擴充功能程式碼

打開 `extension.js` 檔案，並用以下程式碼覆蓋其內容。這段程式碼會在擴充功能啟動及工作區變更時，將當前的路徑發送到我們的本地 MCP 伺服器。

```javascript
// In extension.js

const vscode = require('vscode');
const http = require('http');

// MCP 伺服器的位置
const MCP_SERVER_HOST = 'localhost';
const MCP_SERVER_PORT = 3000; // 確保這個埠號與您的伺服器設定一致

/**
 * 取得當前工作區路徑並發送到 MCP 伺服器
 */
function updateWorkspaceStatus() {
    // 優先使用 workspaceFile (適用於 .code-workspace)
    // 其次使用 workspaceFolders (適用於單一資料夾)
    const workspaceFile = vscode.workspace.workspaceFile;
    const folders = vscode.workspace.workspaceFolders;

    let workspacePath = null;
    if (workspaceFile) {
        workspacePath = workspaceFile.fsPath;
    } else if (folders && folders.length > 0) {
        workspacePath = folders[0].uri.fsPath;
    }

    if (!workspacePath) {
        console.log('VSCode Reporter: No workspace or folder open.');
        return;
    }

    console.log(`VSCode Reporter: Current workspace path is ${workspacePath}`);

    const postData = JSON.stringify({
        path: workspacePath
    });

    const options = {
        hostname: MCP_SERVER_HOST,
        port: MCP_SERVER_PORT,
        path: '/update/vscode/current_workspace', // 更新狀態的端點
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(postData)
        }
    };

    const req = http.request(options, (res) => {
        console.log(`VSCode Reporter: Sent status to MCP Server, response code: ${res.statusCode}`);
    });

    req.on('error', (e) => {
        console.error(`VSCode Reporter: Failed to send status to MCP Server. Is the server running?`);
        console.error(e);
        vscode.window.showErrorMessage('無法連接到本地 MCP 伺服器。請確認它是否正在運行。');
    });

    req.write(postData);
    req.end();
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('Congratulations, your "vscode-mcp-reporter" extension is now active!');

    // 擴充功能啟動時，立即發送一次當前狀態
    updateWorkspaceStatus();

    // 監聽工作區的變更事件
    context.subscriptions.push(vscode.workspace.onDidChangeWorkspaceFolders((_e) => {
        console.log('VSCode Reporter: Workspace folders changed, updating status...');
        updateWorkspaceStatus();
    }));
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
}
```

### 步驟 3: 設定 `package.json`

確保您的 `package.json` 中的 `activationEvents` 包含 `"onStartupFinished"`，這樣 VS Code 啟動完成後就會自動執行您的擴充功能。

```json
// In package.json
"activationEvents": [
    "onStartupFinished"
],
```

---

## Part 2: 建立本地 MCP 伺服器 (The Provider)

這個伺服器將使用 Node.js 和 Express 框架來建立，它非常輕量。

### 步驟 1: 初始化專案並安裝依賴

在您選擇的目錄下，建立一個新的 Node.js 專案。

```bash
npm init -y
npm install express
```

### 步驟 2: 撰寫伺服器程式碼

建立一個 `server.js` 檔案，並貼上以下程式碼。

```javascript
// In server.js

const express = require('express');
const app = express();
const port = 3000; // 確保這個埠號與您的擴充功能設定一致

// 使用 express.json() 中介軟體來解析 POST 請求的 JSON body
app.use(express.json());

// 用一個簡單的物件來儲存我們從各種來源收到的狀態
const state = {
    vscode: {
        current_workspace: {
            path: null,
            last_updated: null
        }
    }
};

// --- MCP Provider Endpoints ---

// 實作 MCP 的 read_resource 功能
// 外部工具會呼叫這個端點來取得資訊
app.get('/resources/vscode/current_workspace', (req, res) => {
    if (state.vscode.current_workspace.path) {
        res.json(state.vscode.current_workspace);
    } else {
        res.status(404).json({ error: 'VSCode workspace path not available. Is the extension running?' });
    }
});

// (可選) 實作 MCP 的 list_resources 功能
app.get('/resources', (req, res) => {
    res.json({
        resources: [
            {
                name: "Current VSCode Workspace",
                uri: "/resources/vscode/current_workspace"
            }
        ]
    });
});


// --- Internal Update Endpoint ---

// 建立一個內部端點，專門給 VS Code 擴充功能用來匯報狀態
app.post('/update/vscode/current_workspace', (req, res) => {
    const { path } = req.body;
    if (path) {
        state.vscode.current_workspace.path = path;
        state.vscode.current_workspace.last_updated = new Date().toISOString();
        console.log(`[MCP Server] Received update. Current workspace is now: ${path}`);
        res.status(200).send('OK');
    } else {
        res.status(400).send('Bad Request: "path" is required.');
    }
});


app.listen(port, () => {
    console.log(`MCP Server listening on http://localhost:${port}`);
});
```

---

## Part 3: 如何運作

1.  **啟動伺服器**：在終端機中執行 `node server.js` 來啟動您的 MCP 伺服器。
2.  **啟動擴充功能**：回到您的 VS Code 擴充功能專案，按下 `F5` 鍵。這會開啟一個新的 VS Code 視窗（Extension Development Host），並且您的擴充功能會在這個視窗中運行。
3.  **自動匯報**：擴充功能啟動後，會立刻將當前工作區的路徑（如果有的話）發送到 MCP 伺服器。您應該會在伺服器的終端機中看到日誌。
4.  **外部查詢**：現在，任何外部工具都可以透過向 `http://localhost:3000/resources/vscode/current_workspace` 發送 GET 請求來取得此資訊。您可以用 `curl` 來測試：
    ```bash
    curl http://localhost:3000/resources/vscode/current_workspace
    ```
5.  **自動更新**：在運行擴充功能的 VS Code 視窗中，嘗試開啟一個新的資料夾或工作區 (`.code-workspace` 檔)。擴充功能會偵測到變更，並自動發送新的路徑到伺服器。再次用 `curl` 查詢，您會發現路徑已經更新了。

這個架構成功地將 VS Code 的內部狀態安全、可靠地暴露給了外部工具，同時保持了元件之間的解耦合。
