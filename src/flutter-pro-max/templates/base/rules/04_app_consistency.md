# Rule: App Consistency

> Kích hoạt: Khi tạo UI, thêm screen, hoặc chỉnh sửa widget

## Nguyên tắc: Mọi thứ phải nhất quán

**TRƯỚC KHI viết UI code**, bạn PHẢI kiểm tra các pattern hiện có trong project để đảm bảo consistency.

## 1. Design Tokens — Dùng chung, không hardcode

| ❌ Sai | ✅ Đúng |
|--------|---------|
| `Color(0xFF1A73E8)` | `Theme.of(context).colorScheme.primary` |
| `EdgeInsets.all(16)` | `EdgeInsets.all(AppSpacing.md)` hoặc constant |
| `TextStyle(fontSize: 14)` | `Theme.of(context).textTheme.bodyMedium` |
| `BorderRadius.circular(8)` | `BorderRadius.circular(AppRadius.sm)` |
| `Duration(milliseconds: 300)` | `AppDurations.normal` |

## 2. Widget Patterns — Copy style từ existing screens

**TRƯỚC KHI tạo screen mới:**

1. Tìm screen tương tự trong codebase (list, detail, form, dashboard)
2. Sao chép cấu trúc, spacing, và layout pattern
3. Dùng cùng widget wrappers (Scaffold, AppBar style, padding)

| Element | Quy tắc |
|---------|---------|
| **AppBar** | Dùng chung 1 style/component cho toàn app |
| **Empty States** | Dùng chung widget, không tạo mới mỗi screen |
| **Loading States** | Dùng chung shimmer/skeleton, không mỗi chỗ 1 kiểu |
| **Error States** | Dùng chung error widget với retry action |
| **List Items** | Cùng padding, divider style, tap behavior |
| **Forms** | Cùng validation style, field spacing, button placement |
| **Dialogs** | Cùng shape, padding, button alignment |

## 3. Navigation & Transitions

- Dùng chung transition animations (không mỗi screen 1 kiểu)
- Consistent back button behavior
- Cùng pattern cho bottom sheets, modals, popups

## 4. Spacing System

Định nghĩa và tuân thủ spacing scale:

```dart
// ✅ Dùng constants
abstract class AppSpacing {
  static const double xs = 4;
  static const double sm = 8;
  static const double md = 16;
  static const double lg = 24;
  static const double xl = 32;
}
```

> 🔴 **Khi có nghi ngờ:** Mở screen hiện tại có cùng chức năng → copy exact spacing và layout pattern. **Không sáng tạo riêng.**
