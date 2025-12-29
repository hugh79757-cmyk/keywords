from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
import time
import datetime
import os

# ==========================================
# 🔑 API 키 설정 (GitHub Secrets 사용 권장)
# ==========================================
# 로컬 테스트 시에는 아래에 직접 입력하세요.
SEARCH_CLIENT_ID = os.environ.get("NAVER_CLIENT_ID", "내_클라이언트_ID")
SEARCH_CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET", "내_시크릿_키")

# ==========================================
# 💰 AdSense 설정
# ==========================================
PUB_ID = "ca-pub-8772455780561463"
SLOT_ID = "1662647947"

# 1. 공통 헤더/스타일/광고 스크립트 생성 함수
def get_common_head(title, description):
    return f"""
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚀</text></svg>">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- ✅ Google AdSense (자동 광고) -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={PUB_ID}"
         crossorigin="anonymous"></script>

    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        
        :root {{
            --bg: #121212; --card: #1e1e1e; --text: #e0e0e0; --accent: #bb86fc;
            --good: #03dac6; --bad: #cf6679;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Pretendard', sans-serif; background: var(--bg); color: var(--text); }}
        
        /* 레이아웃 (사이드레일 광고용) */
        .layout-wrapper {{
            display: flex; justify-content: center; gap: 20px;
            max-width: 1400px; margin: 0 auto; padding: 20px;
        }}
        
        .side-rail {{
            width: 160px; min-width: 160px; height: 600px;
            position: sticky; top: 20px; display: none; /* 모바일 숨김 */
        }}
        
        .main-content {{ flex: 1; max-width: 800px; width: 100%; }}
        
        @media (min-width: 1200px) {{ .side-rail {{ display: block; }} }}

        /* 헤더 */
        header {{ text-align: center; margin-bottom: 30px; }}
        h1 {{ margin: 0; color: #fff; font-size: 2rem; }}
        .subtitle {{ color: #aaa; font-size: 0.9rem; margin-top: 5px; }}
        
        /* 카드 스타일 */
        .card {{ background: var(--card); border-radius: 15px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin-bottom: 20px; }}
        
        /* 테이블 */
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ text-align: left; color: #888; font-size: 0.85rem; padding: 10px; border-bottom: 1px solid #333; }}
        td {{ padding: 15px 10px; border-bottom: 1px solid #333; vertical-align: middle; }}
        tr:last-child td {{ border-bottom: none; }}
        
        /* 등급별 색상 */
        .rank-new {{ color: var(--good); font-weight: bold; }}
        .rank-good {{ color: #4facfe; }}
        .rank-bad {{ color: var(--bad); opacity: 0.7; }}
        
        /* 버튼 */
        .btn-copy {{ background: #333; border: none; color: #fff; padding: 5px 10px; border-radius: 5px; cursor: pointer; font-size: 0.8rem; margin-left: 10px; }}
        .btn-copy:hover {{ background: var(--accent); color: #000; }}
        .btn-link {{ color: #bbb; text-decoration: none; font-size: 0.85rem; }}
        .btn-link:hover {{ color: #fff; text-decoration: underline; }}
        
        /* 아카이브 버튼 */
        .archive-btn {{
            display: block; width: 100%; padding: 15px; text-align: center;
            background: #333; color: white; text-decoration: none; border-radius: 10px;
            font-weight: bold; transition: 0.2s;
        }}
        .archive-btn:hover {{ background: var(--accent); color: #000; }}

        /* 광고 박스 */
        .ad-box {{ text-align: center; margin: 20px 0; background: #1a1a1a; padding: 10px; border-radius: 10px; }}
        
        /* 토스트 메시지 */
        #toast {{ visibility: hidden; min-width: 250px; background-color: #333; color: #fff; text-align: center; border-radius: 5px; padding: 16px; position: fixed; z-index: 1; left: 50%; bottom: 30px; transform: translateX(-50%); }}
        #toast.show {{ visibility: visible; animation: fadein 0.5s, fadeout 0.5s 2.5s; }}
        @keyframes fadein {{ from {{bottom: 0; opacity: 0;}} to {{bottom: 30px; opacity: 1;}} }}
        @keyframes fadeout {{ from {{bottom: 30px; opacity: 1;}} to {{bottom: 0; opacity: 0;}} }}
    </style>
</head>
"""

