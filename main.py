from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
import time
import datetime
import os
import cleanup      # 같은 폴더에 cleanup.py가 있어야 함
import sitemap_gen  # 같은 폴더에 sitemap_gen.py가 있어야 함

# ==========================================
# 🔑 API 키
# ==========================================
SEARCH_CLIENT_ID = os.environ.get("NAVER_CLIENT_ID")
SEARCH_CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET")

# ==========================================
# 💰 AdSense 설정
# ==========================================
PUB_ID = "ca-pub-8772455780561463"
SLOT_ID = "1662647947"

# ==========================================
# SEO 메타 태그 생성 함수
# ==========================================
def get_seo_meta_tags(page_type="index", title="", description="", keywords="", url=""):
    base_url = "https://keywords.rotcha.kr"
    
    if page_type == "index":
        full_title = "🚀 황금 키워드 상황실 - 실시간 블로그 키워드 트렌드 분석"
        full_description = "실시간 트렌드 키워드 분석으로 블루오션 키워드를 찾아보세요. 네이버 블로그 SEO 최적화를 위한 황금 키워드 발굴 대시보드."
        full_keywords = "키워드 분석, 블로그 키워드, SEO, 키워드 도구, 블루오션 키워드, 네이버 블로그"
        canonical_url = f"{base_url}/"
    elif page_type == "archive":
        full_title = "🗄️ 리포트 아카이브 - 황금 키워드 상황실"
        full_description = "과거 키워드 분석 리포트 아카이브. 시간대별 트렌드 변화를 확인하세요."
        full_keywords = "키워드 아카이브, 트렌드 분석, 키워드 히스토리"
        canonical_url = f"{base_url}/archive.html"
    elif page_type == "report":
        full_title = f"📜 {title} - 키워드 리포트"
        full_description = description
        full_keywords = keywords
        canonical_url = url
    
    return f"""
    <meta name="description" content="{full_description}">
    <meta name="keywords" content="{full_keywords}">
    <meta name="author" content="황금 키워드 상황실">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical_url}">
    <meta property="og:title" content="{full_title}">
    <meta property="og:description" content="{full_description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    """

def get_structured_data(page_type="index", update_time=""):
    if page_type == "index":
        return """<script type="application/ld+json">{"@context": "https://schema.org","@type": "WebApplication","name": "황금 키워드 상황실","description": "실시간 블로그 키워드 트렌드 분석 대시보드","url": "https://keywords.rotcha.kr"}</script>"""
    return ""

