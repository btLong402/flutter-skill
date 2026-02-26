# Rule: Code Quality & Hard Constraints

> Kích hoạt: Khi tạo/chỉnh sửa files `.dart`

## Think-Before-Code Protocol

**TRƯỚC KHI tạo file mới hoặc viết widget**, bạn PHẢI trả lời 5 câu hỏi:

1. **File này có vượt 300 dòng không?** → Nếu có khả năng, TÁCH ngay từ đầu
2. **Widget/Component này đã tồn tại chưa?** → Search codebase trước, REUSE nếu có
3. **Widget này có thể reuse cho nơi khác không?** → Nếu có, đặt vào `core/widgets/` hoặc shared folder
4. **Logic này thuộc layer nào?** → UI / Domain / Data — KHÔNG được trộn layers
5. **Có widget/hàm nào đang lặp logic tương tự không?** → Nếu có, REFACTOR thành shared component

## Hard Constraints (Vùng Cấm)

### 🚫 NO GOD CLASSES

| Indicator | Threshold | Action |
|-----------|-----------|--------|
| Public methods | > 10 methods | 🔴 **REFACTOR** |
| Lines of logic | > 200 lines | 🔴 **REFACTOR** |
| Mixed concerns | Logic + UI + DB | 🔴 **TÁCH NGAY** |

### 🚫 NO GOD FILES

| Rule | Limit |
|------|-------|
| **File size** | ≤ 300 dòng (tối đa 500) |
| **Classes per file** | 1 Class chính duy nhất |

### 🚫 NO LOGIC LEAKAGE

| Violation | Correct Layer |
|-----------|---------------|
| Business Logic trong Widget | ➜ Move to `UseCase` / `Service` |
| SQL/Query trong Controller | ➜ Move to `Repository` |
| API calls trong UI | ➜ Move to `DataSource` |

## Nguyên tắc cứng

| ❌ Sai | ✅ Đúng |
|--------|---------|
| Tạo `UserCard` mới khi đã có `ProfileCard` tương tự | Mở rộng `ProfileCard` hoặc extract shared `BaseCard` |
| Screen 500+ dòng | Tách thành `_HeaderSection`, `_ContentBody`, `_ActionBar` |
| 3 screens cùng copy-paste search bar | Tạo `SearchableScaffold` dùng chung |
| Hardcode colors, padding, font sizes | Dùng `Theme.of(context)`, design tokens, constants |
| Business logic trong Widget `build()` | Tách vào UseCase / Service / Provider |

> 🔴 **REUSE > CREATE.** Không bao giờ tạo file mới mà không kiểm tra codebase hiện tại trước.