---
description: Quy trình Phát triển Tính năng (SDLC) 8 Bước từ Yêu cầu đến Tối ưu hóa
globs: *
---

# Rule: Development Workflow (8-Step SDLC)

> Kích hoạt: Khi bắt đầu phát triển một tính năng mới (Feature) hoặc Module mới

Luôn tuân thủ quy trình 8 bước tiêu chuẩn công nghiệp sau đây để đảm bảo phần mềm chất lượng cao:

---

## 1. Requirement (Làm rõ yêu cầu)
- Tiếp nhận và làm rõ yêu cầu từ người dùng; xác định rõ mục tiêu kinh doanh.
- Xác định phạm vi (Scope) và các ràng buộc kỹ thuật.
- **Đầu ra:** Danh sách các yêu cầu cụ thể (Acceptance Criteria / User Stories).

## 2. Feature Analysis (Phân tích tính năng)
- Phân tích các thành phần cần thiết; xác định các trường hợp biên (Edge cases).
- Tra cứu thư viện và kiến trúc thông qua công cụ tìm kiếm: `python3 search.py` (Rule 01).
- **Đầu ra:** Bản phác thảo giải pháp kỹ thuật và danh sách packages phù hợp.

## 3. Screen & UX Design (Thiết kế giao diện nếu có UI)
- Thiết kế layout, UI components dựa trên Design Tokens và App Consistency (Rule 04).
- Đảm bảo tính tiếp cận Accessibility (Rule 11), chuẩn hóa Navigation (Rule 21) và Đa ngôn ngữ (Rule 22).
- **Đầu ra:** Cấu trúc phân rã Widget dạng cây.

## 4. Architecture Design (Thiết kế kiến trúc)
- Phân loại task theo **Architecture Decision Matrix** (Rule 19): Greenfield vs Brownfield.
- Xác định chiến lược State Management theo triết lý **Native-First** (Rule 09).
- Phân định các tầng: Presentation, Domain, Data (Clean Architecture).
- **Đầu ra:** Mô tả cấu trúc thư mục và các class chính.

## 5. Code Generation (Sinh mã nguồn có rào chắn)
- **BẮT BUỘC:** Khởi đầu bằng khối **Pre-Flight Compliance Block** (Rule 02 & Rule 03).
- Tuân thủ **Hard Constraints** (Rule 02): Ngưỡng mềm $\ge 200$ dòng bắt buộc tách file, trần cứng $\le 300$ dòng, tối đa 10 public methods.
- Tuân thủ Naming Conventions (Rule 10) và xử lý lỗi không bao giờ fail im lặng (Rule 05).
- Thường xuyên chạy `dart format .` và `flutter analyze .`.
- **Đầu ra:** Mã nguồn chuẩn mực, không rò rỉ logic.

## 6. Unit & Widget Tests (Kiểm thử tự động)
- Viết Unit Tests cho UseCase / Domain logic và Repository (Rule 06).
- Viết Widget Tests cho các luồng form, validation và trạng thái quan trọng.
- Khi sửa bug: Bắt buộc viết test tái hiện lỗi (Reproduce test) trước khi fix.
- **Đầu ra:** Bộ test suite chạy thành công 100% (Passed).

## 7. Code Review & Self-Audit (Tự rà soát)
- Tự rà soát lại mã nguồn theo chu trình **ABCR** (Audit - Block - Critique/Refactor - Explain - Rule 03).
- Kiểm tra các lỗ hổng bảo mật (Rule 08) và khả năng xử lý rớt mạng (Rule 12).
- **Đầu ra:** Mã nguồn sạch, không nợ kỹ thuật.

## 8. Performance & Lifecycle Optimization (Tối ưu hóa)
- Kiểm tra hiệu suất (Rule 07): `const` constructor, `ListView.builder` phân trang, tránh chạy tác vụ nặng trên UI thread.
- Kiểm tra giải phóng bộ nhớ (Rule 15): Gọi `dispose()` đầy đủ cho controllers và subscriptions.
- Đảm bảo cơ chế Offline-First (Rule 13) và Fallback UI thanh lịch (Rule 14).
- **Đầu ra:** Ứng dụng mượt mà, sẵn sàng đóng gói và phát hành.

---

> 💡 **GHI NHỚ CỐT TỬ:** Tuyệt đối không nhảy bước. Mỗi bước là bệ phóng an toàn cho bước tiếp theo.
