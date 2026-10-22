# Playbook cải thiện

## Mục lục
1. Cách chọn việc để sửa
2. Lỗi thường gặp → cách sửa (theo tiêu chí)
3. Gợi ý theo framework
4. Quy tắc vòng lặp tự cải thiện
5. Iteration log (mẫu)
6. Khi nào nên dừng và hỏi con người

---

## 1. Cách chọn việc để sửa

`score.py` xếp backlog theo:

```
ưu tiên = mức nghiêm trọng × phạm vi (reach) × trọng số tiêu chí ÷ công sức (effort)
mức nghiêm trọng: blocker 8, major 4, minor 2, polish 1
```

Chọn **3–5 mục đầu**, nhưng áp thêm phán đoán:

- **Gộp theo nguyên nhân gốc.** Nếu 6 issue cùng do một token/component sai (vd: IconButton mặc định 36dp), sửa một lần ở gốc = một việc.
- **Gỡ trần điểm trước.** Blocker (trần 59) và accessibility < 3 (trần 79) chặn mọi cải thiện khác hiện ra trên điểm tổng; xử lý chúng đầu tiên.
- **Nhắm nút thắt.** Tiêu chí có (trọng số × khoảng cách tới 5) lớn nhất là nơi lợi nhất.
- **Tablet thường là khoảng trống lớn nhất** với app vốn thiết kế cho phone — nếu điểm tablet thấp hơn mobile hơn 10 điểm, ưu tiên `adaptive_responsive` và `navigation_ia` trên tablet.

---

## 2. Lỗi thường gặp → cách sửa

### Hierarchy & layout
| Lỗi | Cách sửa |
|---|---|
| Nhiều nút cùng nổi | Giữ 1 primary (filled), còn lại secondary (outlined/tonal) hoặc text button |
| Spacing lộn xộn | Định nghĩa thang 4/8/12/16/24/32; thay giá trị lẻ bằng token gần nhất; tăng khoảng cách *giữa* nhóm hơn *trong* nhóm |
| Màn hình quá đặc | Chia section có tiêu đề; ẩn tùy chọn nâng cao sau "Xem thêm"; giảm số hành động ngang hàng xuống ≤ 3–4 |
| Nội dung đè lên notch/home bar | Bọc bằng safe area / `WindowInsets`; tránh `ignoresSafeArea` trừ nền ảnh |
| Ảnh méo hoặc cắt mất chủ thể | Cố định tỉ lệ (aspect ratio), `cover` + focal point, hoặc `contain` cho ảnh sản phẩm |

### Typography
| Lỗi | Cách sửa |
|---|---|
| Chữ nhỏ (<12) | Nâng caption lên ≥ 12–13, body ≥ 16sp/17pt; dùng đơn vị `sp`/Dynamic Type, không `dp`/px cố định |
| Quá nhiều cỡ chữ | Rút về thang 5–6 cấp (display/title/body/label/caption) dưới dạng token |
| Dòng dài trên tablet | `max-width` 600–720dp cho cột đọc; hoặc 2 cột |
| Dấu tiếng Việt bị cắt | `line-height` ≥ 1.4 (body) / 1.25 (title); bỏ `height` cố định của Text; kiểm tra `includeFontPadding`/`TextHeightBehavior` |
| Chữ bị cắt khi font scale lớn | Cho phép xuống dòng, `minHeight` thay `height`, co giãn container, cho cuộn |

### Màu & contrast
| Lỗi | Cách sửa |
|---|---|
| Text xám nhạt trên trắng | Chạy `contrast.py`; dùng màu gợi ý (script in sẵn), cập nhật ở token chứ không từng chỗ |
| Placeholder quá mờ | Đủ 4.5:1; placeholder không thay nhãn — thêm label cố định |
| Chỉ dùng màu để báo lỗi | Thêm icon + dòng chữ lỗi dưới field |
| Dark mode đảo màu lỗi | Thiết kế surface phân tầng (elevation → sáng dần); giảm độ bão hòa accent; kiểm contrast lại |
| Text trên ảnh khó đọc | Overlay gradient/scrim đủ đậm, hoặc đặt text vào panel nền đặc |

