# 程式碼編輯預測模型比較

本文檔比較了幾種專注於「程式碼編輯預測」或「差異預測 (diff prediction)」的開源 AI 模型。

| 特性 | Zed Zeta | CarperAI Diff Models | JetBrains Mellum |
| :--- | :--- | :--- | :--- |
| **主要任務** | 編輯預測 (Edit Prediction) | 差異預測 (Diff Prediction) | 程式碼完成 (未來規劃 Diff 預測) |
| **基礎模型** | Qwen2.5-Coder-7B | CodeGen (350M, 2B, 6B) | 自研 (Small, Medium) |
| **模型開源** | ✅ 是 | ✅ 是 | ✅ 是 |
| **資料集開源** | ✅ 是 (`zed-industries/zeta`) | 概念上是 (GitHub commits) | 否 (但模型可微調) |
| **成熟度** | 已在 Zed 編輯器中產品化 | 已發布可用模型 | 基礎模型已發布，Diff 模型待推出 |
| **優勢** | 資料格式精細，與編輯器整合度高 | 直接專注於 Diff 預測，多種模型大小可選 | 背靠 JetBrains，生態潛力巨大 |

## 參考資料

*   **Zed Zeta**: [Zed AI — Edit Prediction](https://zed.dev/edit-prediction)
*   **CarperAI Diff Models**: [Diff Models – A New Way to Edit Code](https://carper.ai/diff-models-a-new-way-to-edit-code/)
*   **JetBrains Mellum**: [Mellum Goes Open Source](https://blog.jetbrains.com/ai/2025/04/mellum-goes-open-source-a-purpose-built-llm-for-developers-now-on-hugging-face/)
*   **Coeditor**: [Coeditor: Leveraging Repo-level Diffs for Code Auto-editing (arXiv)](https://arxiv.org/html/2305.18584v2)
