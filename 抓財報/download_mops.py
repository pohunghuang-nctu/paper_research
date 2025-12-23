"""
從證交所電子書網站下載財務報告的工具模組
"""
import requests
from bs4 import BeautifulSoup
import os
import re
import urllib3
from datetime import datetime
from typing import Optional, List, Dict

# 停用 SSL 警告 (因為使用 IP 連線時會有憑證不匹配的警告)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# DNS workaround: 如果無法解析 doc.twse.com.tw，使用 IP
DOC_TWSE_IP = "163.29.17.136"
USE_IP_WORKAROUND = True  # 設為 False 如果 DNS 正常

SEASON_MAP = {1: '第一季', 2: '第二季', 3: '第三季', 4: '第四季'}


def _get_base_url() -> str:
    """取得 API 基礎 URL"""
    if USE_IP_WORKAROUND:
        return f"https://{DOC_TWSE_IP}/server-java/t57sb01"
    return "https://doc.twse.com.tw/server-java/t57sb01"


def _get_headers() -> dict:
    """取得 HTTP headers"""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Host': 'doc.twse.com.tw'
    }


def _query_reports(co_id: int, year: int) -> List[Dict]:
    """
    查詢指定公司和年度的財報列表
    
    Returns:
        List of dict with keys: filename, season, row_text
    """
    url = _get_base_url()
    headers = _get_headers()
    
    params = {
        'step': '1',
        'colorchg': '1',
        'co_id': str(co_id),
        'year': str(year),
        'seamon': '',
        'mtype': 'A'
    }
    
    response = requests.get(url, params=params, headers=headers, verify=not USE_IP_WORKAROUND)
    response.encoding = 'big5'
    
    soup = BeautifulSoup(response.text, 'html.parser')
    pattern = re.compile(r'readfile2\("A","(\d+)","([^"]+\.pdf)"\)')
    
    reports = []
    for link in soup.find_all('a', href=True):
        match = pattern.search(link['href'])
        if match:
            filename = match.group(2)
            row = link.find_parent('tr')
            row_text = row.get_text() if row else ''
            
            # 解析季度
            season = None
            for s, s_text in SEASON_MAP.items():
                if s_text in row_text:
                    season = s
                    break
            
            # 只收集中文版合併財報 (AI1)，跳過英文版 (AIA)
            if 'AIA' not in filename:
                reports.append({
                    'filename': filename,
                    'season': season,
                    'row_text': row_text,
                    'year': year
                })
    
    return reports


def _download_single_report(co_id: int, filename: str, output_dir: str = ".") -> Optional[str]:
    """
    下載單一財報檔案
    
    Returns:
        下載成功時回傳檔案路徑，失敗時回傳 None
    """
    url = _get_base_url()
    headers = _get_headers()
    
    # 第一步：POST 取得真正的 PDF 連結
    download_data = {
        'step': '9',
        'kind': 'A',
        'co_id': str(co_id),
        'filename': filename
    }
    
    resp1 = requests.post(url, data=download_data, headers=headers, verify=not USE_IP_WORKAROUND)
    resp1.encoding = 'big5'
    
    soup = BeautifulSoup(resp1.text, 'html.parser')
    pdf_link = soup.find('a', href=re.compile(r'\.pdf$'))
    
    if not pdf_link:
        return None
    
    pdf_path = pdf_link['href']
    if USE_IP_WORKAROUND:
        pdf_url = f"https://{DOC_TWSE_IP}{pdf_path}"
    else:
        pdf_url = f"https://doc.twse.com.tw{pdf_path}"
    
    # 第二步：下載實際的 PDF 檔案
    pdf_resp = requests.get(pdf_url, headers=headers, verify=not USE_IP_WORKAROUND)
    
    if pdf_resp.status_code == 200 and len(pdf_resp.content) > 1000:
        output_path = os.path.join(output_dir, filename)
        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(pdf_resp.content)
        return output_path
    
    return None


def download_latest_report(co_id: int, year: int, output_dir: str = ".") -> Optional[str]:
    """
    下載指定公司和年度的最新一季財報
    
    Args:
        co_id: 公司代號 (如 1101, 2330)
        year: 民國年 (如 113, 114)
        output_dir: 輸出目錄，預設為當前目錄
    
    Returns:
        下載成功時回傳檔案路徑，失敗時回傳 None
    
    Example:
        >>> download_latest_report(2330, 113)
        '202403_2330_AI1.pdf'
    """
    print(f"正在搜尋 {co_id} 在民國 {year} 年的財報...")
    
    reports = _query_reports(co_id, year)
    
    if not reports:
        print("未找到相關財報，可能是該年度財報尚未公佈，或公司代號錯誤。")
        return None
    
    # 找出最新一季 (季度數字最大的)
    reports_with_season = [r for r in reports if r['season'] is not None]
    if not reports_with_season:
        print("無法判斷財報季度")
        return None
    
    latest = max(reports_with_season, key=lambda x: x['season'])
    
    print(f"找到最新財報: 第{latest['season']}季 - {latest['filename']}")
    print(f"準備下載...")
    
    result = _download_single_report(co_id, latest['filename'], output_dir)
    
    if result:
        file_size = os.path.getsize(result)
        print(f"下載成功！已儲存為 {result} ({file_size:,} bytes)")
    else:
        print(f"下載失敗: {latest['filename']}")
    
    return result


def download_all_reports(co_id: int, year: int, output_dir: str = ".") -> List[str]:
    """
    下載指定公司和年度的所有財報
    
    Args:
        co_id: 公司代號 (如 1101, 2330)
        year: 民國年 (如 113, 114)
        output_dir: 輸出目錄，預設為當前目錄
    
    Returns:
        成功下載的檔案路徑列表
    
    Example:
        >>> download_all_reports(2330, 113)
        ['202401_2330_AI1.pdf', '202402_2330_AI1.pdf', ...]
    """
    print(f"正在搜尋 {co_id} 在民國 {year} 年的財報...")
    
    reports = _query_reports(co_id, year)
    
    if not reports:
        print("未找到相關財報，可能是該年度財報尚未公佈，或公司代號錯誤。")
        return []
    
    print(f"找到 {len(reports)} 個檔案")
    
    downloaded = []
    for report in reports:
        print(f"準備下載: {report['filename']}")
        result = _download_single_report(co_id, report['filename'], output_dir)
        
        if result:
            file_size = os.path.getsize(result)
            print(f"  下載成功！({file_size:,} bytes)")
            downloaded.append(result)
        else:
            print(f"  下載失敗")
    
    print(f"\n共下載 {len(downloaded)}/{len(reports)} 個檔案")
    return downloaded


# --- 執行範例 ---
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='下載證交所財務報告')
    parser.add_argument('co_id', type=int, help='公司代號 (如 1101, 2330)')
    parser.add_argument('year', type=int, help='民國年 (如 113, 114)')
    parser.add_argument('-o', '--output', default='.', help='輸出目錄 (預設: 當前目錄)')
    parser.add_argument('-a', '--all', action='store_true', help='下載該年度所有財報，而非僅最新一季')
    
    args = parser.parse_args()
    
    if args.all:
        download_all_reports(co_id=args.co_id, year=args.year, output_dir=args.output)
    else:
        download_latest_report(co_id=args.co_id, year=args.year, output_dir=args.output)