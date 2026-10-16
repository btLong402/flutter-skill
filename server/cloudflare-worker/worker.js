/**
 * Cloudflare Worker - Telemetry & Knowledge Gap Ingestion Server
 * 
 * Storage:
 * - Primary: Cloudflare D1 (5 GB Free, 100,000 writes/day) with UPSERT aggregation
 * - Secondary / Fallback: Cloudflare KV (TELEMETRY_KV)
 * - In-Memory Buffer: Real-time sliding window
 * 
 * Features:
 * 1. Upsert Aggregation: Same query/criteria only updates hit_count + last_seen (drastically saves writes & storage)
 * 2. Rate Limiting: 30 requests / min / IP to prevent spam & quota exhaustion
 * 3. Strict Schema Validation & Sanitization: 10KB size limit, 200 char truncation
 * 4. Automatic 90-Day Retention Cleanup
 * 5. Modern Web Dashboard with ranking of top missing queries & criteria
 * 6. Optional instant Discord / Telegram notification forwarder
 */

// In-memory sliding window rate limiter
const RATE_LIMIT_MAP = new Map();
const RATE_LIMIT_WINDOW_MS = 60 * 1000; // 1 minute
const MAX_REQUESTS_PER_WINDOW = 30; // 30 req/min/IP

// In-memory buffer of recent events for instant fallback
const RECENT_EVENTS = [];
const MAX_RECENT_EVENTS = 50;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type, User-Agent",
        },
      });
    }

    // Router
    if (request.method === "POST" && (url.pathname === "/api/telemetry" || url.pathname === "/telemetry")) {
      return handleTelemetry(request, env, ctx);
    }

    if (request.method === "GET" && (url.pathname === "/api/gaps" || url.pathname === "/api/stats")) {
      return handleGetStats(request, env);
    }

    // Default: Web Dashboard
    return handleDashboard(request, env);
  },
};

/**
 * Check rate limit for client IP
 */
function checkRateLimit(clientIp) {
  const now = Date.now();
  const record = RATE_LIMIT_MAP.get(clientIp);

  if (!record || now > record.resetTime) {
    RATE_LIMIT_MAP.set(clientIp, { count: 1, resetTime: now + RATE_LIMIT_WINDOW_MS });
    return true;
  }

  if (record.count >= MAX_REQUESTS_PER_WINDOW) {
    return false;
  }

  record.count += 1;
  return true;
}

/**
 * Handle incoming telemetry POST request
 */
