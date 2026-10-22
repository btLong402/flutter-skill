# Changelog

All notable changes to the **Flutter Pro Max** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.10.0] - 2026-10-22

### Added & Upgraded
- **🎨 Nâng Cấp Rubric v2 Cho Mobile & Tablet UX Audit (`mobile-tablet-ux-audit`)**:
  - Mở rộng từ 10 lên **12 tiêu chí đánh giá định lượng** (tổng trọng số 100):
    - Bổ sung `performance_perceived` (Hiệu năng cảm nhận & độ mượt, trọng số 5): đo thời gian khởi động, độ mượt khi cuộn 60fps, bộ nhớ, tải dữ liệu cực trị, thích ứng cửa sổ tablet.
    - Bổ sung `theming_dark_mode` (Theming & Dark mode, trọng số 4): kiểm tra độ tương phản và tính nhất quán dark mode trên toàn bộ màn hình, dialog, bottom sheet, status bar của cả mobile và tablet.
    - Điều chỉnh trọng số cân bằng: `visual_hierarchy_layout` (10), `navigation_ia` (11), `touch_interaction` (11), `accessibility` (14), `adaptive_responsive` (10), `feedback_states_motion` (9), `typography` (7), `color_contrast` (7), `consistency_design_system` (7), `content_microcopy` (5).
  - **Tương thích ngược 100% với Scorecard v1 (10 tiêu chí)**: Tự động phát hiện phiên bản qua `rubric_version` hoặc tập thuộc tính, áp dụng đúng trọng số v1/v2.
  - **Cơ chế Alias thông minh**: Tự động quy đổi tên gọi khác (`tablet_adaptive`, `responsive_tablet`, `dark_mode_theming`, `performance_smoothness`...) về khóa chuẩn của rubric.
  - **Đề xuất khoảng trống Rubric (`rubric_gaps`)**: Cho phép ghi nhận các khía cạnh chuyên biệt vào scorecard mà không làm sai lệch điểm số chuẩn, tự động tổng hợp trong báo cáo Markdown & JSON.
  - **Cảnh báo so sánh chéo phiên bản**: Tự động phát hiện và cảnh báo khi so sánh scorecard giữa hai phiên bản rubric khác nhau (`comparable: false`).
- **🛡️ Cập nhật Rule 23, Rule 01, Rule 20 và CLI Templates**: Đồng bộ quy chuẩn đánh giá 12 tiêu chí trên toàn bộ 16 AI coding assistants.
- **🧪 Mở rộng Test Suite**: Bổ sung unit tests cho Rubric v2, kiểm tra chuẩn xác toàn bộ test suite đạt 100% asset parity.

## [2.9.0] - 2026-10-16

### Added & Upgraded
- **📡 Telemetry & Knowledge Gap Feedback Loop**:
  - Tự động phát hiện khoảng trống tri thức khi tra cứu skill `flutter-pro-max`:
    - Truy vấn không có kết quả (`count == 0`).
    - Tìm kiếm gượng ép / kết quả yếu (`token_coverage < 0.35` hoặc điểm BM25 thấp `< 4.5`).
    - Xung đột công nghệ (stack incompatibility: ví dụ `bloc` + `getx`, `riverpod` + `provider`).
  - Tự động phát hiện thiếu tiêu chí đánh giá trong skill `mobile-tablet-ux-audit` khi người dùng nhập dimension không nằm trong 10 tiêu chí chuẩn.
  - Bổ sung cờ `--report-gap` (`-rg`) trong `search.py` và `score.py` cho phép chủ động gửi phản hồi tri thức/tiêu chí còn thiếu.
- **🔒 Privacy-First Data Sanitization**:
  - Module `telemetry.py` chuẩn hóa zero-dependency bằng thư viện chuẩn Python `urllib.request`.
  - Cơ chế thanh lọc thông tin nhạy cảm trước khi gửi đi:
    - Loại bỏ đường dẫn file nội bộ (Windows/Unix paths).
    - Che địa chỉ Email, mã khóa API/Secret tokens/Bearer tokens, địa chỉ IPv4/IPv6.
    - Cắt ngắn nội dung query tối đa 200 ký tự.
  - Tôn trọng tuyệt đối tiêu chuẩn quyền riêng tư của developer: Tắt hoàn toàn khi có `DO_NOT_TRACK=1` hoặc `FLUTTER_PRO_MAX_TELEMETRY=0`.
  - Fallback lưu trữ cục bộ tại `~/.flutter-pro-max/gaps.jsonl` khi mất mạng hoặc không kết nối được server.