# ==========================================
# CSS 스타일 (디자인 핵심)
# ==========================================
def get_optimized_style():
    return """
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        
        :root {
            --bg: #121212; --card: #1e1e1e; --text: #e0e0e0; --accent: #bb86fc;
            --good: #03dac6; --bad: #cf6679;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Pretendard', sans-serif; background: var(--bg); color: var(--text); padding-bottom: 50px; }
        
        /* 레이아웃 */
        .layout-wrapper { display: flex; justify-content: center; gap: 20px; max-width: 1400px; margin: 0 auto; padding: 20px; }
        .side-rail { width: 160px; min-width: 160px; height: 600px; position: sticky; top: 20px; display: none; }
        .main-content { flex: 1; max-width: 800px; width: 100%; }
        @media (min-width: 1200px) { .side-rail { display: block; } }

        /* 헤더 */
        header { text-align: center; margin-bottom: 30px; }
        h1 { margin: 0; color: #fff; font-size: 1.8rem; }
        .subtitle { color: #aaa; font-size: 0.9rem; margin-top: 5px; }
        .update-time { display: inline-flex; align-items: center; gap: 8px; margin-top: 15px; padding: 5px 15px; background: rgba(255,255,255,0.1); border-radius: 20px; font-size: 0.8rem; }
        .pulse { width: 8px; height: 8px; background: var(--good); border-radius: 50%; animation: pulse 2s infinite; }
        @keyframes pulse { 0% { opacity: 1; transform: scale(1); } 50% { opacity: 0.5; transform: scale(1.2); } }

        /* 통계 카드 */
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; margin-bottom: 20px; }
        .stat-card { background: var(--card); border-radius: 10px; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
        .stat-icon { font-size: 1.5rem; margin-bottom: 5px; }
        .stat-value { font-size: 1.2rem; font-weight: bold; color: #fff; }
        .stat-label { font-size: 0.8rem; color: #aaa; }

        /* 키워드 카드 (모바일) */
        .keyword-list-mobile { display: flex; flex-direction: column; gap: 15px; }
        .keyword-card-mobile { background: var(--card); border-radius: 12px; padding: 15px; border-left: 4px solid transparent; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
        
        .rank-diamond { border-left-color: #00e5ff; background: linear-gradient(90deg, rgba(0,229,255,0.05), transparent); }
        .rank-gold { border-left-color: #ffd700; background: linear-gradient(90deg, rgba(255,215,0,0.05), transparent); }
        .rank-silver { border-left-color: #c0c0c0; }
        .rank-red { border-left-color: var(--bad); opacity: 0.7; }

        .mobile-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .mobile-keyword-rank { background: rgba(255,255,255,0.1); width: 24px; height: 24px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: bold; margin-right: 10px; }
        .mobile-keyword-text { font-size: 1.1rem; font-weight: bold; color: #fff; }
        .mobile-count-section { margin-bottom: 10px; }
        .mobile-count-number { font-family: monospace; font-size: 0.9rem; color: #ccc; margin-bottom: 5px; }
        .mobile-count-bar { width: 100%; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; }
        .mobile-count-bar-fill { height: 100%; border-radius: 2px; background: var(--accent); }
        .mobile-actions { display: flex; gap: 10px; margin-top: 10px; }

        /* 테이블 (PC) */
        .keyword-table-desktop { display: none; }
        @media (min-width: 768px) {
            .keyword-list-mobile { display: none; }
            .keyword-table-desktop { display: block; }
        }
        
        table { width: 100%; border-collapse: collapse; background: var(--card); border-radius: 10px; overflow: hidden; }
        th { background: #2a2a2a; padding: 15px; text-align: left; font-size: 0.9rem; color: #aaa; }
        td { padding: 15px; border-bottom: 1px solid #333; }
        
        /* 공통 요소 */
        .badge { padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; background: rgba(255,255,255,0.1); }
        .badge-diamond { color: #00e5ff; background: rgba(0,229,255,0.1); }
        .badge-gold { color: #ffd700; background: rgba(255,215,0,0.1); }
        .badge-red { color: var(--bad); }
        
        .btn { flex: 1; padding: 8px; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85rem; text-decoration: none; text-align: center; transition: 0.2s; }
        .btn-copy { background: rgba(255,255,255,0.1); color: #ccc; }
        .btn-copy:hover { background: var(--accent); color: #000; }
        .btn-link { background: rgba(3, 218, 198, 0.1); color: var(--good); }
        .btn-link:hover { background: var(--good); color: #000; }
        
        .archive-btn { display: block; width: 100%; padding: 15px; text-align: center; background: #333; color: white; text-decoration: none; border-radius: 10px; font-weight: bold; margin-top: 20px; transition: 0.2s; }
        .archive-btn:hover { background: var(--accent); color: #000; }
        
        .nav-btn { display: inline-block; padding: 10px 20px; background: #333; color: #fff; text-decoration: none; border-radius: 20px; margin: 0 5px; }
        
        .ad-box { text-align: center; margin: 20px 0; background: #1a1a1a; padding: 10px; border-radius: 10px; }
        
        #toast { visibility: hidden; min-width: 250px; background-color: #333; color: #fff; text-align: center; border-radius: 5px; padding: 16px; position: fixed; z-index: 99; left: 50%; bottom: 30px; transform: translateX(-50%); }
        #toast.show { visibility: visible; animation: fadein 0.5s, fadeout 0.5s 2.5s; }
        @keyframes fadein { from {bottom: 0; opacity: 0;} to {bottom: 30px; opacity: 1;} }
        @keyframes fadeout { from {bottom: 30px; opacity: 1;} to {bottom: 0; opacity: 0;} }
    </style>
    """