async function handleTelemetry(request, env, ctx) {
  const clientIp = request.headers.get("CF-Connecting-IP") || request.headers.get("X-Forwarded-For") || "unknown";

  // 1. Rate Limiting Check (30 req/min/IP)
  if (!checkRateLimit(clientIp)) {
    return new Response(JSON.stringify({ error: "Too many requests. Rate limit is 30 req/min." }), {
      status: 429,
      headers: {
        "Content-Type": "application/json",
        "Retry-After": "60",
        "Access-Control-Allow-Origin": "*",
      },
    });
  }

  // 2. Payload size check (Max 10KB)
  const contentLength = parseInt(request.headers.get("Content-Length") || "0", 10);
  if (contentLength > 10240) {
    return new Response(JSON.stringify({ error: "Payload too large. Maximum size is 10KB." }), {
      status: 413,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
    });
  }

  try {
    const rawPayload = await request.json();

    // 3. Strict Schema Validation
    const eventType = String(rawPayload.event_type || "");
    if (eventType !== "knowledge_gap" && eventType !== "criteria_gap") {
      return new Response(JSON.stringify({ error: "Invalid event_type. Allowed: knowledge_gap, criteria_gap." }), {
        status: 400,
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
      });
    }

    // Sanitize & truncate strings
    const cleanPayload = {
      event_type: eventType,
      timestamp: String(rawPayload.timestamp || new Date().toISOString()).slice(0, 50),
      client: {
        version: String(rawPayload.client?.version || "unknown").slice(0, 20),
        os: String(rawPayload.client?.os || "unknown").slice(0, 30),
        python: String(rawPayload.client?.python || "unknown").slice(0, 20),
        ai_assistant: String(rawPayload.client?.ai_assistant || "cli").slice(0, 30),
      },
    };

    if (eventType === "knowledge_gap") {
      cleanPayload.query = String(rawPayload.query || "").slice(0, 200);
      cleanPayload.domain = String(rawPayload.domain || "widget").slice(0, 50);
      cleanPayload.gap_type = String(rawPayload.gap_type || "empty_result").slice(0, 50);
      cleanPayload.result_count = Number(rawPayload.result_count) || 0;
      cleanPayload.max_score = Number(rawPayload.max_score) || 0.0;
      cleanPayload.token_coverage = Number(rawPayload.token_coverage) || 0.0;
      if (rawPayload.stack) cleanPayload.stack = String(rawPayload.stack).slice(0, 30);
      if (rawPayload.notes) cleanPayload.notes = String(rawPayload.notes).slice(0, 300);
    } else {
      cleanPayload.missing_dimensions = Array.isArray(rawPayload.missing_dimensions)
        ? rawPayload.missing_dimensions.slice(0, 10).map((d) => String(d).slice(0, 50))
        : [];
      cleanPayload.platforms = Array.isArray(rawPayload.platforms)
        ? rawPayload.platforms.slice(0, 5).map((p) => String(p).slice(0, 30))
        : [];
      cleanPayload.gap_type = String(rawPayload.gap_type || "unrecognized_dimension").slice(0, 50);
      cleanPayload.reason = String(rawPayload.reason || "").slice(0, 300);
      if (rawPayload.notes) cleanPayload.notes = String(rawPayload.notes).slice(0, 300);
    }

    const eventId = `${Date.now()}-${Math.random().toString(36).substring(2, 8)}`;

    // 4. In-Memory fallback buffer
    RECENT_EVENTS.unshift(cleanPayload);
    if (RECENT_EVENTS.length > MAX_RECENT_EVENTS) RECENT_EVENTS.pop();

    // 5. PRIMARY STORAGE: Cloudflare D1 with UPSERT aggregation
    if (env.DB) {
      if (eventType === "knowledge_gap" && cleanPayload.query) {
        ctx.waitUntil(
          env.DB.prepare(`
            INSERT INTO knowledge_gaps (query, domain, gap_type, hit_count, max_score, token_coverage, last_notes, ai_assistant, client_os, last_seen)
            VALUES (?1, ?2, ?3, 1, ?4, ?5, ?6, ?7, ?8, CURRENT_TIMESTAMP)
            ON CONFLICT(query, domain) DO UPDATE SET
              hit_count = hit_count + 1,
              gap_type = ?3,
              max_score = ?4,
              token_coverage = ?5,
              last_notes = COALESCE(?6, last_notes),
              ai_assistant = ?7,
              client_os = ?8,
              last_seen = CURRENT_TIMESTAMP
          `).bind(
            cleanPayload.query,
            cleanPayload.domain,
            cleanPayload.gap_type,
            cleanPayload.max_score,
            cleanPayload.token_coverage,
            cleanPayload.notes || null,
            cleanPayload.client.ai_assistant,
            cleanPayload.client.os
          ).run().catch((e) => console.error("D1 knowledge_gap error:", e))
        );
      } else if (eventType === "criteria_gap" && cleanPayload.missing_dimensions.length) {
        for (const dim of cleanPayload.missing_dimensions) {
          const plats = cleanPayload.platforms.length ? cleanPayload.platforms : ["both"];
          for (const plat of plats) {
            ctx.waitUntil(
              env.DB.prepare(`
                INSERT INTO criteria_gaps (missing_dimension, platform, gap_type, hit_count, reason, ai_assistant, client_os, last_seen)
                VALUES (?1, ?2, ?3, 1, ?4, ?5, ?6, CURRENT_TIMESTAMP)
                ON CONFLICT(missing_dimension, platform) DO UPDATE SET
                  hit_count = hit_count + 1,
                  gap_type = ?3,
                  reason = COALESCE(?4, reason),
                  ai_assistant = ?5,
                  client_os = ?6,
                  last_seen = CURRENT_TIMESTAMP
              `).bind(
                dim,
                plat,
                cleanPayload.gap_type,
                cleanPayload.reason || cleanPayload.notes || null,
                cleanPayload.client.ai_assistant,
                cleanPayload.client.os
              ).run().catch((e) => console.error("D1 criteria_gap error:", e))
            );
          }
        }
      }
    }

    // 6. SECONDARY STORAGE: Cloudflare KV (fallback)
    if (env.TELEMETRY_KV) {
      ctx.waitUntil(
        env.TELEMETRY_KV.put(`gap:${eventId}`, JSON.stringify(cleanPayload), { expirationTtl: 60 * 60 * 24 * 90 })
      );
    }

    // 7. Instant notifications (Discord / Telegram)
    if (env.DISCORD_WEBHOOK_URL) {
      ctx.waitUntil(sendDiscordAlert(env.DISCORD_WEBHOOK_URL, cleanPayload));
    }
    if (env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID) {
      ctx.waitUntil(sendTelegramAlert(env.TELEGRAM_BOT_TOKEN, env.TELEGRAM_CHAT_ID, cleanPayload));
    }

    return new Response(JSON.stringify({ status: "success", id: eventId, storage: env.DB ? "d1" : (env.TELEMETRY_KV ? "kv" : "memory") }), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 400,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    });
  }
}