# 2. 광고 유닛 생성 함수 (수평형)
def get_ad_unit():
    return f"""
    <div class="ad-box">
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="{PUB_ID}"
             data-ad-slot="{SLOT_ID}"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    </div>
    """

# 3. 사이드 레일 광고 생성 함수
def get_side_rail_ad():
    return f"""
    <aside class="side-rail">
        <div style="font-size:0.7rem; color:#555; text-align:center; margin-bottom:5px;">AD</div>
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="{PUB_ID}"
             data-ad-slot="{SLOT_ID}"  <!-- 사이드용 슬롯ID가 따로 있으면 교체 권장 -->
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    </aside>
    """

# 4. 공통 스크립트
common_script = """
<div id="toast">✅ 키워드 복사 완료!</div>
<script>
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(function() {
            var x = document.getElementById("toast");
            x.className = "show";
            setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
        });
    }
</script>
"""

# ==========================================
# 5. 크롤링 및 데이터 처리
# ==========================================
def get_raw_keywords():
    print("🚗 데이터 수집 중...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get("https://adsensefarm.kr/realtime/")
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, 1000);")
        time.sleep(2)
        elements = driver.find_elements(By.CSS_SELECTOR, "td, .keyword, .rank-text, li")
        raw_keywords = []
        for elem in elements:
            text = elem.text.strip()
            if len(text) >= 2 and len(text) < 30 and not text.isdigit():
                clean = ''.join([i for i in text if not i.isdigit()]).replace('.', '').strip()
                if clean: raw_keywords.append(clean)
        return list(dict.fromkeys(raw_keywords))[:40]
    except: return []
    finally: driver.quit()

def get_blog_count(keyword):
    if "내_클라이언트_ID" in SEARCH_CLIENT_ID: return 999999
    url = "https://openapi.naver.com/v1/search/blog.json"
    headers = {"X-Naver-Client-Id": SEARCH_CLIENT_ID, "X-Naver-Client-Secret": SEARCH_CLIENT_SECRET}
    try:
        res = requests.get(url, headers=headers, params={"query": keyword, "display": 1})
        if res.status_code == 200: return res.json().get('total', 0)
        return 999999
    except: return 999999

