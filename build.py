"""MIND FLOW 官網產生器：src/ → public/

  python build.py

src/pages/*.html 開頭的 <!-- ... --> 是頁面資訊（title/description/path/...），
其餘是 <main> 內容。共用的 head、頁首、頁尾在這支程式與 src/partials/ 裡，
聯絡資料只改下面 SITE 一處。public/ 是部署產物（Cloudflare Pages output dir），不要手改。
"""
import datetime
import hashlib
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "public"

SITE = {
    "url": "https://mindflow.tw",
    "name": "MIND FLOW 思維流",
    "legal_name": "思維流有限公司",
    "tax_id": "00176073",
    "founded": "2025-02-13",
    "address_locality": "花蓮市",
    "address_region": "花蓮縣",
    "street": "仁愛街2之7號1樓",
    "postal": "970",
    "demo": "https://demo.mindflow.tw",
    "youtube": "https://www.youtube.com/@mindflowtw",
}
TODAY = datetime.date.today().isoformat()
TRANSCRIPT = (SRC / "partials" / "video_transcript.html").read_text(encoding="utf-8")
RAW = {}
CSS_VER = hashlib.md5((SRC / "static" / "styles.css").read_bytes()).hexdigest()[:8]

NAV = [
    ("agents", "/ai-agents", "服務方式"),
    ("training", "/ai-training", "企業內訓"),
    ("cases", "/cases", "實績案例"),
    ("guide", "/what-is-ai-agent", "導入指南"),
    ("faq", "/faq", "常見問題"),
    ("about", "/about", "關於我們"),
]


def org_graph():
    s = SITE
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{s['url']}/#org",
                "name": s["name"],
                "alternateName": ["MIND FLOW", "思維流", s["legal_name"]],
                "legalName": s["legal_name"],
                "taxID": s["tax_id"],
                "foundingDate": s["founded"],
                "url": s["url"] + "/",
                "logo": f"{s['url']}/assets/icon-512.png",
                "sameAs": [s["youtube"]],
                "description": "MIND FLOW 思維流是台灣花蓮的軟體公司，為企業打造專屬 AI 代理人：人下指令，AI 依排程把工作做完，遇到例外才請人確認，並定期主動匯報結果；也提供企業 AI 內訓與組織培訓，讓團隊自己會用 AI。不限產業與部門，實績涵蓋社群與網紅數據監測、多平台自動發布、AI 教學影片製作與日照機構工作流程系統 CarePro。",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": s["street"],
                    "addressLocality": s["address_locality"],
                    "addressRegion": s["address_region"],
                    "postalCode": s["postal"],
                    "addressCountry": "TW",
                },
                "areaServed": {"@type": "Country", "name": "台灣"},
                "knowsAbout": [
                    "AI 代理人", "AI Agent", "企業流程自動化", "工作流程自動化",
                    "生成式 AI 導入", "企業 AI 內訓", "AI 教育訓練", "組織 AI 培訓", "社群數據分析", "網紅成效監測", "社群自動發布", "AI 教學影片製作", "語音合成", "會議報到系統", "活動 QR Code 報到", "長照資訊系統", "日照管理系統", "FHIR 醫療資料交換",
                ],
                "contactPoint": {
                    "@type": "ContactPoint",
                    "contactType": "sales",
                    "url": f"{s['url']}/contact",
                    "availableLanguage": ["zh-TW", "en"],
                    "areaServed": "TW",
                },
            },
            {
                "@type": "WebSite",
                "@id": f"{s['url']}/#website",
                "url": s["url"] + "/",
                "name": s["name"],
                "inLanguage": "zh-TW",
                "publisher": {"@id": f"{s['url']}/#org"},
            },
        ],
    }


VIDEO = {
    "id": "adwX34Hk85A",
    "name": "MIND FLOW 思維流｜每天的重複工作，交給 AI 代理人",
    "description": "每天都有重複的事情要做嗎？MIND FLOW 思維流幫企業分析流程、設定 AI 工具，把重複的工作交給 AI 代理人：您下指令，AI 去做，做完主動匯報。影片也介紹人工核准與操作紀錄等安全機制、我們每天實際運作的案例，以及企業 AI 內訓與組織訓練。",
    "upload": "2026-10-29T08:00:00+08:00",
    "duration": "PT3M21S",
    "length": 201,
    "chapters": [(0, "開場：每天都有重複的事要做嗎"), (14, "您下指令，AI 去做"), (29, "很多流程都可以交給 AI"),
                 (38, "生活中的例子"), (59, "我們幫您做三件事"), (84, "舉例：每週一的逾期帳款"),
                 (109, "AI 做事，您掌握"), (126, "我們自己每天就是這樣工作"), (148, "企業內訓：讓團隊自己會用 AI"),
                 (176, "從一次對話開始"), (193, "結尾")],
}


def video_ld(transcript):
    """公司介紹影片的 VideoObject：章節寫成 Clip，搜尋結果才會出現重要時刻；附逐字稿給 AI 搜尋讀。"""
    v, s = VIDEO, SITE
    ch = v["chapters"]
    watch = f"https://www.youtube.com/watch?v={v['id']}"
    clips = [{"@type": "Clip", "name": n, "startOffset": t,
              "endOffset": ch[i + 1][0] if i + 1 < len(ch) else v["length"], "url": f"{watch}&t={t}s"}
             for i, (t, n) in enumerate(ch)]
    return ld({
        "@context": "https://schema.org", "@type": "VideoObject", "@id": f"{s['url']}/#brand-video",
        "name": v["name"], "description": v["description"], "inLanguage": "zh-TW",
        "thumbnailUrl": [f"{s['url']}/assets/video-cover.png", f"https://i.ytimg.com/vi/{v['id']}/maxresdefault.jpg"],
        "uploadDate": v["upload"], "duration": v["duration"],
        "embedUrl": f"https://www.youtube.com/embed/{v['id']}", "url": watch,
        "publisher": {"@id": f"{s['url']}/#org"}, "hasPart": clips,
        "transcript": re.sub(r"<[^>]+>|\s+", "", transcript),
    })


