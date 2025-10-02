# mitmproxy Kubernetes 快速開始

## 🚀 5 分鐘快速部署

### 1. 檢查前置條件

```bash
# 確認 kubectl 已安裝並連線到叢集
kubectl version --short
kubectl cluster-info
```

### 2. 部署到 Kubernetes

**方法 A: 使用一鍵部署腳本** (推薦)

```bash
# 賦予執行權限
chmod +x deploy_mitmproxy.sh

# 執行部署
./deploy_mitmproxy.sh deploy
```

**方法 B: 手動部署**

```bash
# 直接 apply YAML
kubectl apply -f mitmproxy_k8s_deployment.yaml

# 查看部署狀態
kubectl get pods -n mitmproxy -w
```

### 3. 驗證部署

```bash
# 使用腳本
./deploy_mitmproxy.sh status

# 或手動查詢
kubectl get all -n mitmproxy
```

### 4. 開始使用

**在本機使用 (Port Forward)**

```bash
# 使用腳本
./deploy_mitmproxy.sh forward 8080

# 或手動執行
kubectl port-forward -n mitmproxy service/mitmproxy 8080:8080
```

然後在瀏覽器或應用中設定代理：
- HTTP Proxy: `localhost:8080`
- HTTPS Proxy: `localhost:8080`

**匯出 CA 證書** (用於 HTTPS)

```bash
# 使用腳本
./deploy_mitmproxy.sh cert

# 或手動匯出
POD=$(kubectl get pod -n mitmproxy -l app=mitmproxy -o jsonpath='{.items[0].metadata.name}')
kubectl cp mitmproxy/$POD:/home/mitmproxy/.mitmproxy/mitmproxy-ca-cert.pem ./mitmproxy-ca-cert.pem
```

然後在系統或瀏覽器中安裝 `mitmproxy-ca-cert.pem`

### 5. 查看日誌

```bash
# 使用腳本
./deploy_mitmproxy.sh logs

# 或手動查詢
kubectl logs -n mitmproxy -l app=mitmproxy -f
```

## 📝 常用指令

```bash
# 部署
./deploy_mitmproxy.sh deploy

# 查看狀態
./deploy_mitmproxy.sh status

# 查看日誌
./deploy_mitmproxy.sh logs

# Port Forward
./deploy_mitmproxy.sh forward 8080

# 匯出證書
./deploy_mitmproxy.sh cert

# 進入 Pod Shell
./deploy_mitmproxy.sh shell

# 重啟
./deploy_mitmproxy.sh restart

# 更新自訂腳本
./deploy_mitmproxy.sh update-script my_addon.py

# 刪除所有資源
./deploy_mitmproxy.sh delete
```

## 🔧 自訂配置

### 修改代理腳本

1. 編輯 `mitmproxy_k8s_deployment.yaml` 中的 ConfigMap
2. 或參考 `mitmproxy_example_addon.py` 創建新腳本
3. 更新並重啟：

```bash
./deploy_mitmproxy.sh update-script mitmproxy_example_addon.py
```

### 調整資源配額

編輯 `mitmproxy_k8s_deployment.yaml`：

```yaml
resources:
  requests:
    memory: "512Mi"  # 根據需求調整
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "2000m"
```

### 變更 Service 類型

預設是 `ClusterIP`，如需外部存取可改為：

```yaml
# NodePort
spec:
  type: NodePort
  ports:
  - port: 8080
    targetPort: 8080
    nodePort: 30080  # 可選

# 或 LoadBalancer (需雲端環境支援)
spec:
  type: LoadBalancer
```

## 🐛 疑難排解

### Pod 無法啟動

```bash
kubectl describe pod -n mitmproxy -l app=mitmproxy
kubectl logs -n mitmproxy -l app=mitmproxy
```

### PVC 綁定失敗

檢查 StorageClass：
```bash
kubectl get storageclass
kubectl get pvc -n mitmproxy
```

編輯 YAML 指定正確的 `storageClassName`

### 記憶體持續增長

確認腳本中有設定 `flow.live = False`：
```bash
kubectl get configmap mitmproxy-script -n mitmproxy -o yaml
```

### 無法攔截 HTTPS

1. 確認已安裝 CA 證書
2. 檢查證書是否正確生成：
   ```bash
   ./deploy_mitmproxy.sh shell
   ls -la /home/mitmproxy/.mitmproxy/
   ```

## 📚 更多資訊

- 完整部署指南: `mitmproxy_k8s_deployment_guide.md`
- 腳本範例: `mitmproxy_example_addon.py`
- 記憶體優化: `mitmdump_memory_optimization.md`

## 🧹 清理

```bash
# 刪除所有資源
./deploy_mitmproxy.sh delete

# 或手動刪除
kubectl delete namespace mitmproxy
```

---

**需要協助？** 查看 `mitmproxy_k8s_deployment_guide.md` 取得更詳細的說明！
