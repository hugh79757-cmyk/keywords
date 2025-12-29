from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
import time
import datetime
import os
import re
import xml.etree.ElementTree as ET

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
# SEO 메타 태그
# ==========================================
def get_seo_meta_tags(page_type="index"):
    base_url = "https://keywords.rotcha.kr"
    
    if page_type == "index":
        title = "🚀 황금 키워드 상황실 - 실시간 블로그 키워드 트렌드 분석"
        desc = "실시간 트렌드 키워드 분석으로 블루오션 키워드를 찾아보세요. 네이버 블로그 SEO 최적화 도구."
        keywords = "키워드 분석, 블로그 키워드, SEO, 블루오션"
        canonical = f"{base_url}/"
    else:
        title = "🗄️ 리포트 아카이브"
        desc = "과거 키워드 분석 리포트"
        keywords = "키워드 히스토리"
        canonical = f"{base_url}/archive.html"
    
    return f"""
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{keywords}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta name="naver-site-verification" content="fc4c11b5b82613bc531109cb4aee0331874d5510" />
    """

# ==========================================
# 🎨 개선된 스타일
# ==========================================
def get_optimized_style():
    return """
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        
        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: rgba(255, 255, 255, 0.03);
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.08);
            --accent-primary: #8b5cf6;
            --accent-secondary: #06b6d4;
            --accent-success: #10b981;
            --accent-warning: #f59e0b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Pretendard', -apple-system, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
            overflow-x: hidden;
        }

        body::before {
            content: '';
            position: fixed;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: 
                radial-gradient(circle at 20% 20%, rgba(139, 92, 246, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 80% 80%, rgba(6, 182, 212, 0.1) 0%, transparent 40%);
            pointer-events: none;
            z-index: 0;
            animation: bgFloat 20s ease-in-out infinite;
        }

        @keyframes bgFloat {
            0%, 100% { transform: translate(0, 0); }
            50% { transform: translate(-2%, -2%); }
        }

        .layout-wrapper {
            display: flex;
            justify-content: center;
            gap: 20px;
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }

        .side-rail {
            width: 160px;
            min-width: 160px;
            position: sticky;
            top: 20px;
            height: fit-content;
            display: none;
        }

        .main-content {
            flex: 1;
            max-width: 900px;
        }

        @media (min-width: 1200px) {
            .side-rail {
                display: block;
            }
        }

        header {
            text-align: center;
            margin-bottom: 30px;
            padding: 30px 20px;
        }

        .logo {
            font-size: 3rem;
            margin-bottom: 10px;
            animation: float 3s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        h1 {
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #f8fafc, #8b5cf6, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 0.95rem;
        }

        .update-time {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 15px;
            padding: 8px 16px;
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 30px;
            font-size: 0.85rem;
            backdrop-filter: blur(10px);
        }

        .pulse {
            width: 8px; height: 8px;
            background: var(--accent-success);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.2); }
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
        }

        .stat-icon { font-size: 2rem; margin-bottom: 8px; }
        .stat-value {
            font-size: 1.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, #f8fafc, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stat-label { font-size: 0.85rem; color: var(--text-secondary); margin-top: 5px; }

        /* 광고 박스 */
        .ad-box {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 20px;
            margin: 30px 0;
            text-align: center;
        }

        .ad-label {
            font-size: 0.7rem;
            color: #555;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .ad-row td {
            padding: 0 !important;
        }

        .ad-box-table {
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0;
            text-align: center;
        }

        .ad-box-mobile {
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 15px;
            margin: 15px 0;
            text-align: center;
        }

        /* 모바일 카드 */
        .keyword-list-mobile {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .keyword-card-mobile {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-left: 4px solid transparent;
            border-radius: 16px;
            padding: 16px;
            transition: all 0.3s;
        }

        .keyword-card-mobile:active {
            transform: scale(0.98);
        }

        .rank-diamond {
            border-left-color: #06b6d4;
            background: linear-gradient(90deg, rgba(6,182,212,0.05), transparent);
        }
        .rank-gold {
            border-left-color: #f59e0b;
            background: linear-gradient(90deg, rgba(245,158,11,0.05), transparent);
        }
        .rank-silver { border-left-color: #6b7280; }
        .rank-red { border-left-color: #ef4444; opacity: 0.6; }

        .mobile-card-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }

        .mobile-keyword-rank {
            min-width: 32px; height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            font-size: 0.9rem;
            font-weight: 700;
        }

        .rank-diamond .mobile-keyword-rank {
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.3), rgba(139, 92, 246, 0.3));
            color: #06b6d4;
        }

        .mobile-keyword-text {
            font-size: 1.1rem;
            font-weight: 700;
            flex: 1;
        }

        .rank-diamond .mobile-keyword-text {
            background: linear-gradient(135deg, #06b6d4, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .rank-gold .mobile-keyword-text { color: #fbbf24; }

        .mobile-count-section { margin-bottom: 12px; }
        .mobile-count-number {
            font-family: 'Courier New', monospace;
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .rank-diamond .mobile-count-number { color: #06b6d4; }
        .rank-gold .mobile-count-number { color: #fbbf24; }

        .mobile-count-bar {
            width: 100%;
            height: 6px;
            background: rgba(255,255,255,0.1);
            border-radius: 3px;
            overflow: hidden;
        }

        .mobile-count-bar-fill {
            height: 100%;
            border-radius: 3px;
            transition: width 0.6s ease;
        }

        .rank-diamond .mobile-count-bar-fill {
            background: linear-gradient(90deg, #06b6d4, #8b5cf6);
        }
        .rank-gold .mobile-count-bar-fill {
            background: linear-gradient(90deg, #f59e0b, #fbbf24);
        }

        .badge {
            display: inline-flex;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 10px;
        }

        .badge-diamond {
            background: linear-gradient(135deg, rgba(6,182,212,0.2), rgba(139,92,246,0.2));
            border: 1px solid rgba(6,182,212,0.3);
            color: #06b6d4;
        }
        .badge-gold {
            background: rgba(245,158,11,0.2);
            border: 1px solid rgba(245,158,11,0.3);
            color: #fbbf24;
        }
        .badge-silver {
            background: rgba(107,114,128,0.15);
            border: 1px solid rgba(107,114,128,0.3);
            color: #9ca3af;
        }
        .badge-red {
            background: rgba(239,68,68,0.15);
            border: 1px solid rgba(239,68,68,0.3);
            color: #f87171;
        }

        .mobile-actions {
            display: flex;
            gap: 8px;
        }

        .btn {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 10px;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            text-align: center;
            transition: all 0.2s;
            -webkit-tap-highlight-color: transparent;
        }

        .btn-copy {
            background: rgba(255,255,255,0.08);
            color: var(--text-primary);
        }
        .btn-copy:active {
            background: rgba(139,92,246,0.3);
            transform: scale(0.95);
        }

        .btn-link {
            background: rgba(6,182,212,0.15);
            color: #06b6d4;
        }
        .btn-link:active {
            background: rgba(6,182,212,0.3);
            transform: scale(0.95);
        }

        /* 데스크톱 테이블 */
        .keyword-table-desktop {
            display: none;
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            overflow: hidden;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        thead {
            background: rgba(0, 0, 0, 0.3);
        }

        th {
            padding: 16px 20px;
            text-align: left;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
        }

        tbody tr {
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
            transition: all 0.2s;
        }

        tbody tr:hover {
            background: rgba(255, 255, 255, 0.05);
        }

        td {
            padding: 16px 20px;
            vertical-align: middle;
        }

        .keyword-cell {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .keyword-rank {
            width: 28px; height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 700;
        }

        .rank-diamond .keyword-rank {
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.3), rgba(139, 92, 246, 0.3));
            color: #06b6d4;
        }

        .keyword-text {
            font-weight: 600;
            font-size: 1rem;
        }

        .rank-diamond .keyword-text {
            background: linear-gradient(135deg, #06b6d4, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .rank-gold .keyword-text { color: #fbbf24; }

        .count-wrapper {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .count-text {
            font-family: 'Courier New', monospace;
            font-size: 0.95rem;
            font-weight: 600;
        }

        .count-bar {
            width: 100%;
            height: 4px;
            background: rgba(255,255,255,0.1);
            border-radius: 2px;
            overflow: hidden;
        }

        .count-bar-fill {
            height: 100%;
            border-radius: 2px;
            transition: width 0.5s ease;
        }

        .rank-diamond .count-bar-fill {
            background: linear-gradient(90deg, #06b6d4, #8b5cf6);
        }
        .rank-gold .count-bar-fill {
            background: linear-gradient(90deg, #f59e0b, #fbbf24);
        }

        /* ✅ 수정: 버튼 가로 정렬 */
        .actions-cell {
            display: flex;
            flex-direction: row; /* 가로 정렬 */
            gap: 8px;
            align-items: center;
        }

        /* 아카이브 버튼 */
        .archive-btn {
            display: block;
            width: 100%;
            padding: 16px;
            margin-top: 30px;
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            color: var(--text-primary);
            text-decoration: none;
            text-align: center;
            font-weight: 700;
            transition: all 0.3s;
        }

        .archive-btn:active {
            transform: scale(0.98);
        }

        #toast {
            position: fixed;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%) translateY(20px);
            background: rgba(16, 185, 129, 0.95);
            backdrop-filter: blur(10px);
            color: white;
            padding: 16px 24px;
            border-radius: 30px;
            font-weight: 600;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s;
            z-index: 1000;
        }

        #toast.show {
            opacity: 1;
            visibility: visible;
            transform: translateX(-50%) translateY(0);
        }

        footer {
            text-align: center;
            padding: 40px 20px;
            color: #555;
            font-size: 0.85rem;
        }

        @media (min-width: 768px) {
            .keyword-list-mobile { display: none; }
            .keyword-table-desktop { display: block; }
            
            h1 { font-size: 2.5rem; }
            .logo { font-size: 3.5rem; }
        }
    </style>
    """

