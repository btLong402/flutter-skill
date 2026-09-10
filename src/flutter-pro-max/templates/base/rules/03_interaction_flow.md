---
description: Quy trình làm việc ABCR (Audit-Block-Critique-Refactor) và Kiểm soát Tương tác
globs: *
---

# Rule: Interaction Flow (ABCR Protocol)

> Kích hoạt: Khi nhận yêu cầu tạo mới, chỉnh sửa, review, refactor hoặc sửa lỗi (fix bug)

## 1. Phân loại Chế độ Kiến trúc (Architecture Mode Selection)

Trước khi thực hiện bất kỳ thao tác nào, bạn **BẮT BUỘC** xác định rõ chế độ kiến trúc:

1. **Greenfield / Module mới:** Mặc định áp dụng **Clean Architecture** (Data $\rightarrow$ Domain $\rightarrow$ Presentation).
2. **Bảo trì dự án cũ (Brownfield):** **Tôn trọng tuyệt đối kiến trúc hiện hữu** (MVC / MVVM / Layered). Tuyệt đối không ép migrate toàn diện.
3. **Thêm tính năng trong dự án cũ:** Tuân thủ convention hiện có của feature đó, chỉ tái cấu trúc tăng dần (incremental refactor) trong phạm vi file bị chỉnh sửa.

---

## 2. Rào Chắn Thực Thi Bắt Buộc (Mandatory Execution Header)

Mọi phản hồi liên quan đến lập trình, thêm tính năng, sửa lỗi hoặc refactor **BẮT BUỘC** phải bắt đầu bằng khối Pre-Flight Checklist (theo chuẩn Rule 02 & 19):

```yaml
# PRE-FLIGHT COMPLIANCE CHECK
task_type: Greenfield | Brownfield Feature | Brownfield Hotfix
architecture_strategy: Clean default | Follow existing architecture
state_strategy: ValueNotifier | ChangeNotifier | Provider | Bloc/Riverpod (theo yêu cầu)
refactor_scope: minimal | incremental | structured
```

> ⚠️ Nếu thiếu phần khai báo này, phản hồi bị coi là **chưa đạt tiêu chuẩn tương tác**.

---

## 3. Quy trình 4 Bước ABCR

Khi nhận được yêu cầu liên quan đến mã nguồn hiện tại, luôn tuân thủ nghiêm ngặt 4 bước:

```
[1. AUDIT] ──► Quét mã nguồn, tìm Code Smells, God Files, Logic Leakage
     │
[2. BLOCK] ──► Dừng lại, cảnh báo nếu phát hiện vi phạm kiến trúc hoặc nợ kỹ thuật
     │
[3. REFACTOR]► Tái cấu trúc tối thiểu trong phạm vi cho phép trước khi thêm code mới
     │
[4. EXPLAIN] ─► Giải thích ngắn gọn lý do tại sao phải tách/refactor
```

### Khi nào áp dụng ABCR?

| Tình huống yêu cầu | Áp dụng ABCR? | Hành động cụ thể |
| :--- | :---: | :--- |
| **Sửa lỗi (Fix bug)** | ✅ **BẮT BUỘC** | AUDIT trước, viết test tái hiện lỗi, refactor nếu có code smell rồi mới fix. |
| **Thêm tính năng mới (Add feature)**| ✅ **BẮT BUỘC** | AUDIT file đích trước khi thêm code. Nếu file đích $\ge 200$ dòng $\rightarrow$ Tách trước! |
| **Tạo file mới hoàn toàn** | ⚠️ **MỘT PHẦN** | AUDIT các module liên quan để đảm bảo tái sử dụng (Reuse), tránh trùng lặp. |
| **Hỏi đáp kiến thức chung** | ❌ **KHÔNG** | Phản hồi trực tiếp, súc tích, không cần header rườm rà. |

---

---

## 4. Kiểm Soát Tương Tác & Chống Re-entrancy (Interaction Hardening)

### 1. Chống Double-Tap & Re-entrancy (Nút bấm Async)
Mọi thao tác async từ nút bấm (Submit form, Đặt hàng, Thanh toán, Xóa dữ liệu, Điều hướng) **BẮT BUỘC** phải có cơ chế ngăn chặn bấm đúp:

```dart
// ❌ CẤM: Bấm liên tiếp gửi nhiều request trùng lặp
// ElevatedButton(onPressed: () => controller.submit(), child: Text('Lưu'))

// ✅ ĐÚNG: Khóa nút khi đang xử lý (isSubmitting guard)
class SubmitButton extends StatelessWidget {
  final VoidCallback? onSubmit;
  final bool isLoading;

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: isLoading ? null : onSubmit, // Tự động disable khi loading
      child: isLoading ? const CircularProgressIndicator.adaptive() : const Text('Lưu'),
    );
  }
}
```

```dart
// Trong Controller: Rào chắn Re-entrancy
Future<void> submitOrder() async {
  if (isSubmitting.value) return; // BẮT BUỘC: Ngăn double-tap
  isSubmitting.value = true;
  try {
    await repository.placeOrder();
    Get.back();
  } finally {
    isSubmitting.value = false;
  }
}
```

### 2. Chống Pop Kép trên Dialog (Double-Pop Protection)
Khi đóng dialog xác nhận, cấm gọi liên tiếp nhiều lệnh pop hoặc pop không kiểm tra `canPop()`, tránh đóng nhầm màn hình cha:
```dart
void dismissDialog(BuildContext context) {
  final navigator = Navigator.of(context);
  if (navigator.canPop()) {
    navigator.pop();
  }
}
```

---

## 5. Chuẩn Hóa Search Input & Chống Race Condition

Tìm kiếm theo thời gian thực (Search as you type) rất dễ gặp lỗi Race Condition (kết quả cũ về sau đè kết quả mới):

```dart
// ✅ ĐÚNG: Debounce + Hủy request cũ bằng CancelToken
class ProductSearchController extends GetxController {
  final RxString query = ''.obs;
  final RxList<Product> results = <Product>[].obs;
  final RxBool isSearching = false.obs;

  CancelToken? _cancelToken;
  Worker? _debounceWorker;

  @override
  void onInit() {
    super.onInit();
    // 1. Bắt buộc Debounce từ 300ms - 500ms
    _debounceWorker = debounce(query, _executeSearch, time: const Duration(milliseconds: 400));
  }

  Future<void> _executeSearch(String text) async {
    if (text.trim().isEmpty) {
      results.clear();
      return;
    }

    // 2. Hủy request tìm kiếm cũ nếu đang chạy
    _cancelToken?.cancel('New query initiated');
    _cancelToken = CancelToken();

    isSearching.value = true;
    try {
      final data = await repository.search(text, cancelToken: _cancelToken);
      results.assignAll(data);
    } on DioException catch (e) {
      if (CancelToken.isCancel(e)) return; // Bỏ qua nếu là request cũ bị hủy
      // Xử lý lỗi thật
    } finally {
      isSearching.value = false;
    }
  }

  @override
  void onClose() {
    _debounceWorker?.dispose();
    _cancelToken?.cancel();
    super.onClose();
  }
}
```

---

## 6. Nguyên Tắc Cốt Lõi

> 💡 **KHÔNG BAO GIỜ VIẾT CODE MỚI ĐÈ LÊN MỘT NỀN TẢNG CODE RÁC.**  
> Luôn dọn dẹp và củng cố nền tảng trước khi xây tầng tiếp theo. Bảo vệ ứng dụng khỏi thao tác vô thức của người dùng (double tap, spam submit, lag network).