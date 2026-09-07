---
description: Ma trận Quyết định Kiến trúc cho Dự án Mới (Greenfield) và Dự án Hiện Hữu (Brownfield)
globs: lib/**/*.dart, test/**/*.dart
---

# Rule: Architecture Decision Matrix

> Kích hoạt: Khi bắt đầu bất kỳ nhiệm vụ nào (Feature mới, sửa bug, refactor hoặc thiết kế module)

## 1. Mục Tiêu Cốt Tử

1. **Mặc định sử dụng Clean Architecture** cho toàn bộ mã nguồn mới.
2. **Bảo tồn và tôn trọng kiến trúc hiện hữu** của dự án cũ (MVC / MVVM / Layered).
3. **Tuyệt đối không ép buộc di chuyển kiến trúc (No Forced Migration)** khi chưa có chỉ định rõ ràng từ người dùng.

---

## 2. Bước 1: Phân Loại Loại Nhiệm Vụ (Task Type)

Trước khi viết bất kỳ dòng code nào, bắt buộc phải xếp yêu cầu vào đúng 1 trong 3 nhóm:

1. **Greenfield (Dự án mới / Module mới):** Module hoặc tính năng mới hoàn toàn, không chịu ràng buộc bởi mã nguồn cũ.
2. **Brownfield Feature (Thêm tính năng trên dự án cũ):** Mở rộng hoặc tích hợp chức năng mới trên nền một module đã hoạt động.
3. **Brownfield Hotfix (Vá lỗi khẩn cấp):** Sửa lỗi nhanh, ưu tiên tính an toàn tuyệt đối, không gây hồi quy (No regression).

---

## 3. Bước 2: Ma Trận Quyết Định Kiến Trúc (Decision Matrix)

| Loại nhiệm vụ | Chiến lược Kiến trúc (Architecture Strategy) | Chiến lược State (State Strategy) | Phạm vi Tái cấu trúc (Refactor Scope) |
| :--- | :--- | :--- | :--- |
| **Greenfield** | **Bắt buộc Clean Architecture** (Domain $\rightarrow$ Data $\rightarrow$ Presentation) | **Native-First** (ValueNotifier $\rightarrow$ ChangeNotifier) trừ khi được yêu cầu | Được phép tổ chức thư mục chuẩn hóa Clean từ đầu |
| **Brownfield Feature** | **Tuân thủ kiến trúc hiện hữu của module** (Không tự ý đổi framework lớn) | **Giữ nguyên stack state của module** (Provider giữ Provider, Bloc giữ Bloc) | Chỉ refactor tăng dần (incremental) trong phạm vi file/feature bị đụng tới |
| **Brownfield Hotfix** | **Vá đúng điểm rơi**, tối thiểu hóa tác động | **Không thay đổi framework state** | Không refactor mở rộng; chỉ tách nhỏ nếu cần thiết để fix an toàn |

---

## 4. Bước 3: Bốn Nguyên Tắc Bất Di Bất Dịch

1. **Không Tự Ý Di Cư (No Forced Migration):** CẤM tự ý chuyển đổi `MVC -> Clean Architecture`, `Bloc -> Riverpod`, `Provider -> Bloc` hoặc ngược lại.
2. **Không Tạo Thêm Nợ (No New Debt):** Dù đang theo kiến trúc nào, vẫn phải tuân thủ nghiêm ngặt Hard Constraints của Rule 02 (Cấm God Class, Cấm God File $>300$ dòng, Cấm rò rỉ logic).
3. **Tái Cấu Trúc Tăng Dần (Incremental Refactor):** Mỗi lần chạm vào file cũ là một cơ hội dọn dẹp một phần nợ kỹ thuật nhỏ; tuyệt đối không "đại phẫu" toàn bộ hệ thống khi không được yêu cầu.
4. **Nhất Quán Là Trên Hết (Consistency First):** Code mới viết vào module cũ phải nhìn giống như được viết cùng một phong cách với module đó.

---

## 5. Bảng Ánh Xạ Vị Trí Đặt Business Logic

| Hiện trạng của Module | Nơi đặt Business Logic ưu tiên | Nơi gọi API / DB ưu tiên |
| :--- | :--- | :--- |
| **Clean Architecture** | `UseCase` $\rightarrow$ `Domain Service` | `RemoteDataSource` $\rightarrow$ `Repository` |
| **MVC** | `Controller` $\rightarrow$ `Service` | `Service` hoặc Data layer hiện có |
| **MVVM** | `ViewModel` $\rightarrow$ `Repository` | `Repository` $\rightarrow$ `ApiClient` |
| **Layered cũ** | Tách riêng file logic, không để trong UI | Data layer hiện hữu |

---

## 6. Điều Kiện Đề Xuất Đại Phẫu Kiến Trúc (Migration)

AI **CHỈ ĐƯỢC PHÉP** đề xuất tái cấu trúc toàn diện khi hội đủ ít nhất 1 điều kiện sau:
1. Người dùng yêu cầu bằng văn bản rõ ràng: *"Hãy migrate module này sang Clean Architecture"*.
2. Chi phí duy trì vượt ngưỡng chịu đựng (Lỗi lặp lại liên tục, việc thêm code mới gây vỡ nhiều màn hình khác, không thể viết test).

---

## 7. Khung Xuất Bắt Buộc (Mandatory Output)

Mọi phản hồi lập trình phải mở đầu bằng 4 dòng sau:

```yaml
Task Type: <Greenfield | Brownfield Feature | Brownfield Hotfix>
Architecture Strategy: <Clean default | Follow existing architecture>
State Strategy: <stack được chọn cho module>
Refactor Scope: <minimal | incremental | structured>
```
