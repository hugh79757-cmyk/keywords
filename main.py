from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
import time
import datetime
import os
import xml.etree.ElementTree as ET # XML 파싱용 (구글 트렌드)

# ==========================================
# 🔑 API 키 설정
# ==========================================
SEARCH_CLIENT_ID = os.environ.get("NAVER_CLIENT_ID")
SEARCH_CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET")

# ==========================================
# 💰 AdSense 설정
# ==========================================
PUB_ID = "ca-pub-8772455780561463"
SLOT_ID = "1662647947"

# ==========================================
# 1-A. 애드센스팜 크롤링 (메인)
# ==========================================
def get_keywords_from_farm():
    print("🚗 [메인] 애드센스팜 데이터 수집 시도...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # 봇 탐지 회피 옵션 추가
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get("https://adsensefarm.kr/realtime/")
        time.sleep(7) # 로딩 대기 시간 늘림
        
        # 스크롤
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(1)
        
        # 다양한 선택자로 시도
        elements = driver.find_elements(By.CSS_SELECTOR, "td, .keyword, .rank-text, li, span.txt_rank")
        
        raw_keywords = []
        for elem in elements:
            text = elem.text.strip()
            if len(text) >= 2 and len(text) < 30 and not text.isdigit():
                # 순위 숫자(1.) 제거 및 정제
                clean = ''.join([i for i in text if not i.isdigit()]).replace('.', '').strip()
                if clean and clean not in ["순위", "키워드", "검색량"]: # 헤더 제외
                    raw_keywords.append(clean)
        
        unique = list(dict.fromkeys(raw_keywords))
        print(f"   ↳ 수집 성공: {len(unique)}개")
        return unique[:40]

    except Exception as e:
        print(f"   ↳ ❌ 크롤링 에러: {e}")
        return []
    finally:
        driver.quit()

# ==========================================
# 1-B. 구글 트렌드 RSS (백업용 - 무조건 됨)
# ==========================================
def get_keywords_from_google():
    print("⚠️ [백업] 구글 트렌드 RSS 가동...")
    url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=KR"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            keywords = []
            for item in root.findall(".//item"):
                title = item.find("title").text
                keywords.append(title)
            print(f"   ↳ 백업 데이터 {len(keywords)}개 확보 완료")
            return keywords
    except Exception as e:
        print(f"   ↳ ❌ 백업 실패: {e}")
    
    # 진짜 최후의 비상용 데이터
    return ["손흥민", "날씨", "로또", "환율", "비트코인", "아이폰", "삼성전자", "부동산", "주식", "여행"]

# ==========================================
# 2. 블로그 수 조회
# ==========================================
def get_blog_count(keyword):
    if not SEARCH_CLIENT_ID: return 999999
    
    url = "https://openapi.naver.com/v1/search/blog.json"
    headers = {"X-Naver-Client-Id": SEARCH_CLIENT_ID, "X-Naver-Client-Secret": SEARCH_CLIENT_SECRET}
    try:
        res = requests.get(url, headers=headers, params={"query": keyword, "display": 1})
        if res.status_code == 200: return res.json().get('total', 0)
        return 999999
    except: return 999999

# ==========================================
# 3. HTML 생성 관련 함수들
# ==========================================
def get_common_head(title, description):
    return f"""
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚀</text></svg>">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={PUB_ID}" crossorigin="anonymous"></script>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        :root {{ --bg: #121212; --card: #1e1e1e; --text: #e0e0e0; --accent: #bb86fc; --good: #03dac6; --bad: #cf6679; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Pretendard', sans-serif; background: var(--bg); color: var(--text); }}
        .layout-wrapper {{ display: flex; justify-content: center; gap: 20px; max-width: 1400px; margin: 0 auto; padding: 20px; }}
        .side-rail {{ width: 160px; min-width: 160px; height: 600px; position: sticky; top: 20px; display: none; }}
        .main-content {{ flex: 1; max-width: 800px; width: 100%; }}
        @media (min-width: 1200px) {{ .side-rail {{ display: block; }} }}
        header {{ text-align: center; margin-bottom: 30px; }}
        h1 {{ margin: 0; color: #fff; font-size: 2rem; }}
        .subtitle {{ color: #aaa; font-size: 0.9rem; margin-top: 5px; }}
        .card {{ background: var(--card); border-radius: 15px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ text-align: left; color: #888; font-size: 0.85rem; padding: 10px; border-bottom: 1px solid #333; }}
        td {{ padding: 15px 10px; border-bottom: 1px solid #333; vertical-align: middle; }}
        tr:last-child td {{ border-bottom: none; }}
        .rank-new {{ color: var(--good); font-weight: bold; }}
        .rank-good {{ color: #4facfe; }}
        .rank-bad {{ color: var(--bad); opacity: 0.7; }}
        .btn-copy {{ background: #333; border: none; color: #fff; padding: 5px 10px; border-radius: 5px; cursor: pointer; font-size: 0.8rem; margin-left: 10px; }}
        .btn-copy:hover {{ background: var(--accent); color: #000; }}
        .btn-link {{ color: #bbb; text-decoration: none; font-size: 0.85rem; }}
        .btn-link:hover {{ color: #fff; text-decoration: underline; }}
        .archive-btn {{ display: block; width: 100%; padding: 15px; text-align: center; background: #333; color: white; text-decoration: none; border-radius: 10px; font-weight: bold; transition: 0.2s; }}
        .archive-btn:hover {{ background: var(--accent); color: #000; }}
        .ad-box {{ text-align: center; margin: 20px 0; background: #1a1a1a; padding: 10px; border-radius: 10px; }}
        #toast {{ visibility: hidden; min-width: 250px; background-color: #333; color: #fff; text-align: center; border-radius: 5px; padding: 16px; position: fixed; z-index: 1; left: 50%; bottom: 30px; transform: translateX(-50%); }}
        #toast.show {{ visibility: visible; animation: fadein 0.5s, fadeout 0.5s 2.5s; }}
        @keyframes fadein {{ from {{bottom: 0; opacity: 0;}} to {{bottom: 30px; opacity: 1;}} }}
        @keyframes fadeout {{ from {{bottom: 30px; opacity: 1;}} to {{bottom: 0; opacity: 0;}} }}
    </style>
"""

def get_ad_unit():
    return f"""<div class="ad-box"><ins class="adsbygoogle" style="display:block" data-ad-client="{PUB_ID}" data-ad-slot="{SLOT_ID}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script></div>"""

def get_side_rail_ad():
    return f"""<aside class="side-rail"><div style="font-size:0.7rem; color:#555; text-align:center; margin-bottom:5px;">AD</div><ins class="adsbygoogle" style="display:block" data-ad-client="{PUB_ID}" data-ad-slot="{SLOT_ID}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script></aside>"""

common_script = """<div id="toast">✅ 키워드 복사 완료!</div><script>function copyToClipboard(text) { navigator.clipboard.writeText(text).then(function() { var x = document.getElementById("toast"); x.className = "show"; setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000); }); }</script>"""

# ==========================================
# 4. 메인 실행 함수
# ==========================================
def create_site():
    # 1. 메인 소스 시도
    keywords = get_keywords_from_farm()
    
    # 2. 실패 시 백업 소스 가동 (핵심!)
    if not keywords:
        keywords = get_keywords_from_google()
        
    print(f"📊 최종 {len(keywords)}개 키워드 분석 시작...")
    
    data = []
    for word in keywords:
        count = get_blog_count(word)
        if count < 100: grade="💎 신생"; css="rank-new"
        elif count < 1000: grade="🥇 꿀통"; css="rank-good"
        elif count < 5000: grade="🥈 보통"; css=""
        else: grade="💀 레드오션"; css="rank-bad"
        data.append({"word": word, "count": count, "grade": grade, "css": css})
        time.sleep(0.05)
    
    data.sort(key=lambda x: x['count'])
    
    # HTML 생성
    rows = ""
    for item in data:
        link = f"https://search.naver.com/search.naver?where=view&sm=tab_jum&query={item['word']}"
        rows += f"""<tr><td><span class="{item['css']}">{item['word']}</span><button class="btn-copy" onclick="copyToClipboard('{item['word']}')">복사</button></td><td>{format(item['count'], ',')}</td><td class="{item['css']}">{item['grade']}</td><td><a href="{link}" target="_blank" class="btn-link">분석 ↗</a></td></tr>"""

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    file_date = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    
    # 리포트 저장
    if not os.path.exists("reports"): os.makedirs("reports")
    with open(f"reports/{file_date}.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html lang="ko">{get_common_head(f"리포트 - {now}", "과거 기록")}<body><div class="layout-wrapper">{get_side_rail_ad()}<main class="main-content"><header><h1>📜 리포트</h1><p class="subtitle">{now}</p></header>{get_ad_unit()}<div class="card"><table><thead><tr><th>키워드</th><th>문서수</th><th>등급</th><th>링크</th></tr></thead><tbody>{rows}</tbody></table></div><div style="text-align:center; margin-top:30px;"><a href="../index.html" class="archive-btn">🏠 메인으로</a></div></main>{get_side_rail_ad()}</div>{common_script}</body></html>""")

    # 아카이브 페이지
    report_files = sorted(os.listdir("reports"), reverse=True)
    archive_list = "".join([f'<a href="reports/{rf}" class="archive-btn" style="margin-bottom:10px; text-align:left;">📄 {rf.replace(".html", "").replace("_", " : ")}</a>' for rf in report_files if rf.endswith(".html")])
    with open("archive.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html lang="ko">{get_common_head("🗄️ 아카이브", "지난 기록")}<body><div class="layout-wrapper">{get_side_rail_ad()}<main class="main-content"><header><h1>🗄️ 아카이브</h1><p class="subtitle">지난 기록</p></header>{get_ad_unit()}<div class="card">{archive_list}</div><div style="text-align:center; margin-top:30px;"><a href="index.html" class="archive-btn">🏠 메인으로</a></div></main>{get_side_rail_ad()}</div></body></html>""")

    # 메인 페이지
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html lang="ko">{get_common_head("🚀 황금 키워드 상황실", "실시간 분석")}<body><div class="layout-wrapper">{get_side_rail_ad()}<main class="main-content"><header><h1>🚀 황금 키워드 상황실</h1><p class="subtitle">업데이트: {now}</p></header>{get_ad_unit()}<div class="card"><table><thead><tr><th>키워드</th><th>문서수</th><th>등급</th><th>링크</th></tr></thead><tbody>{rows}</tbody></table></div>{get_ad_unit()}<div style="text-align:center; margin-top:40px;"><a href="archive.html" class="archive-btn">🗄️ 지난 리포트 보기</a></div><footer style="text-align:center; margin-top:50px; color:#555; font-size:0.8rem;">© 2025 Keyword Miner Lab</footer></main>{get_side_rail_ad()}</div>{common_script}</body></html>""")
        
    print("✅ 모든 페이지 생성 완료!")

import cleanup
if __name__ == "__main__":
    create_site()
    cleanup.cleanup_old_reports()
