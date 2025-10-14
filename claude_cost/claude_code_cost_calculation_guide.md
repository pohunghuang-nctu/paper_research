# Claude Code 成本計算完整指南

## 目錄

- [概述](#概述)
- [Claude Code 本地儲存結構](#claude-code-本地儲存結構)
- [Session ID 與 Resume 行為重要發現](#session-id-與-resume-行為重要發現)
- [Claude API 完整計價表](#claude-api-完整計價表)
- [AWS Bedrock 定價](#aws-bedrock-定價)
- [Token 類型說明](#token-類型說明)
- [計算公式](#計算公式)
- [實作建議](#實作建議)
- [參考資源](#參考資源)

## 概述

Claude Code 會在本地儲存完整的對話歷史，包含每則訊息的詳細 token 使用量。這些資料可以用來精確計算每個 session 的總成本。

## Claude Code 本地儲存結構

### 儲存位置

```
~/.claude/projects/[project-hash]/[session-id].jsonl
```

### 檔案格式

每個 session 對應一個 JSONL 檔案（JSON Lines 格式），每一行代表一則訊息的完整資訊。

### JSONL 欄位結構

根據研究發現，每則訊息包含以下 token 使用資訊：

```json
{
  "usage": {
    "input_tokens": 1000,
    "output_tokens": 500,
    "cache_creation_input_tokens": 2000,
    "cache_read_input_tokens": 5000
  }
}
```

### 相關設定檔

- `~/.claude/settings` - 官方有文件說明的設定檔
- `~/.claude/projects/` - 未在官方文件中詳細說明，但包含所有 session 歷史

## Session ID 與 Resume 行為重要發現

### ⚠️ 已知 Bug: Resume 會創建新 Session

**重要**：根據 [GitHub Issue #4926](https://github.com/anthropics/claude-code/issues/4926)，Claude Code CLI 的 `--resume` 功能目前存在 bug。

#### 預期行為 vs 實際行為

| 操作 | 預期行為 | 實際行為 (Bug) |
|------|---------|---------------|
| `claude --resume <session-id>` | 繼續使用原 session ID | ❌ **創建新的 session ID** |
| `claude -c` (continue) | 繼續最近的 session | ❌ **創建新的 session ID** |
| 檔案結構 | 寫入原有 JSONL 檔案 | ❌ **創建新的 JSONL 檔案** |

#### Bug 重現範例

```bash
# 1. 創建初始 session
$ claude --session-id abc123 -p "what is 4 + 4 * 4?"
# 產生: abc123.jsonl

# 2. Resume 該 session
$ claude --resume abc123 -p "remove 10 from it"
# 產生: xyz789.jsonl  ← 新的 session ID!

# 3. 再次 resume 原始 session
$ claude --resume abc123 -p "add 20 to it"
# 產生: def456.jsonl  ← 又是新的!

# 結果：三個不同的 JSONL 檔案，而非一個
```

#### 對成本計算的影響

❌ **不能假設**：
- 一個邏輯對話 = 一個 session ID
- Resume 會繼續寫入原有檔案

✅ **實際情況**：
- 一個邏輯對話可能分散在**多個 session JSONL 檔案**中
- 每次 resume 都會產生新的 session ID
- 需要追蹤對話鏈或使用時間範圍來計算總成本

#### Fork vs Continue 的設計

根據 [SDK 文件](https://docs.claude.com/en/api/agent-sdk/sessions)，SDK 支援兩種模式：

```javascript
// Continue (預設) - 應該繼續原 session
query({
  resume: sessionId,
  forkSession: false  // 預設值
})

// Fork - 創建新 session 分支
query({
  resume: sessionId,
  forkSession: true
})
```

**但 CLI 的 `--resume` 目前表現得像 `forkSession: true`**，即使預設應該是 `false`。

#### 解決方案建議

在此 bug 修復前，計算成本時可以：

1. **使用時間範圍**而非 session ID
   ```bash
   # 計算今天所有對話的成本
   python claude_session_cost.py --date 2025-10-14
   ```

2. **手動群組相關 sessions**
   ```bash
   # 計算多個相關 session 的總成本
   python claude_session_cost.py abc123.jsonl xyz789.jsonl def456.jsonl
   ```

3. **追蹤對話鏈**（進階）
   - 解析 JSONL 檔案中的 `resumed_from` 欄位（如果存在）
   - 重建完整的對話樹狀結構

## Claude API 完整計價表

### 基礎定價（Per Million Tokens）

| 模型 | API Model Name | Input Price | Output Price | Context Window |
|------|----------------|-------------|--------------|----------------|
| **Claude Opus 4.1** | `claude-opus-4-1-20250805` | $15.00 | $75.00 | 200K (標準) |
| **Claude Opus 4** | `claude-opus-4-20250514` | $15.00 | $75.00 | 200K (標準) |
| **Claude Sonnet 4.5** | `claude-sonnet-4-5-20250929` | $3.00 | $15.00 | 200K (標準), 1M (長文本) |
| **Claude Sonnet 4** | `claude-sonnet-4-20250514` | $3.00 | $15.00 | 200K (標準), 1M (長文本) |
| **Claude Sonnet 3.7** | `claude-3-7-sonnet-20250219` | $3.00 | $15.00 | 200K (標準) |
| **Claude Haiku 3.5** | `claude-3-5-haiku-20241022` | $0.80 | $4.00 | 200K (標準) |
| **Claude Haiku 3** | `claude-3-haiku-20240307` | $0.25 | $1.25 | 200K (標準) |

### Prompt Caching 計價倍數

Prompt Caching 提供兩種 TTL (Time To Live) 選項：

| Cache 類型 | TTL | 計價倍數 | 說明 |
|-----------|-----|---------|------|
| **Cache Creation (5-min)** | 5 分鐘 | 基礎價 × **1.25** | 預設選項，寫入 cache 的成本 |
| **Cache Creation (1-hour)** | 1 小時 | 基礎價 × **2.0** | Beta 功能，較長的 cache 保留時間 |
| **Cache Read** | - | 基礎價 × **0.1** | 從 cache 讀取，節省 **90%** 成本 |

#### Cache 計價規則

- `cache_creation_input_tokens`: 建立 cache 時的 tokens，成本較高但後續可重複使用
- `cache_read_input_tokens`: 從已建立的 cache 讀取，成本大幅降低（僅 10%）
- Cache 會在閒置後自動過期（5 分鐘或 1 小時，視設定而定）

### 其他折扣與特殊計價

#### Batch API

- **折扣**: 50% off
- **適用**: 非即時處理的工作負載
- **處理時間**: 24 小時內完成
- **範例**: Sonnet 4.5 降至 $1.50/$7.50 per million tokens

#### Long Context Pricing

- **適用模型**: Sonnet 4.5, Sonnet 4
- **觸發條件**: 使用超過 200K tokens 的 context window
- **特殊計價**: 基礎價格會有額外加成
- **折扣可疊加**: Batch API 與 Prompt Caching 折扣可應用於長文本

## AWS Bedrock 定價

如果透過 AWS Bedrock 使用 Claude（例如企業內部部署），定價結構略有不同。

### AWS Bedrock 定價表（全球跨區域推論）

#### 標準 Context (≤200K tokens)

| 模型 | Input (per 1K) | Output (per 1K) | Cache Write (per 1K) | Cache Read (per 1K) | Batch Input | Batch Output |
|------|---------------|----------------|---------------------|-------------------|-------------|-------------|
| **Claude Sonnet 4.5** | $0.003 | $0.015 | $0.00375 | $0.0003 | 不支援 | 不支援 |
| **Claude Sonnet 4** | $0.003 | $0.015 | $0.00375 | $0.0003 | $0.0015 | $0.0075 |

#### 長上下文 (Long Context, >200K tokens)

| 模型 | Input (per 1K) | Output (per 1K) | Cache Write (per 1K) | Cache Read (per 1K) |
|------|---------------|----------------|---------------------|-------------------|
| **Sonnet 4.5 - 長上下文** | $0.006 | $0.0225 | $0.0075 | $0.0006 |
| **Sonnet 4 - 長上下文** | $0.006 | $0.0225 | $0.0075 | $0.0006 |

### AWS Bedrock Token 類型對照

| JSONL 欄位 | AWS Bedrock 顯示名稱 | Sonnet 4.5 | Sonnet 4 |
|-----------|-------------------|-----------|----------|
| `input_tokens` | 每 1,000 個輸入字符的定價 | $0.003 | $0.003 |
| `output_tokens` | 每 1,000 個輸出字符的定價 | $0.015 | $0.015 |
| `cache_creation_input_tokens` | 每 1,000 個輸入字符的定價 **(快取寫入)** | $0.00375 | $0.00375 |
| `cache_read_input_tokens` | 每 1,000 個輸入字符的定價 **(快取讀取)** | $0.0003 | $0.0003 |

### 驗證計算

**Cache Write 倍數驗證**：
```
基礎 input: $0.003 / 1000 tokens
Cache write: $0.00375 / 1000 tokens
比例: 0.00375 ÷ 0.003 = 1.25 ✓ (符合 Anthropic 官方規則)
```

**Cache Read 倍數驗證**：
```
基礎 input: $0.003 / 1000 tokens
Cache read: $0.0003 / 1000 tokens
比例: 0.0003 ÷ 0.003 = 0.1 ✓ (節省 90%)
```

### AWS vs Anthropic API 差異

| 項目 | Anthropic API | AWS Bedrock |
|------|--------------|-------------|
| **計價單位** | Per **million** tokens | Per **1000** tokens |
| **Batch 支援** | 多數模型支援 | 僅 Sonnet 4 支援 |
| **長上下文** | 自動觸發 (>200K) | 需明確選擇「長上下文」版本 |
| **區域定價** | 全球統一 | 可能有區域差異 |
| **帳單整合** | Anthropic Console | AWS 帳單系統 |

## Token 類型說明

### 1. `input_tokens`

- **定義**: 用戶發送給 Claude 的文字 tokens
- **包含內容**:
  - 用戶的 prompt
  - System messages
  - Tool 定義（tools parameter）
  - Tool result content blocks
  - 對話歷史（如果需要）
- **計價**: 基礎 input 價格

### 2. `output_tokens`

- **定義**: Claude 生成回應的 tokens
- **包含內容**:
  - Claude 的回覆文字
  - Tool use content blocks
- **計價**: 基礎 output 價格（通常是 input 的 3-5 倍）

### 3. `cache_creation_input_tokens`

- **定義**: 建立 prompt cache 時寫入的 tokens
- **AWS Bedrock 對應**: 「每 1,000 個輸入字符的定價 (快取寫入)」
- **使用時機**:
  - 第一次使用某個 prompt 模板
  - Cache 過期後重新建立
  - 頻繁重複使用的 context（如文件、程式碼庫）
- **計價**: 
  - Anthropic API: 基礎 input 價格 × 1.25（5-min）或 × 2.0（1-hour）
  - AWS Bedrock: $0.00375 / 1K tokens (Sonnet 4/4.5)
- **投資回報**: 如果 cache 被重複讀取，整體成本會降低

### 4. `cache_read_input_tokens`

- **定義**: 從已建立的 cache 讀取的 tokens
- **AWS Bedrock 對應**: 「每 1,000 個輸入字符的定價 (快取讀取)」
- **使用時機**: 
  - 在 cache TTL 期間重複使用相同的 context
  - 多輪對話中的固定 system message
- **計價**: 
  - Anthropic API: 基礎 input 價格 × 0.1（節省 90%）
  - AWS Bedrock: $0.0003 / 1K tokens (Sonnet 4/4.5)
- **效益**: 大幅降低重複 context 的成本

## 計算公式

### 單則訊息成本計算

```python
def calculate_message_cost(usage: dict, base_input_price: float, base_output_price: float) -> float:
    """
    計算單則訊息的成本
    
    Args:
        usage: 包含 token 使用量的字典
        base_input_price: 基礎 input 價格（per million tokens）
        base_output_price: 基礎 output 價格（per million tokens）
    
    Returns:
        該則訊息的成本（美元）
    """
    # 取得各類 token 數量（可能不存在的欄位預設為 0）
    input_tokens = usage.get('input_tokens', 0)
    output_tokens = usage.get('output_tokens', 0)
    cache_creation_tokens = usage.get('cache_creation_input_tokens', 0)
    cache_read_tokens = usage.get('cache_read_input_tokens', 0)
    
    # 計算各部分成本
    input_cost = input_tokens * base_input_price / 1_000_000
    output_cost = output_tokens * base_output_price / 1_000_000
    cache_creation_cost = cache_creation_tokens * base_input_price * 1.25 / 1_000_000
    cache_read_cost = cache_read_tokens * base_input_price * 0.1 / 1_000_000
    
    # 總成本
    total_cost = input_cost + output_cost + cache_creation_cost + cache_read_cost
    
    return total_cost
```

### Session 總成本計算

```python
def calculate_session_cost(jsonl_file_path: str) -> dict:
    """
    計算整個 session 的總成本
    
    Args:
        jsonl_file_path: Claude Code session JSONL 檔案路徑
    
    Returns:
        包含詳細統計的字典
    """
    import json
    from datetime import datetime
    
    total_input_tokens = 0
    total_output_tokens = 0
    total_cache_creation_tokens = 0
    total_cache_read_tokens = 0
    message_count = 0
    
    # 用於儲存模型資訊（可能一個 session 使用多個模型）
    models_used = {}
    
    with open(jsonl_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
                
            try:
                data = json.loads(line)
                
                # 提取 usage 資訊
                if 'usage' in data:
                    usage = data['usage']
                    total_input_tokens += usage.get('input_tokens', 0)
                    total_output_tokens += usage.get('output_tokens', 0)
                    total_cache_creation_tokens += usage.get('cache_creation_input_tokens', 0)
                    total_cache_read_tokens += usage.get('cache_read_input_tokens', 0)
                    message_count += 1
                
                # 提取模型資訊（假設在 'model' 欄位）
                if 'model' in data:
                    model_name = data['model']
                    models_used[model_name] = models_used.get(model_name, 0) + 1
                    
            except json.JSONDecodeError:
                continue
    
    # 計算成本（需要根據使用的模型來決定價格）
    # 這裡需要實作模型價格對應邏輯
    
    return {
        'message_count': message_count,
        'total_input_tokens': total_input_tokens,
        'total_output_tokens': total_output_tokens,
        'total_cache_creation_tokens': total_cache_creation_tokens,
        'total_cache_read_tokens': total_cache_read_tokens,
        'models_used': models_used,
        # 'total_cost': total_cost,  # 需要根據模型計算
    }
```

### 模型價格映射

#### Anthropic API 定價（per million tokens）

```python
MODEL_PRICING_ANTHROPIC = {
    'claude-opus-4-1-20250805': {'input': 15.00, 'output': 75.00},
    'claude-opus-4-20250514': {'input': 15.00, 'output': 75.00},
    'claude-sonnet-4-5-20250929': {'input': 3.00, 'output': 15.00},
    'claude-sonnet-4-20250514': {'input': 3.00, 'output': 15.00},
    'claude-3-7-sonnet-20250219': {'input': 3.00, 'output': 15.00},
    'claude-3-5-haiku-20241022': {'input': 0.80, 'output': 4.00},
    'claude-3-haiku-20240307': {'input': 0.25, 'output': 1.25},
}
```

#### AWS Bedrock 定價（per 1000 tokens）

```python
MODEL_PRICING_AWS_BEDROCK = {
    'claude-sonnet-4-5': {
        'input': 0.003,
        'output': 0.015,
        'cache_write': 0.00375,
        'cache_read': 0.0003,
    },
    'claude-sonnet-4': {
        'input': 0.003,
        'output': 0.015,
        'cache_write': 0.00375,
        'cache_read': 0.0003,
        'batch_input': 0.0015,
        'batch_output': 0.0075,
    },
    # 長上下文版本
    'claude-sonnet-4-5-long': {
        'input': 0.006,
        'output': 0.0225,
        'cache_write': 0.0075,
        'cache_read': 0.0006,
    },
    'claude-sonnet-4-long': {
        'input': 0.006,
        'output': 0.0225,
        'cache_write': 0.0075,
        'cache_read': 0.0006,
    },
}
```

#### 通用模型名稱對應

```python
MODEL_NAME_MAPPING = {
    'opus-4.1': 'claude-opus-4-1-20250805',
    'opus-4': 'claude-opus-4-20250514',
    'sonnet-4.5': 'claude-sonnet-4-5-20250929',
    'sonnet-4': 'claude-sonnet-4-20250514',
    'sonnet-3.7': 'claude-3-7-sonnet-20250219',
    'haiku-3.5': 'claude-3-5-haiku-20241022',
    'haiku-3': 'claude-3-haiku-20240307',
}
```

### AWS Bedrock 成本計算

```python
def calculate_cost_aws_bedrock(
    usage: dict,
    model: str = 'claude-sonnet-4',
    is_long_context: bool = False
) -> float:
    """
    計算 AWS Bedrock 上的 Claude 使用成本
    
    Args:
        usage: 包含 token 使用量的字典
        model: 模型名稱
        is_long_context: 是否使用長上下文版本
    
    Returns:
        成本（美元）
    """
    # 選擇定價
    model_key = f"{model}-long" if is_long_context else model
    pricing = MODEL_PRICING_AWS_BEDROCK.get(model_key)
    
    if not pricing:
        raise ValueError(f"Unknown model: {model_key}")
    
    # 取得 token 數量
    input_tokens = usage.get('input_tokens', 0)
    output_tokens = usage.get('output_tokens', 0)
    cache_creation = usage.get('cache_creation_input_tokens', 0)
    cache_read = usage.get('cache_read_input_tokens', 0)
    
    # 計算成本（AWS 價格已是 per 1000 tokens）
    cost = (
        input_tokens * pricing['input'] / 1000 +
        output_tokens * pricing['output'] / 1000 +
        cache_creation * pricing['cache_write'] / 1000 +
        cache_read * pricing['cache_read'] / 1000
    )
    
    return cost
```

## 實作建議

### Python 腳本功能規劃

建議實作一個輕量級的 CLI 工具，功能如下：

```bash
# 基本使用
python claude_session_cost.py <session-jsonl-path>

# 指定模型（如果 JSONL 中沒有模型資訊）
python claude_session_cost.py <session-jsonl-path> --model sonnet-4.5

# 輸出詳細資訊
python claude_session_cost.py <session-jsonl-path> --verbose

# 輸出 JSON 格式（便於後續處理）
python claude_session_cost.py <session-jsonl-path> --output-json
```

### 輸出格式建議

```
═══════════════════════════════════════════════════════
  Claude Code Session Cost Analysis
═══════════════════════════════════════════════════════

Session File: ~/.claude/projects/abc123/session-xyz.jsonl
Session ID: session-xyz
Message Count: 42

─────────────────────────────────────────────────────
  Token Usage Summary
─────────────────────────────────────────────────────
Input Tokens:                    15,234
Output Tokens:                    8,567
Cache Creation Tokens:           45,000
Cache Read Tokens:              123,456

Total Tokens:                   192,257

─────────────────────────────────────────────────────
  Cost Breakdown
─────────────────────────────────────────────────────
Model: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

Input Cost:              $0.0457  (15,234 tokens @ $3.00/M)
Output Cost:             $0.1285  (8,567 tokens @ $15.00/M)
Cache Creation Cost:     $0.1688  (45,000 tokens @ $3.75/M)
Cache Read Cost:         $0.0370  (123,456 tokens @ $0.30/M)

─────────────────────────────────────────────────────
Total Cost:              $0.38
─────────────────────────────────────────────────────

Cache Efficiency: 73.3% (cache read tokens / total context tokens)
Average Cost per Message: $0.0091
```

### 關鍵實作注意事項

1. **錯誤處理**
   - JSONL 格式可能不完整或損壞
   - 某些欄位可能不存在（舊版本 Claude Code）
   - 使用 `try-except` 處理 JSON 解析錯誤

2. **模型偵測**
   - 優先從 JSONL 中讀取模型資訊
   - 如果無法偵測，提供 `--model` 參數讓用戶指定
   - 支援模型名稱的各種變體

3. **Cache 效率分析**
   - 計算 cache read 與總 context tokens 的比例
   - 顯示使用 cache 節省的成本
   - 提供優化建議

4. **多模型支援**
   - 一個 session 可能使用多個模型
   - 分別計算每個模型的成本
   - 提供總和與分項統計

5. **時間範圍分析**
   - 從 JSONL 提取時間戳記（如果有）
   - 顯示 session 的開始與結束時間
   - 計算 session 持續時間

### 目錄掃描功能（進階）

```python
# 掃描整個 projects 目錄
python claude_session_cost.py --scan-all

# 掃描特定 project
python claude_session_cost.py --scan-project <project-hash>

# 統計特定時間範圍
python claude_session_cost.py --scan-all --from 2025-01-01 --to 2025-01-31
```

### 第三方工具整合

雖然本指南建議自行實作簡單腳本，但也可以參考現有的開源工具：

- **[Claude Code Usage Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor)**
  - 功能強大的即時監控工具
  - 提供預測、警告、多種視圖
  - 適合需要持續監控使用量的情境
  - 對於單純計算特定 session 成本可能過於複雜

## 參考資源

### 官方文件

- [Claude API Pricing](https://docs.claude.com/en/docs/about-claude/pricing) - Anthropic 官方計價頁面
- [Prompt Caching Documentation](https://docs.claude.com/en/docs/build-with-claude/prompt-caching) - Cache 使用指南
- [Usage and Cost API](https://docs.claude.com/en/api/usage-cost-api) - API 使用量追蹤
- [Claude Code Cost Management](https://docs.claude.com/en/docs/claude-code/costs) - Claude Code 成本管理

### 相關工具

- [Claude Code Usage Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor) - 開源監控工具
- [CostGoat Claude Calculator](https://costgoat.com/pricing/claude-api) - 線上成本計算器

### 技術文章

- [The Hidden Costs of Claude Code](https://www.aiengineering.report/p/the-hidden-costs-of-claude-code-token) - 深入分析 Claude Code 成本
- [Prompt Caching Announcement](https://www.anthropic.com/news/prompt-caching) - Anthropic 官方說明

### 發現來源

本指南的 Claude Code 本地儲存發現來自社群研究：
- GitHub Issue: [Feature Request: Access Full Claude Code Conversation History](https://github.com/BeehiveInnovations/zen-mcp-server/issues/155)
- 儲存位置: `~/.claude/projects/[project-hash]/[session-id].jsonl`
- Session Resume Bug: [GitHub Issue #4926](https://github.com/anthropics/claude-code/issues/4926)

---

## 更新記錄

- **2025-10-14 v2**: 
  - 新增 AWS Bedrock 定價表與計算公式
  - 新增 Session ID Resume Bug 的重要發現 (Issue #4926)
  - 補充 Token 類型的 AWS Bedrock 對應欄位名稱
- **2025-10-14 v1**: 初始版本，包含 Anthropic API 完整計價表與實作指南
- 價格資訊基於 2025 年 10 月的資料，請定期檢查官方文件更新

## 授權

本文件為技術研究與學習用途，價格資訊以 Anthropic 官方公告為準。
