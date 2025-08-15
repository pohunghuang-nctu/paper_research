# 使用 claude-code 進行無頭 (Headless) 自動化

這份文件總結了如何將 Anthropic 的 `claude-code` 工具以無頭模式整合到自動化流程中，例如背景排程工作或 CI/CD pipeline。

## 核心概念

理論上，`claude-code` 作為一個命令列工具，完全可以透過腳本實現自動化，無需手動互動。主要方法是透過標準輸入 (stdin) 將指令傳遞給它。

## 關鍵發現與實踐方法

根據網路搜尋和官方文件，無頭模式不僅可行，而且是官方推薦的進階用法。

1.  **官方支援與範例**:
    *   Anthropic 的官方文件 **[Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)** 明確提到了「Headless mode」。
    *   官方舉例說明，他們利用此模式自動化分析 GitHub Issues 並加上標籤，證實了這是其核心功能之一。

2.  **必要的指令參數**:
    *   在自動化腳本中，為了避免程式因等待使用者手動批准而中斷，必須使用 `--dangerously-skip-permissions` 參數。
    *   這可以跳過執行指令或修改檔案時的權限確認步驟。
    *   參考資料：**[How I use Claude Code (+ my best tips)](https://www.builder.io/blog/claude-code)**

3.  **實現方式**:
    *   **指令傳遞**: 使用 shell 的管道 (pipe) 將指令傳送給 `claude-code`。
      ```bash
      echo "你的指令" | claude-code --project-path /path/to/project --dangerously-skip-permissions
      ```
    *   **整合**: 將上述命令包裝成 shell 腳本，並透過 `cron` (Linux/macOS)、工作排程器 (Windows) 或整合到 GitHub Actions 等 CI/CD 工具中來觸發。

## 推薦資源

*   **教學影片**: **[Building headless automation with Claude Code](https://www.youtube.com/watch?v=dRsjO-88nBs)** - 這支影片應為學習此主題的最佳起點。

## 總結

將 `claude-code` 用於自動化排程是完全可行的。關鍵在於透過腳本化輸入和使用 `--dangerously-skip-permissions` 參數來實現非互動式執行。
