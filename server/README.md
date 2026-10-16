# ☁️ Flutter Pro Max Cloud Telemetry & Feedback Server

Máy chủ thu thập phản hồi tri thức thiếu (**Knowledge Gaps**) và tiêu chí chấm điểm UI/UX thiếu (**Criteria Gaps**) từ các AI Coding Assistants (Claude Code, Cursor, Windsurf, Antigravity, GitHub Copilot,...).

---

## 🚀 Tùy Chọn Triển Khai (3 Phương Án Dễ Dàng)

### 🌟 Cách 1: Cloudflare Workers + D1 Database (Khuyên dùng - 5 GB Free • 100,000 writes/ngày)

Mã nguồn nằm trong thư mục [`server/cloudflare-worker/`](cloudflare-worker/):
- **Cơ chế lưu trữ:** Sử dụng **Cloudflare D1 (Serverless SQLite)** làm kho dữ liệu chính, giải quyết triệt để nút thắt ghi của KV (KV giới hạn 1.000 writes/ngày, còn D1 miễn phí **100.000 writes/ngày** và **5 GB dung lượng**).
- **Kỹ thuật UPSERT Aggregation:** Cùng 1 từ khóa query hoặc tiêu chí lạ chỉ tốn duy nhất 1 dòng trong database; các lần xuất hiện sau chỉ tự động tăng `hit_count = hit_count + 1` và cập nhật `last_seen`. Điều này giúp tiết kiệm tối đa cả dung lượng lưu trữ lẫn hạn mức ghi.

1. Khởi tạo cơ sở dữ liệu D1 (đã tạo sẵn trong repo):
   ```bash
   cd server/cloudflare-worker
   npx wrangler d1 create flutter-pro-max-db
   npx wrangler d1 execute flutter-pro-max-db --remote --file=schema.sql -y
   ```
2. (Tùy chọn) Cấu hình Webhook gửi thông báo tức thì về điện thoại:
   ```bash
   npx wrangler secret put DISCORD_WEBHOOK_URL
   # Hoặc Telegram:
   npx wrangler secret put TELEGRAM_BOT_TOKEN
   npx wrangler secret put TELEGRAM_CHAT_ID
   ```
3. Triển khai:
   ```bash
   npx wrangler deploy
   ```
4. Truy cập Web Dashboard trực quan tại URL của bạn:
   - Dashboard: `https://flutter-pro-max-telemetry.<your-subdomain>.workers.dev`
   - Endpoint: `https://flutter-pro-max-telemetry.<your-subdomain>.workers.dev/api/telemetry`

---

### 🗄️ Cách 2: Supabase (SQL Database & Giao Diện Studio)

Mã nguồn nằm trong thư mục [`server/supabase/`](supabase/):
1. Đăng nhập [Supabase](https://supabase.com) và tạo 1 Project mới miễn phí.
2. Vào **SQL Editor**, dán toàn bộ nội dung từ file [`schema.sql`](supabase/schema.sql) và nhấn **Run**.
3. Bạn đã có sẵn 2 bảng:
   - `knowledge_gaps`: Lưu mọi từ khóa tra cứu thiếu, BM25 score, tỷ lệ token coverage, AI client.
   - `criteria_gaps`: Lưu mọi tiêu chí chấm điểm lạ hoặc thiếu.
   - Views phân tích: `v_top_knowledge_gaps`, `v_top_criteria_gaps` sắp xếp theo số lần xuất hiện nhiều nhất.
4. Lấy REST API Endpoint:
   - URL: `https://<your-project-ref>.supabase.co/rest/v1/knowledge_gaps`
   - Header: `apikey: <your-anon-key>`

---

### 💻 Cách 3: Mock Server Cục Bộ (Dùng Test Ngay Trên Máy Dev)

Chạy trực tiếp micro server Python đi kèm:
```bash
python3 server/mock_server.py --port 8787
```
Mở trình duyệt tại `http://localhost:8787` để xem giao diện Inspector thời gian thực.

---

## ⚙️ Cấu Hình Cho Người Dùng / Trợ Lý AI

Để kích hoạt gửi telemetry từ skill về Cloud Server của bạn:

### Cách 1: Biến Môi Trường (Terminal / `.zshrc` / `.bashrc`)
```bash
export FLUTTER_PRO_MAX_TELEMETRY_ENDPOINT="https://your-server-endpoint/api/telemetry"
```

### Cách 2: File Cấu Hình Toàn Cục (`~/.flutter-pro-max/config.json`)
```json
{
  "endpoint": "https://your-server-endpoint/api/telemetry"
}
```

### Cách 3: Tắt Telemetry (Opt-Out)
Nếu người dùng không muốn gửi telemetry:
```bash
export DO_NOT_TRACK=1
# Hoặc:
export FLUTTER_PRO_MAX_TELEMETRY=0
```

---

## 📡 Các Sự Kiện Được Thu Thập (Payload Schemas)

1. **Knowledge Gap (Tra cứu thiếu):**
   ```json
   {
     "event_type": "knowledge_gap",
     "query": "webrtc live streaming peer to peer",
     "domain": "package",
     "gap_type": "empty_result", // hoặc "weak_match" hoặc "explicit_report"
     "result_count": 0,
     "max_score": 0.0,
     "token_coverage": 0.0,
     "client": {
       "version": "2.8.0",
       "os": "darwin",
       "ai_assistant": "cursor"
     },
     "timestamp": "2026-10-16T09:00:00Z"
   }
   ```

2. **Criteria Gap (Tiêu chí chấm điểm thiếu):**
   ```json
   {
     "event_type": "criteria_gap",
     "missing_dimensions": ["haptic_feedback", "biometric_auth"],
     "platforms": ["mobile", "tablet"],
     "gap_type": "unrecognized_dimension", // hoặc "explicit_report"
     "reason": "Phát hiện 2 tiêu chí chưa có trong rubric 10 chuẩn",
     "client": {
       "version": "2.8.0",
       "os": "darwin",
       "ai_assistant": "claude"
     },
     "timestamp": "2026-10-16T09:00:00Z"
   }
   ```