# ==========================================
# 6. 메인 실행 함수
# ==========================================
def create_site():
    keywords = get_raw_keywords()
    data = []
    print(f"📊 {len(keywords)}개 키워드 분석 중...")
    
    for word in keywords:
        count = get_blog_count(word)
        if count < 100: grade = "💎 신생"; css = "rank-new"
        elif count < 1000: grade = "🥇 꿀통"; css = "rank-good"
        elif count < 5000: grade = "🥈 보통"; css = ""
        else: grade = "💀 레드오션"; css = "rank-bad"
        data.append({"word": word, "count": count, "grade": grade, "css": css})
        time.sleep(0.05)
    
    data.sort(key=lambda x: x['count'])
    
    # 테이블 행 생성
    rows = ""
    for item in data:
        link = f"https://search.naver.com/search.naver?where=view&sm=tab_jum&query={item['word']}"
        rows += f"""
        <tr>
            <td>
                <span class="{item['css']}">{item['word']}</span>
                <button class="btn-copy" onclick="copyToClipboard('{item['word']}')">복사</button>
            </td>
            <td>{format(item['count'], ',')}</td>
            <td class="{item['css']}">{item['grade']}</td>
            <td><a href="{link}" target="_blank" class="btn-link">분석 ↗</a></td>
        </tr>
        """

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    file_date = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    
    # 1) 개별 리포트 생성 (Archive)
    if not os.path.exists("reports"): os.makedirs("reports")
    report_html = f"""<!DOCTYPE html><html lang="ko">
    {get_common_head(f"리포트 - {now}", "과거 키워드 분석 기록")}
    <body>
        <div class="layout-wrapper">
            {get_side_rail_ad()} <!-- 왼쪽 광고 -->
            
            <main class="main-content">
                <header>
                    <h1>📜 과거 리포트</h1>
                    <p class="subtitle">{now} 기준 분석 데이터</p>
                </header>
                
                {get_ad_unit()} <!-- 상단 광고 -->
                
                <div class="card">
                    <table>
                        <thead><tr><th>키워드</th><th>문서수</th><th>등급</th><th>링크</th></tr></thead>
                        <tbody>{rows}</tbody>
                    </table>
                </div>
                
                {get_ad_unit()} <!-- 하단 광고 -->
                
                <div style="text-align:center; margin-top:30px;">
                    <a href="../index.html" class="archive-btn">🏠 메인으로 돌아가기</a>
                </div>
            </main>
            
            {get_side_rail_ad()} <!-- 오른쪽 광고 -->
        </div>
        {common_script}
    </body></html>"""
    
    with open(f"reports/{file_date}.html", "w", encoding="utf-8") as f:
        f.write(report_html)

    # 2) 아카이브 목록 페이지 생성 (archive.html)
    report_files = sorted(os.listdir("reports"), reverse=True)
    archive_list = ""
    for rf in report_files:
        if rf.endswith(".html"):
            name = rf.replace(".html", "").replace("_", " : ")
            archive_list += f'<a href="reports/{rf}" class="archive-btn" style="margin-bottom:10px; text-align:left;">📄 리포트 - {name}</a>'
            
    archive_page_html = f"""<!DOCTYPE html><html lang="ko">
    {get_common_head("🗄️ 리포트 보관함", "지난 키워드 분석 기록 모음")}
    <body>
        <div class="layout-wrapper">
            {get_side_rail_ad()}
            <main class="main-content">
                <header>
                    <h1>🗄️ 리포트 보관함</h1>
                    <p class="subtitle">지난 분석 기록을 확인하세요</p>
                </header>
                {get_ad_unit()}
                <div class="card">
                    {archive_list}
                </div>
                <div style="text-align:center; margin-top:30px;">
                    <a href="index.html" class="archive-btn">🏠 메인으로 돌아가기</a>
                </div>
            </main>
            {get_side_rail_ad()}
        </div>
    </body></html>"""
    
    with open("archive.html", "w", encoding="utf-8") as f:
        f.write(archive_page_html)

    # 3) 메인 페이지 생성 (index.html) - 최신 데이터만 표시
    index_html = f"""<!DOCTYPE html><html lang="ko">
    {get_common_head("🚀 황금 키워드 상황실", "실시간 트렌드 및 블루오션 키워드 분석")}
    <body>
        <div class="layout-wrapper">
            {get_side_rail_ad()} <!-- 왼쪽 사이드레일 -->
            
            <main class="main-content">
                <header>
                    <h1>🚀 황금 키워드 상황실</h1>
                    <p class="subtitle">실시간 트렌드 & 경쟁률 분석 (업데이트: {now})</p>
                </header>
                
                {get_ad_unit()} <!-- 상단 광고 -->
                
                <div class="card">
                    <table>
                        <thead><tr><th>키워드</th><th>문서수</th><th>등급</th><th>링크</th></tr></thead>
                        <tbody>{rows}</tbody>
                    </table>
                </div>
                
                {get_ad_unit()} <!-- 하단 광고 -->
                
                <div style="text-align:center; margin-top:40px;">
                    <a href="archive.html" class="archive-btn">🗄️ 지난 리포트 보기 (Archive)</a>
                </div>
                
                <footer style="text-align:center; margin-top:50px; color:#555; font-size:0.8rem;">
                    © 2025 Keyword Miner Lab
                </footer>
            </main>
            
            {get_side_rail_ad()} <!-- 오른쪽 사이드레일 -->
        </div>
        {common_script}
    </body></html>"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
        
    print("✅ 모든 페이지 생성 완료!")

if __name__ == "__main__":
    create_site()
