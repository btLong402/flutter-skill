---
description: Quy trình phát triển tính năng (SDLC) từ Requirement đến Optimization
globs: *
---

# Rule: Development Workflow

> Kích hoạt: Khi bắt đầu phát triển một tính năng mới (Feature) hoặc Module mới.

Luôn tuân thủ quy trình 8 bước sau đây để đảm bảo chất lượng phần mềm:

## 1. Requirement
- Tiếp nhận và làm rõ yêu cầu từ người dùng.
- Xác định mục tiêu, phạm vi (scope) và các ràng buộc của tính năng.
- Đầu ra: Danh sách các yêu cầu (User Stories/Requirements) được hiểu rõ.

## 2. Feature Analysis
- Phân tích các thành phần cần thiết để thực hiện yêu cầu.
- Xác định các edge cases, logic nghiệp vụ phức tạp.
- Tìm kiếm các patterns hoặc packages liên quan (sử dụng `search.py`).
- Đầu ra: Tài liệu phân tích hoặc ghi chú về giải pháp.

## 3. Screen Design (nếu có UI)
- Thiết kế layout, UI components dựa trên Design Tokens và App Consistency (Rule 04).
- Đảm bảo tính Accessibility (Rule 11) và UX guidelines.
- Đầu ra: Mô tả cấu trúc Widget hoặc mã giả cho giao diện.

## 4. Architecture Design
- Lựa chọn kiến trúc (thường là Clean Architecture - Rule 19).
- Phân chia các layer: Data, Domain, Presentation.
- Xác định State Management strategy (Rule 09).
- Đầu ra: Sơ đồ hoặc mô tả cấu trúc thư mục và các class chính.

## 5. Code Generation
- Thực hiện viết code logic và UI.
- Tuân thủ Hard Constraints (Rule 02) và Naming Conventions (Rule 10).
- Sử dụng `dart_format` và `analyze_files` liên tục.
- Đầu ra: Mã nguồn hoàn thiện.

## 6. Unit Tests
- Viết Unit Tests cho Domain logic (Rule 06).
- Viết Widget Tests cho các UI components quan trọng.
- Đảm bảo code coverage đạt yêu cầu.
- Đầu ra: Bộ test suite xanh (passed).

## 7. Code Review
- Tự rà soát lại code (Self-review) theo quy trình ABCR (Rule 03).
- Kiểm tra các lỗi tiềm ẩn, bảo mật (Rule 08) và xử lý lỗi (Rule 05).
- Đầu ra: Code đã được tối ưu hóa về mặt cấu trúc và độ sạch.

## 8. Performance Optimization
- Kiểm tra hiệu suất (Rule 07): `const` widgets, `ListView.builder`, memory leaks.
- Tối ưu hóa Network Resiliency (Rule 12) và Offline-First (Rule 13) nếu cần.
- Đầu ra: Ứng dụng chạy mượt mà, tối ưu tài nguyên.

---

> 💡 **Ghi nhớ:** Không nhảy bước. Mỗi bước hoàn thành là nền tảng vững chắc cho bước tiếp theo.
