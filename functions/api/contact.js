// 官網「預約諮詢」表單：驗證 → 轉給 Apps Script 寄信。
// 環境變數（Cloudflare Pages secrets）：GAS_URL、FORM_SECRET。收件信箱只在 Apps Script 裡。
const LIMITS = { name: 50, company: 100, email: 120, phone: 30, message: 3000, systems: 500 };

export async function onRequestPost({ request, env }) {
  const wantsHtml = !(request.headers.get('accept') || '').includes('application/json');
  let d;
  try {
    const ct = request.headers.get('content-type') || '';
    d = ct.includes('application/json')
      ? await request.json()
      : Object.fromEntries(await request.formData());
  } catch {
    return reply(wantsHtml, 400, '資料格式錯誤');
  }

  // 機器人陷阱：真人看不到 website 欄位；送出時間太快也視為機器人（回成功，不寄信）
  if (d.website || (d.t && Date.now() - Number(d.t) < 3000)) return reply(wantsHtml, 200);

  const f = {};
  for (const k of Object.keys(LIMITS)) f[k] = String(d[k] ?? '').trim().slice(0, LIMITS[k]);
  if (!f.name || !f.company || !f.message) return reply(wantsHtml, 400, '請填寫必填欄位');
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email)) return reply(wantsHtml, 400, '電子郵件格式不正確');
  if (!d.consent) return reply(wantsHtml, 400, '請勾選同意隱私權政策');

  const payload = {
    ...f,
    secret: env.FORM_SECRET,
    page: String(d.page || '').slice(0, 200),
    at: new Date().toLocaleString('zh-TW', { timeZone: 'Asia/Taipei', hour12: false }),
  };
  try {
    const r = await fetch(env.GAS_URL, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(payload),
      redirect: 'follow',
    });
    const j = await r.json();
    if (!j.ok) throw new Error(j.error || 'send failed');
  } catch (e) {
    console.log('contact send failed', String(e));
    return reply(wantsHtml, 502, '系統暫時無法送出，請稍後再試');
  }
  return reply(wantsHtml, 200);
}

function reply(html, status, error) {
  if (html) {
    const to = error ? `/contact?error=${encodeURIComponent(error)}` : '/contact?sent=1';
    return new Response(null, { status: 303, headers: { Location: to } });
  }
  return Response.json(error ? { ok: false, error } : { ok: true }, { status });
}
