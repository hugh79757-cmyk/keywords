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
            .side-rail { display: block; }
        }

        header {
            text-align: center;
            margin-bottom: 20px;
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

        .subtitle { color: var(--text-secondary); font-size: 0.95rem; }

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

        /* ==========================================
           📌 액션 바 (북마크 + PWA + 공유)
           ========================================== */
        .action-bar {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
            padding: 20px;
            margin-bottom: 20px;
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
        }

        .action-bar-title {
            width: 100%;
            text-align: center;
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .action-bar-title::before,
        .action-bar-title::after {
            content: '';
            flex: 1;
            max-width: 60px;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--glass-border), transparent);
        }

        .action-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            padding: 10px 16px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            color: var(--text-primary);
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
            white-space: nowrap;
        }

        .action-btn:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.2);
        }

        .action-btn:active {
            transform: scale(0.95);
        }

        .action-btn .icon {
            font-size: 1.1rem;
        }

        /* 특별 버튼 스타일 */
        .action-btn.pwa-btn {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(6, 182, 212, 0.2));
            border-color: rgba(139, 92, 246, 0.3);
        }

        .action-btn.pwa-btn:hover {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.3), rgba(6, 182, 212, 0.3));
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
        }

        .action-btn.bookmark-btn {
            background: rgba(245, 158, 11, 0.15);
            border-color: rgba(245, 158, 11, 0.3);
        }

        .action-btn.bookmark-btn:hover {
            background: rgba(245, 158, 11, 0.25);
            box-shadow: 0 8px 25px rgba(245, 158, 11, 0.2);
        }

        /* SNS 공유 버튼 섹션 */
        .share-divider {
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin: 10px 0 5px;
            font-size: 0.75rem;
            color: var(--text-secondary);
        }

        .share-divider::before,
        .share-divider::after {
            content: '';
            flex: 1;
            max-width: 40px;
            height: 1px;
            background: var(--glass-border);
        }

        .share-buttons {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 8px;
            width: 100%;
        }

        .share-btn {
            width: 44px;
            height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            font-size: 1.2rem;
            cursor: pointer;
            border: none;
            transition: all 0.3s ease;
            text-decoration: none;
        }

        .share-btn:hover {
            transform: translateY(-3px) scale(1.05);
        }

        .share-btn:active {
            transform: scale(0.95);
        }

        /* ===== SNS 버튼 색상 (수정됨) ===== */
        
        /* 카카오톡 - 노란 배경 */
        .share-btn.kakao {
            background: #FEE500;
        }

        .share-btn.kakao:hover {
            box-shadow: 0 8px 20px rgba(254, 229, 0, 0.5);
        }

        /* X (트위터) - 검정 배경 */
        .share-btn.twitter-x {
            background: #000000;
        }

        .share-btn.twitter-x:hover {
            box-shadow: 0 8px 20px rgba(255, 255, 255, 0.2);
        }

        /* 스레드 - 검정 배경 */
        .share-btn.threads {
            background: #000000;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        .share-btn.threads:hover {
            box-shadow: 0 8px 20px rgba(255, 255, 255, 0.2);
        }

        /* 네이버 블로그 - 초록 배경 */
        .share-btn.naver {
            background: #03C75A;
        }

        .share-btn.naver:hover {
            box-shadow: 0 8px 20px rgba(3, 199, 90, 0.5);
        }

        /* 페이스북 - 파란 배경 */
        .share-btn.facebook {
            background: #1877F2;
        }

        .share-btn.facebook:hover {
            box-shadow: 0 8px 20px rgba(24, 119, 242, 0.5);
        }

        /* 링크 복사 - 글래스 스타일 */
        .share-btn.copy-link {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        .share-btn.copy-link:hover {
            background: rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 20px rgba(255, 255, 255, 0.1);
        }

        /* 북마크 팁 팝업 */
        .bookmark-tip {
            display: none;
            position: fixed;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(139, 92, 246, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 16px;
            padding: 16px 24px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
            z-index: 1001;
            max-width: 90%;
            animation: slideUp 0.4s ease;
        }

        .bookmark-tip.show {
            display: block;
        }

        @keyframes slideUp {
            from { transform: translateX(-50%) translateY(30px); opacity: 0; }
            to { transform: translateX(-50%) translateY(0); opacity: 1; }
        }

        .bookmark-tip-content {
            display: flex;
            align-items: center;
            gap: 15px;
            color: white;
        }

        .bookmark-tip-icon {
            font-size: 2rem;
        }

        .bookmark-tip-text h4 {
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .bookmark-tip-text p {
            font-size: 0.85rem;
            opacity: 0.9;
        }

        .bookmark-tip-text kbd {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 3px 8px;
            border-radius: 6px;
            font-family: monospace;
            font-size: 0.8rem;
            margin: 0 2px;
        }

        .bookmark-tip-close {
            position: absolute;
            top: 10px;
            right: 12px;
            background: none;
            border: none;
            color: white;
            font-size: 1.2rem;
            cursor: pointer;
            opacity: 0.7;
            transition: opacity 0.2s;
        }

        .bookmark-tip-close:hover {
            opacity: 1;
        }

        /* ==========================================
           기존 스타일 계속
           ========================================== */
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

        .ad-row td { padding: 0 !important; }

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

        .keyword-card-mobile:active { transform: scale(0.98); }

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
            text-align: center; 
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
            flex-direction: row !important;
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
            display: inline-block;
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

        .keyword-table-desktop {
            display: none;
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            overflow: hidden;
        }

        table { width: 100%; border-collapse: collapse; }

        thead { background: rgba(0, 0, 0, 0.3); }

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

        tbody tr:hover { background: rgba(255, 255, 255, 0.05); }

        td { padding: 16px 20px; vertical-align: middle; }

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

        .keyword-text { font-weight: 600; font-size: 1rem; }

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

        .actions-cell {
            display: flex !important;
            flex-direction: row !important;
            gap: 8px !important;
            align-items: center !important;
        }

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

        .archive-btn:active { transform: scale(0.98); }

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
# 📌 액션 바 HTML (북마크 + PWA + 공유) - SVG 아이콘 버전
# ==========================================
def get_action_bar_html():
    return f"""
    <!-- 액션 바: 북마크 + PWA + 공유 -->
    <div class="action-bar">
        <div class="action-bar-title">빠른 저장 & 공유</div>
        
        <!-- 메인 액션 버튼들 -->
        <button class="action-btn pwa-btn" id="installBtn" style="display:none;" onclick="installPWA()">
            <span class="icon">📲</span>
            <span>앱으로 저장</span>
        </button>
        
        <button class="action-btn bookmark-btn" onclick="showBookmarkTip()">
            <span class="icon">⭐</span>
            <span>북마크 추가</span>
        </button>
        
        <button class="action-btn" onclick="copyPageLink()">
            <span class="icon">🔗</span>
            <span>링크 복사</span>
        </button>
        
        <!-- SNS 공유 버튼들 -->
        <div class="share-divider">SNS 공유</div>
        
        <div class="share-buttons">
            <!-- 카카오톡 -->
            <button class="share-btn kakao" onclick="shareKakao()" title="카카오톡">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="#3C1E1E">
                    <path d="M12 3C6.48 3 2 6.58 2 11c0 2.83 1.89 5.31 4.7 6.7-.17.6-.64 2.2-.73 2.54-.12.43.16.42.34.31.14-.09 2.23-1.5 3.12-2.1.52.07 1.05.11 1.57.11 5.52 0 10-3.58 10-8s-4.48-8-10-8z"/>
                </svg>
            </button>
            
            <!-- X (트위터) -->
            <a href="https://twitter.com/intent/tweet?url={SITE_URL}&text=🚀 황금 키워드 상황실 - 실시간 블루오션 키워드 분석" target="_blank" class="share-btn twitter-x" title="X (트위터)">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
                    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
            </a>
            
            <!-- 스레드 -->
            <a href="https://www.threads.net/intent/post?text=🚀 황금 키워드 상황실 {SITE_URL}" target="_blank" class="share-btn threads" title="스레드">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
                    <path d="M12.186 24h-.007c-3.581-.024-6.334-1.205-8.184-3.509C2.35 18.44 1.5 15.586 1.472 12.01v-.017c.03-3.579.879-6.43 2.525-8.482C5.845 1.205 8.6.024 12.18 0h.014c2.746.02 5.043.725 6.826 2.098 1.677 1.29 2.858 3.13 3.509 5.467l-2.04.569c-1.104-3.96-3.898-5.984-8.304-6.015-2.91.022-5.11.936-6.54 2.717C4.307 6.504 3.616 8.914 3.59 12c.025 3.086.718 5.496 2.057 7.164 1.43 1.783 3.631 2.698 6.54 2.717 2.623-.02 4.358-.631 5.8-2.045 1.647-1.613 1.618-3.593 1.09-4.798-.31-.71-.873-1.3-1.634-1.75-.192 1.352-.622 2.446-1.284 3.272-.886 1.102-2.14 1.704-3.73 1.79-1.202.065-2.361-.218-3.259-.801-1.063-.689-1.685-1.74-1.752-2.96-.065-1.17.408-2.133 1.332-2.727.834-.536 1.943-.79 3.389-.79l.463.013c.333.012.637.04.912.085.098-.772.097-1.472-.028-2.063-.267-1.265-1.079-1.93-2.415-1.977-1.476.044-2.27.73-2.511 1.168l-1.774-1.014c.495-.87 1.653-1.97 4.236-2.082 1.873-.037 3.28.527 4.184 1.674.821 1.04 1.153 2.472 1.013 4.378.502.167.96.39 1.363.671 1.073.748 1.837 1.79 2.205 3.017.49 1.628.288 3.922-1.64 5.81C18.303 23.095 15.697 23.973 12.186 24z"/>
                </svg>
            </a>
            
            <!-- 네이버 블로그 -->
            <a href="https://blog.naver.com/openapi/share?url={SITE_URL}&title=황금 키워드 상황실" target="_blank" class="share-btn naver" title="네이버 블로그">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
                    <path d="M16.273 12.845L7.376 0H0v24h7.726V11.156L16.624 24H24V0h-7.727z"/>
                </svg>
            </a>
            
            <!-- 페이스북 -->
            <a href="https://www.facebook.com/sharer/sharer.php?u={SITE_URL}" target="_blank" class="share-btn facebook" title="페이스북">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
                    <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
            </a>
            
            <!-- 링크 복사 -->
            <button class="share-btn copy-link" onclick="copyPageLink()" title="링크 복사">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
                </svg>
            </button>
        </div>
    </div>
    
    <!-- 북마크 안내 팝업 -->
    <div class="bookmark-tip" id="bookmarkTip">
        <button class="bookmark-tip-close" onclick="closeBookmarkTip()">✕</button>
        <div class="bookmark-tip-content">
            <span class="bookmark-tip-icon">⭐</span>
            <div class="bookmark-tip-text">
                <h4>브라우저 북마크 추가하기</h4>
                <p>
                    <strong>PC:</strong> <kbd>Ctrl</kbd> + <kbd>D</kbd><br>
                    <strong>Mac:</strong> <kbd>⌘</kbd> + <kbd>D</kbd><br>
                    <strong>모바일:</strong> 공유 버튼 → 북마크 추가
                </p>
            </div>
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
        
        # ✅ 광고 배치 전략: 3번째(idx==2) 뒤에 1개, 이후 5개마다 1개
        # idx: 0,1,2 → 3번째(idx==2) 다음에 광고
        # 그 이후: idx==8, idx==13, idx==18... (5개 간격)
        should_show_ad = (idx == 3) or (idx > 3 and (idx - 3) % 5 == 0)

        if should_show_ad:
            # 모바일 광고
            mobile_cards += f"""
            <div class="ad-box-mobile">
                <div class="ad-label">Advertisement</div>
                <ins class="adsbygoogle" style="display:block" data-ad-client="{PUB_ID}" data-ad-slot="{SLOT_ID}" data-ad-format="auto" data-full-width-responsive="true"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
            </div>
            """
            
            # PC 테이블 광고
            desktop_rows += f"""
            <tr class="ad-row">
                <td colspan="4" style="padding: 0;">
                    <div class="ad-box-table">
                        <div class="ad-label">Advertisement</div>
                        <ins class="adsbygoogle" style="display:block" data-ad-client="{PUB_ID}" data-ad-slot="{SLOT_ID}" data-ad-format="auto" data-full-width-responsive="true"></ins>
                        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
                    </div>
                </td>
            </tr>
            """

        # PC 테이블 행
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

    # ✅ 통계 카드
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

    # ✅ SEO 고단가 키워드 가이드 (애드센스 고단가 광고 유도)
    seo_guide_html = """
    <div class="seo-guide-box">
        <h4>📈 블로그 수익화 & SEO 최적화 가이드</h4>
        <p>
            본 데이터는 <strong>네이버 블로그, 티스토리, 워드프레스, 구글 SEO</strong> 최적화를 위한 실시간 분석 자료입니다.
            황금 키워드를 활용하여 <strong>애드센스 수익, 제휴 마케팅, 웹사이트 트래픽</strong>을 극대화하세요.
        </p>
        <div class="seo-keywords">
            <span class="seo-tag">도메인 등록</span>
            <span class="seo-tag">웹호스팅</span>
            <span class="seo-tag">서버 구축</span>
            <span class="seo-tag">VPS 호스팅</span>
            <span class="seo-tag">클라우드 서버</span>
            <span class="seo-tag">SSL 인증서</span>
            <span class="seo-tag">CDN 서비스</span>
            <span class="seo-tag">워드프레스 호스팅</span>
        </div>
        <p class="seo-sub">
            <strong>디지털 마케팅, SaaS 솔루션, 온라인 비즈니스, 이커머스 플랫폼, 
            결제 시스템, CRM 소프트웨어, ERP 시스템, 클라우드 컴퓨팅</strong> 
            등 고수익 키워드 전략 수립에 활용하세요.
        </p>
    </div>
    """

    # ✅ 중간 SEO 콘텐츠 (키워드 중간에 삽입용)
    mid_seo_content = """
    <div class="seo-guide-box mid-content">
        <h4>💰 고수익 키워드 활용 전략</h4>
        <p>
            <strong>보험 비교, 대출 금리, 신용카드 추천, 주식 투자, 부동산 투자, 
            법률 상담, 세무 상담, 건강 보험</strong> 등 CPC 단가가 높은 키워드와 
            연계하여 블로그 콘텐츠를 작성하면 광고 수익을 극대화할 수 있습니다.
        </p>
        <div class="seo-keywords">
            <span class="seo-tag">보험 비교</span>
            <span class="seo-tag">대출 금리</span>
            <span class="seo-tag">신용카드 혜택</span>
            <span class="seo-tag">주식 투자</span>
            <span class="seo-tag">부동산 투자</span>
            <span class="seo-tag">법률 상담</span>
            <span class="seo-tag">세무 상담</span>
            <span class="seo-tag">건강 보험</span>
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
    <title>🚀 황금 키워드 상황실 - 블로그 SEO 키워드 분석 도구</title>
    {seo_meta}
    {style}
    
    <!-- SEO 고단가 키워드 스타일 -->
    <style>
        .seo-guide-box {{
            margin: 30px 0;
            padding: 24px;
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(6, 182, 212, 0.05));
            border-radius: 16px;
            border: 1px solid rgba(139, 92, 246, 0.2);
            line-height: 1.8;
        }}
        
        .seo-guide-box h4 {{
            margin: 0 0 12px 0;
            color: #8b5cf6;
            font-size: 1.1rem;
            font-weight: 700;
        }}
        
        .seo-guide-box p {{
            margin: 0 0 15px 0;
            color: #94a3b8;
            font-size: 0.9rem;
        }}
        
        .seo-guide-box .seo-sub {{
            margin: 15px 0 0 0;
            font-size: 0.85rem;
            color: #64748b;
        }}
        
        .seo-keywords {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 15px 0;
        }}
        
        .seo-tag {{
            padding: 6px 12px;
            background: rgba(139, 92, 246, 0.15);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 20px;
            font-size: 0.8rem;
            color: #a78bfa;
            font-weight: 500;
        }}
        
        .seo-guide-box.mid-content {{
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(239, 68, 68, 0.05));
            border-color: rgba(245, 158, 11, 0.2);
        }}
        
        .seo-guide-box.mid-content h4 {{
            color: #f59e0b;
        }}
        
        .seo-guide-box.mid-content .seo-tag {{
            background: rgba(245, 158, 11, 0.15);
            border-color: rgba(245, 158, 11, 0.3);
            color: #fbbf24;
        }}
    </style>
    
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={PUB_ID}" crossorigin="anonymous"></script>
</head>
<body>
    <div class="layout-wrapper">
        {get_side_rail_ad()}
        
        <main class="main-content">
            <header>
                <div class="logo">🚀</div>
                <h1>황금 키워드 상황실</h1>
                <p class="subtitle">실시간 트렌드 키워드 분석 · 블로그 SEO 최적화</p>
                <div class="update-time">
                    <span class="pulse"></span>
                    <span>{now} 업데이트 (KST)</span>
                </div>
            </header>
            
            {action_bar}
            
            {stats_html}
            
            <!-- 상단 SEO 가이드 -->
            {seo_guide_html}
            
            {get_ad_unit()}
            
            <!-- 모바일 키워드 리스트 -->
            <div class="keyword-list-mobile">
                {mobile_cards}
            </div>
            
            <!-- PC 키워드 테이블 -->
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
            
            <!-- 중간 SEO 콘텐츠 (고단가 키워드) -->
            {mid_seo_content}
            
            {get_ad_unit()}
            
            <!-- 하단 SEO 콘텐츠 -->
            <div class="seo-guide-box">
                <h4>🎯 키워드 분석 활용법</h4>
                <p>
                    <strong>블루오션 키워드</strong>는 경쟁이 낮아 상위 노출이 쉽고, 
                    <strong>꿀통 키워드</strong>는 적절한 경쟁과 검색량을 갖춘 최적의 키워드입니다.
                    이 데이터를 활용하여 <strong>구글 애드센스, 네이버 애드포스트, 카카오 애드핏</strong> 
                    수익을 극대화하세요.
                </p>
                <div class="seo-keywords">
                    <span class="seo-tag">구글 애드센스</span>
                    <span class="seo-tag">네이버 애드포스트</span>
                    <span class="seo-tag">카카오 애드핏</span>
                    <span class="seo-tag">제휴 마케팅</span>
                    <span class="seo-tag">CPA 마케팅</span>
                    <span class="seo-tag">인플루언서 마케팅</span>
                </div>
            </div>
            
            {get_ad_unit()}
            
            <a href="archive.html" class="archive-btn">🗄️ 지난 리포트 보기</a>
            
            <footer>
                <p>© 2025 황금 키워드 상황실 · 블로그 SEO 최적화 도구</p>
                <p style="margin-top: 10px; font-size: 0.75rem; color: #475569;">
                    키워드 분석 · 블로그 수익화 · 애드센스 최적화 · 검색엔진 최적화 · 디지털 마케팅
                </p>
            </footer>
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
