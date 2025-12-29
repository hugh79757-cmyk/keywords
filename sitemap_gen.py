import os
import datetime

DOMAIN = "https://keywords.rotcha.kr"

def generate_sitemap():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{DOMAIN}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{DOMAIN}/archive.html</loc>
    <lastmod>{today}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>0.8</priority>
  </url>
'''

    # 리포트 파일들 추가
    if os.path.exists("reports"):
        for filename in os.listdir("reports"):
            if filename.endswith(".html"):
                xml += f'''  <url>
    <loc>{DOMAIN}/reports/{filename}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
'''

    xml += '</urlset>'

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml)
    
    print("✅ sitemap.xml 생성 완료!")

if __name__ == "__main__":
    generate_sitemap()