def get_ad_unit():
    return f"""<div class="ad-box"><ins class="adsbygoogle" style="display:block" data-ad-client="{PUB_ID}" data-ad-slot="{SLOT_ID}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script></div>"""

def get_side_rail_ad():
    return f"""<aside class="side-rail"><div style="font-size:0.7rem; color:#555; text-align:center; margin-bottom:5px;">AD</div><ins class="adsbygoogle" style="display:block" data-ad-client="{PUB_ID}" data-ad-slot="{SLOT_ID}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script></aside>"""

common_script = """<div id="toast">✅ 키워드 복사 완료!</div><script>function copyToClipboard(text) { navigator.clipboard.writeText(text).then(function() { var x = document.getElementById("toast"); x.className = "show"; setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000); }); }</script>"""

# ==========================================
# 크롤링 & 분석 로직 (기존과 동일)
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
    if not SEARCH_CLIENT_ID: return 999999
    url = "https://openapi.naver.com/v1/search/blog.json"
    headers = {"X-Naver-Client-Id": SEARCH_CLIENT_ID, "X-Naver-Client-Secret": SEARCH_CLIENT_SECRET}
    try:
        res = requests.get(url, headers=headers, params={"query": keyword, "display": 1})
        if res.status_code == 200: return res.json().get('total', 0)
        return 999999
    except: return 999999

# ==========================================
# 🚀 메인 실행 함수 (함수명 수정됨!)
# ==========================================
def create_seo_optimized_dashboard():
    keywords = get_raw_keywords()
    data = []
    print(f"📊 {len(keywords)}개 키워드 분석 중...")
    
    for word in keywords:
        count = get_blog_count(word)
        if count < 100: grade="💎 신생"; css="rank-diamond"; badge="badge-diamond"
        elif count < 1000: grade="🥇 꿀통"; css="rank-gold"; badge="badge-gold"
        elif count < 5000: grade="🥈 보통"; css="rank-silver"; badge="badge-silver"
        else: grade="💀 레드오션"; css="rank-red"; badge="badge-red"
        data.append({"word": word, "count": count, "grade": grade, "css": css, "badge": badge})
        time.sleep(0.05)
    
    data.sort(key=lambda x: x['count'])
    
    # 통계
    diamond_count = len([d for d in data if d['css'] == 'rank-diamond'])
    gold_count = len([d for d in data if d['css'] == 'rank-gold'])
    
    # 리스트 생성 (모바일/PC 공용 데이터 준비)
    desktop_rows = ""
    mobile_cards = ""
    max_count = max([d['count'] for d in data]) if data else 10000

    for idx, item in enumerate(data):
        link = f"https://search.naver.com/search.naver?where=view&sm=tab_jum&query={item['word']}"
        bar_width = min((item['count'] / max_count) * 100, 100)
        
        # PC 테이블 행
        desktop_rows += f"""
        <tr class="{item['css']}">
            <td><div class="keyword-cell"><span class="keyword-rank">{idx+1}</span><span class="keyword-text">{item['word']}</span></div></td>
            <td><div class="count-wrapper"><span class="count-text">{format(item['count'], ',')}</span><div class="count-bar"><div class="count-bar-fill" style="width:{bar_width}%; background:var(--accent)"></div></div></div></td>
            <td><span class="badge {item['badge']}">{item['grade']}</span></td>
            <td><div class="actions-cell"><button class="btn btn-copy" onclick="copyToClipboard('{item['word']}')">복사</button><a href="{link}" target="_blank" class="btn btn-link">분석</a></div></td>
        </tr>"""
        
        # 모바일 카드
        mobile_cards += f"""
        <div class="keyword-card-mobile {item['css']}">
            <div class="mobile-card-header"><span class="mobile-keyword-rank">{idx+1}</span><span class="mobile-keyword-text">{item['word']}</span></div>
            <div class="mobile-count-section"><div class="mobile-count-number">{format(item['count'], ',')}건</div><div class="mobile-count-bar"><div class="mobile-count-bar-fill" style="width:{bar_width}%; background:var(--accent)"></div></div></div>
            <span class="badge {item['badge']}">{item['grade']}</span>
            <div class="mobile-actions"><button class="btn btn-copy" onclick="copyToClipboard('{item['word']}')">복사</button><a href="{link}" target="_blank" class="btn btn-link">분석</a></div>
        </div>"""

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    now_iso = datetime.datetime.now().isoformat()
    file_date = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    
    style = get_optimized_style()
    
    stats_html = f"""
    <div class="stats-grid">
        <div class="stat-card"><div class="stat-icon">💎</div><div class="stat-value">{diamond_count}</div><div class="stat-label">블루오션</div></div>
        <div class="stat-card"><div class="stat-icon">🥇</div><div class="stat-value">{gold_count}</div><div class="stat-label">꿀통</div></div>
        <div class="stat-card"><div class="stat-icon">📊</div><div class="stat-value">{len(data)}</div><div class="stat-label">분석됨</div></div>
    </div>"""

    # 메인 페이지 생성
    index_html = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>🚀 황금 키워드 상황실</title>{get_seo_meta_tags("index")}{get_structured_data("index", now_iso)}{style}</head><body>
    <div class="layout-wrapper">
        {get_side_rail_ad()}
        <main class="main-content">
            <header><h1>🚀 황금 키워드 상황실</h1><p class="subtitle">업데이트: {now}</p><div class="update-time"><span class="pulse"></span><span>실시간 분석 중</span></div></header>
            {stats_html}
            {get_ad_unit()}
            <div class="keyword-list-mobile">{mobile_cards}</div>
            <div class="keyword-table-desktop"><table><thead><tr><th>키워드</th><th>문서수</th><th>등급</th><th>액션</th></tr></thead><tbody>{desktop_rows}</tbody></table></div>
            {get_ad_unit()}
            <div style="text-align:center; margin-top:40px;"><a href="archive.html" class="archive-btn">🗄️ 지난 리포트 보기</a></div>
            <footer style="text-align:center; margin-top:50px; color:#555; font-size:0.8rem;">© 2025 Keyword Miner Lab</footer>
        </main>
        {get_side_rail_ad()}
    </div>
    {common_script}
    </body></html>"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    # 아카이브 저장 등 나머지 로직... (생략된 부분 없이 아까 작성해드린 archive 생성 로직 포함됨)
    # (간략화를 위해 여기서는 index.html 생성까지만 보여드림, 실제론 아까 드린 create_archive_page() 등 호출해야 함)
    
    # 리포트 파일 생성
    if not os.path.exists("reports"): os.makedirs("reports")
    with open(f"reports/{file_date}.html", "w", encoding="utf-8") as f:
        f.write(index_html.replace('href="archive.html"', 'href="../archive.html"').replace('href="index.html"', 'href="../index.html"'))
        
    # 아카이브 페이지 업데이트
    create_archive_page()

    print("✅ 모든 페이지 생성 및 저장 완료!")

