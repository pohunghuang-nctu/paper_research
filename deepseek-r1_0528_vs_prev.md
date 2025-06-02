# DeepSeek-R1-0528 與前一版本差異整理

## 1. 模型升級與能力提升
- `deepseek-reasoner` 升級為 DeepSeek-R1-0528。
- 推理能力顯著提升，主要基準測試（Pass@1）成績：
  - **AIME 2025**: 70.0 → 87.5（+17.5）
  - **GPQA**: 71.5 → 81.0（+9.5）
  - **LCB_v6**: 63.5 → 73.3（+9.8）
  - **Aider**: 57.0 → 71.6（+14.6）
- 複雜推理任務在新版上可能會消耗更多 token。

## 2. 前端生成能力優化
- 生成的網頁與遊戲外觀更美觀，前端開發體驗提升。

## 3. 幻覺（Hallucination）問題減少
- 明顯抑制了舊版 R1 的幻覺現象，生成內容更可靠。

## 4. 支援 JSON 輸出與 Function Calling
- 新增支援 JSON 格式輸出與函數調用。
- Function call 性能（Tau-bench 分數）：
  - Airline: 53.5
  - Retail: 63.9

## 5. API 使用方式不變
- API 調用方式與舊版一致，無需額外調整。

---

### 前一版本（2025/01/20）重點
- 引入 deepseek-reasoner（DeepSeek-R1），允許指定 `model='deepseek-reasoner'` 調用。
- 無明顯的 benchmark 或功能細節提升，屬於新模型上線階段。

---

## 參考資料
- [DeepSeek-R1-0528 Release](https://api-docs.deepseek.com/news/news250528)
- [Change Log](https://api-docs.deepseek.com/updates/)
