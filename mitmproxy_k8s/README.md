# mitmproxy Kubernetes 部署套件

此資料夾包含在 Kubernetes 中部署 mitmproxy 的完整配置和文件。

## 📁 文件說明

### 核心文件

- **`mitmproxy_k8s_deployment.yaml`** (5.5 KB)
  - 完整的 Kubernetes 部署配置
  - 包含 Namespace, ConfigMap, PVC, Deployment, Service
  - 內建記憶體優化和健康檢查配置

- **`deploy_mitmproxy.sh`** (7.8 KB)
  - 一鍵部署和管理腳本 (可執行)
  - 提供 deploy, status, logs, forward, cert, delete 等功能
  - 彩色輸出和互動式確認

### 文檔

- **`mitmproxy_k8s_quickstart.md`** (3.7 KB)
  - ⚡ 快速開始指南 - 5 分鐘快速部署
  - 常用指令速查表
  - 適合快速上手

- **`mitmproxy_k8s_deployment_guide.md`** (12 KB)
  - 📖 完整部署指南
  - 詳細的配置說明和進階功能
  - 疑難排解和最佳實踐
  - 適合深入了解和生產環境部署

### 範例

- **`mitmproxy_example_addon.py`** (7.7 KB)
  - mitmproxy 自訂腳本範例
  - 包含多種攔截和處理場景
  - 內建記憶體優化最佳實踐

## 🚀 快速開始

### 1. 基本部署

```bash
# 進入資料夾
cd mitmproxy_k8s

# 執行部署
./deploy_mitmproxy.sh deploy
```

### 2. 查看狀態

```bash
./deploy_mitmproxy.sh status
```

### 3. 開始使用

```bash
# Port Forward 到本機
./deploy_mitmproxy.sh forward 8080

# 匯出 CA 證書
./deploy_mitmproxy.sh cert
```

### 4. 查看日誌

```bash
./deploy_mitmproxy.sh logs
```

## 📚 閱讀順序建議

1. **初次使用**: 先閱讀 `mitmproxy_k8s_quickstart.md`
2. **深入了解**: 再閱讀 `mitmproxy_k8s_deployment_guide.md`
3. **自訂腳本**: 參考 `mitmproxy_example_addon.py`
4. **修改配置**: 編輯 `mitmproxy_k8s_deployment.yaml`

## ⚙️ 前置需求

- Kubernetes 叢集 (1.20+)
- kubectl 工具已安裝並配置
- 具備建立 Namespace、Deployment、Service 等資源的權限
- (可選) StorageClass 用於 PVC

## 🎯 特色功能

✅ **記憶體優化**: 整合了記憶體管理最佳實踐
✅ **一鍵部署**: 提供自動化部署腳本
✅ **健康檢查**: 內建 Liveness 和 Readiness Probes
✅ **持久化**: 自動保存證書和日誌
✅ **彈性配置**: 支援多種 Service 類型和資源調整

## 🔧 自訂配置

### 修改腳本

```bash
# 編輯或創建新的 addon 腳本
vi my_custom_addon.py

# 更新到 K8S
./deploy_mitmproxy.sh update-script my_custom_addon.py
```

### 調整資源

編輯 `mitmproxy_k8s_deployment.yaml` 中的 resources 區段：

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "2000m"
```

### 變更 Service 類型

在 `mitmproxy_k8s_deployment.yaml` 中修改 Service 的 `type`:
- `ClusterIP` (預設): 僅限叢集內部
- `NodePort`: 透過節點 Port 存取
- `LoadBalancer`: 透過負載平衡器存取 (需雲端環境)

## 🐛 疑難排解

```bash
# 檢查 Pod 狀態
kubectl describe pod -n mitmproxy -l app=mitmproxy

# 查看日誌
./deploy_mitmproxy.sh logs

# 進入 Pod 除錯
./deploy_mitmproxy.sh shell

# 重啟服務
./deploy_mitmproxy.sh restart
```

詳細的疑難排解步驟請參考 `mitmproxy_k8s_deployment_guide.md`

## 🧹 清理

```bash
# 刪除所有資源
./deploy_mitmproxy.sh delete
```

## 📖 相關文件

在上層目錄中還有以下相關文件：

- `mitmdump_memory_optimization.md` - 記憶體優化策略
- `mitmdump_systemd_setup_guide.md` - systemd 服務配置
- `mitmproxy_chinese_video_tutorials.md` - 中文教學資源

## 💡 最佳實踐

1. **測試先行**: 先在測試環境驗證配置
2. **資源監控**: 定期檢查記憶體和 CPU 使用情況
3. **日誌管理**: 適時清理或輪轉日誌
4. **證書備份**: 保存生成的 CA 證書
5. **腳本管理**: 版本控制你的自訂腳本

## 📞 需要協助？

- 查看 `mitmproxy_k8s_deployment_guide.md` 的疑難排解章節
- 參考 mitmproxy 官方文檔: https://docs.mitmproxy.org/
- 檢查 Kubernetes 日誌和事件

---

**建立日期**: 2025-10-02  
**版本**: 1.0  
**適用於**: mitmproxy latest, Kubernetes 1.20+