# ==========================================
# 4. 아카이브 페이지 생성 함수 (재정의)
# ==========================================
def create_archive_page():
    if not os.path.exists("reports"): os.makedirs("reports")
    report_files = sorted(os.listdir("reports"), reverse=True)
    
    archive_list = ""
    for rf in report_files:
        if rf.endswith(".html"):
            name = rf.replace(".html", "").replace("_", " : ")
            archive_list += f'<a href="reports/{rf}" class="archive-btn" style="margin-bottom:10px; text-align:left;">📄 {name}</a>'
            
    html = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>🗄️ 리포트 아카이브</title>{get_optimized_style()}</head><body>
    <div class="layout-wrapper">{get_side_rail_ad()}<main class="main-content"><header><h1>🗄️ 리포트 보관함</h1></header>{get_ad_unit()}<div class="card" style="padding:20px;">{archive_list}</div><div style="text-align:center; margin-top:30px;"><a href="index.html" class="archive-btn">🏠 메인으로</a></div></main>{get_side_rail_ad()}</div></body></html>"""
    
    with open("archive.html", "w", encoding="utf-8") as f:
        f.write(html)

# ==========================================
# 7. 실행 (올바른 함수 호출)
# ==========================================
if __name__ == "__main__":
    create_seo_optimized_dashboard()
    cleanup.cleanup_old_reports()
    sitemap_gen.generate_sitemap()
