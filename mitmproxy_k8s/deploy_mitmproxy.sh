#!/bin/bash

# mitmproxy Kubernetes 快速部署腳本
# 使用方式: ./deploy_mitmproxy.sh [action]
# Actions: deploy, status, logs, delete, forward

set -e

NAMESPACE="mitmproxy"
DEPLOYMENT_FILE="mitmproxy_k8s_deployment.yaml"
APP_LABEL="app=mitmproxy"

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

function print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

function print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

function print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

function print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

function check_prerequisites() {
    print_info "檢查前置需求..."
    
    # 檢查 kubectl
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl 未安裝，請先安裝 kubectl"
        exit 1
    fi
    
    # 檢查叢集連線
    if ! kubectl cluster-info &> /dev/null; then
        print_error "無法連線到 Kubernetes 叢集"
        exit 1
    fi
    
    # 檢查部署檔案
    if [ ! -f "$DEPLOYMENT_FILE" ]; then
        print_error "找不到部署檔案: $DEPLOYMENT_FILE"
        exit 1
    fi
    
    print_success "前置檢查完成"
}

function deploy() {
    print_info "開始部署 mitmproxy 到 Kubernetes..."
    
    check_prerequisites
    
    # 顯示將要部署的資源
    print_info "即將部署以下資源:"
    kubectl apply -f "$DEPLOYMENT_FILE" --dry-run=client | grep -E "^(namespace|configmap|persistentvolumeclaim|deployment|service)"
    
    echo ""
    read -p "是否繼續部署? (y/N): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "部署已取消"
        exit 0
    fi
    
    # 執行部署
    kubectl apply -f "$DEPLOYMENT_FILE"
    
    print_success "資源已提交到 Kubernetes"
    
    # 等待 Pod 就緒
    print_info "等待 Pod 啟動..."
    kubectl wait --for=condition=ready pod -l "$APP_LABEL" -n "$NAMESPACE" --timeout=120s || {
        print_warning "Pod 啟動超時，請使用 'status' 指令檢查狀態"
    }
    
    # 顯示狀態
    echo ""
    status
}

function status() {
    print_info "查詢 mitmproxy 狀態..."
    
    echo ""
    echo "=== Namespace ==="
    kubectl get namespace "$NAMESPACE" 2>/dev/null || print_warning "Namespace $NAMESPACE 不存在"
    
    echo ""
    echo "=== Pods ==="
    kubectl get pods -n "$NAMESPACE" -l "$APP_LABEL"
    
    echo ""
    echo "=== Services ==="
    kubectl get svc -n "$NAMESPACE"
    
    echo ""
    echo "=== PVC ==="
    kubectl get pvc -n "$NAMESPACE"
    
    echo ""
    echo "=== Deployment ==="
    kubectl get deployment -n "$NAMESPACE"
    
    echo ""
    echo "=== 資源使用情況 ==="
    kubectl top pod -n "$NAMESPACE" 2>/dev/null || print_warning "需要安裝 metrics-server 才能查看資源使用情況"
}

function logs() {
    print_info "查看 mitmproxy 日誌..."
    
    # 檢查 Pod 是否存在
    if ! kubectl get pods -n "$NAMESPACE" -l "$APP_LABEL" &> /dev/null; then
        print_error "找不到 mitmproxy Pod"
        exit 1
    fi
    
    # 即時追蹤日誌
    kubectl logs -n "$NAMESPACE" -l "$APP_LABEL" -f --tail=100
}

function forward() {
    print_info "設定 Port Forward..."
    
    # 檢查 Pod 是否就緒
    if ! kubectl get pods -n "$NAMESPACE" -l "$APP_LABEL" -o jsonpath='{.items[0].status.phase}' | grep -q "Running"; then
        print_error "Pod 尚未就緒"
        exit 1
    fi
    
    LOCAL_PORT="${1:-8080}"
    
    print_success "正在轉發 localhost:$LOCAL_PORT -> mitmproxy:8080"
    print_info "請在瀏覽器或應用中設定代理為 localhost:$LOCAL_PORT"
    print_info "按 Ctrl+C 停止轉發"
    
    kubectl port-forward -n "$NAMESPACE" service/mitmproxy "$LOCAL_PORT:8080"
}

