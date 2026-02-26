# Rule: Accessibility

> Kích hoạt: Khi tạo UI, interactive elements, hoặc form inputs

## Nguyên tắc: App phải dùng được cho MỌI NGƯỜI

### Bắt buộc cho mọi widget

| Requirement | Standard | Cách check |
|-------------|----------|------------|
| **Contrast** | Minimum 4.5:1 cho text | Dùng contrast checker tool |
| **Large Text** | Minimum 3:1 (18pt hoặc 14pt bold) | Visual check |
| **Touch Target** | Minimum 48x48dp | `SizedBox` wrapper nếu cần |
| **Semantics** | Label tất cả interactive elements | `Semantics()` widget |
| **Dynamic Scaling** | Hỗ trợ lên đến 200% font size | Test với `textScaleFactor` |

### Code Patterns

```dart
// ✅ Semantics cho interactive elements
Semantics(
  label: 'Xóa sản phẩm khỏi giỏ hàng',
  button: true,
  child: IconButton(
    icon: const Icon(Icons.delete),
    onPressed: onDelete,
  ),
);

// ✅ Form field accessible
TextFormField(
  decoration: const InputDecoration(
    labelText: 'Email', // Screen reader đọc được
    hintText: 'example@email.com',
  ),
);

// ✅ Image có description
Image.network(
  url,
  semanticLabel: 'Ảnh đại diện của người dùng',
);
```

### Checklist

| Element | Kiểm tra |
|---------|----------|
| Buttons/Icons | Có `tooltip` hoặc `Semantics.label` |
| Images | Có `semanticLabel` |
| Forms | Có `labelText`, không chỉ `hintText` |
| Alerts/Dialogs | Có title mô tả rõ |
| Navigation | Focus order hợp lý |
| Colors | Không dùng màu là cách duy nhất truyền thông tin |

> 🔴 **Mỗi `IconButton` PHẢI có `tooltip`.** Mỗi `Image` PHẢI có `semanticLabel`.