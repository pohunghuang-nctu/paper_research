# Zeta 模型研究摘要

本文檔總結了關於 Zed Editor 的 Zeta 模型、其資料集以及如何進行推斷的關鍵發現。

## 1. Zeta 模型簡介

*   **用途**: Zeta 是 Zed Editor 用於其 "Edit Prediction" (編輯預測) 功能的原生 AI 模型。
*   **基礎**: Zeta 基於 `Qwen2.5-Coder-7B` 模型進行微調。
*   **目標**: 預測開發者下一步的程式碼編輯，允許透過按 `Tab` 鍵快速接受單行或多行建議。
*   **整合**: 對於 Zed Editor 使用者，Zeta 通常是預設啟用的，無需手動下載或設定。

## 2. Zeta 資料集 (`zed-industries/zeta`)

*   **獲取方式**:
    *   推薦使用 Hugging Face `datasets` Python 函式庫 (`load_dataset("zed-industries/zeta")`)。
    *   也可透過 Git LFS 手動複製: `git clone https://huggingface.co/datasets/zed-industries/zeta` (Git LFS 會處理大檔案)。資料集會被下載到執行命令的目錄下一個名為 `zeta` 的資料夾中。
*   **資料夾結構與檔案含義**:
    *   **`train/` (對應 `train.jsonl`)**: 包含用於**監督式微調 (Supervised Fine-Tuning, SFT)** 的訓練資料。教模型「如何做」。
    *   **`dpo/` (對應 `dpo.jsonl`)**: 包含用於**直接偏好優化 (Direct Preference Optimization, DPO)** 的資料。教模型「做得更好」或「更符合偏好」。
    *   **`eval/` (對應 `eval.jsonl`)**: 包含用於評估 Zeta 模型效能的資料。檢驗模型「學得怎麼樣」。
    *   `.jsonl` 檔案由各自對應資料夾中的 Markdown (`.md`) 檔案透過 `script/gen-dataset` 腳本生成。

## 3. DPO 資料條目解析 (以 `dpo/0003.md` 為例)

一個 DPO `.md` 資料條目通常包含：

*   **`<events>` 區塊**:
    *   使用 `diff` 格式描述使用者編輯事件，顯示從原始狀態到修改後狀態的變化。
    *   定義了「偏好的編輯」或「期望的行為」。
*   **`<input>` 區塊**:
    *   提供編輯發生時的完整程式碼上下文。
    *   包含特殊標記如 `<|editable_region_start|>`, `<|editable_region_end|>`, `<|user_cursor_is_here|>` 來指示編輯區域和游標位置。
    *   此部分構成 DPO 訓練中的「提示 (Prompt)」。
*   **`<output>` 區塊**:
    *   展示套用「偏好編輯」後的完整程式碼狀態。
    *   代表 DPO 訓練中的「偏好的回應 (Chosen Response)」。
*   **`<outline>` 區塊**:
    *   提供程式碼結構的摘要，可能作為額外的上下文特徵。

**DPO 訓練目標**: 教導模型在給定 `<input>` (提示) 時，生成更接近 `<output>` (偏好回應) 的結果，並避免生成「不偏好回應」(可能由模型即時生成或資料預處理時构造)。

## 4. Zeta 模型推斷 (Inference)

*   **推斷時的輸入**:
    *   主要是當前編輯器中游標位置前後的程式碼上下文 (prefix 和 suffix)。
    *   可能包含游標位置、語言類型等。
    *   推斷提示 (`input_text`) 需要模擬編輯器上下文，並且**必須**包含模型訓練時使用的特殊標記，例如用 `<|editable_region_start|>` 和 `<|editable_region_end|>` 界定可編輯區域，並用 `<|user_cursor_is_here|>` 標示確切的游標位置。這些標記對於模型正確理解上下文和生成準確建議至關重要。
    *   **不需要傳入 `<events>` 區塊。**
*   **推斷時的預期輸出**:
    *   模型生成的程式碼建議，旨在插入游標位置或修改周圍程式碼。
    *   目標是達到類似訓練資料中「偏好輸出」的品質。