### Điều hướng & IA
| Lỗi | Cách sửa |
|---|---|
| >5 mục ở thanh dưới | Gộp/đưa mục ít dùng sang "Tôi"/menu; dùng rail/sidebar trên màn lớn |
| Không rõ đang ở đâu | Highlight tab đang chọn rõ (icon filled + nhãn + màu), tiêu đề màn hình, breadcrumb trên tablet |
| Việc chính chôn sâu | Đưa lên màn hình chủ / thanh hành động; rút bước; lưu lựa chọn gần nhất |
| Back không như kỳ vọng | Dùng điều hướng chuẩn của framework (NavigationStack, `popBackStack`), hỗ trợ swipe-back/predictive back, không chặn back vô cớ |
| Mất trạng thái khi quay lại | Lưu scroll/filter/form vào state giữ qua điều hướng (`rememberSaveable`, `@SceneStorage`, `PageStorageKey`) |
| Tablet dùng lại bottom bar rộng | Chuyển sang NavigationRail/Sidebar ở width ≥ 600dp |

### Tương tác chạm
| Lỗi | Cách sửa |
|---|---|
| Icon-button < 44/48 | Giữ icon 24dp nhưng mở vùng chạm lên 48 (padding, `hitSlop`, `minimumInteractiveComponentSize`) |
| Nút sát nhau | Khoảng cách ≥ 8dp; tách hành động phá hủy ra xa hoặc đổi sang menu |
| Chỉ có swipe để xóa | Thêm menu "⋯"/nút Xóa hiển thị; swipe chỉ là phím tắt |
| Xác nhận xóa bằng dialog | Xóa ngay + snackbar "Hoàn tác" (nếu có thể undo) |
| Form khó nhập | Đặt `keyboardType`, `textInputAction`, autofill hints; `scrollPadding`/`windowSoftInputMode=adjustResize`; nút Tiếp tục dính trên bàn phím |
| Hành động chính ở đỉnh | Chuyển xuống thanh dưới/FAB/bottom sheet trên phone lớn |

### Phản hồi, trạng thái, chuyển động
| Lỗi | Cách sửa |
|---|---|
| Màn trắng khi tải | Skeleton có bố cục giống nội dung; hiển thị dữ liệu cache trước (stale-while-revalidate) |
| Lỗi chung chung | "Không tải được đơn hàng — kiểm tra kết nối rồi thử lại." + nút **Thử lại**; giữ dữ liệu đã nhập |
| Empty trống trơn | Minh họa nhẹ + 1 câu giải thích + nút hành động đầu tiên |
| Bấm không thấy phản hồi | Thêm pressed/ripple state; disable + spinner trên nút khi đang gửi (chống bấm đôi) |
| Animation dài, chặn thao tác | Rút về 150–300ms; không chặn input; dùng `Reduce Motion` để thay bằng fade |
| Thất bại âm thầm | Snackbar/inline error có hành động; log |

### Accessibility
| Lỗi | Cách sửa |
|---|---|
| Icon button không nhãn | Thêm nhãn mô tả hành động (`contentDescription`/`accessibilityLabel`/`Semantics(label:)`), không nhãn rỗng |
| Card đọc rời rạc | Gộp (`mergeDescendants` / `accessibilityElement(children: .combine)` / `MergeSemantics`) với nhãn có nghĩa |
| Decorative icon bị đọc | Ẩn khỏi cây accessibility |
| Font scale 200% vỡ | Layout co giãn, `minHeight`, `Flexible/Wrap`, cho cuộn; không `allowFontScaling=false` |
| Trạng thái không được đọc | Gán `selected/checked/expanded`, role đúng (button, switch, tab) |
| Thay đổi động im lặng | Live region / `UIAccessibility.post(.announcement)` cho toast, lỗi, kết quả tìm |
| Tablet + bàn phím ngoài thiếu focus | Focus ring rõ, thứ tự Tab theo thị giác, phím Enter/Esc, `FocusTraversalGroup` / `focusable` |

