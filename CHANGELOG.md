# Changelog

All notable changes to the **Flutter Pro Max** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
