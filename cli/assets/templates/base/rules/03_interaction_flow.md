---
description: Quy trình làm việc ABCR (Audit-Block-Critique-Refactor) khi nhận request
globs: *
---

# Rule: Interaction Flow (ABCR)

> Kích hoạt: Khi review, refactor, hoặc fix bugs

## Architecture Mode Selection (Bắt buộc)

Truoc khi vao ABCR, xac dinh mode kien truc:

1. **Greenfield/New Module** -> Mac dinh dung **Clean Architecture**.
2. **Maintenance du an cu** -> **Ton trong kien truc hien huu** (MVC/MVVM/Layered), khong ep migrate tong the.
3. **Them feature trong du an cu** -> Follow convention hien tai cua feature, chi refactor tang dan de giam no ky thuat.

## Mandatory Execution Header (Bat buoc)

Truoc moi lan implement, refactor, hoac review code, phai bat dau bang header sau:

```md
Task Type: <Greenfield | Brownfield Feature | Brownfield Hotfix>
Architecture Strategy: <Clean default | Follow existing architecture>
State Strategy: <stack duoc chon cho module>
Refactor Scope: <minimal | incremental | structured>
```

Neu thieu header nay, coi nhu chua dat quy trinh ABCR.

Khi nhận request liên quan đến code hiện tại, luôn tuân thủ quy trình:

1. **AUDIT** - Quét code smells, kiểm tra God Class/File
2. **BLOCK** - Cảnh báo nếu vi phạm, giải thích Technical Debt
3. **REFACTOR** - Refactor toi thieu trong kien truc hien huu truoc khi fix bug (chi de xuat migrate tong the khi user yeu cau)
4. **EXPLAIN** - Giải thích lý do tách/refactor

### Khi nào áp dụng ABCR?

| Tình huống | Áp dụng? |
|------------|----------|
| User yêu cầu fix bug | ✅ AUDIT trước, refactor nếu có code smell |
| User yêu cầu thêm feature | ✅ AUDIT file đích trước khi thêm code |
| User yêu cầu tạo file mới | ⚠️ Chỉ AUDIT các file liên quan |
| User hỏi kiến thức chung | ❌ Không cần ABCR |

> 💡 **Mục đích:** Không bao giờ thêm code rác lên code rác. Fix nền tảng trước.