### Nhất quán & design system
| Lỗi | Cách sửa |
|---|---|
| Màu/spacing hardcode | Gom về token/theme (`ThemeData`, `MaterialTheme`, Asset Catalog/`Color` extension); thay hàng loạt rồi thêm lint |
| Nhiều biến thể nút | Một `AppButton` với `variant`; xoá bản sao |
| Icon lẫn bộ | Chọn một bộ (SF Symbols / Material Symbols), cùng weight và kích thước |
| Thuật ngữ lẫn lộn | Lập bảng thuật ngữ; tìm-thay toàn app |

### Nội dung & microcopy
| Lỗi | Cách sửa |
|---|---|
| "OK / Submit" | Đổi sang động từ cụ thể: "Đặt hàng", "Lưu thay đổi" |
| Lỗi mã trần | Nêu nguyên nhân + cách sửa; ẩn mã lỗi sau "Chi tiết" |
| Xin quyền đột ngột | Màn giải thích lý do trước (priming), xin đúng lúc cần |
| Chuỗi hardcode | Đưa vào file localization; kiểm tra với pseudo-locale +40% |

### Thích ứng đa kích thước
| Lỗi | Cách sửa |
|---|---|
| Tablet = phone kéo giãn | Thêm bố cục theo window size class: compact → 1 cột + bottom bar; medium → rail + 1–2 cột; expanded → list-detail/supporting pane |
| Form trải hết 1200dp | `max-width` ~ 560–720dp, căn giữa |
| Khóa dọc/ngang | Gỡ khóa orientation (trừ ngoại lệ chính đáng); xử lý config change |
| Mất state khi xoay/resize | `rememberSaveable`/`@SceneStorage`/ViewModel/State restoration |
| Vỡ ở split view hẹp | Dùng breakpoint theo **độ rộng cửa sổ hiện tại**, không theo kích thước thiết bị |
| Ảnh mờ trên tablet | Cung cấp ảnh độ phân giải cao hơn / vector / `srcset` tương đương |

### Hiệu năng cảm nhận
| Lỗi | Cách sửa |
|---|---|
| Màn trắng lúc khởi động | Splash/skeleton ngay frame đầu; hoãn khởi tạo nặng (SDK, DB) sang sau frame đầu; hiển thị dữ liệu cache trước |
| Cuộn danh sách giật | Dùng lazy/virtualized list (`ListView.builder`, `FlatList`/`FlashList`, `LazyColumn`, `LazyVStack`); item có key ổn định; tránh layout phức tạp trong item |
| Ảnh nặng | Tải đúng kích thước hiển thị, cache, placeholder, decode ngoài main thread; dùng định dạng nén (WebP/AVIF) |
| Thao tác trễ | Chuyển việc nặng ra background/isolate/coroutine; phản hồi UI trước, xử lý sau (optimistic) |
| Rebuild cả màn hình | Tách widget/composable nhỏ, `const`/`remember`/`memo`, state cục bộ thay vì state toàn cục đổi liên tục |
| Treo với dữ liệu lớn (10k mục) | Phân trang/streaming, tìm kiếm phía server hoặc debounce; không sắp xếp/lọc toàn bộ trên UI thread |
| Giật khi xoay/resize tablet | Không tải lại dữ liệu khi đổi cấu hình (giữ state, ViewModel/Bloc); tránh dựng lại cây UI không cần |
| Mạng chậm/offline treo UI | Timeout hợp lý, hủy được, skeleton + thông báo, hàng đợi cho thao tác ghi |

### Theming & Dark mode
| Lỗi | Cách sửa |
|---|---|
| Màu hardcode phá dark mode | Gom về token ngữ nghĩa (`surface`, `onSurface`…), thay hàng loạt, thêm lint chặn hex trong màn hình |
| Dialog/bottom sheet nền sáng trong dark | Dùng theme của hệ component (`DialogTheme`, `ModalBottomSheet` colors) thay vì màu cố định |
| Logo/ảnh nền trắng chói | Thêm biến thể dark hoặc nền trung tính; ảnh PNG trong suốt kiểm lại trên nền tối |
| Nền `#000` + chữ `#FFF` quá gắt | Surface phân tầng (`#121212` → lớp cao sáng dần), chữ ~87% độ sáng, giảm bão hòa accent |
| Status/nav bar không đổi | Đặt biểu tượng thanh hệ thống sáng/tối theo theme; kiểm tra splash/launch screen |
| WebView/chart/bản đồ không theo theme | Truyền theme (CSS `prefers-color-scheme`, tùy chọn style bản đồ, màu series chart) |
| Đổi theme mất state/nháy trắng | Theme là state toàn cục đổi tại gốc cây UI; không tạo lại các màn hình khi đổi |
| Không có lựa chọn trong app | Settings: Hệ thống / Sáng / Tối, lưu lựa chọn |

