# Flutter Pro Max — Agent Rules

> Các rules này được tự động generate bởi `flutter-pro-max-cli`.
> Chúng là project-level rules, TÁCH BIỆT khỏi skill content.

---

## Rule 1: Tự động sử dụng Skill

**TRƯỚC KHI viết code Flutter**, bạn PHẢI tự động sử dụng skill để lấy knowledge phù hợp. Không được bỏ qua bước này.

| Tình huống | Domains cần search |
|------------|-------------------|
| Tạo UI/Screen mới | `style`, `pattern`, `color`, `typography`, `landing` |
| Chọn package/thư viện | `package` (kèm `--stack` filter nếu có) |
| Thiết kế kiến trúc | `architect`, `pattern` |
| Tối ưu performance | `performance` |
| Accessibility | `accessibility` |
| Không chắc UI style | Dùng `--design-system` để generate design system |

**Workflow bắt buộc:**

```
User request → Search skill (≥2 domains) → Đọc kết quả → Áp dụng vào code
```

> ⚠️ Viết code Flutter mà không tham khảo skill trước = thiếu context = code chất lượng thấp.

---

## Rule 2: Think-Before-Code Protocol

**TRƯỚC KHI tạo file mới hoặc viết widget**, bạn PHẢI trả lời 5 câu hỏi:

1. **File này có vượt 300 dòng không?** → Nếu có khả năng, TÁCH ngay từ đầu
2. **Widget/Component này đã tồn tại chưa?** → Search codebase trước, REUSE nếu có
3. **Widget này có thể reuse cho nơi khác không?** → Nếu có, đặt vào `core/widgets/` hoặc shared folder
4. **Logic này thuộc layer nào?** → UI / Domain / Data — KHÔNG được trộn layers
5. **Có widget/hàm nào đang lặp logic tương tự không?** → Nếu có, REFACTOR thành shared component

### Nguyên tắc cứng

| ❌ Sai | ✅ Đúng |
|--------|---------|
| Tạo `UserCard` mới khi đã có `ProfileCard` tương tự | Mở rộng `ProfileCard` hoặc extract shared `BaseCard` |
| Screen 500+ dòng | Tách thành `_HeaderSection`, `_ContentBody`, `_ActionBar` |
| 3 screens cùng copy-paste search bar | Tạo `SearchableScaffold` dùng chung |
| Hardcode colors, padding, font sizes | Dùng `Theme.of(context)`, design tokens, constants |
| Business logic trong Widget `build()` | Tách vào UseCase / Service / Provider |

> 🔴 **REUSE > CREATE.** Không bao giờ tạo file mới mà không kiểm tra codebase hiện tại trước.