def parse_page(text):
    m = re.match(r"\s*<!--(.*?)-->\s*", text, re.S)
    meta = {}
    for line in m.group(1).strip().splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    return meta, text[m.end():]


def breadcrumb_ld(meta):
    if meta["path"] == "/":
        return ""
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首頁", "item": SITE["url"] + "/"},
            {"@type": "ListItem", "position": 2, "name": meta.get("crumb", meta["title"]),
             "item": SITE["url"] + meta["path"]},
        ],
    }
    return ld(data)


def faq_ld(body):
    """從頁面上的 <details><summary>問</summary><p>答</p> 產生 FAQPage，確保結構化資料與畫面一致。"""
    items = []
    for q, a in re.findall(r"<summary>(.*?)</summary>\s*(.*?)</details>", body, re.S):
        answer = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", a)).strip()
        items.append({"@type": "Question", "name": html.unescape(q.strip()),
                      "acceptedAnswer": {"@type": "Answer", "text": html.unescape(fill(answer))}})
    return ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items})


def ld(data):
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


def fill(text):
    s = SITE
    rep = {
        "{{ADDRESS}}": f"{s['address_region']}{s['address_locality']}{s['street']}",
        "{{DEMO}}": s["demo"],
        "{{SITE}}": s["url"],
        "{{UPDATED}}": TODAY,
        "{{YEAR}}": TODAY[:4],
        "{{TAX_ID}}": s["tax_id"],
        "{{LEGAL_NAME}}": s["legal_name"],
    }
    for k, v in rep.items():
        text = text.replace(k, v)
    return text


def render(meta, body, header, footer):
    url = SITE["url"] + meta["path"]
    og = SITE["url"] + meta.get("og_image", "/assets/og.png")
    title = meta["title"]
    desc = meta["description"]
    nav_html = header
    for key, href, _ in NAV:
        cur = ' aria-current="page"' if meta.get("nav") == key else ""
        nav_html = nav_html.replace(f'href="{href}" data-nav', f'href="{href}"{cur} data-nav')
    robots = meta.get("robots", "index, follow, max-image-preview:large, max-snippet:-1")
    e = html.escape
    head = f"""<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="zh-Hant-TW" href="{url}">
<meta name="theme-color" content="#0D1B2A">
<meta property="og:type" content="{meta.get('og_type', 'website')}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:locale" content="zh_TW">
<meta property="og:title" content="{e(meta.get('og_title', title))}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(meta.get('og_title', title))}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og}">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="alternate" type="text/plain" title="LLM summary" href="/llms.txt">
<link rel="stylesheet" href="/styles.css?v={CSS_VER}">
{ld(org_graph())}
{breadcrumb_ld(meta)}
{faq_ld(body) if meta.get("faq_schema") == "yes" else ""}
{video_ld(TRANSCRIPT) if "{{BRAND_VIDEO" in RAW[meta["path"]] else ""}
</head>
<body>
<a class="skip" href="#main">跳到主要內容</a>
{nav_html}
<main id="main">
{body.strip()}
</main>
{footer}
<script>
document.querySelector('.nav-toggle').addEventListener('click', function () {{
  var l = document.getElementById('nav-links');
  var open = l.classList.toggle('open');
  this.setAttribute('aria-expanded', open);
}});
</script>
</body>
</html>
"""
    return fill(head)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC / "static", OUT)
    header = (SRC / "partials" / "header.html").read_text(encoding="utf-8")
    footer = (SRC / "partials" / "footer.html").read_text(encoding="utf-8")
    form = (SRC / "partials" / "contact_form.html").read_text(encoding="utf-8")
    video = (SRC / "partials" / "video.html").read_text(encoding="utf-8").replace("{{VIDEO_ID}}", VIDEO["id"])
    transcript_box = '<details class="transcript"><summary>影片逐字稿</summary>\n' + TRANSCRIPT + "    </details>"

    sitemap = []
    for f in sorted((SRC / "pages").glob("*.html")):
        meta, body = parse_page(f.read_text(encoding="utf-8"))
        RAW[meta["path"]] = body
        body = body.replace("{{CONTACT_FORM}}", form)
        body = body.replace("{{BRAND_VIDEO_WITH_TRANSCRIPT}}", video.replace("{{TRANSCRIPT}}", transcript_box))
        body = body.replace("{{BRAND_VIDEO}}", video.replace("{{TRANSCRIPT}}", ""))
        (OUT / f.name).write_text(render(meta, body, header, footer), encoding="utf-8")
        if meta.get("sitemap", "yes") != "no":
            sitemap.append((meta["path"], meta.get("priority", "0.6"), meta.get("changefreq", "monthly")))

    sitemap.sort(key=lambda x: -float(x[1]))
    urls = "\n".join(
        f"  <url><loc>{SITE['url']}{p}</loc><lastmod>{TODAY}</lastmod>"
        f"<changefreq>{c}</changefreq><priority>{pr}</priority></url>"
        for p, pr, c in sitemap
    )
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n",
        encoding="utf-8",
    )
    for name in ("llms.txt", "robots.txt"):
        p = OUT / name
        p.write_text(fill(p.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"built {len(sitemap)} pages → {OUT}")


if __name__ == "__main__":
    main()
