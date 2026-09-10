# Changelog - Flutter Pro Max CLI

All notable changes to the **flutter-pro-max-cli** package will be documented in this file.

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
- **22 Modular Rules (Tier 5 Expansion)**: Mở rộng hệ thống lên 22 rules với Tier 5:
  - `21_navigation_governance.md`: Chuẩn hóa Declarative Routing (`go_router`), type-safe parameters, Auth Redirect Guards và kiểm tra Deep Link an toàn.
  - `22_localization.md`: Thiết lập tiêu chuẩn cấm hardcode chuỗi text trên UI (**Zero Hardcoded Strings**), chuẩn hóa định dạng ARB và extension `context.l10n`.
- **Ironclad Compliance Framework (Ép buộc AI tuân thủ Rules)**:
  - **Pre-Flight Compliance Block**: Bắt buộc AI phải xuất khối YAML cam kết thẩm định tiêu chuẩn kiến trúc và hard constraints trước khi sinh bất kỳ dòng code Dart nào.
  - **Ngưỡng hành động mềm 200 dòng**: Bắt buộc chủ động phân rã file khi ước tính đạt $\ge 200$ dòng thay vì chờ chạm trần 300 dòng.
- **100% Vietnamese Diacritics Standardization**: Chuẩn hóa toàn bộ 22 rules sang tiếng Việt có dấu đầy đủ, tối ưu hóa quá trình phân giải token của BPE Tokenizer, ngăn ngừa hallucination và hiểu sai chỉ thị.
- **Context Window Token Optimization**: Tinh chỉnh cấu hình `globs` cho nhóm Rule Google Play Store (`16`, `17`, `18`) giúp tiết kiệm ~1,000 tokens cho mỗi lượt prompt lập trình thông thường.
- **Production Reference Implementations**: Bổ sung code mẫu thực chiến của `ResilientRetryInterceptor`, Stream Repository và checklist `dispose()`.

---

## [2.5.1] - 2026-09-07

### Added
- **AI-Tailored Gitignore**: Hỗ trợ may đo quy tắc `.gitignore` riêng biệt cho 16 nền tảng trợ lý AI (`-a <type>`, `--all`). Tự động phát hiện AI đang sử dụng và chèn chính xác các thư mục như `.agents/`, `.claude/skills/`, `.cursor/rules/`, `.shared/`, v.v.
- **FVM Auto-Detection in Makefile**: Makefile template tự động kiểm tra sự tồn tại của `.fvmrc` hoặc `.fvm/` để tự điều phối giữa `fvm flutter` / `fvm dart` và Flutter SDK hệ thống.
- **Unified CI/CD Pipeline**: Đồng bộ hóa CI/CD, kiểm thử 21 unit tests, assets parity và CLI E2E tests trước khi publish lên npm registry.
- **Restored Full Changelog**: Khôi phục và chuẩn hóa toàn bộ lịch sử thay đổi từ v2.0.0 đến v2.5.1.

---

## [2.5.0] - 2026-09-07

### Added
- **Developer Utility Tools**: Bổ sung bộ 3 công cụ tự động hóa `makefile` (kèm auto-detect FVM), `fastlane` (CI/CD Android & iOS) và `gitignore` (may đo riêng cho từng AI trợ lý).
- **AI-specific Gitignore**: Tự động nhận diện trợ lý AI (`antigravity`, `claude`, `cursor`, `copilot`...) để ngăn ngừa rò rỉ file skill/rules lên repository.
- **Design Dials**: 3 nút điều khiển `--variance`, `--motion`, `--density` tinh chỉnh biên độ sáng tạo, hoạt họa và spacing.
- **Production Dart Theme Generator**: Tùy chọn `--export-dart` xuất trực tiếp `app_theme.dart` chuẩn Material 3 với 3-Layer Tokens.
- **Flutter Motion Intelligence**: Bổ sung domain thứ 18 `motion` với cơ sở dữ liệu `flutter-motion.csv`.
- **Closed-Grammar Reasoning Contract**: Tích hợp `reasoning_contract.py` loại bỏ hoàn toàn AI hallucination.
- **Flutter Design Review Subagent & Command**: Ra mắt subagent `@flutter-design-review` và slash command `/flutter-review` với quy trình audit 6 pha.
- **20 Modular Rules**: Cập nhật chuẩn hóa đủ 20 rules với `20_development_workflow.md`.

---

## [2.4.5] - 2026-05-14

### Added
- **Development Workflow Rule**: Bổ sung rule 20 chuẩn hóa quy trình SDLC 8 bước.
- **Architecture Decision Matrix**: Tích hợp hướng dẫn kiến trúc Greenfield vs Brownfield.

---

## [2.3.0] - 2026-02-06

### Added
- **VS Code 1.109 Support**: GitHub Copilot và VS Code sử dụng `.github/skills/` format.
- **Breaking Change**: Copilot/VS Code chuyển từ prompts/instructions sang Skills.
- **Full Install**: Copilot và VS Code nay sử dụng full template (~15KB) thay vì mini.

---

## [2.2.0] - 2026-02-02

### Added
- **Flutter AI Rules**: Cập nhật theo [Flutter Official AI Rules](https://docs.flutter.dev/ai/ai-rules).
- **Platform Limits**: Tạo templates phù hợp với giới hạn từng platform (4k, 10k, full).
- **New Platforms**: JetBrains AI (Junie), VS Code.
- **Native-First State**: ValueNotifier/ChangeNotifier mặc định.

---

## [2.1.0] - 2026-01-27

### Added
- **Type Safety**: Full Python type hints cho Pylance strict mode.
- **Python 3.10+**: Minimum Python version updated.
- **Code Quality**: Xóa unused imports, fix linter warnings.

---

## [2.0.0] - 2026-01-20

### Initial Release
- Phiên bản public đầu tiên với 14 AI assistant support.
- BM25-based semantic search engine.
