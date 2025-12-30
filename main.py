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
from zoneinfo import ZoneInfo

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
# 🌐 사이트 설정
# ==========================================
SITE_URL = "https://keywords.rotcha.kr"
SITE_TITLE = "황금 키워드 상황실"
SITE_DESC = "실시간 트렌드 키워드 분석으로 블루오션 키워드를 찾아보세요!"

# ==========================================
# 🚫 제외 키워드 리스트
# ==========================================
EXCLUDE_KEYWORDS = {
    "adsensefarm", "adsense", "farm",
    "구글애드센스", "google adsense",
    "순위", "키워드", "검색량", "조회수", "검색어",
    "실시간", "트렌드", "급상승", "랭킹", "인기",
    "hot", "new", "top", "best",
    "더보기", "전체보기", "목록", "상세", "검색",
    "이전", "다음", "홈", "메뉴",
    "위", "건", "개", "회", "명"
}

# ==========================================
# SEO 메타 태그
# ==========================================
def get_seo_meta_tags(page_type="index"):
    if page_type == "index":
        title = "🚀 황금 키워드 상황실 - 실시간 블로그 키워드 트렌드 분석"
        desc = "실시간 트렌드 키워드 분석으로 블루오션 키워드를 찾아보세요. 네이버 블로그 SEO 최적화 도구."
        keywords = "키워드 분석, 블로그 키워드, SEO, 블루오션"
        canonical = f"{SITE_URL}/"
    else:
        title = "🗄️ 리포트 아카이브"
        desc = "과거 키워드 분석 리포트"
        keywords = "키워드 히스토리"
        canonical = f"{SITE_URL}/archive.html"

    return f"""
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{keywords}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="website">
    <meta property="og:image" content="{SITE_URL}/og-image.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="naver-site-verification" content="fc4c11b5b82613bc531109cb4aee0331874d5510" />
    <link rel="manifest" href="/manifest.json">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚀</text></svg>">
    """