- **☁️ Cloudflare Worker & D1 Database Ingestion**:
  - Endpoint serverless hiệu năng cao `POST /api/telemetry` trên Cloudflare Worker.
  - Lưu trữ cơ sở dữ liệu quan hệ Cloudflare D1 (5 GB dung lượng miễn phí, 100.000 lượt ghi/ngày).
  - Thuật toán tổng hợp gộp UPSERT: cùng một câu truy vấn/tiêu chí thiếu sẽ tự động tăng `hit_count` và cập nhật `last_seen_at` thay vì tạo dòng mới, tối ưu triệt để dung lượng và số lần ghi.
  - Bộ giới hạn tần suất (Rate Limiter) 30 requests/phút/IP và chặn payload quá 10 KB.
  - Tích hợp Webhook thông báo Discord/Telegram và Web Dashboard trực quan hiển thị top tri thức cần bổ sung.
- **⚡ Async Non-Blocking Daemon & Exit Grace Flush**:
  - Gửi dữ liệu trong background daemon thread với timeout ngắn (1.5s).
  - Cơ chế `atexit` graceful flush (1.0s) đảm bảo các tiến trình CLI ngắn hạn không bị dừng đột ngột trước khi hoàn thành gửi gói tin.
- **🔗 NPM Relative Link Fix**:
  - Chuyển toàn bộ liên kết tương đối (`CHANGELOG.md`, `LICENSE`) trong `cli/README.md` sang đường dẫn tuyệt đối GitHub để khắc phục lỗi 404 trên npmjs.com.

## [2.8.0] - 2026-10-15

### Added & Upgraded
- **🎨 Tích hợp Skill mới: Mobile & Tablet UI/UX Audit (`mobile-tablet-ux-audit`)**:
  - Đóng gói trọn vẹn bộ công cụ audit chất lượng UI/UX chuyên sâu vào CLI:
    - `score.py`: Công cụ chấm điểm định lượng (thang 0–100, 10 tiêu chí), hỗ trợ chấm riêng biệt cho Mobile và Tablet, tự động áp trần điểm tới hạn (hard caps: blocker 59, tiêu chí $\le 1.5$ 69, accessibility $< 3$ 79), thuật toán xếp hạng backlog ưu tiên theo $(\text{Severity} \times \text{Reach} \times \text{Weight}) / \text{Effort}$, và so sánh delta phát hiện hồi quy giữa các vòng audit.
    - `contrast.py`: Đo đạc độ tương phản theo chuẩn WCAG 2.x (ngưỡng 4.5:1 text thường, 3.0:1 text lớn và UI), tự động pha màu thông minh (suggest) để gợi ý mã màu đạt chuẩn.
    - Cẩm nang tài liệu tham chiếu: Rubric 10 tiêu chí (`rubric.md`), checklist nền tảng iOS/Android/iPadOS/Foldable (`platform-checks.md`), hướng dẫn trích xuất bằng chứng (`evidence-collection.md`), và playbook sửa nhanh lỗi UI Flutter (`improvement-playbook.md`).
    - Bộ test tự động toàn diện: 41 automated unit tests kiểm tra toàn bộ logic tính điểm, trần điểm, đo màu và toàn vẹn tài nguyên.
- **🧠 23 Modular Rules (Bổ sung Rule 23: UI/UX Audit & Quality Governance)**:
  - `23_mobile_tablet_ux_audit.md`: Quy chuẩn hóa việc kiểm thử giao diện định lượng, nguyên tắc dựa trên bằng chứng (evidence-based), thiết kế riêng biệt cho tablet ($\ge 600\text{dp}$ dùng NavigationRail & List-Detail), và chu trình tự cải thiện khép kín.
- **⚡ Nâng cấp Rule 01: Context-Aware Skill Usage & Fast-Path Routing**:
  - Chuyển đổi từ cơ chế ép buộc cứng nhắc sang phân luồng theo ngữ cảnh (Context-Aware):
    - **Luồng Full-Flight (Bắt buộc dùng skill):** Áp dụng cho tính năng mới (Greenfield), thiết kế kiến trúc, chọn package, audit UI/UX tablet, hoặc tái cấu trúc lớn.
    - **Luồng Fast-Path (Được đi tắt):** Cho phép sửa trực tiếp không cần tra cứu đối với hotfix nhỏ (< 15 dòng), sửa typo text, sửa null-safety, đổi config, hoặc format code.
- **🔄 Nâng cấp Rule 20: Tích hợp UI/UX Audit vào SDLC 8 bước**:
  - Tích hợp kiểm tra tương phản và layout tablet vào Step 3 (Screen & UX Design) và Step 7 (Code Review & UI/UX Self-Audit).