# ==========================================
# 광고 유닛
# ==========================================
def get_ad_unit():
    return f"""
    <div class="ad-box">
        <div class="ad-label">Advertisement</div>
        <ins class="adsbygoogle" 
             style="display:block" 
             data-ad-client="{PUB_ID}" 
             data-ad-slot="{SLOT_ID}" 
             data-ad-format="auto" 
             data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    </div>
    """

def get_side_rail_ad():
    return f"""
    <aside class="side-rail">
        <div style="font-size:0.7rem; color:#555; text-align:center; margin-bottom:10px;">AD</div>
        <ins class="adsbygoogle" 
             style="display:block" 
             data-ad-client="{PUB_ID}" 
             data-ad-slot="{SLOT_ID}" 
             data-ad-format="auto" 
             data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    </aside>
    """

# ==========================================
# 1. 키워드 수집 (숫자 제거)
# ==========================================
def get_keywords_from_farm():
    print("🚗 애드센스팜 크롤링 시작...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get("https://adsensefarm.kr/realtime/")
        time.sleep(7)
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(2)
        
        elements = driver.find_elements(By.CSS_SELECTOR, "td, .keyword, .rank-text, li, span")
        raw_keywords = []
        
        for elem in elements:
            text = elem.text.strip()
            if 2 <= len(text) < 30:
                # 정규식으로 앞쪽 숫자 제거
                clean = re.sub(r'^[\d\s.]+', '', text).strip()
                
                if clean and not clean.isdigit() and clean not in ["순위", "키워드", "검색량", "조회수"]:
                    raw_keywords.append(clean)
        
        unique_keywords = list(dict.fromkeys(raw_keywords))
        print(f"✅ {len(unique_keywords)}개 키워드 수집")
        return unique_keywords[:40]
        
    except Exception as e:
        print(f"❌ 에러: {e}")
        return []
    finally:
        driver.quit()

def get_keywords_from_google():
    print("⚠️ 백업: 구글 트렌드 RSS")
    url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=KR"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            keywords = []
            for item in root.findall(".//item"):
                title = item.find("title").text
                if title:
                    keywords.append(title)
            return keywords[:40]
    except Exception as e:
        print(f"❌ 백업 실패: {e}")
    
    return ["인공지능", "ChatGPT", "블로그", "SEO", "키워드"]

# ==========================================
# 2. 블로그 수 조회
# ==========================================
def get_blog_count(keyword):
    if not SEARCH_CLIENT_ID or not SEARCH_CLIENT_SECRET:
        import random
        return random.randint(50, 5000)
    
    url = "https://openapi.naver.com/v1/search/blog.json"
    headers = {
        "X-Naver-Client-Id": SEARCH_CLIENT_ID,
        "X-Naver-Client-Secret": SEARCH_CLIENT_SECRET
    }
    
    try:
        res = requests.get(url, headers=headers, params={"query": keyword, "display": 1}, timeout=5)
        if res.status_code == 200:
            return res.json().get('total', 0)
        return 999999
    except:
        return 999999

# ==========================================
# 3. 메인 대시보드 생성
# ==========================================
def create_seo_optimized_dashboard():
    keywords = get_keywords_from_farm()
    if not keywords:
        print("🚨 메인 실패 → 백업 사용")
        keywords = get_keywords_from_google()
    
    print(f"📊 {len(keywords)}개 키워드 분석 중...")
    
    data = []
    for word in keywords:
        count = get_blog_count(word)
        
        if count < 100:
            grade = "💎 신생 블루오션"
            css = "rank-diamond"
            badge = "badge-diamond"
        elif count < 1000:
            grade = "🥇 꿀통 키워드"
            css = "rank-gold"
            badge = "badge-gold"
        elif count < 5000:
            grade = "🥈 보통"
            css = "rank-silver"
            badge = "badge-silver"
        else:
            grade = "💀 레드오션"
            css = "rank-red"
            badge = "badge-red"
        
        data.append({
            "word": word,
            "count": count,
            "grade": grade,
            "css": css,
            "badge": badge
        })
        time.sleep(0.05)
    
    data.sort(key=lambda x: x['count'])
    
    diamond_cnt = len([d for d in data if d['css'] == 'rank-diamond'])
    gold_cnt = len([d for d in data if d['css'] == 'rank-gold'])
    max_count = max([d['count'] for d in data]) if data else 10000
    
    desktop_rows = ""
    mobile_cards = ""
    
    for idx, item in enumerate(data):
        link = f"https://search.naver.com/search.naver?where=view&sm=tab_jum&query={item['word']}"
        bar_width = min((item['count'] / max_count) * 100, 100)
        
        # ✅ 모바일: 5개마다 / 데스크톱: 7개마다
        # 모바일 광고 (5개마다)
        if idx > 0 and idx % 5 == 0:
            mobile_cards += f"""
            <div class="ad-box-mobile">
                <div class="ad-label">Advertisement</div>
                <ins class="adsbygoogle" style="display:block" data-ad-client="{PUB_ID}" data-ad-slot="{SLOT_ID}" data-ad-format="auto" data-full-width-responsive="true"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
            </div>
            """
        
        # 데스크톱 광고 (7개마다)
        if idx > 0 and idx % 7 == 0:
            desktop_rows += f"""
            <tr class="ad-row">
                <td colspan="4" style="padding:0;">
                    <div class="ad-box-table">
                        <div class="ad-label">Advertisement</div>
                        <ins class="adsbygoogle" style="display:block" data-ad-client="{PUB_ID}" data-ad-slot="{SLOT_ID}" data-ad-format="auto" data-full-width-responsive="true"></ins>
                        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
                    </div>
                </td>
            </tr>
            """
        
        # 테이블 행
        desktop_rows += f"""
        <tr class="{item['css']}">
            <td>
                <div class="keyword-cell">
                    <span class="keyword-rank">{idx+1}</span>
                    <span class="keyword-text">{item['word']}</span>
                </div>
            </td>
            <td>
                <div class="count-wrapper">
                    <span class="count-text">{format(item['count'], ',')}건</span>
                    <div class="count-bar">
                        <div class="count-bar-fill" style="width:{bar_width}%"></div>
                    </div>
                </div>
            </td>
            <td><span class="badge {item['badge']}">{item['grade']}</span></td>
            <td>
                <div class="actions-cell">
                    <button class="btn btn-copy" onclick="copyKeyword('{item['word']}')">📋 복사</button>
                    <a href="{link}" target="_blank" class="btn btn-link">분석 ↗</a>
                </div>
            </td>
        </tr>
        """
        
        # 모바일 카드
        mobile_cards += f"""
        <div class="keyword-card-mobile {item['css']}">
            <div class="mobile-card-header">
                <span class="mobile-keyword-rank">{idx+1}</span>
                <span class="mobile-keyword-text">{item['word']}</span>
            </div>
            <div class="mobile-count-section">
                <div class="mobile-count-number">{format(item['count'], ',')}건</div>
                <div class="mobile-count-bar">
                    <div class="mobile-count-bar-fill" style="width:{bar_width}%"></div>
                </div>
            </div>
            <span class="badge {item['badge']}">{item['grade']}</span>
            <div class="mobile-actions">
                <button class="btn btn-copy" onclick="copyKeyword('{item['word']}')">📋 복사</button>
                <a href="{link}" target="_blank" class="btn btn-link">분석 ↗</a>
            </div>
        </div>
        """
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    file_date = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    
    style = get_optimized_style()
    seo_meta = get_seo_meta_tags("index")
    
    stats_html = f"""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-icon">💎</div>
            <div class="stat-value">{diamond_cnt}</div>
            <div class="stat-label">블루오션</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">🥇</div>
            <div class="stat-value">{gold_cnt}</div>
            <div class="stat-label">꿀통 키워드</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-value">{len(data)}</div>
            <div class="stat-label">분석 키워드</div>
        </div>
    </div>
    """
    
    script = """
    <script>
        function copyKeyword(text) {
            navigator.clipboard.writeText(text).then(function() {
                const toast = document.getElementById('toast');
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 2500);
            }).catch(function() {
                alert('복사됨: ' + text);
            });
        }
    </script>
    """
    
    index_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <meta name="theme-color" content="#0a0a0f">
    <title>🚀 황금 키워드 상황실</title>
    {seo_meta}
    {style}
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={PUB_ID}" crossorigin="anonymous"></script>
</head>
<body>
    <div class="layout-wrapper">
        {get_side_rail_ad()}
        
        <main class="main-content">
            <header>
                <div class="logo">🚀</div>
                <h1>황금 키워드 상황실</h1>
                <p class="subtitle">실시간 트렌드 키워드 분석</p>
                <div class="update-time">
                    <span class="pulse"></span>
                    <span>{now} 업데이트</span>
                </div>
            </header>
            
            {stats_html}
            {get_ad_unit()}
            
            <div class="keyword-list-mobile">
                {mobile_cards}
            </div>
            
            <div class="keyword-table-desktop">
                <table>
                    <thead>
                        <tr>
                            <th width="35%">키워드</th>
                            <th width="25%">문서수</th>
                            <th width="20%">등급</th>
                            <th width="20%">액션</th>
                        </tr>
                    </thead>
                    <tbody>
                        {desktop_rows}
                    </tbody>
                </table>
            </div>
            
            {get_ad_unit()}
            
            <a href="archive.html" class="archive-btn">🗄️ 지난 리포트 보기</a>
            
            <footer>© 2025 황금 키워드 상황실</footer>
        </main>
        
        {get_side_rail_ad()}
    </div>
    
    <div id="toast">✅ 키워드가 복사되었습니다!</div>
    {script}
</body>
</html>"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    
    if not os.path.exists("reports"):
        os.makedirs("reports")
    
    report_html = index_html.replace('href="archive.html"', 'href="../archive.html"')
    with open(f"reports/{file_date}.html", "w", encoding="utf-8") as f:
        f.write(report_html)
    
    create_archive_page()
    
    print("✅ 대시보드 완성!")
    print(f"💎 블루오션: {diamond_cnt}개 | 🥇 꿀통: {gold_cnt}개")

# ==========================================
# 4. 아카이브 페이지
# ==========================================
def create_archive_page():
    if not os.path.exists("reports"):
        os.makedirs("reports")
    
    report_files = sorted(os.listdir("reports"), reverse=True)
    archive_list = ""
    
    for rf in report_files:
        if rf.endswith(".html"):
            date_time = rf.replace(".html", "").replace("_", " ")
            archive_list += f'<a href="reports/{rf}" class="archive-btn" style="margin-bottom:10px;">📄 {date_time}</a>'
    
    style = get_optimized_style()
    seo_meta = get_seo_meta_tags("archive")
    
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🗄️ 리포트 아카이브</title>
    {seo_meta}
    {style}
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={PUB_ID}" crossorigin="anonymous"></script>
</head>
<body>
    <div class="layout-wrapper">
        {get_side_rail_ad()}
        
        <main class="main-content">
            <header>
                <div class="logo">🗄️</div>
                <h1>리포트 아카이브</h1>
                <p class="subtitle">과거 키워드 분석 기록</p>
            </header>
            
            {get_ad_unit()}
            
            <div style="display:flex; flex-direction:column; gap:10px;">
                {archive_list if archive_list else '<p style="text-align:center; color:#555; padding:40px;">저장된 리포트가 없습니다.</p>'}
            </div>
            
            {get_ad_unit()}
            
            <a href="index.html" class="archive-btn">🏠 메인으로 돌아가기</a>
            
            <footer>© 2025 황금 키워드 상황실</footer>
        </main>
        
        {get_side_rail_ad()}
    </div>
</body>
</html>"""
    
    with open("archive.html", "w", encoding="utf-8") as f:
        f.write(html)

# ==========================================
# 실행
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 황금 키워드 상황실 시작")
    print("=" * 60)
    
    try:
        create_seo_optimized_dashboard()
        print("\n✅ 완료!")
    except Exception as e:
        print(f"\n❌ 에러: {e}")
        import traceback
        traceback.print_exc()