# ==========================================
# 🎨 스타일 (공유 버튼 + PWA 버튼 추가)
# ==========================================
def get_optimized_style():
    return """
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        
        :root {
            /* 배경 및 기본 컬러 */
            --bg-body: #0f172a;
            --bg-card: rgba(30, 41, 59, 0.7);
            --bg-card-hover: rgba(51, 65, 85, 0.8);
            
            /* 텍스트 컬러 */
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --text-muted: #64748b;
            
            /* 등급별 포인트 컬러 (네온 효과) */
            --color-diamond: #22d3ee;
            --color-gold: #fbbf24;
            --color-silver: #94a3b8;
            --color-red: #f87171;
            --color-accent: #8b5cf6;
            
            /* 글래스모피즘 */
            --glass-border: 1px solid rgba(255, 255, 255, 0.1);
            --glass-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Pretendard', -apple-system, sans-serif;
            background: var(--bg-body);
            color: var(--text-main);
            min-height: 100vh;
            line-height: 1.5;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(139, 92, 246, 0.15), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(34, 211, 238, 0.15), transparent 25%);
            background-attachment: fixed;
        }

        /* 레이아웃 */
        .layout-wrapper {
            display: flex; justify-content: center; gap: 24px;
            max-width: 1440px; margin: 0 auto; padding: 20px;
        }
        
        .side-rail {
            width: 160px; min-width: 160px;
            position: sticky; top: 20px; height: fit-content;
            display: none;
        }
        
        .main-content { flex: 1; max-width: 860px; width: 100%; }
        
        @media (min-width: 1200px) { .side-rail { display: block; } }

        /* 헤더 */
        header { text-align: center; margin-bottom: 32px; padding-top: 20px; }
        
        .logo { font-size: 3.5rem; margin-bottom: 10px; display: inline-block; animation: float 3s ease-in-out infinite; }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
        
        h1 {
            font-size: 2.2rem; font-weight: 800; margin: 0;
            background: linear-gradient(135deg, #fff, #94a3b8);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        
        .subtitle { color: var(--text-sub); font-size: 1rem; margin-top: 8px; }
        
        .update-badge {
            display: inline-flex; align-items: center; gap: 6px;
            margin-top: 16px; padding: 6px 14px;
            background: rgba(34, 211, 238, 0.1);
            border: 1px solid rgba(34, 211, 238, 0.2);
            border-radius: 20px; color: var(--color-diamond); font-size: 0.85rem; font-weight: 600;
        }
        .pulse-dot { width: 8px; height: 8px; background: currentColor; border-radius: 50%; box-shadow: 0 0 8px currentColor; }

        /* 액션 바 (리뉴얼) */
        .action-bar {
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: var(--glass-border);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            align-items: center;
        }
        
        .action-row {
            display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; width: 100%;
        }
        
        .btn-action {
            display: inline-flex; align-items: center; gap: 8px;
            padding: 10px 18px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            color: var(--text-main); font-size: 0.9rem; font-weight: 600;
            cursor: pointer; transition: all 0.2s ease;
        }
        .btn-action:hover { background: rgba(255, 255, 255, 0.1); transform: translateY(-2px); }
        .btn-primary { background: linear-gradient(135deg, rgba(139, 92, 246, 0.3), rgba(34, 211, 238, 0.3)); border-color: rgba(139, 92, 246, 0.4); }
        
        .sns-btn {
            width: 42px; height: 42px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.2rem; color: #fff; text-decoration: none;
            transition: all 0.2s ease;
        }
        .sns-btn:hover { transform: scale(1.1); box-shadow: 0 0 15px rgba(255,255,255,0.2); }
        
        /* 통계 카드 */
        .stats-grid {
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 24px;
        }
        .stat-card {
            background: var(--bg-card); border: var(--glass-border);
            border-radius: 16px; padding: 16px; text-align: center;
        }
        .stat-val { font-size: 1.5rem; font-weight: 800; color: var(--text-main); }
        .stat-label { font-size: 0.8rem; color: var(--text-sub); margin-top: 4px; }
        
        /* 테이블 (PC) */
        .keyword-table-desktop {
            background: var(--bg-card); border: var(--glass-border);
            border-radius: 20px; overflow: hidden; display: none;
        }
        table { width: 100%; border-collapse: collapse; }
        th { 
            text-align: left; padding: 16px 24px; 
            color: var(--text-sub); font-size: 0.85rem; font-weight: 600;
            border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2);
        }
        td { padding: 16px 24px; border-bottom: 1px solid rgba(255,255,255,0.05); vertical-align: middle; }
        tr:hover td { background: var(--bg-card-hover); }
        
        /* 키워드 셀 */
        .kwd-wrapper { display: flex; align-items: center; gap: 12px; }
        .rank-badge {
            width: 28px; height: 28px; display: flex; align-items: center; justify-content: center;
            border-radius: 8px; font-weight: 700; font-size: 0.85rem;
            background: rgba(255,255,255,0.05); color: var(--text-sub);
        }
        .kwd-text { font-size: 1.05rem; font-weight: 600; letter-spacing: -0.02em; cursor: pointer; }
        
        /* 랭크 스타일 */
        .r-diamond .rank-badge { background: rgba(34, 211, 238, 0.2); color: var(--color-diamond); }
        .r-diamond .kwd-text { color: var(--color-diamond); text-shadow: 0 0 10px rgba(34, 211, 238, 0.3); }
        
        .r-gold .rank-badge { background: rgba(251, 191, 36, 0.2); color: var(--color-gold); }
        .r-gold .kwd-text { color: var(--color-gold); }
        
        .r-red .kwd-text { color: var(--text-muted); text-decoration: line-through; }

        /* 모바일 카드 */
        .keyword-list-mobile { display: flex; flex-direction: column; gap: 12px; }
        .m-card {
            background: var(--bg-card); border: var(--glass-border); border-radius: 16px;
            padding: 16px; position: relative; overflow: hidden;
        }
        .m-card::before {
            content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
        }
        .m-card.r-diamond::before { background: var(--color-diamond); box-shadow: 0 0 10px var(--color-diamond); }
        .m-card.r-gold::before { background: var(--color-gold); }
        
        .m-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
        .m-rank { font-size: 0.9rem; color: var(--text-sub); font-weight: 600; }
        .m-kwd { font-size: 1.1rem; font-weight: 700; color: var(--text-main); }
        .r-diamond .m-kwd { color: var(--color-diamond); }
        
        .m-stat { display: flex; justify-content: space-between; background: rgba(0,0,0,0.2); padding: 10px; border-radius: 8px; margin-bottom: 12px; }
        .m-stat span { font-size: 0.85rem; color: var(--text-sub); }
        .m-stat strong { font-family: monospace; font-size: 1rem; color: var(--text-main); }
        
        /* 버튼 공통 */
        .btn-sm {
            padding: 6px 12px; border-radius: 8px; font-size: 0.8rem; font-weight: 500;
            border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.05);
            color: var(--text-sub); cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;
        }
        .btn-sm:hover { background: rgba(255,255,255,0.1); color: var(--text-main); }
        
        .badge {
            padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700;
        }
        .badge-new { background: rgba(34, 211, 238, 0.15); color: var(--color-diamond); border: 1px solid rgba(34, 211, 238, 0.3); }
        .badge-good { background: rgba(251, 191, 36, 0.15); color: var(--color-gold); border: 1px solid rgba(251, 191, 36, 0.3); }
        
        /* 미디어 쿼리 */
        @media (min-width: 768px) {
            .keyword-list-mobile { display: none; }
            .keyword-table-desktop { display: block; }
        }
        @media (max-width: 767px) {
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            h1 { font-size: 1.8rem; }
            .logo { font-size: 2.5rem; }
        }
        
        /* 토스트 & 아카이브 */
        .archive-link {
            display: block; text-align: center; margin-top: 40px; padding: 16px;
            background: var(--bg-card); border-radius: 16px; border: var(--glass-border);
            color: var(--text-main); text-decoration: none; font-weight: 600;
            transition: 0.2s;
        }
        .archive-link:hover { background: var(--bg-card-hover); border-color: var(--color-accent); }
        
        #toast {
            position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(20px);
            background: var(--color-accent); color: white; padding: 12px 24px; border-radius: 30px;
            font-weight: 600; opacity: 0; visibility: hidden; transition: all 0.3s;
            box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4); z-index: 9999;
        }
        #toast.show { opacity: 1; visibility: visible; transform: translateX(-50%) translateY(0); }
        
        .ad-container { margin: 24px 0; text-align: center; border-radius: 12px; overflow: hidden; background: rgba(0,0,0,0.2); padding: 10px; }
    </style>
    """


