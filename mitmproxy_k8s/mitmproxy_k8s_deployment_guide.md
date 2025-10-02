# mitmproxy Kubernetes 部署指南

本指南說明如何在 Kubernetes 叢集中部署 mitmproxy，並基於你現有的 mitmproxy 使用經驗，整合了記憶體優化策略。

## 📋 目錄

- [架構概述](#架構概述)
- [前置需求](#前置需求)
- [部署步驟](#部署步驟)
- [配置說明](#配置說明)
- [使用方式](#使用方式)
- [進階配置](#進階配置)
- [疑難排解](#疑難排解)

## 🏗 架構概述

此部署方案包含以下 Kubernetes 資源：

- **Namespace**: `mitmproxy` - 隔離的命名空間
- **ConfigMap**: 存放 mitmproxy 自訂腳本
- **PersistentVolumeClaim**: 持久化存儲證書和日誌
- **Deployment**: 主要的 mitmproxy 應用
- **Service**: 暴露代理服務

### 內建的最佳實踐

✅ **記憶體優化**
- 使用 `--set stream_large_bodies=1m` 串流大型檔案
- 腳本中設定 `flow.live = False` 主動釋放記憶體
- 配置適當的資源限制

✅ **可靠性**
- LivenessProbe 和 ReadinessProbe 確保服務健康
- 設定自動重啟策略
- 持久化重要資料

## 📦 前置需求

1. **Kubernetes 叢集** (版本 1.20+)
   ```bash
   kubectl version --short
   ```

2. **kubectl 工具** 已安裝並配置
   ```bash
   kubectl cluster-info
   ```

3. **StorageClass** (用於 PVC)
   ```bash
   kubectl get storageclass
   ```

4. **權限**: 需要有建立 Namespace、Deployment、Service 等資源的權限

## 🚀 部署步驟

### 1. 檢查並調整配置

在部署前，請根據你的需求編輯 `mitmproxy_k8s_deployment.yaml`：

```bash
# 編輯配置檔
vi mitmproxy_k8s_deployment.yaml
```

**重要配置項**：

- **StorageClassName**: 根據你的 K8S 環境設定
- **資源限制**: 根據實際負載調整 `resources` 設定
- **Service 類型**: 選擇 `ClusterIP`、`NodePort` 或 `LoadBalancer`
- **自訂腳本**: 修改 ConfigMap 中的 `addon.py`

### 2. 部署到 Kubernetes

```bash
# 一次性部署所有資源
kubectl apply -f mitmproxy_k8s_deployment.yaml

# 或者分步驟部署（推薦用於生產環境）
kubectl apply -f mitmproxy_k8s_deployment.yaml --dry-run=client
kubectl apply -f mitmproxy_k8s_deployment.yaml
```

### 3. 驗證部署狀態

```bash
# 檢查所有資源
kubectl get all -n mitmproxy

# 檢查 Pod 狀態
kubectl get pods -n mitmproxy

# 檢查詳細資訊
kubectl describe pod -n mitmproxy

# 查看日誌
kubectl logs -n mitmproxy -l app=mitmproxy -f
```

預期輸出：
```
NAME                             READY   STATUS    RESTARTS   AGE
pod/mitmproxy-xxxxxxxxxx-xxxxx   1/1     Running   0          1m

NAME                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/mitmproxy   ClusterIP   10.96.xxx.xxx   <none>        8080/TCP   1m

NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/mitmproxy   1/1     1            1           1m
```

## ⚙️ 配置說明

### ConfigMap: 自訂處理腳本

ConfigMap 中的 `addon.py` 是 mitmproxy 的核心處理邏輯。基於你的記憶體優化經驗，腳本中已經包含 `flow.live = False` 來主動釋放記憶體。

**修改腳本**：

1. 編輯 YAML 檔中的 ConfigMap 部分
2. 或者使用以下方式動態更新：

```bash
# 建立新的腳本檔案
cat > custom_addon.py << 'EOF'
from mitmproxy import http
from mitmproxy import ctx

def response(flow: http.HTTPFlow) -> None:
    # 你的自訂邏輯
    ctx.log.info(f"{flow.request.method} {flow.request.pretty_url}")
    
    # 重要：釋放記憶體
    flow.live = False
EOF

# 更新 ConfigMap
kubectl create configmap mitmproxy-script \
  --from-file=addon.py=custom_addon.py \
  --namespace=mitmproxy \
  --dry-run=client -o yaml | kubectl apply -f -

# 重啟 Pod 以載入新腳本
kubectl rollout restart deployment/mitmproxy -n mitmproxy
```

### PersistentVolumeClaim: 持久化存儲

PVC 用於存放：
- **mitmproxy 證書** (`/home/mitmproxy/.mitmproxy`)
- **日誌檔案** (`/logs`)

**調整存儲大小**：

```bash
# 編輯 PVC
kubectl edit pvc mitmproxy-data -n mitmproxy

# 修改 storage 大小 (需要 StorageClass 支援動態擴展)
spec:
  resources:
    requests:
      storage: 10Gi  # 從 5Gi 改為 10Gi
```

### Service: 網路存取

提供三種 Service 類型選擇：

#### 1. ClusterIP (預設)
僅限叢集內部存取：
```yaml
spec:
  type: ClusterIP
```

#### 2. NodePort
透過節點 IP + NodePort 存取：
```yaml
spec:
  type: NodePort
  ports:
  - name: proxy
    port: 8080
    targetPort: 8080
    nodePort: 30080  # 可選，範圍 30000-32767
```

存取方式：
```bash
# 取得節點 IP
kubectl get nodes -o wide

# 使用 <NodeIP>:30080 設定代理
```

#### 3. LoadBalancer
透過雲端供應商的負載平衡器存取：
```yaml
spec:
  type: LoadBalancer
```

## 🔧 使用方式

### 從叢集內部使用

如果有其他應用需要使用代理：

```yaml
# 在其他 Pod 中設定環境變數
env:
- name: HTTP_PROXY
  value: "http://mitmproxy.mitmproxy.svc.cluster.local:8080"
- name: HTTPS_PROXY
  value: "http://mitmproxy.mitmproxy.svc.cluster.local:8080"
```

### 從叢集外部使用

#### 方法 1: Port Forward (開發/測試)
```bash
# 轉發到本機
kubectl port-forward -n mitmproxy service/mitmproxy 8080:8080

# 在瀏覽器或應用中設定代理為 localhost:8080
```

#### 方法 2: NodePort (生產環境)
```bash
# 取得 NodePort
kubectl get svc mitmproxy-nodeport -n mitmproxy

# 使用 <NodeIP>:<NodePort> 作為代理位址
```

#### 方法 3: LoadBalancer (雲端環境)
```bash
# 取得外部 IP
kubectl get svc mitmproxy -n mitmproxy

# 等待 EXTERNAL-IP 分配完成
# 使用 <EXTERNAL-IP>:8080 作為代理位址
```

### 安裝 mitmproxy 證書

要攔截 HTTPS 流量，需要安裝 mitmproxy 的 CA 證書：

```bash
# 從 Pod 中複製證書
kubectl cp mitmproxy/<pod-name>:/home/mitmproxy/.mitmproxy/mitmproxy-ca-cert.pem \
  ./mitmproxy-ca-cert.pem -n mitmproxy

# 在你的系統或瀏覽器中安裝此證書
```

或者透過 Web 界面下載：
1. 啟用 web interface (取消 YAML 中相關註解)
2. 瀏覽器設定代理後，訪問 `http://mitm.it`
3. 下載對應平台的證書

## 🔥 進階配置

### 啟用 Web Interface

取消 YAML 中的相關註解，啟用 mitmproxy 的 Web UI：

```yaml
args:
  # ... 其他參數 ...
  - "--web-host"
  - "0.0.0.0"
  - "--web-port"
  - "8081"

ports:
  - name: web
    containerPort: 8081
```

然後透過 Port Forward 存取：
```bash
kubectl port-forward -n mitmproxy service/mitmproxy 8081:8081
# 瀏覽器開啟 http://localhost:8081
```

### 使用 Ingress 暴露服務

如果叢集中有 Ingress Controller：

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mitmproxy-ingress
  namespace: mitmproxy
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  ingressClassName: nginx
  rules:
  - host: mitmproxy.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: mitmproxy
            port:
              number: 8081  # Web interface
```

### 多副本部署 (需謹慎)

mitmproxy 主要用於開發/測試，通常不需要多副本。如果確實需要：

```yaml
spec:
  replicas: 3  # 增加副本數

# 同時需要調整 Service
spec:
  sessionAffinity: ClientIP  # 確保相同客戶端連到同一 Pod
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 3600
```

### 資源配額調整

根據實際流量調整：

```yaml
resources:
  requests:
    memory: "512Mi"   # 基礎記憶體
    cpu: "500m"       # 基礎 CPU
  limits:
    memory: "2Gi"     # 最大記憶體
    cpu: "2000m"      # 最大 CPU
```

### 使用 Secret 存放敏感配置

如果腳本需要 API Key 或密碼：

```bash
# 建立 Secret
kubectl create secret generic mitmproxy-secrets \
  --from-literal=API_KEY=your-api-key \
  -n mitmproxy

# 在 Deployment 中引用
env:
- name: API_KEY
  valueFrom:
    secretKeyRef:
      name: mitmproxy-secrets
      key: API_KEY
```

## 🐛 疑難排解

### Pod 無法啟動

```bash
# 檢查詳細狀態
kubectl describe pod -n mitmproxy -l app=mitmproxy

# 查看事件
kubectl get events -n mitmproxy --sort-by='.lastTimestamp'

# 常見問題：
# 1. PVC 綁定失敗 -> 檢查 StorageClass
# 2. 映像拉取失敗 -> 檢查網路或 ImagePullSecrets
# 3. ConfigMap 掛載失敗 -> 檢查 ConfigMap 是否存在
```

### 記憶體持續增長

檢查是否正確實作記憶體釋放：

```bash
# 查看記憶體使用
kubectl top pod -n mitmproxy

# 檢查日誌是否有異常
kubectl logs -n mitmproxy -l app=mitmproxy --tail=100

# 確認腳本中有 flow.live = False
kubectl get configmap mitmproxy-script -n mitmproxy -o yaml
```

### 無法攔截 HTTPS 流量

```bash
# 確認證書已正確生成
kubectl exec -n mitmproxy -it deployment/mitmproxy -- \
  ls -la /home/mitmproxy/.mitmproxy/

# 匯出證書
kubectl cp mitmproxy/<pod-name>:/home/mitmproxy/.mitmproxy/mitmproxy-ca-cert.pem \
  ./mitmproxy-ca-cert.pem -n mitmproxy

# 確認客戶端已安裝證書
```

### 連線逾時或失敗

```bash
# 測試 Pod 內部連線
kubectl exec -n mitmproxy -it deployment/mitmproxy -- \
  curl -x http://localhost:8080 http://example.com

# 測試 Service 連線
kubectl run -n mitmproxy test-pod --rm -it --image=curlimages/curl -- \
  curl -x http://mitmproxy:8080 http://example.com

# 檢查網路策略
kubectl get networkpolicies -n mitmproxy
```

### 查看即時日誌

```bash
# 即時查看日誌
kubectl logs -n mitmproxy -l app=mitmproxy -f

# 查看特定時間範圍
kubectl logs -n mitmproxy -l app=mitmproxy --since=1h

# 查看前一個容器的日誌 (如果有重啟)
kubectl logs -n mitmproxy -l app=mitmproxy --previous
```

## 📊 監控與維護

### 基本監控

```bash
# 查看資源使用 (需要 metrics-server)
kubectl top pod -n mitmproxy
kubectl top node

# 查看 Pod 狀態
kubectl get pods -n mitmproxy -w

# 查看服務端點
kubectl get endpoints -n mitmproxy
```

### 定期維護

```bash
# 滾動更新 (例如更新映像版本)
kubectl set image deployment/mitmproxy \
  mitmproxy=mitmproxy/mitmproxy:10.2.0 \
  -n mitmproxy

# 擴展/縮減
kubectl scale deployment/mitmproxy --replicas=2 -n mitmproxy

# 重啟 (例如載入新的 ConfigMap)
kubectl rollout restart deployment/mitmproxy -n mitmproxy

# 查看滾動更新狀態
kubectl rollout status deployment/mitmproxy -n mitmproxy

# 回滾到前一版本
kubectl rollout undo deployment/mitmproxy -n mitmproxy
```

### 備份與還原

```bash
# 備份配置
kubectl get all,configmap,pvc -n mitmproxy -o yaml > mitmproxy-backup.yaml

# 備份證書資料
kubectl cp mitmproxy/<pod-name>:/home/mitmproxy/.mitmproxy ./mitmproxy-certs-backup -n mitmproxy

# 還原時重新 apply
kubectl apply -f mitmproxy-backup.yaml
```

## 🧹 清理資源

```bash
# 刪除所有資源 (包含 namespace)
kubectl delete namespace mitmproxy

# 或者選擇性刪除
kubectl delete -f mitmproxy_k8s_deployment.yaml

# 單獨刪除特定資源
kubectl delete deployment mitmproxy -n mitmproxy
kubectl delete service mitmproxy -n mitmproxy
kubectl delete pvc mitmproxy-data -n mitmproxy  # 注意：這會刪除持久化資料
```

## 📚 參考資源

- [mitmproxy 官方文檔](https://docs.mitmproxy.org/)
- [mitmproxy Docker Hub](https://hub.docker.com/r/mitmproxy/mitmproxy)
- [Kubernetes 官方文檔](https://kubernetes.io/docs/)
- 你的現有文檔:
  - `mitmdump_memory_optimization.md` - 記憶體優化策略
  - `mitmdump_systemd_setup_guide.md` - systemd 服務配置

## 💡 最佳實踐建議

1. **記憶體管理**
   - 始終在腳本中設定 `flow.live = False`
   - 使用 `stream_large_bodies` 處理大檔案
   - 設定合理的資源限制

2. **安全性**
   - 不要在公網暴露 mitmproxy 服務
   - 妥善保管 CA 證書
   - 使用 NetworkPolicy 限制流量

3. **可靠性**
   - 配置健康檢查
   - 使用 PVC 持久化重要資料
   - 定期備份配置

4. **效能**
   - 根據流量調整資源配額
   - 考慮使用節點親和性將 Pod 調度到高效能節點
   - 監控記憶體和 CPU 使用情況

---

**需要協助？** 如有任何問題或需要進一步客製化，歡迎隨時詢問！
