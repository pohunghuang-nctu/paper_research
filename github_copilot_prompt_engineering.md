# GitHub Copilot Prompt Engineering 最佳實踐

GitHub 官方提供了詳細的文件與部落格文章，指導使用者如何透過有效的 Prompt Engineering (提示工程) 來提升與 GitHub Copilot 的互動品質與產出效率。雖然文件未直接提及如何命令 AI "使用工具 (tools)"，但其核心概念是相通的：透過精準的提示來引導 AI 執行特定任務。

## 撰寫有效 Prompt 的核心原則

根據 GitHub 官方文件 [Prompt engineering for Copilot Chat](https://docs.github.com/copilot/using-github-copilot/prompt-engineering-for-github-copilot)，以下是幾個關鍵的技巧：

1.  **從概括到具體 (Start general, then get specific)**
    *   先描述宏觀目標，再逐步加入具體要求。
    *   **範例**: 先說「寫一個檢查質數的函式」，再補充「輸入為整數，回傳布林值」、「處理非正整數的錯誤情況」。

2.  **提供範例 (Give examples)**
    *   給予具體的輸入、輸出範例，能幫助 Copilot 更精準地理解需求。
    *   **範例**: 要求解析日期時，列出所有可能的日期格式 (`05/02/24`, `5-2-2024` 等)。

3.  **拆解複雜任務 (Break complex tasks into simpler tasks)**
    *   將大型、複雜的任務拆解成數個簡單的小任務，分步引導 Copilot 完成。
    *   **範例**: 製作單字搜尋遊戲時，可拆分為「產生字母網格」、「從網格找單字」、「結合兩者」等步驟。

4.  **避免模糊不清 (Avoid ambiguity)**
    *   使用明確詞語，避免代名詞。例如，明確指出「解釋 `createUser` 函式」，而非「解釋這個」。
    *   若使用不常見的函式庫，可先簡單描述其功能。

5.  **指定相關程式碼 (Indicate relevant code)**
    *   **IDE 中**: 只開啟相關檔案，讓 Copilot 利用這些檔案作為上下文。
    *   **Copilot Chat 中**: 反白程式碼區塊，或使用 `@workspace` (VS Code) / `@project` (JetBrains IDEs) 讓 Copilot 參考整個專案。

6.  **實驗與迭代 (Experiment and iterate)**
    *   若初次結果不佳，可修改提示後再試一次，或參考上次回應來修正問題。

7.  **保持對話歷史的關聯性 (Keep history relevant)**
    *   為不同任務開啟新的對話串，並刪除不相關或結果不佳的問答，以提供最精準的上下文。

8.  **遵循良好的程式碼實踐 (Follow good coding practices)**
    *   高品質、風格一致、命名清晰、模組化的程式碼是給予 Copilot 最好的上下文。

## 總結

要讓 GitHub Copilot 發揮最大效益，關鍵在於提供**清晰、具體、有上下文**的指示。將 Copilot 視為需要引導的程式設計夥伴，而非全知的魔法師。

## 官方參考資料

以下是官方部落格中提供更多實例和技巧的文章：

*   [How to use GitHub Copilot: Prompts, tips, and use cases](https://github.blog/2023-06-20-how-to-write-better-prompts-for-github-copilot/)
*   [A developer’s guide to prompt engineering and LLMs](https://github.blog/2023-07-17-prompt-engineering-guide-generative-ai-llms/)
*   [Using GitHub Copilot in your IDE: Tips, tricks, and best practices](https://github.blog/2024-03-25-how-to-use-github-copilot-in-your-ide-tips-tricks-and-best-practices/)
*   [Prompting GitHub Copilot Chat to become your personal AI assistant for accessibility](https://github.blog/2023-10-09-prompting-github-copilot-chat-to-become-your-personal-ai-assistant-for-accessibility/)