- **🚀 CLI Dual-Skill Auto-Installer**:
  - Lệnh `flutter-pro-max init` tự động cài đặt song song cả 2 skills (`flutter-pro-max` + `mobile-tablet-ux-audit`) và 23 rules cho toàn bộ 16 trợ lý AI (Claude, Antigravity, Cursor, Windsurf, Copilot, Trae, Gemini, Roo Code, v.v.).
- **🧪 Assets Parity & Test Suite Expansion**:
  - Mở rộng bộ kiểm thử tự động lên tổng cộng **85 tests** (bổ sung test parity cho skill UI/UX audit và kiểm tra toàn vẹn 23 rules), đạt tỷ lệ vượt qua 100%.

---

## [2.7.0] - 2026-09-10

### Added & Hardened
- **Production Hardening & Code Sentinel Audit Compliance**: Nâng cấp toàn diện 6 bộ quy tắc cốt lõi dựa trên thực tiễn quét mã nguồn dự án sản xuất (Code Sentinel SAST Audit):
  - **Guaranteed UI Cleanup (`05_error_handling.md`)**: Bắt buộc bọc mọi UI Loader / Dialog trong khối `finally` (`hideLoader()`), chống kẹt màn hình vĩnh viễn khi có ngoại lệ; cấm fake success; bắt buộc có UI Error State kèm nút Thử lại (Retry path) thay vì nuốt lỗi thành Empty State.
  - **Async Gap & Framework Lifecycle (`15_state_lifecycle.md`)**: Thiết lập rào chắn `if (!mounted) return;` trong StatefulWidget và `if (isClosed) return;` trong Controller (GetX/Bloc/Notifier). Chuẩn hóa vòng đời GetX (`onClose()`, cấm tự chế `dispose()`, hủy toàn bộ `Worker` debounce/ever). Cấm triệt để side-effects trong phương thức `build()`.
  - **Bảo mật File I/O & Network Hardening (`08_security.md`)**: Phòng vệ Path Traversal (`path.basename()` + regex sanitize), kiểm tra MIME type whitelist và kích thước file tối đa. Cấm bypass SSL trong WebView (`onReceivedServerTrustAuthRequest`), khóa domain allowlist và scheme https. Chuẩn hóa Log Masking (che token, password, Authorization header).
  - **Chống Re-entrancy & Search Race Condition (`03_interaction_flow.md`)**: Tự động vô hiệu hóa nút bấm khi đang xử lý async (`isSubmitting` guard), chống pop kép trên confirmation dialog. Chuẩn hóa tìm kiếm thời gian thực với debounce (300–500ms) kết hợp `CancelToken` hủy request cũ.
  - **Zero Force-Unwrap & Pure Build (`02_code_quality.md`)**: Cấm tuyệt đối toán tử ép null (`!`) trên Remote Data và dynamic json payload (thay bằng `firstOrNull`, `?.`, `?? fallback`); bắt buộc bảo đảm hàm `build()` thuần khiết (Pure Build Function, không in-place mutate).
  - **Localization SAST Hardening (`22_localization.md`)**: Quy ước tiền tố đặt tên key i18n (`lbl_`, `hint_`, `title_`, `msg_`) chống báo động giả hardcoded secrets trong công cụ quét SAST/CI-CD, kèm hướng dẫn exclude file từ điển.
- **Assets Parity**: Đồng bộ 100% giữa canonical `src/flutter-pro-max/templates/base/rules/` và `cli/assets/templates/base/rules/`.

---

## [2.6.0] - 2026-09-07

### Added
- **22 Modular Rules (Tier 5 Expansion)**: Mở rộng toàn diện hệ thống lên 22 rules:
  - `21_navigation_governance.md`: Chuẩn hóa Declarative Routing (`go_router`), Type-Safe parameters, Auth Redirect Guards và validate Deep Link an toàn.
  - `22_localization.md`: Thiết lập tiêu chuẩn **Zero Hardcoded Strings**, cấm hardcode text trên UI, chuẩn hóa cấu trúc ARB và extension `context.l10n`.
- **Ironclad Compliance Framework**:
  - **Pre-Flight Compliance Block**: Bắt buộc AI phải xuất khối YAML cam kết thẩm định tiêu chuẩn kiến trúc và hard constraints trước khi sinh bất kỳ dòng code Dart nào.
  - **Ngưỡng hành động mềm 200 dòng**: Bắt buộc chủ động phân rã file khi ước tính đạt $\ge 200$ dòng thay vì chờ chạm trần 300 dòng.
