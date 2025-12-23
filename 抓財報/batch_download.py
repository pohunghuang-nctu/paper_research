"""
批次下載所有上市台股的最新財報
"""
import requests
from bs4 import BeautifulSoup
import time
import re
import os
from datetime import datetime
from download_mops import download_latest_report

# 設定
CURRENT_ROC_YEAR = 114  # 民國 114 年
DOWNLOAD_INTERVAL = 10  # 每次下載間隔秒數
OUTPUT_DIR = "./財報下載"


def get_listed_stocks() -> list:
    """
    從證交所取得所有上市股票代號列表
    
    Returns:
        list of tuples: [(stock_id, stock_name), ...]
    """
    url = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    print("正在取得上市公司列表...")
    
    resp = requests.get(url, headers=headers)
    resp.encoding = 'big5'
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    stocks = []
    in_stock_section = False
    
    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if not cells:
            continue
        
        first_cell = cells[0].get_text(strip=True)
        
        # 檢查是否進入「股票」區段
        if '股票' in first_cell and len(cells) == 1:
            in_stock_section = True
            continue
        
        # 檢查是否離開「股票」區段 (進入其他類型如 ETF、權證等)
        if in_stock_section and len(cells) == 1:
            # 遇到下一個類別標題，結束股票區段
            break
        
        # 解析股票資料
        if in_stock_section and len(cells) >= 4:
            code_name = first_cell
            market = cells[3].get_text(strip=True) if len(cells) > 3 else ''
            
            # 只取上市股票，格式如 "1101　台泥"
            if '上市' in market:
                # 解析代號和名稱
                match = re.match(r'^(\d{4})\s*(.+)$', code_name)
                if match:
                    stock_id = match.group(1)
                    stock_name = match.group(2).strip()
                    stocks.append((stock_id, stock_name))
    
    print(f"共找到 {len(stocks)} 檔上市股票")
    return stocks


def batch_download_reports(year: int = CURRENT_ROC_YEAR, 
                           output_dir: str = OUTPUT_DIR,
                           interval: int = DOWNLOAD_INTERVAL,
                           start_from: str = None,
                           max_count: int = None):
    """
    批次下載所有上市股票的最新財報
    
    Args:
        year: 民國年 (預設: 114)
        output_dir: 輸出目錄
        interval: 每次下載間隔秒數 (預設: 10)
        start_from: 從指定股票代號開始 (用於續傳)
        max_count: 最多下載幾檔 (用於測試)
    """
    stocks = get_listed_stocks()
    
    if not stocks:
        print("無法取得股票列表")
        return
    
    # 如果指定從某個代號開始
    if start_from:
        start_idx = next((i for i, s in enumerate(stocks) if s[0] == start_from), 0)
        stocks = stocks[start_idx:]
        print(f"從 {start_from} 開始，剩餘 {len(stocks)} 檔")
    
    # 限制數量
    if max_count:
        stocks = stocks[:max_count]
    
    # 建立輸出目錄
    os.makedirs(output_dir, exist_ok=True)
    
    # 記錄檔
    log_file = os.path.join(output_dir, "download_log.txt")
    
    success_count = 0
    fail_count = 0
    
    print(f"\n開始批次下載，共 {len(stocks)} 檔股票")
    print(f"輸出目錄: {output_dir}")
    print(f"下載間隔: {interval} 秒")
    print("=" * 50)
    
    for i, (stock_id, stock_name) in enumerate(stocks, 1):
        print(f"\n[{i}/{len(stocks)}] {stock_id} {stock_name}")
        
        try:
            result = download_latest_report(
                co_id=int(stock_id), 
                year=year, 
                output_dir=output_dir
            )
            
            if result:
                success_count += 1
                status = "成功"
            else:
                fail_count += 1
                status = "無資料"
            
            # 寫入 log
            with open(log_file, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{timestamp} | {stock_id} | {stock_name} | {status}\n")
                
        except Exception as e:
            fail_count += 1
            print(f"  錯誤: {e}")
            with open(log_file, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{timestamp} | {stock_id} | {stock_name} | 錯誤: {e}\n")
        
        # 間隔等待 (最後一筆不用等)
        if i < len(stocks):
            print(f"  等待 {interval} 秒...")
            time.sleep(interval)
    
    print("\n" + "=" * 50)
    print(f"下載完成！成功: {success_count}, 失敗/無資料: {fail_count}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='批次下載所有上市台股財報')
    parser.add_argument('-y', '--year', type=int, default=CURRENT_ROC_YEAR,
                        help=f'民國年 (預設: {CURRENT_ROC_YEAR})')
    parser.add_argument('-o', '--output', default=OUTPUT_DIR,
                        help=f'輸出目錄 (預設: {OUTPUT_DIR})')
    parser.add_argument('-i', '--interval', type=int, default=DOWNLOAD_INTERVAL,
                        help=f'下載間隔秒數 (預設: {DOWNLOAD_INTERVAL})')
    parser.add_argument('-s', '--start', default=None,
                        help='從指定股票代號開始 (用於續傳)')
    parser.add_argument('-n', '--max', type=int, default=None,
                        help='最多下載幾檔 (用於測試)')
    
    args = parser.parse_args()
    
    batch_download_reports(
        year=args.year,
        output_dir=args.output,
        interval=args.interval,
        start_from=args.start,
        max_count=args.max
    )
