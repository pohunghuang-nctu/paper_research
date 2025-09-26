#!/usr/bin/env python3
"""
Codeium Analytics API 測試腳本
專門用於 Cascade Lines Analytics 查詢
API 端點: https://server.codeium.com/api/v1/Analytics
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class CodeiumAnalyticsAPI:
    def __init__(self, service_key: str):
        """
        初始化 Codeium Analytics API 客戶端
        
        Args:
            service_key: Codeium 服務金鑰
        """
        self.base_url = "https://server.codeium.com/api/v1"
        self.service_key = service_key
        self.session = requests.Session()
        
    def analytics_query(self, query_requests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        執行 Analytics 查詢
        
        Args:
            query_requests: 查詢請求列表
            
        Returns:
            API 回應結果
        """
        url = f"{self.base_url}/Analytics"
        
        payload = {
            "service_key": self.service_key,
            "query_requests": query_requests
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            response = self.session.post(
                url, 
                json=payload, 
                headers=headers,
                timeout=30
            )
            
            print(f"請求 URL: {url}")
            print(f"請求狀態碼: {response.status_code}")
            print(f"請求標頭: {headers}")
            print(f"請求內容: {json.dumps(payload, indent=2, ensure_ascii=False)}")
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"錯誤回應: {response.text}")
                response.raise_for_status()
                
        except requests.exceptions.RequestException as e:
            print(f"請求失敗: {e}")
            raise
    
    def query_cascade_lines_analytics(
        self, 
        fields: List[str] = None, 
        start_date: str = None, 
        end_date: str = None
    ) -> Dict[str, Any]:
        """
        查詢 Cascade Lines Analytics 資料
        
        Args:
            fields: 要查詢的欄位列表
            start_date: 開始日期 (格式: YYYY-MM-DD 或 YYYY-MM-DDTHH:MM:SS)
            end_date: 結束日期 (格式: YYYY-MM-DD 或 YYYY-MM-DDTHH:MM:SS)
            
        Returns:
            查詢結果
        """
        if fields is None:
            fields = ["api_key", "email", "hour", "lines_accepted", "cascade_insertions"]
            
        selections = [
            {
                "field": field,
                "name": field
            }
            for field in fields
        ]
        
        # 建構查詢請求
        query_request = {
            "data_source": "QUERY_DATA_SOURCE_CASCADE_LINES_ANALYTICS",
            "selections": selections
        }
        
        # 如果有日期篩選條件，加入 filters
        if start_date or end_date:
            filters = []
            
            if start_date:
                filters.append({
                    "name": "hour",
                    "filter": "QUERY_FILTER_GE",
                    "value": start_date
                })
                
            if end_date:
                filters.append({
                    "name": "hour", 
                    "filter": "QUERY_FILTER_LE",
                    "value": end_date
                })
                
            query_request["filters"] = filters
        
        query_requests = [query_request]
        return self.analytics_query(query_requests)
    
    def query_recent_cascade_data(self, days: int = 7) -> Dict[str, Any]:
        """
        查詢最近幾天的 Cascade 資料
        
        Args:
            days: 查詢最近幾天的資料，預設 7 天
            
        Returns:
            查詢結果
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return self.query_cascade_lines_analytics(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d")
        )
    
    def query_specific_fields(self, fields: List[str]) -> Dict[str, Any]:
        """
        查詢特定欄位的資料
        
        Args:
            fields: 要查詢的欄位列表
            
        Returns:
            查詢結果
        """
        return self.query_cascade_lines_analytics(fields=fields)

def main():
    """
    主要測試函數
    """
    print("=== Codeium Cascade Lines Analytics API 測試腳本 ===\n")
    
    # 從多種來源取得 API 金鑰
    service_key = None
    
    # 1. 嘗試從 .windsurf_svc_key 檔案讀取
    key_file_path = os.path.join(os.path.dirname(__file__), ".windsurf_svc_key")
    if os.path.exists(key_file_path):
        try:
            with open(key_file_path, 'r') as f:
                service_key = f.read().strip()
                print(f"從 {key_file_path} 讀取服務金鑰")
        except Exception as e:
            print(f"讀取金鑰檔案失敗: {e}")
    
    # 2. 如果檔案不存在或讀取失敗，嘗試環境變數
    if not service_key:
        service_key = os.getenv("CODEIUM_SERVICE_KEY")
        if service_key:
            print("從環境變數 CODEIUM_SERVICE_KEY 讀取服務金鑰")
    
    # 3. 最後選項：使用者輸入
    if not service_key:
        service_key = input("請輸入您的 Codeium Service Key: ").strip()
        
    if not service_key:
        print("錯誤: 未提供 Service Key")
        return
    
    # 初始化 API 客戶端
    api = CodeiumAnalyticsAPI(service_key)
    
    try:
        print("1. 測試基本 Cascade Lines Analytics 查詢...")
        print("查詢所有可用欄位...")
        basic_data = api.query_cascade_lines_analytics()
        print("基本查詢結果:")
        print(json.dumps(basic_data, indent=2, ensure_ascii=False))
        print("\n" + "="*50 + "\n")
        
        print("2. 測試最近 7 天的資料查詢...")
        recent_data = api.query_recent_cascade_data(days=7)
        print("最近 7 天資料查詢結果:")
        print(json.dumps(recent_data, indent=2, ensure_ascii=False))
        print("\n" + "="*50 + "\n")
        
        print("3. 測試特定欄位查詢...")
        specific_fields = ["lines_accepted", "cascade_insertions"]
        field_data = api.query_specific_fields(specific_fields)
        print("特定欄位查詢結果:")
        print(json.dumps(field_data, indent=2, ensure_ascii=False))
        print("\n" + "="*50 + "\n")
        
        print("4. 測試帶日期範圍的查詢...")
        # 查詢最近 3 天的資料
        end_date = datetime.now()
        start_date = end_date - timedelta(days=3)
        
        date_range_data = api.query_cascade_lines_analytics(
            fields=["api_key", "hour", "lines_accepted", "cascade_insertions"],
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d")
        )
        print(f"日期範圍查詢結果 ({start_date.strftime('%Y-%m-%d')} 到 {end_date.strftime('%Y-%m-%d')}):")
        print(json.dumps(date_range_data, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"測試失敗: {e}")
        import traceback
        traceback.print_exc()

def demo_payload():
    """
    展示範例 payload 結構
    """
    print("=== 範例 API Payload 結構 ===\n")
    
    sample_payload = {
        "service_key": "YOUR_SERVICE_KEY",
        "query_requests": [
            {
                "data_source": "QUERY_DATA_SOURCE_CASCADE_LINES_ANALYTICS",
                "selections": [
                    {"field": "api_key", "name": "api_key"},
                    {"field": "email", "name": "email"},
                    {"field": "hour", "name": "hour"},
                    {"field": "lines_accepted", "name": "lines_accepted"},
                    {"field": "cascade_insertions", "name": "cascade_insertions"}
                ],
                "filters": [
                    {
                        "name": "hour",
                        "filter": "QUERY_FILTER_GE",
                        "value": "START_DATE"
                    },
                    {
                        "name": "hour",
                        "filter": "QUERY_FILTER_LE", 
                        "value": "END_DATE"
                    }
                ]
            }
        ]
    }
    
    print(json.dumps(sample_payload, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_payload()
    else:
        main()