- **100% Vietnamese Diacritics Standardization**: Chuẩn hóa toàn bộ 22 rules sang tiếng Việt có dấu chuẩn xác.
- **Context Window Token Optimization**: Tinh chỉnh cấu hình `globs` cho nhóm Rule Google Play Store (`16`, `17`, `18`) giúp tiết kiệm ~1,000 tokens cho mỗi lượt prompt.
- **Production Reference Implementations**: Bổ sung code mẫu thực chiến của `ResilientRetryInterceptor`, Stream Repository và checklist `dispose()`.

---

## [2.5.1] - 2026-09-07

### Added
- **AI-Tailored Gitignore**: Nâng cấp lệnh `flutter-pro-max gitignore` hỗ trợ may đo chính xác cho từng trợ lý AI (`-a <type>`, `--all`) với 16 nền tảng.
- **FVM Auto-Detection in Makefile**: Makefile template tự động nhận diện cấu hình FVM (`.fvmrc`, `.fvm/`) để điều phối `fvm flutter` / `fvm dart`.
- **Unified CI/CD Pipeline**: Tích hợp quy trình kiểm thử hoàn chỉnh (21 unit tests, assets parity, E2E CLI testing) và publish npm tự động.
- **Full Changelog & Documentation**: Chuẩn hóa tài liệu CLI, khôi phục đầy đủ lịch sử phát hành từ v2.0.0.

---

## [2.5.0] - 2026-09-07

### Added
- **Design Dials**: Bổ sung 3 nút điều khiển thiết kế `--variance`, `--motion`, và `--density`.
- **Production Dart Theme Generator**: Hỗ trợ cờ `--export-dart` xuất trực tiếp code Dart hoàn chỉnh với 3-Layer Tokens.
- **Flutter Motion Intelligence**: Bổ sung domain thứ 18 `motion` với cơ sở dữ liệu `flutter-motion.csv`.
- **Closed-Grammar Reasoning Contract**: Tích hợp `reasoning_contract.py` loại bỏ hoàn toàn AI hallucination.
- **Flutter Design Review Subagent & Command**: Ra mắt subagent `@flutter-design-review` và slash command `/flutter-review` với quy trình audit 6 pha.
- **Catalog Governance & Unit Testing**: Tích hợp `catalog-summary.json`, `data-provenance.json` và bộ test suite 9 unit tests bao phủ 100%.
- **Developer Utility Tools**: Bổ sung các lệnh `makefile`, `fastlane`, `gitignore`.

---

## [2.4.5] - 2026-05-14

### Added
- **Development Workflow Rule**: Bổ sung rule `20_development_workflow.md` chuẩn hóa quy trình SDLC 8 bước.
- **Architecture Decision Matrix**: Tích hợp hướng dẫn kiến trúc Greenfield vs Brownfield trong `19_architecture_decision_matrix.md`.
- **Lifecycle & State Enhancements**: Nâng cấp các quy tắc quản lý state & lifecycle linh hoạt theo kiến trúc dự án.

---

## [2.3.3] - 2026-02-26

### Added
- **15 Modular Rules**: Bổ sung các chuẩn mực từ Software Engineering (Resiliency, Offline-First, Graceful Degradation).
- **Cursor MDC Support**: Tự động sinh XML/YAML frontmatter và format `.mdc` khi sử dụng nền tảng Cursor.

---

## [2.3.2] - 2026-02-25

### Changed
- **Rules/Skill Separation**: Tách hoàn toàn Brain (Rules) và Hands (Skill).
- **11 Modular Rules**: Modular Generation ra file riêng lẻ từng logic.
- **Skill Tools-Only**: Skill content chỉ còn search commands + data reference.

---

## [2.3.1] - 2026-02-25

### Added
- **Standalone Rules Generation**: CLI tự động gen rules file riêng biệt khỏi skill.
- **Source of Truth**: Restructure `src/flutter-pro-max/` làm canonical source.
- **3 New Domains**: `performance`, `accessibility`, `ui-reasoning`.

---

## [2.2.0] - 2026-02-02

### Added
- **Flutter AI Rules**: Cập nhật theo [Flutter Official AI Rules](https://docs.flutter.dev/ai/ai-rules).
- **Native-First State Management**: Mặc định ValueNotifier/ChangeNotifier.
- **Platform Limits**: Tạo templates phù hợp với giới hạn từng platform (4k, 10k, full).
- **New Platforms**: Thêm JetBrains AI (Junie), VS Code.

---

## [2.1.0] - 2026-01-27

### Added
- **Type Safety**: Full Python type hints cho Pylance strict mode compatibility.
- **Python 3.10+**: Cập nhật minimum Python version.

---

## [2.0.0] - 2026-01-20

### Initial Release
- Phiên bản public đầu tiên với 14 AI assistant support.
- BM25-based semantic search engine.
