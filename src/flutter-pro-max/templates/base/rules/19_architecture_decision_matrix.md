---
description: Ma tran quyet dinh kien truc cho Greenfield va Brownfield
globs: lib/**/*.dart, test/**/*.dart
---

# Rule: Architecture Decision Matrix

> Kich hoat: Khi bat dau task moi, them feature, sua bug, hoac refactor

## Muc tieu

- Mac dinh su dung Clean Architecture cho code moi.
- Van maintain duoc du an cu theo kien truc hien huu (MVC/MVVM/Layered).
- Khong ep migrate tong the khi chua co yeu cau ro rang.

## Step 1 - Xac dinh loai task

Chon dung 1 trong 3 loai truoc khi code:

1. **Greenfield:** Module/feature moi, chua co rang buoc kien truc cu.
2. **Brownfield Feature:** Them/chinh sua chuc nang tren module da ton tai.
3. **Brownfield Hotfix:** Sua loi nhanh, uu tien an toan va khong gay hoi quy.

## Step 2 - Decision Matrix

| Task Type | Architecture Strategy | State Strategy | Refactor Scope |
|----------|------------------------|----------------|----------------|
| Greenfield | Bat buoc Clean Architecture | Native-first theo rule state, dat state owner o presentation | Cho phep to chuc lai theo chuan Clean |
| Brownfield Feature | Follow kien truc hien huu cua module, khong doi framework lon | Giu stack state hien co cua module | Chi refactor tang dan trong pham vi file/feature bi cham toi |
| Brownfield Hotfix | Fix toi thieu, dung diem roi | Khong thay doi state framework | Khong refactor rong, chi tach nho neu can de fix an toan |

## Step 3 - Nguyen tac bat buoc

1. **No Forced Migration:** Khong tu y doi MVC -> Clean, Bloc -> Riverpod, Provider -> Bloc.
2. **No New Debt:** Du theo kien truc nao, van cam God File, God Class, Logic Leakage.
3. **Incremental Refactor:** Moi lan cham code la mot co hoi giam no ky thuat nho, khong dai phau neu khong duoc yeu cau.
4. **Consistency First:** Pattern moi phai giong module hien huu truoc, roi moi de xuat nang cap.

## Mapping nhanh theo kien truc hien huu

| Hien trang module | Noi dat business logic uu tien |
|-------------------|---------------------------------|
| Clean | UseCase/Service/Repository theo layer |
| MVC | Controller + Service + data layer hien huu |
| MVVM | ViewModel + Service + Repository |
| Layered cu | Theo convention module, tach ro UI/logic/data |

## Khi nao duoc de xuat migrate tong the?

Chi de xuat migration lon khi co it nhat 1 dieu kien:

1. User yeu cau ro rang migrate.
2. Chi phi maintain vuot nguong (bug lap lai, velocity giam manh, testability rat kem).
3. Co ke hoach rollout theo giai doan (khong big-bang) va co test safety net.

Neu khong dat dieu kien, tiep tuc chien luoc maintain theo kien truc hien huu.

## Checklist truoc khi implement

- [ ] Da gan task vao dung nhom Greenfield/Brownfield Feature/Brownfield Hotfix.
- [ ] Da chon architecture strategy tu matrix.
- [ ] Da xac dinh state strategy dung voi module.
- [ ] Da gioi han refactor scope phu hop muc tieu task.
- [ ] Khong co hanh dong forced migration ngoai pham vi yeu cau.

## Output format bat buoc (implement/review)

Moi task phai mo dau bang 4 dong sau truoc khi mo ta cach lam:

```md
Task Type: <Greenfield | Brownfield Feature | Brownfield Hotfix>
Architecture Strategy: <Clean default | Follow existing architecture>
State Strategy: <stack duoc chon cho module>
Refactor Scope: <minimal | incremental | structured>
```