---

## 3. Gợi ý theo framework

**Flutter**
- Hiệu năng: `flutter run --profile`, DevTools; dùng `ListView.builder`, `const` widget, `RepaintBoundary` có chọn lọc; ảnh dùng `cacheWidth`/`cacheHeight`.
- Theme: `ThemeData.light()/dark()` + `ColorScheme.fromSeed`, `themeMode: ThemeMode.system`; truy cập màu qua `Theme.of(context).colorScheme`.
- Breakpoint: `LayoutBuilder` + `MediaQuery.sizeOf(context).width`; đóng gói `WindowClass` enum (compact <600, medium <840, expanded).
- Điều hướng thích ứng: `NavigationBar` ↔ `NavigationRail` ↔ `Drawer`; `adaptive_scaffold` (package) cho list-detail.
- Vùng chạm: `visualDensity: VisualDensity.standard`, `materialTapTargetSize: MaterialTapTargetSize.padded`, `ConstrainedBox(constraints: BoxConstraints(minWidth: 48, minHeight: 48))`.
- A11y: `Semantics`, `MergeSemantics`, `ExcludeSemantics` (chỉ cho trang trí); test `tester.ensureSemantics()`; `textScaler`.
- Test hồi quy: golden test ở nhiều size/`textScaler`/dark.

**React Native**
- Hiệu năng: `FlashList` cho danh sách dài, `React.memo`/`useCallback` ở item, bản release khi đo, tránh tác vụ nặng trên JS thread.
- Theme: `useColorScheme()`, ThemeProvider với token, không hardcode màu.
- Breakpoint: `useWindowDimensions`; tránh `Dimensions.get` tĩnh (không cập nhật khi resize/split).
- A11y: `accessibilityLabel`, `accessibilityRole`, `accessibilityState`, `importantForAccessibility`; không `allowFontScaling={false}`.
- Vùng chạm: `hitSlop`, `Pressable` với `minHeight`.
- Safe area: `react-native-safe-area-context`.
- Tablet: kiểm tra `Platform.isPad` chỉ để *khởi điểm*; quyết định bố cục theo độ rộng.

**SwiftUI / UIKit**
- Hiệu năng: `LazyVStack`/`List`, tránh `body` nặng, Instruments → Animation Hitches.
- Theme: Asset Catalog colors có biến thể Any/Dark, semantic colors (`Color.primary`, `.secondary`), `.preferredColorScheme` chỉ khi cần ép.
- Size classes: `@Environment(\.horizontalSizeClass)`, `NavigationSplitView`, `TabView` dạng sidebar (iPad), `ViewThatFits`.
- Dynamic Type: `.font(.body)` semantic styles, `@ScaledMetric`, test `.dynamicTypeSize(...accessibility5)`.
- A11y: `.accessibilityLabel`, `.accessibilityElement(children:)`, `.accessibilityAddTraits`, rotor/actions tùy chỉnh.
- Phím tắt/pointer: `.keyboardShortcut`, `.hoverEffect`, `.contextMenu`.

**Jetpack Compose**
- Hiệu năng: `LazyColumn` với `key`, `remember`/`derivedStateOf`, Baseline Profiles cho khởi động, Macrobenchmark để đo.
- Theme: `MaterialTheme(colorScheme = if (isSystemInDarkTheme()) dark else light)`, `dynamicColorScheme` (Android 12+) nếu chọn hỗ trợ, `@PreviewLightDark`.
- `currentWindowAdaptiveInfo()` + `WindowSizeClass`; `NavigationSuiteScaffold`, `ListDetailPaneScaffold`/`SupportingPaneScaffold`.
- Vùng chạm: `Modifier.minimumInteractiveComponentSize()`; `Modifier.sizeIn(minWidth = 48.dp, minHeight = 48.dp)`.
- A11y: `Modifier.semantics { contentDescription = ...; role = ... }`, `clearAndSetSemantics` (thận trọng), `mergeDescendants = true`.
- State: `rememberSaveable`; `Preview` với `@PreviewScreenSizes`, `@PreviewFontScale`, `@PreviewLightDark`.