# ==========================================
# 📌 액션 바 HTML (북마크 + PWA + 공유)
# ==========================================
def get_action_bar_html():
    return f"""
    <div class="action-bar">
        <!-- 1행: 메인 기능 버튼 -->
        <div class="action-row">
            <button class="btn-action btn-primary" id="installBtn" style="display:none;" onclick="installPWA()">
                <i class="fas fa-download"></i> 앱 설치
            </button>
            <button class="btn-action" onclick="showBookmarkTip()">
                <i class="fas fa-star"></i> 북마크
            </button>
            <button class="btn-action" onclick="copyPageLink()">
                <i class="fas fa-link"></i> 링크복사
            </button>
        </div>
        
        <!-- 2행: SNS 공유 -->
        <div class="action-row" style="margin-top:5px; gap:12px;">
            <a href="javascript:shareKakao()" class="sns-btn" style="background:#FEE500; color:#3C1E1E;"><i class="fas fa-comment"></i></a>
            <a href="https://twitter.com/intent/tweet?url={SITE_URL}" target="_blank" class="sns-btn" style="background:#000;"><i class="fa-brands fa-x-twitter"></i></a>
            <a href="https://blog.naver.com/openapi/share?url={SITE_URL}" target="_blank" class="sns-btn" style="background:#03C75A;"><i class="fa-solid fa-n"></i></a>
            <a href="https://www.facebook.com/sharer/sharer.php?u={SITE_URL}" target="_blank" class="sns-btn" style="background:#1877F2;"><i class="fab fa-facebook-f"></i></a>
        </div>
        
        <!-- 북마크 팁 팝업 (숨김) -->
        <div class="bookmark-tip" id="bookmarkTip" style="display:none; /* 스타일은 CSS에서 제어 */">
            <!-- (기존 팝업 내용과 동일) -->
        </div>
    </div>
    """

