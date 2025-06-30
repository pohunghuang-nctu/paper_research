# GitHub Copilot for Business 使用情況分析摘要

本文旨在總結如何監控與分析 GitHub Copilot for Business 的使用情況，特別是如何獲取使用率 (usage) 與程式碼完成接受率 (acceptance rate) 等關鍵指標。

## 總覽

GitHub Copilot for Business **確實提供**了監控使用情況的機制。這主要透過兩大核心元件實現：

1.  **Copilot Metrics API**：一個 RESTful API，用於獲取原始的使用數據。
2.  **視覺化儀表板方案 (Dashboard Solutions)**：官方提供的開源專案，用於將 API 數據視覺化，方便分析。

---

## 1. Copilot Metrics API

這是獲取所有使用數據的基礎。企業管理員可以透過此 API 取得精細的匯總指標。

### 可獲取的關鍵指標

API 提供了過去 28 天的每日匯總數據，主要包含：

*   **整體使用量**:
    *   `total_suggestions_count`: 總建議次數。
    *   `total_acceptances_count`: 總接受次數。
    *   `total_lines_suggested`: 建議的程式碼總行數。
    *   `total_lines_accepted`: 接受的程式碼總行數。
*   **使用者活躍度**:
    *   `total_active_users`: 活躍使用者總數 (有觸發建議)。
    *   `total_active_chat_users`: 活躍的 Copilot Chat 使用者總數。
*   **細分維度**:
    *   可按**程式語言 (Language)** 和**開發工具 (IDE/Editor)** 進行細分，了解在不同情境下的使用效率。

### API 呼叫範例

以下是使用 `curl` 獲取特定組織 (organization) 使用數據的範例：

```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_PERSONAL_ACCESS_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/orgs/YOUR_ORGANIZATION_NAME/copilot/usage"
```

**注意**:
*   `YOUR_PERSONAL_ACCESS_TOKEN` 需要替換為具有 `manage_copilot_for_org` 權限的 Personal Access Token。
*   `YOUR_ORGANIZATION_NAME` 需替換為您的組織名稱。

---

## 2. Copilot Metrics Dashboard

為了方便地將 API 數據視覺化，Microsoft 官方提供了一個開源專案 `Copilot Metrics Dashboard`。

### 專案特性

*   **開源性質**: 此專案完全開源 (MIT License)，可自由使用與修改。
*   **解決方案加速器**: 它提供了一套預先建置好的程式碼與部署腳本，讓您可以快速建立自己的儀表板，而無需從零開始開發。
*   **部署與設定**:
    *   專案提供了「一鍵部署至 Azure」的功能。
    *   部署後，僅需設定幾個關鍵參數 (如 GitHub 組織名稱、Personal Access Token)，即可開始運作。

---

## 結論

透過 **Copilot Metrics API** 和 **Copilot Metrics Dashboard** 專案的結合，企業可以有效地建立一套完整的使用分析系統。這不僅能追蹤整體的採用率和投資回報率，還能深入分析不同團隊、不同程式語言下的使用模式，從而最大化 GitHub Copilot 帶來的生產力效益。
