# MIND FLOW 思維流 官網（mindflow.tw）

主軸：企業流程 AI 代理人（一句話交辦 → 自動執行 → 主動匯報），CarePro 為長照落地案例。

## 結構
- `src/pages/*.html` — 各頁內容；開頭 `<!-- -->` 是 title / description / path 等 SEO 資訊
- `src/partials/` — 共用頁首、頁尾
- `src/static/` — CSS、圖片、robots.txt、llms.txt、_headers、_redirects
- `build.py` — 產生 `public/`（含 sitemap.xml、FAQPage 結構化資料）；**聯絡資料只改 build.py 的 SITE**
- `tools_make_og.py` — 重畫首頁分享圖 `assets/og.png`

## 建置與部署
```
python build.py
npx wrangler pages deploy public --project-name mindflow-site
```
`public/` 是產物，不要手改。

## GEO / SEO 清單
- 每頁獨立 title / description / canonical / OG
- JSON-LD：Organization、WebSite、Service、Article、DefinedTerm、FAQPage、SoftwareApplication、BreadcrumbList
- `robots.txt` 明確允許 GPTBot、ClaudeBot、PerplexityBot、Google-Extended 等 AI 爬蟲
- `llms.txt` 給 AI 助理的公司摘要
- 導入指南頁 `/what-is-ai-agent`：定義句、比較表、步驟、公式，最容易被生成式搜尋引用

## 預約諮詢表單
網站不顯示任何信箱。表單 → `functions/api/contact.js`（Pages Function，驗證＋防機器人）→ Apps Script 網頁應用程式寄信給負責人。
- Apps Script 原始碼在 `gas_contact/`（`Code.js` 含收件信箱與共用密鑰，不進版控；`clasp push` 後要「新增部署作業」或 `clasp deploy -i <id>` 更新同一個網址）
- Pages secrets：`GAS_URL`、`FORM_SECRET`（本機 `.gas_url`、`.form_secret`，不進版控）
