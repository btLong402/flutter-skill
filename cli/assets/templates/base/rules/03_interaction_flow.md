---
description: Quy trình làm việc ABCR (Audit-Block-Critique-Refactor) khi nhận request
globs: *
---

# Rule: Interaction Flow (ABCR)

> Kích hoạt: Khi review, refactor, hoặc fix bugs

Khi nhận request liên quan đến code hiện tại, luôn tuân thủ quy trình:

1. **AUDIT** - Quét code smells, kiểm tra God Class/File
2. **BLOCK** - Cảnh báo nếu vi phạm, giải thích Technical Debt
3. **REFACTOR** - Sửa kiến trúc trước khi fix bug
4. **EXPLAIN** - Giải thích lý do tách/refactor

### Khi nào áp dụng ABCR?

| Tình huống | Áp dụng? |
|------------|----------|
| User yêu cầu fix bug | ✅ AUDIT trước, refactor nếu có code smell |
| User yêu cầu thêm feature | ✅ AUDIT file đích trước khi thêm code |
| User yêu cầu tạo file mới | ⚠️ Chỉ AUDIT các file liên quan |
| User hỏi kiến thức chung | ❌ Không cần ABCR |

> 💡 **Mục đích:** Không bao giờ thêm code rác lên code rác. Fix nền tảng trước.