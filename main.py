import os
import time
import datetime
import re
import requests
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Timezone 처리 (Python 3.9+ 지원)
try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None  # 하위 버전 호환

# 외부 모듈 (같은 폴더에 있어야 함)
import cleanup
import sitemap_gen

# ==========================================
# 1. ⚙️ 설정 (Configuration)
# ==========================================
class Config:
    # 네이버 API
    NAVER_ID = os.environ.get("NAVER_CLIENT_ID")
    NAVER_SECRET = os.environ.get("NAVER_CLIENT_SECRET")
    
    # AdSense
    PUB_ID = "ca-pub-8772455780561463"
    SLOT_ID = "1662647947"
    
    # Site Info
    URL = "https://keywords.rotcha.kr"
    TITLE = "황금 키워드 상황실"
    DESC = "실시간 트렌드 키워드 분석으로 블루오션 키워드를 찾아보세요."

# ==========================================
# 2. 🎨 디자인 & 템플릿 (HTML/CSS)
# ==========================================
class Template:
    @staticmethod
    def get_style():
        return f"""
        <style>
            @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
            @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');
            
            :root {{
                --bg-body: #0f172a; --bg-card: rgba(30, 41, 59, 0.6); --text-main: #f8fafc;
                --text-sub: #94a3b8; --text-muted: #64748b;
                --color-diamond: #22d3ee; --color-gold: #fbbf24; 
                --color-silver: #94a3b8; --color-red: #f87171; --color-accent: #8b5cf6;
                --glass-border: 1px solid rgba(255, 255, 255, 0.08);
            }}
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Pretendard', sans-serif; background: var(--bg-body); color: var(--text-main); min-height: 100vh; padding-bottom: 60px; 
                    background-image: radial-gradient(circle at 10% 20%, rgba(139, 92, 246, 0.1), transparent 40%), radial-gradient(circle at 90% 80%, rgba(34, 211, 238, 0.1), transparent 40%); background-attachment: fixed; }}
            
            /* 레이아웃 */
            .layout-wrapper {{ display: flex; justify-content: center; gap: 24px; max-width: 1440px; margin: 0 auto; padding: 20px; }}
            .side-rail {{ width: 160px; min-width: 160px; position: sticky; top: 20px; height: fit-content; display: none; }}
            .main-content {{ flex: 1; max-width: 860px; width: 100%; }}
            @media (min-width: 1200px) {{ .side-rail {{ display: block; }} }}
            @media (max-width: 768px) {{ .keyword-list-mobile {{ display: flex; flex-direction: column; gap: 12px; }} .keyword-table-desktop {{ display: none; }} }}
            @media (min-width: 769px) {{ .keyword-list-mobile {{ display: none; }} .keyword-table-desktop {{ display: block; }} }}

            /* 헤더 */
            header {{ text-align: center; margin-bottom: 32px; padding-top: 20px; }}
            .logo {{ font-size: 3rem; margin-bottom: 10px; display: inline-block; animation: float 3s infinite ease-in-out; }}
            h1 {{ font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #fff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
            .subtitle {{ color: var(--text-sub); margin-top: 8px; }}
            @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
            .update-time {{ display: inline-flex; align-items: center; gap: 6px; margin-top: 15px; padding: 6px 14px; background: rgba(34, 211, 238, 0.1); border-radius: 20px; color: var(--color-diamond); font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(34, 211, 238, 0.2); }}
            .pulse {{ width: 8px; height: 8px; background: currentColor; border-radius: 50%; box-shadow: 0 0 8px currentColor; }}

            /* 통계 카드 */
            .stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 24px; }}
            .stat-card {{ background: var(--bg-card); border-radius: 16px; padding: 16px; text-align: center; border: var(--glass-border); }}
            .stat-val {{ font-size: 1.5rem; font-weight: 800; }}
            .stat-label {{ font-size: 0.8rem; color: var(--text-sub); margin-top: 4px; }}

            /* 액션 바 */
            .action-bar {{ background: var(--bg-card); backdrop-filter: blur(12px); border: var(--glass-border); border-radius: 20px; padding: 20px; margin-bottom: 24px; display: flex; flex-direction: column; gap: 16px; align-items: center; }}
            .action-row {{ display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; width: 100%; }}
            .btn-action {{ display: inline-flex; align-items: center; gap: 8px; padding: 10px 18px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; color: var(--text-main); font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: 0.2s; }}
            .btn-action:hover {{ background: rgba(255, 255, 255, 0.1); transform: translateY(-2px); }}
            .sns-btn {{ width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; color: #fff; text-decoration: none; transition: 0.2s; }}
            .sns-btn:hover {{ transform: scale(1.1); box-shadow: 0 0 15px rgba(255,255,255,0.2); }}

            /* 테이블 (PC) */
            .keyword-table-desktop {{ background: var(--bg-card); border-radius: 20px; overflow: hidden; border: var(--glass-border); }}
            table {{ width: 100%; border-collapse: collapse; }}
            th {{ text-align: left; padding: 16px 24px; color: var(--text-sub); font-size: 0.85rem; font-weight: 600; background: rgba(0,0,0,0.2); }}
            td {{ padding: 16px 24px; border-bottom: 1px solid rgba(255,255,255,0.05); vertical-align: middle; }}
            tr:hover td {{ background: rgba(51, 65, 85, 0.8); }}
            
            /* 카드 (모바일) */
            .keyword-card-mobile {{ background: var(--bg-card); border-radius: 16px; padding: 16px; border: var(--glass-border); border-left: 4px solid transparent; }}
            .m-head {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
            .m-rank {{ font-size: 0.9rem; color: var(--text-sub); font-weight: 600; }}
            .m-word {{ font-size: 1.1rem; font-weight: 700; color: var(--text-main); }}
            .m-stat {{ background: rgba(0,0,0,0.2); padding: 10px; border-radius: 8px; margin-bottom: 12px; display: flex; justify-content: space-between; }}
            .m-btns {{ display: flex; gap: 8px; }}

            /* 유틸리티 */
            .rank-diamond {{ color: var(--color-diamond); border-left-color: var(--color-diamond) !important; }}
            .rank-gold {{ color: var(--color-gold); border-left-color: var(--color-gold) !important; }}
            .rank-silver {{ color: var(--color-silver); border-left-color: var(--color-silver) !important; }}
            .rank-red {{ color: var(--color-red); border-left-color: var(--color-red) !important; opacity: 0.7; }}
            
            .badge {{ padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }}
            .badge-diamond {{ background: rgba(34, 211, 238, 0.15); color: var(--color-diamond); border: 1px solid rgba(34, 211, 238, 0.3); }}
            .badge-gold {{ background: rgba(251, 191, 36, 0.15); color: var(--color-gold); border: 1px solid rgba(251, 191, 36, 0.3); }}
            .badge-silver {{ background: rgba(148, 163, 184, 0.15); color: var(--color-silver); border: 1px solid rgba(148, 163, 184, 0.3); }}
            .badge-red {{ background: rgba(248, 113, 113, 0.15); color: var(--color-red); border: 1px solid rgba(248, 113, 113, 0.3); }}

            .btn-sm {{ flex: 1; padding: 8px; border-radius: 8px; font-size: 0.8rem; font-weight: 500; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.05); color: var(--text-sub); text-align: center; cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; justify-content: center; gap: 4px; }}
            .btn-sm:hover {{ background: rgba(255,255,255,0.1); color: var(--text-main); }}
            .btn-copy:hover {{ background: var(--color-accent); color: white; }}
            .btn-link {{ color: var(--color-diamond); }}
            .btn-link:hover {{ background: rgba(34, 211, 238, 0.15); }}

            .archive-btn {{ display: block; width: 100%; padding: 16px; margin-top: 30px; background: var(--bg-card); border-radius: 16px; text-align: center; color: var(--text-main); text-decoration: none; font-weight: 700; border: var(--glass-border); transition: 0.3s; }}
            .archive-btn:hover {{ background: rgba(51, 65, 85, 0.8); border-color: var(--color-accent); }}

            /* 광고 박스 */
            .ad-box {{ text-align: center; margin: 20px 0; background: #1a1a1a; padding: 10px; border-radius: 12px; border: var(--glass-border); }}
            .ad-label {{ font-size: 0.7rem; color: var(--text-muted); margin-bottom: 5px; }}
            
            /* SEO 박스 */
            .seo-box {{ margin: 30px 0; padding: 24px; background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(6, 182, 212, 0.05)); border-radius: 16px; border: 1px solid rgba(139, 92, 246, 0.2); line-height: 1.8; }}
            .seo-box h4 {{ margin: 0 0 12px 0; color: var(--color-accent); font-size: 1.1rem; font-weight: 700; }}
            .seo-box p {{ margin: 0; color: var(--text-sub); font-size: 0.9rem; }}
            .seo-tags {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 15px; }}
            .seo-tag {{ padding: 4px 10px; background: rgba(139, 92, 246, 0.15); border-radius: 20px; font-size: 0.8rem; color: #a78bfa; }}

            #toast {{ position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(20px); background: var(--color-accent); color: white; padding: 12px 24px; border-radius: 30px; font-weight: 600; opacity: 0; visibility: hidden; transition: 0.3s; z-index: 9999; }}
            #toast.show {{ opacity: 1; visibility: visible; transform: translateX(-50%) translateY(0); }}
            footer {{ text-align: center; margin-top: 50px; color: var(--text-muted); font-size: 0.8rem; }}
        </style>
        """

    @staticmethod
    def get_scripts():
        return """
        <div id="toast">✅ 복사 완료!</div>
        <script>
            function copyKeyword(text) {
                navigator.clipboard.writeText(text).then(() => { showToast('✅ "' + text + '" 복사 완료!'); })
                .catch(() => { alert('복사됨: ' + text); });
            }
            function copyPageLink() {
                navigator.clipboard.writeText(window.location.href).then(() => { showToast('✅ 링크 복사 완료!'); });
            }
            function showToast(msg) {
                const t = document.getElementById('toast'); t.textContent = msg; t.classList.add('show');
                setTimeout(() => t.classList.remove('show'), 2500);
            }
            function shareKakao() { alert('카카오톡 API 키 설정이 필요합니다.'); }
            function showBookmarkTip() { alert('PC: Ctrl+D / Mobile: 메뉴 > 북마크 추가'); }
        </script>
        """

    @staticmethod
    def get_action_bar():
        return f"""
        <div class="action-bar">
            <div class="action-row">
                <button class="btn-action" onclick="showBookmarkTip()"><i class="fas fa-star"></i> 북마크</button>
                <button class="btn-action" onclick="copyPageLink()"><i class="fas fa-link"></i> 링크복사</button>
            </div>
            <div class="action-row" style="margin-top:5px; gap:12px;">
                <a href="javascript:shareKakao()" class="sns-btn" style="background:#FEE500; color:#3C1E1E;"><i class="fas fa-comment"></i></a>
                <a href="https://twitter.com/intent/tweet?url={Config.URL}" target="_blank" class="sns-btn" style="background:#000;"><i class="fa-brands fa-x-twitter"></i></a>
                <a href="https://blog.naver.com/openapi/share?url={Config.URL}" target="_blank" class="sns-btn" style="background:#03C75A;"><i class="fa-solid fa-n"></i></a>
                <a href="https://www.facebook.com/sharer/sharer.php?u={Config.URL}" target="_blank" class="sns-btn" style="background:#1877F2;"><i class="fab fa-facebook-f"></i></a>
            </div>
        </div>
        """

    @staticmethod
    def get_ad_unit():
        return f"""<div class="ad-box"><div class="ad-label">Advertisement</div><ins class="adsbygoogle" style="display:block" data-ad-client="{Config.PUB_ID}" data-ad-slot="{Config.SLOT_ID}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script></div>"""

    @staticmethod
    def get_side_rail():
        return f"""<aside class="side-rail"><div class="ad-label">AD</div><ins class="adsbygoogle" style="display:block" data-ad-client="{Config.PUB_ID}" data-ad-slot="{Config.SLOT_ID}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script></aside>"""

    @staticmethod
    def get_seo_content(position="top"):
        if position == "top":
            return """
            <div class="seo-box">
                <h4>📈 수익형 블로그 키워드 분석</h4>
                <p>본 데이터는 <strong>네이버 블로그, 티스토리, 워드프레스 SEO</strong> 최적화를 위한 실시간 분석 자료입니다. 황금 키워드를 선점하여 <strong>애드센스 수익</strong>을 극대화하세요.</p>
                <div class="seo-tags">
                    <span class="seo-tag">블로그 수익화</span><span class="seo-tag">키워드 도구</span><span class="seo-tag">SEO 최적화</span>
                </div>
            </div>
            """
        return """
        <div class="seo-box" style="border-color: rgba(245, 158, 11, 0.3);">
            <h4 style="color: #fbbf24;">💰 고단가 키워드 전략</h4>
            <p><strong>보험, 대출, 정부지원금, IT 기기</strong> 등 CPC 단가가 높은 키워드와 연계하여 콘텐츠를 작성하면 광고 수익 효율을 높일 수 있습니다.</p>
        </div>
        """

