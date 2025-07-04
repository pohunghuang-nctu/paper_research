# 引導 GitHub Copilot 正確使用工具 (Extensions) 的官方指引

與其讓 AI 自行判斷何時使用工具，GitHub Copilot 的模式是讓使用者**明確地、有意識地呼叫 (invoke)** 特定的工具。這些工具在 Copilot 的生態系中被稱為 **"Copilot Extensions"**。

以下是根據官方文件整理出的核心指引，說明如何引導 Copilot 正確挑選及使用這些工具。

### 1. 如何挑選並呼叫工具 (Tool Selection)

這是最關鍵的一步，使用者需要明確地告訴 Copilot 要使用哪一個工具。

*   **語法**: 在 Copilot Chat 的輸入框中，使用 `@{工具名稱}` 的語法來呼叫。
*   **探索工具**: 當你輸入 `@` 符號時，Copilot Chat 會自動彈出一個列表，顯示所有你已安裝且可用的擴充功能 (工具)，讓你從中挑選。
*   **持續指定**: 在同一個對話中，如果要對同一個工具下達多個指令，**每一個指令都必須以 `@{工具名稱}` 開頭**。Copilot 不會「記住」你上一個指令是用哪個工具。

### 2. 如何引導工具正確執行 (Prompting Guidance)

一旦選定了工具，接下來的引導原則非常直觀且強大。

*   **核心原則**: **「思考一下，如果沒有 Copilot，你會如何使用這個工具？然後用自然語言將這個操作描述出來。」**
*   **結合 GitHub 功能**: 擴充功能的強大之處在於能將外部工具的能力與 GitHub 的功能（如建立 issue、指派任務）無縫結合。你的提示詞 (Prompt) 應該要能體現這一點。

#### 官方範例 (以 Sentry 擴充功能為例)

Sentry 是一個應用程式監控工具。以下官方範例完美展示了如何引導它工作：

*   **查詢外部工具的資訊**:
    ```
    @sentry list my most recent issues
    ```
    *(→ 直接使用 Sentry 的功能，列出最近的錯誤。)*

*   **深入查詢特定項目**:
    ```
    @sentry tell me more about issue ISSUE-ID-OR-ISSUE-LINK
    ```
    *(→ 針對 Sentry 的特定錯誤 ID 進行查詢。)*

*   **結合外部工具與 GitHub 的操作**:
    ```
    @sentry create a GitHub issue for the most recent Sentry issue and assign it to @DEVELOPER
    ```
    *(→ 這是一個完美的整合範例：它先用 `@sentry` 的能力找到最新的錯誤，然後利用 GitHub 的能力「建立一個 issue」並「指派給某個開發者」。)*

### 3. 如何了解一個工具能做什麼？

官方建議，要了解特定擴充功能的最佳使用方式，最好的方法是**閱讀該擴充功能在 [GitHub Marketplace](https://github.com/marketplace?type=apps&copilot_app=true) 上的說明文件**。每個工具的開發者都會在那裡詳細說明它的功能與使用範例。

### 總結

總結來說，GitHub Copilot 對於「使用工具」的官方指引，並非一套複雜的提示工程技巧，而是更直接、明確的互動模式：

1.  **明確呼叫**: 使用 `@` 語法指定你要用的工具。
2.  **自然語言下令**: 像平常對話一樣，告訴工具你希望它做什麼。
3.  **結合情境**: 將工具自身的功能與你在 GitHub 上的工作流程結合，以發揮最大效益。