function get_cert() {
    print_info "匯出 mitmproxy CA 證書..."
    
    POD_NAME=$(kubectl get pods -n "$NAMESPACE" -l "$APP_LABEL" -o jsonpath='{.items[0].metadata.name}')
    
    if [ -z "$POD_NAME" ]; then
        print_error "找不到 mitmproxy Pod"
        exit 1
    fi
    
    OUTPUT_FILE="mitmproxy-ca-cert.pem"
    
    kubectl cp "$NAMESPACE/$POD_NAME:/home/mitmproxy/.mitmproxy/mitmproxy-ca-cert.pem" "$OUTPUT_FILE"
    
    if [ -f "$OUTPUT_FILE" ]; then
        print_success "證書已匯出到: $OUTPUT_FILE"
        print_info "請在你的系統或瀏覽器中安裝此證書以攔截 HTTPS 流量"
    else
        print_error "證書匯出失敗"
        exit 1
    fi
}

function shell() {
    print_info "連線到 mitmproxy Pod..."
    
    POD_NAME=$(kubectl get pods -n "$NAMESPACE" -l "$APP_LABEL" -o jsonpath='{.items[0].metadata.name}')
    
    if [ -z "$POD_NAME" ]; then
        print_error "找不到 mitmproxy Pod"
        exit 1
    fi
    
    kubectl exec -n "$NAMESPACE" -it "$POD_NAME" -- /bin/sh
}

function delete() {
    print_warning "這將刪除所有 mitmproxy 相關資源，包含持久化資料!"
    echo ""
    read -p "確定要刪除嗎? 請輸入 'yes' 確認: " -r
    echo ""
    
    if [[ "$REPLY" != "yes" ]]; then
        print_warning "刪除已取消"
        exit 0
    fi
    
    print_info "開始刪除資源..."
    
    # 刪除所有資源
    kubectl delete -f "$DEPLOYMENT_FILE" --ignore-not-found=true
    
    # 也可以直接刪除整個 namespace
    # kubectl delete namespace "$NAMESPACE" --ignore-not-found=true
    
    print_success "所有資源已刪除"
}

function restart() {
    print_info "重啟 mitmproxy deployment..."
    
    kubectl rollout restart deployment/mitmproxy -n "$NAMESPACE"
    
    print_info "等待新 Pod 就緒..."
    kubectl rollout status deployment/mitmproxy -n "$NAMESPACE"
    
    print_success "重啟完成"
}

function update_script() {
    print_info "更新 mitmproxy 自訂腳本..."
    
    SCRIPT_FILE="${1:-addon.py}"
    
    if [ ! -f "$SCRIPT_FILE" ]; then
        print_error "找不到腳本檔案: $SCRIPT_FILE"
        exit 1
    fi
    
    print_info "從檔案建立 ConfigMap: $SCRIPT_FILE"
    
    kubectl create configmap mitmproxy-script \
        --from-file=addon.py="$SCRIPT_FILE" \
        --namespace="$NAMESPACE" \
        --dry-run=client -o yaml | kubectl apply -f -
    
    print_success "ConfigMap 已更新"
    
    # 重啟以載入新腳本
    restart
}

function usage() {
    cat << EOF
mitmproxy Kubernetes 部署管理腳本

使用方式:
    $0 [action] [options]

Actions:
    deploy              部署 mitmproxy 到 Kubernetes
    status              查看部署狀態
    logs                查看即時日誌
    forward [port]      設定 Port Forward (預設: 8080)
    cert                匯出 CA 證書
    shell               進入 Pod Shell
    restart             重啟 deployment
    update-script <file> 更新自訂腳本 (預設: addon.py)
    delete              刪除所有資源
    help                顯示此說明

範例:
    $0 deploy                    # 部署 mitmproxy
    $0 status                    # 查看狀態
    $0 logs                      # 查看日誌
    $0 forward 8080              # 轉發到本機 8080 port
    $0 cert                      # 匯出證書
    $0 update-script my_addon.py # 更新腳本
    $0 delete                    # 刪除資源

EOF
}

# 主程式
ACTION="${1:-help}"

case "$ACTION" in
    deploy)
        deploy
        ;;
    status)
        status
        ;;
    logs)
        logs
        ;;
    forward)
        forward "$2"
        ;;
    cert)
        get_cert
        ;;
    shell)
        shell
        ;;
    restart)
        restart
        ;;
    update-script)
        update_script "$2"
        ;;
    delete)
        delete
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        print_error "未知的 action: $ACTION"
        echo ""
        usage
        exit 1
        ;;
esac