# ==========================================
# 3. 🕸️ 크롤링 및 데이터 처리
# ==========================================
class Crawler:
    @staticmethod
    def get_keywords_farm():
        print("🚗 [메인] 애드센스팜 수집 시도...")
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        try:
            driver.get("https://adsensefarm.kr/realtime/")
            time.sleep(7)
            driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(1)
            elements = driver.find_elements(By.CSS_SELECTOR, "td, .keyword, .rank-text, li, span.txt_rank")
            raw = []
            for e in elements:
                t = e.text.strip()
                if 2 <= len(t) < 30:
                    clean = re.sub(r'^[0-9]+\.?', '', t).strip()
                    if clean and not clean.isdigit() and clean not in ["순위", "키워드"]:
                        raw.append(clean)
            return list(dict.fromkeys(raw))[:40]
        except Exception as e:
            print(f"❌ Farm Error: {e}")
            return []
        finally:
            driver.quit()

    @staticmethod
    def get_keywords_google():
        print("⚠️ [백업] 구글 트렌드 가동")
        try:
            res = requests.get("https://trends.google.com/trends/trendingsearches/daily/rss?geo=KR", timeout=10)
            if res.status_code == 200:
                root = ET.fromstring(res.content)
                return [i.find("title").text for i in root.findall(".//item")]
        except Exception as e:
            print(f"❌ 백업 실패: {e}")
        return ["손흥민", "날씨", "로또", "비트코인", "환율", "아이폰", "삼성전자", "부동산", "주식", "여행"]

    @staticmethod
    def get_blog_count(keyword):
        if not Config.NAVER_ID: return 999999
        url = "https://openapi.naver.com/v1/search/blog.json"
        headers = {"X-Naver-Client-Id": Config.NAVER_ID, "X-Naver-Client-Secret": Config.NAVER_SECRET}
        try:
            res = requests.get(url, headers=headers, params={"query": keyword, "display": 1}, timeout=5)
            if res.status_code == 200: return res.json().get('total', 0)
            return 999999
        except: return 999999