*   **Python 推斷範例程式碼 (使用 `transformers` 函式庫)**:

    ```python
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch

    # 1. 載入模型和 Tokenizer
    model_name = "zed-industries/zeta"  # 或微調後的模型路徑
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # 將模型移至 GPU (如果可用)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # 2. 準備輸入提示 (input_text)
    # input_text 需要模擬編輯器上下文，並包含特殊標記。
    # 以下是一個基於 dpo/0003.md 結構的示例 prompt：
    input_text = """<input>
    ```untitled
            }
        "#;

        let mut state = State::new(canvas, wgsl_source).await.unwrap();

        // For simplicity, we'll just render once here.
        // In a real application, you'd set up a render loop.
        state.render().unwrap();
    }
    ```

    2. Update your `Cargo.toml`:

    ```toml
    [package]
    name = "wgpu-previewer"
    version = "0.1.0"
    edition = "2021"

    [lib]
    crate-type = ["cdylib"]

    [dependencies]
    wasm-bindgen = "0.2"
    wasm-bindgen-futures = "0.4"
    web-sys = { version = "0.3", features = [
        "Document",
        "Window",
        "HtmlCanvasElement",
        "DomRect",
    ]}
    wgpu = { version = "0.19", features = ["webgl"] }
    console_error_panic_hook = "0.1"
    console_log = "1.0"
    log = "0.4"
    ```

    3. In your `State::new` function, you can now use `create_surface_from_canvas` directly without conditional compilation:

    ```rust
    impl State {
        async fn new(
            canvas: HtmlCanvasElement,
            shader_source: &str,
        ) -> Result<Self, Box<dyn std::error::Error>> {
            let instance = Instance::new(wgpu::InstanceDescriptor {
                backends: wgpu::Backends::all(),
    <|editable_region_start|>
                ..Default::default()
            });

            let surface = instance.create_surface_from_canvas(&canvas)
                .map_err(|e| format!("Failed to create surface: {:?}", e))?;

            // ... rest of the function
        }
    }
    ```

    These changes will:
    1. Ensure the code only compiles for the wasm32 target.
    2. Remove the need for a separate `main` function.
    3. Simplify the `Cargo.toml` by setting `crate-type = ["cdylib"]`.
    4. Allow direct use of WebAssembly-specific functions without conditional compilation.

    This approach is cleaner and more straightforward for a WebAssembly-only project. It removes any ambiguity about the target platform and simplifies the codebase.
    can I cargo check for wasm32? all my diagnostics are gone even when I inte<|user_cursor_is_here|>
    <|editable_region_end|>
    ```
    </input>""" # 實際使用時，<input> 標籤可能不需要，取決於模型訓練方式

    # 3. 將輸入文本轉換為模型可接受的格式
    inputs = tokenizer(input_text, return_tensors="pt").to(device)

    # 4. 使用模型生成輸出
    # max_length 和其他生成參數可以調整
    # len(inputs['input_ids'][0]) + 50 表示生成最多 50 個新 token
    with torch.no_grad(): # 在推斷時不需要計算梯度
        outputs = model.generate(
            **inputs, 
            max_length=len(inputs['input_ids'][0]) + 50, 
            num_return_sequences=1, 
            pad_token_id=tokenizer.eos_token_id  # 避免 pad_token_id 未設定的警告
        )

    # 5. 將模型輸出的 token 解碼回文本
    # 只獲取模型新生成的文本部分 (在原始輸入之後的部分)
    generated_text_ids = outputs[0][len(inputs['input_ids'][0]):]
    generated_text = tokenizer.decode(generated_text_ids, skip_special_tokens=True)

    print(f"Input Text (simplified for context):\n'''\n...can I cargo check for wasm32? all my diagnostics are gone even when I inte<|user_cursor_is_here|>...\n'''")
    print(f"\nGenerated Suggestion: '{generated_text}'")
    ```

*   **關鍵點**:
    *   **提示工程 (Prompt Engineering)**: `input_text` 的格式對輸出品質至關重要，需盡可能接近模型訓練時的格式，包括特殊標記。
    *   **特殊標記**: `tokenizer` 需要能正確處理模型使用的特殊標記。
    *   **輸出後處理**: 模型輸出可能需要進一步清理。
