# Q&A: GitHub Copilot for Business 的原始數據提供情況

## 問題

> github copilot for business 是否提供使用紀錄的 raw data 讓企業內部可以根據這些 raw data 套用自己的計算公式得到結果？

## 回答

是的，GitHub Copilot for Business **確實提供**使用紀錄的原始數據 (raw data)，讓企業可以根據這些數據套用自己的計算公式來分析使用情況。

這些原始數據主要是透過 **Copilot Metrics API** 來獲取的。以下是關於這些 raw data 的詳細說明：

### 原始數據的關鍵指標

您可以透過 API 取得過去 28 天內，每日匯總的以下關鍵指標：

*   **整體建議與接受情況**:
    *   `total_suggestions_count`: Copilot 產生的總建議次數。
    *   `total_acceptances_count`: 開發者接受建議的總次數。
    *   `total_lines_suggested`: Copilot 建議的程式碼總行數。
    *   `total_lines_accepted`: 開發者接受的程式碼總行數。

*   **使用者活躍度**:
    *   `total_active_users`: 在指定日期內，有觸發過 Copilot 建議的活躍使用者總數。
    *   `total_active_chat_users`: 活躍的 Copilot Chat 使用者總數。

### 數據的細分維度 (Breakdown)

除了上述的總體數據，API 回傳的資料還包含了更細緻的維度，可以讓您進行深入分析。數據可以按照以下兩個維度進行細分：

1.  **程式語言 (Language)**: 您可以查看每種程式語言（如 Python, JavaScript, C++）各自的建議數、接受數等指標。
2.  **開發工具 (Editor)**: 您可以查看在不同開發環境（如 VS Code, JetBrains IDEs, Vim）下的使用情況。

### 如何應用這些 Raw Data

有了這些原始數據，您的企業就可以進行各種自定義的分析，例如：

*   **計算接受率 (Acceptance Rate)**:
    `total_acceptances_count / total_suggestions_count`
*   **計算每位活躍使用者的平均接受行數**:
    `total_lines_accepted / total_active_users`
*   **分析特定語言的投資回報率**: 比較特定語言（例如 C++）的 `total_lines_accepted`，評估 Copilot 在該技術棧上的具體效益。
*   **追蹤不同 IDE 的採用情況**: 了解哪個開發工具的 Copilot 使用率最高或最低，以便提供針對性的內部培訓。

總結來說，GitHub Copilot for Business 透過其 Metrics API 提供了相當豐富的匯總後原始數據，雖然不是逐條操作的紀錄 (event-level log)，但這些每日匯總的指標和細分維度，已足夠讓企業建立自己的監控儀表板並進行深入的量化分析。