# ==========================================
# 4. 🚀 메인 로직
# ==========================================
def create_dashboard():
    keywords = Crawler.get_keywords_farm()
    if not keywords:
        print("🚨 메인 실패 → 백업 전환")
        keywords = Crawler.get_keywords_google()

    print(f"📊 {len(keywords)}개 분석 시작...")
    
    data = []
    for word in keywords:
        count = Crawler.get_blog_count(word)
        if count < 100: grade, css, badge = "💎 신생", "rank-diamond", "badge-diamond"
        elif count < 1000: grade, css, badge = "🥇 꿀통", "rank-gold", "badge-gold"
        elif count < 5000: grade, css, badge = "🥈 보통", "rank-silver", "badge-silver"
        else: grade, css, badge = "💀 레드", "rank-red", "badge-red"
        
        data.append({"word": word, "count": count, "grade": grade, "css": css, "badge": badge})
        time.sleep(0.05)
    
    data.sort(key=lambda x: x['count'])
    
    # 통계
    stats = {
        "diamond": len([d for d in data if d['css'] == 'rank-diamond']),
        "gold": len([d for d in data if d['css'] == 'rank-gold']),
        "total": len(data),
        "max": max([d['count'] for d in data]) if data else 10000
    }

    # 리스트 생성
    pc_rows, mo_cards = "", ""
    for idx, item in enumerate(data):
        link = f"https://search.naver.com/search.naver?where=view&sm=tab_jum&query={item['word']}"
        width = min((item['count'] / stats['max']) * 100, 100)
        
        # 광고 삽입 (모바일: 5개마다, PC: 7개마다)
        if idx > 0:
            if idx % 5 == 0: mo_cards += f'<div class="ad-box-mobile">{Template.get_ad_unit()}</div>'
            if idx % 7 == 0: pc_rows += f'<tr class="ad-row"><td colspan="4" style="padding:0;">{Template.get_ad_unit()}</td></tr>'

        # PC Row
        pc_rows += f"""
        <tr class="{item['css']}">
            <td><div class="kwd-wrapper"><span class="rank-badge">{idx+1}</span><span class="kwd-text" onclick="copyKeyword('{item['word']}')">{item['word']}</span></div></td>
            <td><div class="count-wrapper"><span class="count-text">{format(item['count'], ',')}건</span><div class="count-bar"><div class="count-bar-fill" style="width:{width}%; background:var(--color-accent)"></div></div></div></td>
            <td><span class="badge {item['badge']}">{item['grade']}</span></td>
            <td><div class="actions-cell"><button class="btn-sm btn-copy" onclick="copyKeyword('{item['word']}')">📋</button><a href="{link}" target="_blank" class="btn-sm btn-link">분석 ↗</a></div></td>
        </tr>"""
        
        # Mobile Card
        mo_cards += f"""
        <div class="keyword-card-mobile {item['css']}">
            <div class="m-head"><span class="m-rank">#{idx+1}</span><span class="badge {item['badge']}">{item['grade']}</span></div>
            <div class="m-word" onclick="copyKeyword('{item['word']}')">{item['word']}</div>
            <div class="m-stat"><span>문서수</span><strong>{format(item['count'], ',')}건</strong></div>
            <div class="m-btns"><button class="btn-sm btn-copy" onclick="copyKeyword('{item['word']}')">📋 복사</button><a href="{link}" target="_blank" class="btn-sm btn-link">분석 ↗</a></div>
        </div>"""

    # 시간
    try:
        now_kst = datetime.datetime.now(ZoneInfo("Asia/Seoul"))
    except:
        now_kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    now_str = now_kst.strftime("%Y-%m-%d %H:%M")
    file_id = now_kst.strftime("%Y%m%d_%H%M")

    # HTML 조립
    head = f"""
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{Config.TITLE}</title>
        <meta name="description" content="{Config.DESC}">
        <meta name="naver-site-verification" content="fc4c11b5b82613bc531109cb4aee0331874d5510" />
        <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚀</text></svg>">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={Config.PUB_ID}" crossorigin="anonymous"></script>
        {Template.get_style()}
    </head>
    """

    body_content = f"""
    <div class="layout-wrapper">
        {Template.get_side_rail()}
        <main class="main-content">
            <header>
                <div class="logo">🚀</div>
                <h1>{Config.TITLE}</h1>
                <p class="subtitle">실시간 트렌드 & 경쟁률 분석</p>
                <div class="update-time"><span class="pulse"></span><span>{now_str} 업데이트 (KST)</span></div>
            </header>
            
            {Template.get_action_bar()}
            
            <div class="stats-grid">
                <div class="stat-card"><div class="stat-icon">💎</div><div class="stat-val" style="color:var(--color-diamond)">{stats['diamond']}</div><div class="stat-label">블루오션</div></div>
                <div class="stat-card"><div class="stat-icon">🥇</div><div class="stat-val" style="color:var(--color-gold)">{stats['gold']}</div><div class="stat-label">꿀통</div></div>
                <div class="stat-card"><div class="stat-icon">📊</div><div class="stat-val">{stats['total']}</div><div class="stat-label">분석됨</div></div>
            </div>
            
            {Template.get_seo_content("top")}
            {Template.get_ad_unit()}
            
            <div class="keyword-list-mobile">{mo_cards}</div>
            <div class="keyword-table-desktop"><table><thead><tr><th width="40%">키워드</th><th width="25%">문서수</th><th width="20%">등급</th><th width="15%">액션</th></tr></thead><tbody>{pc_rows}</tbody></table></div>
            
            {Template.get_seo_content("bottom")}
            {Template.get_ad_unit()}
            
            <a href="archive.html" class="archive-btn">🗄️ 지난 리포트 보기</a>
            <footer>© 2025 {Config.TITLE}</footer>
        </main>
        {Template.get_side_rail()}
    </div>
    {Template.get_scripts()}
    """

    full_html = f"<!DOCTYPE html><html lang='ko'>{head}<body>{body_content}</body></html>"

    # 저장
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    
    if not os.path.exists("reports"): os.makedirs("reports")
    report_html = full_html.replace('href="archive.html"', 'href="../archive.html"').replace('href="index.html"', 'href="../index.html"')
    with open(f"reports/{file_id}.html", "w", encoding="utf-8") as f: f.write(report_html)
    
    update_archive_page()
    print(f"✅ 완료! (블루오션: {stats['diamond']}개)")