/**
 * Forward notification to Discord Webhook
 */
async function sendDiscordAlert(webhookUrl, payload) {
  try {
    const isKnowledge = payload.event_type === "knowledge_gap";
    const title = isKnowledge ? "🚨 Knowledge Gap Detected" : "⚠️ Audit Criteria Gap Detected";
    const color = isKnowledge ? 0x0284c7 : 0xe11d48;

    const fields = [];
    if (isKnowledge) {
      fields.push({ name: "Search Query", value: `\`${payload.query || "N/A"}\``, inline: false });
      fields.push({ name: "Domain", value: payload.domain || "N/A", inline: true });
      fields.push({ name: "Gap Type", value: payload.gap_type || "N/A", inline: true });
      fields.push({ name: "BM25 Score", value: String(payload.max_score ?? "0"), inline: true });
    } else {
      fields.push({
        name: "Missing Dimension(s)",
        value: `\`${(payload.missing_dimensions || []).join(", ") || "N/A"}\``,
        inline: false,
      });
      fields.push({ name: "Platforms", value: (payload.platforms || []).join(", ") || "N/A", inline: true });
      fields.push({ name: "Reason", value: payload.reason || "N/A", inline: false });
    }

    if (payload.notes) {
      fields.push({ name: "User/AI Notes", value: payload.notes, inline: false });
    }

    const client = payload.client || {};
    fields.push({
      name: "Client Environment",
      value: `Assistant: **${client.ai_assistant || "CLI"}** | OS: **${client.os || "N/A"}** | Version: **${client.version || "N/A"}**`,
      inline: false,
    });

    const body = {
      embeds: [
        {
          title,
          color,
          fields,
          timestamp: payload.timestamp || new Date().toISOString(),
          footer: { text: "Flutter Pro Max Telemetry" },
        },
      ],
    };

    await fetch(webhookUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch (_) {}
}

/**
 * Forward notification to Telegram Bot
 */
async function sendTelegramAlert(botToken, chatId, payload) {
  try {
    const isKnowledge = payload.event_type === "knowledge_gap";
    let text = "";

    if (isKnowledge) {
      text =
        `🚨 *[Knowledge Gap Reported]*\n\n` +
        `🔍 *Query:* \`${payload.query}\`\n` +
        `📂 *Domain:* ${payload.domain} | *Type:* ${payload.gap_type}\n` +
        `📊 *Max Score:* ${payload.max_score} | *Count:* ${payload.result_count}\n`;
    } else {
      text =
        `⚠️ *[Audit Criteria Gap Reported]*\n\n` +
        `📐 *Missing:* \`${(payload.missing_dimensions || []).join(", ")}\`\n` +
        `📱 *Platforms:* ${(payload.platforms || []).join(", ")}\n` +
        `💬 *Reason:* ${payload.reason || "N/A"}\n`;
    }

    if (payload.notes) {
      text += `📝 *Notes:* ${payload.notes}\n`;
    }

    const client = payload.client || {};
    text += `\n🤖 *Client:* ${client.ai_assistant || "CLI"} (${client.os || "N/A"}) | v${client.version || "N/A"}`;

    await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_id: chatId,
        text,
        parse_mode: "Markdown",
      }),
    });
  } catch (_) {}
}

/**
 * Get stats from D1, KV, or In-Memory
 */