---

## 4. Quy tắc vòng lặp tự cải thiện

1. **Một vòng = một lô nhỏ.** 3–5 việc, cùng nguyên nhân hoặc cùng mục tiêu. Mỗi việc gắn với issue ID.
2. **Sửa ở gốc.** Token/component dùng chung trước, từng màn hình sau.
3. **Không phá luật chơi.** Không xóa nội dung/tính năng để "sạch lỗi"; không thêm label giả; không thu nhỏ phạm vi bằng chứng (bỏ thiết bị khó) để điểm đẹp. Phạm vi bằng chứng của vòng sau **không được hẹp hơn** vòng trước.
4. **Chấm lại độc lập** (đọc SKILL.md, nguyên tắc 4).
5. **Hồi quy = hoàn tác.** Nếu một tiêu chí giảm ≥ 1 hoặc tổng giảm → xác định thay đổi gây ra (bật/tắt từng thay đổi), hoàn tác hoặc sửa lại, chấm lại.
6. **Ghi lại mọi quyết định** vào iteration log; mỗi vòng có thể truy vết và đảo ngược.
7. **Đóng issue có điều kiện.** Chỉ đánh `fixed` khi có bằng chứng *mới* chứng minh đã sửa (screenshot sau sửa, kết quả `uiautomator`, v.v.). Không có bằng chứng → để `open`.
8. **Phát sinh lỗi mới thì ghi vào backlog**, đừng giấu.
9. **Không quá 5 vòng** và dừng khi plateau (SKILL.md → Điều kiện dừng).

---

## 5. Iteration log (mẫu)

Lưu vào `iteration-log.md` cạnh scorecard:

```markdown
## Vòng 2 — 2026-10-15
Điểm: mobile 71.5 → 78.0 | tablet 58.0 → 66.5 | tổng 64.8 → 72.3 (+7.5)
Phạm vi bằng chứng: P-S, P-L, T-P, T-L, font 2.0, dark (giữ nguyên so với vòng 1)

Thay đổi:
- TC-04 (touch_interaction, both): IconButton mặc định 48dp ở `lib/ui/app_icon_button.dart` → sửa 14 chỗ dùng
- A11-02 (accessibility, both): thêm label cho 9 icon-button ở Home/Cart (C-HomeScreen.dart:84…)
- AD-01 (adaptive_responsive, tablet): thêm NavigationRail khi width ≥ 600dp (C-app_shell.dart:22)

Hoàn tác:
- VH-07: tăng padding card làm danh sách quá dài trên P-S → hoàn tác, giữ 12dp

Phát sinh:
- AD-05 (minor, tablet): rail chồng lên FAB ở T-P → thêm vào backlog

Quyết định: giữ; tiếp tục vòng 3 (backlog đầu: AD-02, FS-03)
```

---

## 6. Khi nào nên dừng và hỏi con người

Dừng vòng lặp và báo người dùng khi:

- Cải thiện cần **quyết định thương hiệu/sản phẩm** (đổi bộ màu thương hiệu, bỏ tính năng, đổi mô hình điều hướng cả app).
- Cần **dữ liệu người dùng thật** để biết chỗ nào đang gây khó (ví dụ không rõ luồng nào quan trọng nhất, A/B test, usability test).
- Sửa **chạm vào logic nghiệp vụ/an toàn** (thanh toán, quyền, bảo mật) ngoài phạm vi UI.
- Hai mục tiêu xung đột thật sự (vd: mật độ thông tin cao cho power user vs. đơn giản cho người mới).
- Bị chặn bởi giới hạn môi trường (không có emulator, không build được) khiến không thể kiểm chứng.

Khi báo, nêu: đã làm gì, điểm hiện tại, rào cản, và 2–3 lựa chọn kèm đánh đổi.
