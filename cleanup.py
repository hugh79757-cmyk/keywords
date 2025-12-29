import os
import datetime
import csv
import re

# ==========================================
# 설정
# ==========================================
RETENTION_DAYS = 90  # 90일(3개월) 보관
REPORTS_DIR = "reports"
BACKUP_DIR = "backups"

def cleanup_old_reports():
    print("🧹 오래된 리포트 정리 시작...")
    
    if not os.path.exists(REPORTS_DIR):
        print("❌ reports 폴더가 없습니다.")
        return

    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    now = datetime.datetime.now()
    cutoff_date = now - datetime.timedelta(days=RETENTION_DAYS)
    
    # 삭제할 파일 목록 찾기
    files_to_archive = []
    for filename in os.listdir(REPORTS_DIR):
        if not filename.endswith(".html"): continue
        
        # 파일명에서 날짜 추출 (20251229_1400.html)
        try:
            date_str = filename.split("_")[0] # 20251229
            file_date = datetime.datetime.strptime(date_str, "%Y%m%d")
            
            if file_date < cutoff_date:
                files_to_archive.append(filename)
        except:
            continue # 날짜 형식이 안 맞으면 패스

    if not files_to_archive:
        print("✅ 삭제할 오래된 파일이 없습니다.")
        return

    print(f"📦 {len(files_to_archive)}개의 파일을 백업하고 삭제합니다...")

    # CSV 파일명 (예: backup_2025-01.csv)
    backup_filename = f"{BACKUP_DIR}/backup_{now.strftime('%Y-%m')}.csv"
    file_exists = os.path.isfile(backup_filename)

    with open(backup_filename, "a", newline="", encoding="utf-8-sig") as csvfile:
        fieldnames = ["date", "keyword", "count", "grade"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()

        for filename in files_to_archive:
            filepath = os.path.join(REPORTS_DIR, filename)
            
            # HTML 파일 읽어서 데이터 추출 (간단 파싱)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 정규식으로 데이터 추출 (테이블 행)
            # <tr>...<span class="keyword-text">키워드</span>...<td class="count-cell">1,234건</td>...</tr>
            matches = re.findall(r'<span class="keyword-text">([^<]+)</span>.*?class="count-cell">([^<]+)건</td>.*?<span class="badge">([^<]+)</span>', content, re.DOTALL)
            
            file_time = filename.replace(".html", "")
            
            for match in matches:
                writer.writerow({
                    "date": file_time,
                    "keyword": match[0],
                    "count": match[1],
                    "grade": match[2]
                })
            
            # 원본 파일 삭제
            os.remove(filepath)
            print(f"🗑️ 삭제됨: {filename}")

    print(f"✅ 백업 완료: {backup_filename}")

if __name__ == "__main__":
    cleanup_old_reports()
