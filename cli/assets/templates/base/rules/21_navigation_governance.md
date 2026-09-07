---
description: Quản trị Điều hướng (Navigation), GoRouter, Type-Safe Routes, Deep Linking, Auth Guards
globs: lib/presentation/**/*.dart, lib/core/router/**/*.dart, lib/routes/**/*.dart
---

# Rule: Navigation Governance & Deep Linking

> Kích hoạt: Khi cấu hình routing, chuyển trang, truyền tham số màn hình hoặc xử lý Deep Link

## 1. Nguyên Tắc Cốt Lõi: Khai Báo Tập Trung (Declarative Routing)

> 🔴 **CẤM:** Viết rải rác `Navigator.push(context, MaterialPageRoute(builder: ...))` khắp codebase.  
> Toàn bộ luồng điều hướng phải được quản trị tập trung thông qua Declarative Routing (khuyến nghị `go_router`).

---

## 2. Quy Chuẩn Triển Khai Routing

| Thành phần | Tiêu chuẩn bắt buộc |
| :--- | :--- |
| **Route Path** | Khai báo dạng hằng số tập trung: `class AppRoutes { static const home = '/'; ... }` |
| **Tham số màn hình** | Type-safe: Trích xuất và validate params qua DTO hoặc typed routes, không truyền `dynamic` object không rõ cấu trúc. |
| **Auth Redirect Guard** | Quản lý chuyển hướng đăng nhập tập trung trong cấu hình `redirect` của router dựa trên trạng thái xác thực (Auth State). |
| **Nested Navigation** | Dùng `StatefulShellRoute` cho Bottom Navigation Bar để bảo tồn trạng thái cuộn của từng tab. |

---

## 3. Deep Linking & An Toàn Tham Số (Security)

1. **Không tin tưởng dữ liệu từ Deep Link:** Mọi query parameters (`?id=123&token=xyz`) từ URL bên ngoài phải được validate và sanitize nghiêm ngặt trước khi sử dụng.
2. **Fallback cho Route không tồn tại:** Luôn định nghĩa `errorBuilder` để hiển thị trang 404 thân thiện thay vì crash ứng dụng.

---

## 4. Mẫu Triển Khai Chuẩn với GoRouter

```dart
// ✅ Định nghĩa routes tập trung và an toàn
final appRouter = GoRouter(
  initialLocation: AppRoutes.home,
  errorBuilder: (context, state) => const NotFoundPage(),
  redirect: (context, state) {
    final isLoggedIn = authNotifier.isLoggedIn;
    final isGoingToLogin = state.matchedLocation == AppRoutes.login;

    if (!isLoggedIn && !isGoingToLogin) return AppRoutes.login;
    if (isLoggedIn && isGoingToLogin) return AppRoutes.home;
    return null; // Không cần chuyển hướng
  },
  routes: [
    GoRoute(
      path: AppRoutes.home,
      builder: (context, state) => const HomePage(),
    ),
    GoRoute(
      path: '${AppRoutes.productDetail}/:id',
      builder: (context, state) {
        final id = state.pathParameters['id'] ?? '';
        return ProductDetailPage(productId: id);
      },
    ),
  ],
);
```

> 💡 **Quy tắc vàng:** Sử dụng `context.go(AppRoutes.path)` khi thay thế luồng và `context.push(AppRoutes.path)` khi mở trang con có nút Back.