# ==========================================
# 📜 JavaScript (PWA + 공유 기능)
# ==========================================
def get_scripts():
    return f"""
    <script>
        // ==========================================
        // PWA 설치 기능
        // ==========================================
        let deferredPrompt;
        
        window.addEventListener('beforeinstallprompt', (e) => {{
            e.preventDefault();
            deferredPrompt = e;
            // PWA 설치 버튼 표시
            document.getElementById('installBtn').style.display = 'inline-flex';
        }});

        function installPWA() {{
            if (deferredPrompt) {{
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {{
                    if (choiceResult.outcome === 'accepted') {{
                        showToast('✅ 홈 화면에 추가되었습니다!');
                    }}
                    deferredPrompt = null;
                    document.getElementById('installBtn').style.display = 'none';
                }});
            }} else {{
                // iOS Safari 안내
                showToast('📱 공유 버튼 → "홈 화면에 추가"를 눌러주세요');
            }}
        }}

        // ==========================================
        // 북마크 안내
        // ==========================================
        function showBookmarkTip() {{
            document.getElementById('bookmarkTip').classList.add('show');
        }}

        function closeBookmarkTip() {{
            document.getElementById('bookmarkTip').classList.remove('show');
        }}

        // 바깥 클릭 시 닫기
        document.addEventListener('click', (e) => {{
            const tip = document.getElementById('bookmarkTip');
            const btn = document.querySelector('.bookmark-btn');
            if (tip.classList.contains('show') && 
                !tip.contains(e.target) && 
                !btn.contains(e.target)) {{
                closeBookmarkTip();
            }}
        }});

        // ==========================================
        // 링크 복사
        // ==========================================
        function copyPageLink() {{
            navigator.clipboard.writeText(window.location.href).then(() => {{
                showToast('✅ 링크가 복사되었습니다!');
            }}).catch(() => {{
                // 폴백
                const textArea = document.createElement('textarea');
                textArea.value = window.location.href;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                showToast('✅ 링크가 복사되었습니다!');
            }});
        }}

        // ==========================================
        // 카카오톡 공유
        // ==========================================
        function shareKakao() {{
            // 카카오 SDK가 없으면 URL 공유
            if (typeof Kakao === 'undefined') {{
                const kakaoUrl = 'https://sharer.kakao.com/talk/friends/picker/link?app_key=YOUR_APP_KEY&url=' + encodeURIComponent(window.location.href);
                // 간단한 방법: 카카오톡 앱 스킴 또는 웹 공유
                if (navigator.share) {{
                    navigator.share({{
                        title: '🚀 황금 키워드 상황실',
                        text: '실시간 블루오션 키워드 분석',
                        url: window.location.href
                    }});
                }} else {{
                    copyPageLink();
                    showToast('💬 링크를 복사했어요! 카카오톡에 붙여넣기 하세요');
                }}
            }} else {{
                Kakao.Share.sendDefault({{
                    objectType: 'feed',
                    content: {{
                        title: '🚀 황금 키워드 상황실',
                        description: '실시간 트렌드 키워드 분석으로 블루오션을 찾아보세요!',
                        imageUrl: '{SITE_URL}/og-image.png',
                        link: {{
                            mobileWebUrl: window.location.href,
                            webUrl: window.location.href
                        }}
                    }},
                    buttons: [{{
                        title: '키워드 분석하기',
                        link: {{
                            mobileWebUrl: window.location.href,
                            webUrl: window.location.href
                        }}
                    }}]
                }});
            }}
        }}

        // ==========================================
        // 키워드 복사
        // ==========================================
        function copyKeyword(text) {{
            navigator.clipboard.writeText(text).then(function() {{
                showToast('✅ "' + text + '" 복사 완료!');
            }}).catch(function() {{
                alert('복사됨: ' + text);
            }});
        }}

        // ==========================================
        // 토스트 메시지
        // ==========================================
        function showToast(message) {{
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 3000);
        }}

        // ==========================================
        // 첫 방문자에게 북마크 팁 자동 표시 (선택사항)
        // ==========================================
        /*
        if (!localStorage.getItem('bookmarkTipShown')) {{
            setTimeout(() => {{
                showBookmarkTip();
                localStorage.setItem('bookmarkTipShown', 'true');
            }}, 10000); // 10초 후 표시
        }}
        */
    </script>
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
# ✅ 키워드 수집 함수 (기존과 동일)
# ==========================================
def get_keywords_from_farm():
    print("🚗 애드센스팜 크롤링...")
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

        elements = driver.find_elements(By.CSS_SELECTOR, "td, .keyword, .rank-text, li")
        raw_keywords = []

        for elem in elements:
            text = elem.text.strip()
            if 2 <= len(text) < 30:
                clean = re.sub(r'^[\d\s.]+', '', text).strip()
                clean_lower = clean.lower()

                if (clean and 
                    not clean.isdigit() and 
                    clean_lower not in EXCLUDE_KEYWORDS and
                    len(clean) >= 2):

                    if clean.isalpha() and clean.lower() in ['ad', 'ads', 'new', 'hot']:
                        continue

                    raw_keywords.append(clean)
                    print(f"  수집: {clean}")

        unique_keywords = list(dict.fromkeys(raw_keywords))
        filtered_keywords = [
            kw for kw in unique_keywords 
            if kw.lower() not in EXCLUDE_KEYWORDS
        ]

        print(f"✅ {len(filtered_keywords)}개 키워드 수집 (필터링 후)")
        return filtered_keywords[:40]

    except Exception as e:
        print(f"❌ 에러: {e}")
        return []
    finally:
        driver.quit()

def get_keywords_from_google():
    print("⚠️ 백업: 구글 트렌드")
    url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=KR"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            keywords = []
            for item in root.findall(".//item"):
                title = item.find("title").text
                if title and title.lower() not in EXCLUDE_KEYWORDS:
                    keywords.append(title)
            return keywords[:40]
    except Exception as e:
        print(f"❌ 백업 실패: {e}")

    return ["인공지능", "ChatGPT", "블로그", "SEO", "키워드"]

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
        print("🚨 메인 실패 → 백업")
        keywords = get_keywords_from_google()

    print(f"📊 {len(keywords)}개 분석 중...")

    data = []
    for word in keywords:
        count = get_blog_count(word)

        # 등급별 CSS 클래스 매핑
    if count < 100:
        grade = "💎 신생"; row_css = "r-diamond"; badge_css = "badge-new"
    elif count < 1000:
        grade = "🥇 꿀통"; row_css = "r-gold"; badge_css = "badge-good"
    elif count < 5000:
        grade = "🥈 보통"; row_css = "r-silver"; badge_css = ""
    else:
        grade = "💀 레드"; row_css = "r-red"; badge_css = ""

    # 데스크톱 행 (수정됨)
    desktop_rows += f"""
    <tr class="{row_css}">
        <td>
            <div class="kwd-wrapper">
                <span class="rank-badge">{idx+1}</span>
                <span class="kwd-text" onclick="copyKeyword('{item['word']}')">{item['word']}</span>
            </div>
        </td>
        <td>{format(item['count'], ',')}</td>
        <td><span class="badge {badge_css}">{item['grade']}</span></td>
        <td>
            <div style="display:flex; gap:6px;">
                <button class="btn-sm" onclick="copyKeyword('{item['word']}')"><i class="fas fa-copy"></i></button>
                <a href="{link}" target="_blank" class="btn-sm"><i class="fas fa-external-link-alt"></i></a>
            </div>
        </td>
    </tr>
    """
    
    # 모바일 카드 (수정됨)
    mobile_cards += f"""
    <div class="m-card {row_css}">
        <div class="m-header">
            <span class="m-rank">#{idx+1}</span>
            <span class="badge {badge_css}">{item['grade']}</span>
        </div>
        <div class="m-kwd" onclick="copyKeyword('{item['word']}')">{item['word']}</div>
        <div style="margin:12px 0;">
            <div class="m-stat">
                <span>블로그 문서수</span>
                <strong>{format(item['count'], ',')}건</strong>
            </div>
        </div>
        <div style="display:flex; gap:10px;">
            <button class="btn-sm" style="flex:1; justify-content:center;" onclick="copyKeyword('{item['word']}')">키워드 복사</button>
            <a href="{link}" target="_blank" class="btn-sm" style="flex:1; justify-content:center;">네이버 분석</a>
        </div>
    </div>
    """

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
                    <button class="btn btn-copy" onclick="copyKeyword('{item['word']}')">📋복사</button>
                    <a href="{link}" target="_blank" class="btn btn-link">분석↗</a>
                </div>
            </td>
        </tr>
        """

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
                <button class="btn btn-copy" onclick="copyKeyword('{item['word']}')">📋복사</button>
                <a href="{link}" target="_blank" class="btn btn-link">분석↗</a>
            </div>
        </div>
        """

    # 한국 시간
    try:
        kst = datetime.datetime.now(ZoneInfo("Asia/Seoul"))
        now = kst.strftime("%Y-%m-%d %H:%M")
        file_date = kst.strftime("%Y%m%d_%H%M")
    except:
        utc_now = datetime.datetime.utcnow()
        kst_now = utc_now + datetime.timedelta(hours=9)
        now = kst_now.strftime("%Y-%m-%d %H:%M")
        file_date = kst_now.strftime("%Y%m%d_%H%M")

    style = get_optimized_style()
    seo_meta = get_seo_meta_tags("index")
    action_bar = get_action_bar_html()
    scripts = get_scripts()

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

    index_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <meta name="theme-color" content="#0a0a0f">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="키워드상황실">
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
                    <span>{now} 업데이트 (KST)</span>
                </div>
            </header>
            
            {action_bar}
            
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
    
    <div id="toast">✅ 복사되었습니다!</div>
    {scripts}
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

    print(f"✅ 완성! ({now})")
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
    action_bar = get_action_bar_html()
    scripts = get_scripts()

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#0a0a0f">
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
            
            {action_bar}
            
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
    
    <div id="toast">✅ 복사되었습니다!</div>
    {scripts}
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