async function handleGetStats(request, env) {
  if (env.DB) {
    const knowledgeResults = await env.DB.prepare(
      "SELECT * FROM knowledge_gaps ORDER BY hit_count DESC, last_seen DESC LIMIT 50"
    ).all();
    const criteriaResults = await env.DB.prepare(
      "SELECT * FROM criteria_gaps ORDER BY hit_count DESC, last_seen DESC LIMIT 50"
    ).all();

    return new Response(
      JSON.stringify({
        storage: "d1",
        knowledge_gaps: knowledgeResults.results || [],
        criteria_gaps: criteriaResults.results || [],
      }),
      { headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" } }
    );
  }

  if (env.TELEMETRY_KV) {
    const list = await env.TELEMETRY_KV.list({ prefix: "gap:", limit: 100 });
    const events = [];
    for (const key of list.keys) {
      const val = await env.TELEMETRY_KV.get(key.name);
      if (val) events.push(JSON.parse(val));
    }
    return new Response(JSON.stringify({ storage: "kv", total: events.length, events }), {
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
    });
  }

  return new Response(JSON.stringify({ storage: "memory", total: RECENT_EVENTS.length, events: RECENT_EVENTS }), {
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
  });
}

/**
 * Modern Dashboard UI with D1 Aggregated Analytics
 */
async function handleDashboard(request, env) {
  let knowledgeRows = [];
  let criteriaRows = [];
  let totalKnowledgeHits = 0;
  let totalCriteriaHits = 0;
  let storageType = "In-Memory Buffer";

  if (env.DB) {
    storageType = "Cloudflare D1 (5 GB SQL • 100k Writes/Day)";
    try {
      const kgRes = await env.DB.prepare(
        "SELECT * FROM knowledge_gaps ORDER BY hit_count DESC, last_seen DESC LIMIT 50"
      ).all();
      const cgRes = await env.DB.prepare(
        "SELECT * FROM criteria_gaps ORDER BY hit_count DESC, last_seen DESC LIMIT 50"
      ).all();

      knowledgeRows = kgRes.results || [];
      criteriaRows = cgRes.results || [];

      for (const r of knowledgeRows) totalKnowledgeHits += r.hit_count || 1;
      for (const r of criteriaRows) totalCriteriaHits += r.hit_count || 1;
    } catch (e) {
      console.error("D1 dashboard query error:", e);
    }
  } else if (env.TELEMETRY_KV) {
    storageType = "Cloudflare KV";
    try {
      const list = await env.TELEMETRY_KV.list({ prefix: "gap:", limit: 50 });
      for (const key of list.keys) {
        const val = await env.TELEMETRY_KV.get(key.name);
        if (val) {
          const item = JSON.parse(val);
          if (item.event_type === "knowledge_gap") knowledgeRows.push(item);
          else criteriaRows.push(item);
        }
      }
    } catch (_) {}
  } else {
    for (const item of RECENT_EVENTS) {
      if (item.event_type === "knowledge_gap") knowledgeRows.push(item);
      else criteriaRows.push(item);
    }
  }

  const kgHtml = knowledgeRows.length
    ? knowledgeRows
        .map(
          (r) => `
        <tr>
            <td><strong style="color: #38bdf8;">${escapeHtml(r.query)}</strong></td>
            <td><code>${escapeHtml(r.domain)}</code></td>
            <td><span class="badge badge-knowledge">${escapeHtml(r.gap_type || "empty_result")}</span></td>
            <td><span class="badge" style="background: rgba(244,63,94,0.18); color: #f43f5e; font-weight: bold;">${r.hit_count || 1} lần</span></td>
            <td><span style="color: #94a3b8; font-size: 0.85rem;">${escapeHtml(r.ai_assistant || "CLI")}</span></td>
            <td style="color: #94a3b8; font-size: 0.85rem;">${escapeHtml(String(r.last_seen || r.timestamp || "").slice(0, 19).replace("T", " "))}</td>
        </tr>`
        )
        .join("")
    : `<tr><td colspan="6" style="text-align: center; color: #94a3b8; padding: 2rem;">Chưa có từ khóa tra cứu thiếu nào được ghi nhận.</td></tr>`;

  const cgHtml = criteriaRows.length
    ? criteriaRows
        .map(
          (r) => `
        <tr>
            <td><strong style="color: #f43f5e;">${escapeHtml(r.missing_dimension || (r.missing_dimensions || []).join(", "))}</strong></td>
            <td><code>${escapeHtml(r.platform || (r.platforms || []).join(", "))}</code></td>
            <td><span class="badge badge-criteria">${r.hit_count || 1} lần</span></td>
            <td style="max-width: 320px; font-size: 0.85rem; color: #cbd5e1;">${escapeHtml(r.reason || r.last_notes || "N/A")}</td>
            <td style="color: #94a3b8; font-size: 0.85rem;">${escapeHtml(String(r.last_seen || r.timestamp || "").slice(0, 19).replace("T", " "))}</td>
        </tr>`
        )
        .join("")
    : `<tr><td colspan="5" style="text-align: center; color: #94a3b8; padding: 2rem;">Chưa có tiêu chí đánh giá thiếu nào được ghi nhận.</td></tr>`;

  const html = `<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flutter Pro Max — Telemetry & Knowledge Gaps</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #090d16;
            --card-bg: #111827;
            --border: #1f2937;
            --primary: #38bdf8;
            --accent: #f43f5e;
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Outfit', sans-serif;
            background: var(--bg-dark);
            color: var(--text-main);
            padding: 2.5rem;
            line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2.5rem; flex-wrap: wrap; gap: 1rem; }
        h1 { font-size: 2rem; font-weight: 700; color: var(--primary); letter-spacing: -0.5px; }
        .subtitle { color: var(--text-dim); font-size: 0.95rem; }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.25rem;
            margin-bottom: 2.5rem;
        }
        .metric-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
        }
        .metric-title { font-size: 0.85rem; color: var(--text-dim); text-transform: uppercase; font-weight: 600; }
        .metric-value { font-size: 2.2rem; font-weight: 700; color: var(--text-main); margin-top: 0.5rem; }
        .table-container {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 2.5rem;
        }
        .table-header { padding: 1.25rem 1.5rem; border-bottom: 1px solid var(--border); font-size: 1.15rem; font-weight: 600; display: flex; justify-content: space-between; align-items: center; }
        table { width: 100%; border-collapse: collapse; text-align: left; }
        th, td { padding: 1rem 1.5rem; border-bottom: 1px solid var(--border); font-size: 0.95rem; }
        th { color: var(--text-dim); font-weight: 600; font-size: 0.85rem; text-transform: uppercase; }
        tr:last-child td { border-bottom: none; }
        code { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; background: #1e293b; padding: 0.2rem 0.5rem; border-radius: 4px; color: #38bdf8; }
        .badge {
            display: inline-block;
            padding: 0.25rem 0.7rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .badge-knowledge { background: rgba(56, 189, 248, 0.15); color: #38bdf8; }
        .badge-criteria { background: rgba(244, 63, 94, 0.15); color: #f43f5e; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1>⚡ Flutter Pro Max Telemetry</h1>
                <p class="subtitle">Bảng phân tích từ khóa tra cứu & tiêu chí UI/UX thiếu từ AI Coding Assistants (D1 Aggregated)</p>
            </div>
            <div>
                <span class="badge badge-knowledge" style="font-size: 0.9rem; padding: 0.5rem 1rem;">Storage: ${storageType}</span>
            </div>
        </header>

        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-title">Từ Khóa Tra Cứu Thiếu (Unique)</div>
                <div class="metric-value" style="color: var(--primary);">${knowledgeRows.length} <span style="font-size: 1rem; color: var(--text-dim); font-weight: normal;">(${totalKnowledgeHits} lượt)</span></div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Tiêu Chí UI/UX Thiếu (Unique)</div>
                <div class="metric-value" style="color: var(--accent);">${criteriaRows.length} <span style="font-size: 1rem; color: var(--text-dim); font-weight: normal;">(${totalCriteriaHits} lượt)</span></div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Hạn Mức Miễn Phí (D1 SQL)</div>
                <div class="metric-value" style="font-size: 1.5rem; margin-top: 0.8rem; color: #34d399;">5 GB • 100k writes/ngày</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Rate Limiter</div>
                <div class="metric-value" style="font-size: 1.5rem; margin-top: 0.8rem;">30 req/min/IP</div>
            </div>
        </div>

        <!-- Bảng 1: Knowledge Gaps -->
        <div class="table-container">
            <div class="table-header">
                <span>🔍 Top Từ Khóa Tra Cứu Thiếu (Cần Bổ Sung Dataset CSV)</span>
                <span style="font-size: 0.85rem; color: var(--text-dim); font-weight: normal;">Tự động gộp trùng lặp bằng UPSERT</span>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Từ Khóa Tra Cứu</th>
                        <th>Domain</th>
                        <th>Loại Thiếu</th>
                        <th>Số Lần Xuất Hiện</th>
                        <th>Trợ Lý AI</th>
                        <th>Lần Cuối Thấy</th>
                    </tr>
                </thead>
                <tbody>
                    ${kgHtml}
                </tbody>
            </table>
        </div>

        <!-- Bảng 2: Criteria Gaps -->
        <div class="table-container">
            <div class="table-header">
                <span>📐 Top Tiêu Chí UI/UX Audit Còn Thiếu (Cần Bổ Sung Rubric)</span>
                <span style="font-size: 0.85rem; color: var(--text-dim); font-weight: normal;">Phát hiện từ scorecard.json</span>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Tiêu Chí Thiếu</th>
                        <th>Nền Tảng</th>
                        <th>Số Lần Xuất Hiện</th>
                        <th>Lý Do / Ghi Chú</th>
                        <th>Lần Cuối Thấy</th>
                    </tr>
                </thead>
                <tbody>
                    ${cgHtml}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>`;

  return new Response(html, {
    headers: { "Content-Type": "text/html; charset=utf-8" },
  });
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
