---
description: Tiêu chuẩn Chất lượng Mã nguồn, Khung Pre-Flight Compliance, Ngưỡng Cấm Tuyệt Đối
globs: lib/**/*.dart
---

# Rule: Code Quality & Hard Constraints

> Kích hoạt: Khi tạo mới hoặc chỉnh sửa bất kỳ file `.dart` nào

## 1. Chính sách Kiến trúc (Architecture Policy)

- **Mặc định (Greenfield / Module mới):** Bắt buộc tuân thủ **Clean Architecture** (UI/Presentation $\rightarrow$ Domain $\rightarrow$ Data).
- **Bảo trì dự án cũ (Brownfield):** Tuyệt đối tôn trọng kiến trúc hiện hữu (MVC / MVVM / Layered), **KHÔNG** tự ý ép đổi framework state hoặc kiến trúc nếu người dùng không yêu cầu.
- **Nguyên tắc bất biến:** Không trộn lẫn tầng trách nhiệm (Separation of Concerns), không rò rỉ logic (No Logic Leakage), chỉ tái cấu trúc tăng dần theo từng phạm vi tính năng.

---

## 2. Khung Bắt Buộc: Pre-Flight Compliance Block

> 🔴 **RÀO CHẮN BẮT BUỘC:** TRƯỚC KHI sinh bất kỳ khối mã nguồn Dart nào, AI **BẮT BUỘC PHẢI XUẤT KHỐI YAML NÀY** ở đầu phản hồi.  
> Nếu thiếu khối này hoặc tự ý sinh mã ngay mà không lập kế hoạch, phản hồi bị coi là **VI PHẠM QUY TẮC NGHIÊM TRỌNG**.

```yaml
# PRE-FLIGHT COMPLIANCE CHECK
task_type: Greenfield | Brownfield Feature | Brownfield Hotfix
architecture_strategy: Clean default | Follow existing architecture
state_strategy: ValueNotifier | ChangeNotifier | Provider | (Riverpod/Bloc nếu có yêu cầu)
planned_files:
  - path: lib/.../file_name.dart (Ước tính: < 200 dòng)
hard_constraints_verified:
  will_exceed_300_lines: NO (Đã chủ động tách sub-widgets nếu > 200 dòng)
  god_class_prevented: YES (Tối đa 10 public methods, 1 class chính/file)
  logic_leakage_prevented: YES (Không gọi API / SQL trực tiếp trong Widget)
  theme_tokens_used: YES (Dùng Theme.of(context) & AppSpacing, không hardcode)
```

---

## 3. Think-Before-Code: 5 Câu hỏi Sống Còn

Trước khi tạo file mới hoặc viết Widget, bạn **PHẢI** tự vấn và trả lời:

1. **File này có nguy cơ vượt 200 dòng không?** $\rightarrow$ Nếu có, **TÁCH FILE NGAY TỪ ĐẦU**, không viết dồn rồi mới tách.
2. **Widget / Component này đã tồn tại trong codebase chưa?** $\rightarrow$ Tra cứu codebase trước, **TÁI SỬ DỤNG (REUSE)** nếu đã có.
3. **Widget này có thể dùng chung cho nơi khác không?** $\rightarrow$ Nếu có, đặt vào `core/widgets/` hoặc thư mục shared.
4. **Logic này thuộc layer nào?** $\rightarrow$ UI / Domain / Data — **TUYỆT ĐỐI KHÔNG** trộn lẫn layers.
5. **Có đoạn logic / hàm nào đang lặp lại không?** $\rightarrow$ Trích xuất thành shared component hoặc utility function.

---

## 4. Ngưỡng Cấm Tuyệt Đối (Hard Constraints)

### 🚫 1. CẤM GOD CLASSES

| Chỉ số kiểm tra | Ngưỡng vi phạm | Hành động bắt buộc |
| :--- | :--- | :--- |
| **Public methods** | $> 10$ methods | 🔴 **TÁCH CLASS NGAY** (Dùng Facade / Delegate) |
| **Số dòng logic nghiệp vụ** | $> 200$ dòng | 🔴 **CHUYỂN VÀO USECASE / SERVICE** |
| **Trộn lẫn trách nhiệm** | Logic + UI + DB / API trong 1 class | 🔴 **BÓC TÁCH TẦNG TRÁCH NHIỆM NGAY LẬP TỨC** |

### 🚫 2. CẤM GOD FILES (Quy tắc Ngưỡng 200/300)

| Quy tắc | Giới hạn | Hành vi cưỡng chế |
| :--- | :--- | :--- |
| **Ngưỡng hành động mềm** | **$\ge 200$ dòng** | ⚠️ **BẮT BUỘC TÁCH SUB-WIDGETS RA FILE RIÊNG**. Tuyệt đối không chờ chạm 300 dòng mới xử lý. |
| **Ngưỡng trần cứng** | **$\le 300$ dòng** | 🔴 File không được phép vượt quá 300 dòng (Trừ generated code `.g.dart`). |
| **Classes per file** | **Đúng 1 class chính** | Mỗi file chỉ chứa 1 class public chính (có thể kèm private helper widgets nếu ngắn). |

### 🚫 3. CẤM RÒ RỈ LOGIC (NO LOGIC LEAKAGE)

| Hành vi vi phạm | Giải pháp Clean Architecture | Giải pháp Legacy (MVC / MVVM) |
| :--- | :--- | :--- |
| Business Logic nằm trong Widget / View | ➜ Chuyển vào `UseCase` / `Domain Service` | ➜ Chuyển vào `Controller` / `ViewModel` |
| Viết câu lệnh SQL / Query trong Controller | ➜ Chuyển vào `Repository` / `Dao` | ➜ Chuyển vào data layer hiện hữu |
| Gọi trực tiếp API (Dio / Http) trong UI | ➜ Chuyển vào `RemoteDataSource` | ➜ Chuyển vào `Service` / `Controller` |

---

## 5. Bảng Đối Chiếu Tử Huyệt: Sai vs Đúng

| ❌ Vi phạm nghiêm trọng (Bị từ chối) | ✅ Chuẩn mực bắt buộc (Được chấp thuận) |
| :--- | :--- |
| Tạo `UserCard` mới khi codebase đã có `ProfileCard` | Mở rộng `ProfileCard` hoặc trích xuất shared `BaseCard` |
| Viết Screen dồn 400 dòng trong 1 file | Tách thành `login_header.dart`, `login_form.dart`, `login_social_buttons.dart` |
| `initState()` gọi thẳng API `dio.get('/users')` | `notifier.loadUser()` thông qua UseCase / Controller |
| Hardcode màu: `Color(0xFF1E88E5)` | Dùng token: `Theme.of(context).colorScheme.primary` |
| Hardcode khoảng cách: `SizedBox(height: 16)` | Dùng spacing token: `SizedBox(height: AppSpacing.md)` |
| `catch (e) {}` (Nuốt lỗi im lặng) | `Result.failure(AppError.from(e))` kèm `developer.log` |

> 🔴 **KHẮC CỐT GHI TÂM:** **REUSE > CREATE**. Không bao giờ sinh file mới mà không kiểm tra codebase hiện tại trước.