# ==========================================
# 5. 아카이브 업데이트
# ==========================================
def update_archive_page():
    if not os.path.exists("reports"): return
    files = sorted([f for f in os.listdir("reports") if f.endswith(".html")], reverse=True)
    
    links = ""
    for f in files:
        name = f.replace(".html", "").replace("_", " : ")
        links += f'<a href="reports/{f}" class="archive-btn" style="margin-top:10px; text-align:left;">📄 {name}</a>'
    
    head = f"""<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>🗄️ 아카이브</title>{Template.get_style()}</head>"""
    body = f"""<body><div class="layout-wrapper">{Template.get_side_rail()}<main class="main-content"><header><h1>🗄️ 리포트 보관함</h1></header>{Template.get_ad_unit()}<div style="padding:20px;">{links}</div><div style="text-align:center; margin-top:30px;"><a href="index.html" class="archive-btn">🏠 메인으로</a></div></main>{Template.get_side_rail()}</div></body>"""
    
    with open("archive.html", "w", encoding="utf-8") as f: f.write(f"<!DOCTYPE html><html lang='ko'>{head}{body}</html>")

# ==========================================
# 실행
# ==========================================
if __name__ == "__main__":
    create_dashboard()
    cleanup.cleanup_old_reports()
    sitemap_gen.generate_sitemap()
