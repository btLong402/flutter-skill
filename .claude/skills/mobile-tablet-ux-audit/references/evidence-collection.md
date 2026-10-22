# Thu thập bằng chứng

## Mục lục
1. Chọn chế độ bằng chứng
2. Chế độ A — Screenshot / ảnh màn hình
3. Chế độ B — Source code
4. Chế độ C — App đang chạy (emulator / thiết bị)
5. Chế độ D — Figma / mockup
6. Gán ID bằng chứng
7. Bảng "đo được gì, tin được đến đâu"

---

## 1. Chọn chế độ bằng chứng

Kết hợp càng nhiều chế độ càng tốt. Thứ tự tin cậy: **C (chạy thật) > A (screenshot thật) > B (code) > D (mockup)**. Code cho biết *ý định*, chạy thật cho biết *kết quả*; hai thứ này hay lệch nhau.

Nếu agent có thể chạy emulator/thiết bị → ưu tiên C, dùng B để truy nguyên nguyên nhân và sửa. Nếu chỉ có ảnh → chỉ chấm được những gì nhìn thấy; phần còn lại là `confidence: low`.

---

## 2. Chế độ A — Screenshot

Khi người dùng gửi ảnh:

1. Xác định thiết bị/viewport (suy từ kích thước ảnh, thanh trạng thái, hoặc hỏi nếu không rõ). Ảnh có thể là @2x/@3x → chia ra dp/pt.
2. Liệt kê từng màn hình theo flow, gắn ID (`S-<màn>-<thiết bị>`).
3. Đo bằng mắt có phương pháp:
   - **Vùng chạm:** ước lượng kích thước icon/nút theo dp (đo pixel ÷ mật độ). Nếu không đo chắc chắn được, ghi "ước lượng".
   - **Contrast:** lấy màu từ ảnh (nếu có thể chạy script, lấy mẫu pixel) rồi chạy `scripts/contrast.py`. Màu bị nén/gradient/ảnh nền thì ghi `medium`.
   - **Spacing:** so sánh khoảng cách tương đối giữa các nhóm (có theo thang không).
4. Những thứ **không** thể xác nhận từ ảnh tĩnh: hành vi cuộn, animation, trạng thái pressed, focus order, nhãn screen reader, hành vi khi xoay/font lớn. Ghi vào "giới hạn" và hạ confidence.

Lấy mẫu pixel (khi có file ảnh trên đĩa):

```bash
python3 - <<'EOF'
from PIL import Image
im = Image.open("/path/shot.png").convert("RGB")
print(im.size)
# lấy màu tại (x, y); điền toạ độ cần đo
for xy in [(40, 120), (200, 600)]:
    print(xy, "#%02X%02X%02X" % im.getpixel(xy))
EOF
```

---

## 3. Chế độ B — Source code

Khi có repo. Đọc theo thứ tự: theme/tokens → component dùng chung → màn hình trong flow chính → cấu hình nền tảng (manifest/Info.plist).

### Việc cần tìm (mọi framework)

| Câu hỏi | Tìm gì |
|---|---|
| Có token/theme không, hay hardcode? | Số lượng màu hex, `fontSize`, `padding` rải rác trong màn hình |
| Vùng chạm | Kích thước button/IconButton; `minimumSize`, `minHeight`, `hitSlop`, `Modifier.minimumInteractiveComponentSize` |
| Accessibility | `Semantics`, `accessibilityLabel`, `contentDescription`, `accessibilityRole`, `ExcludeSemantics`, test với font scale |
| Responsive/tablet | `LayoutBuilder`, `MediaQuery`, `WindowSizeClass`, `useWindowDimensions`, `horizontalSizeClass`, `NavigationRail`, `NavigationSuiteScaffold`, `ListDetailPaneScaffold`, `NavigationSplitView` |
| Orientation lock | `SystemChrome.setPreferredOrientations`, `android:screenOrientation`, `UISupportedInterfaceOrientations` |
| State UI | Có `loading`/`error`/`empty` trong ViewModel/Bloc/Store và có UI tương ứng không |
| Reduce motion | `MediaQuery.disableAnimations`, `AccessibilityInfo.isReduceMotionEnabled`, `accessibilityReduceMotion` |
| Font scale | `textScaler`, `allowFontScaling={false}` (cờ đỏ), `sp` vs `dp` cho chữ, `adjustsFontForContentSizeCategory` |
| Insets/safe area | `SafeArea`, `useSafeAreaInsets`, `WindowInsets`, `safeAreaInset`, `ignoresSafeArea` |

Gợi ý tìm nhanh (điều chỉnh theo repo):

```bash
# Màu/cỡ chữ/padding hardcode (chỉ số lượng để ước lượng độ kỷ luật token)
grep -rEho "Color\(0x[0-9A-Fa-f]{8}\)|#[0-9A-Fa-f]{6}\b" lib src app 2>/dev/null | sort | uniq -c | sort -rn | head -30
grep -rEn "fontSize:\s*[0-9]+|font-size|textSize=\"[0-9]+sp\"" lib src app 2>/dev/null | head -40

# Cờ đỏ về accessibility
grep -rEn "allowFontScaling=\{false\}|textScaleFactor:\s*1\.0|ExcludeSemantics|importantForAccessibility=\"no\"" . 2>/dev/null | head

# Khoá orientation
grep -rEn "setPreferredOrientations|screenOrientation|UISupportedInterfaceOrientations" . 2>/dev/null | head

# Dấu hiệu có bố cục thích ứng
grep -rEln "WindowSizeClass|NavigationRail|NavigationSuiteScaffold|ListDetailPaneScaffold|NavigationSplitView|horizontalSizeClass|LayoutBuilder" . 2>/dev/null | head
```

Những lệnh `grep` này chỉ là **tín hiệu**, không phải kết luận. Luôn mở file để xác nhận ngữ cảnh trước khi ghi thành lỗi.

### Chấm từ code: nguyên tắc

- Code cho thấy **ý định** → thường `confidence: medium`. Nâng lên `high` chỉ khi đã thấy kết quả render (Chế độ A/C) hoặc hành vi đó hiển nhiên từ code (ví dụ orientation bị khóa trong manifest).
- Nếu code có token spacing/typography nhưng màn hình hardcode đè lên → ghi ở `consistency_design_system`, nêu file:dòng.

---

## 4. Chế độ C — App đang chạy

Khi agent có shell với emulator/simulator. Các lệnh dưới đây thường dùng được; kiểm tra thiết bị tồn tại trước.

### Android (adb)

```bash
adb devices                                         # xác nhận thiết bị
adb exec-out screencap -p > shot.png                # chụp màn hình
adb shell wm size                                   # kích thước hiện tại
adb shell wm size 800x1280                          # giả lập kích thước tablet (nhớ reset)
adb shell wm density 160                            # đổi density khi cần
adb shell wm size reset && adb shell wm density reset
adb shell settings put system font_scale 2.0        # font scale tối đa phổ biến
adb shell settings put system font_scale 1.0        # reset
adb shell cmd uimode night yes                      # dark mode (no để tắt)
adb shell settings put global animator_duration_scale 0   # tắt animation (để test reduce motion)
adb shell uiautomator dump /sdcard/ui.xml && adb pull /sdcard/ui.xml   # cây UI: bounds, content-desc, clickable
```

`uiautomator dump` rất hữu ích: từ `bounds="[x1,y1][x2,y2]"` tính được **kích thước vùng chạm thật** (pixel ÷ density = dp) và liệt kê element `clickable="true"` thiếu `content-desc` — bằng chứng `high` cho `touch_interaction` và `accessibility`.

### iOS (simctl)

```bash
xcrun simctl list devices booted
xcrun simctl io booted screenshot shot.png
xcrun simctl ui booted appearance dark              # dark mode (light để về)
xcrun simctl ui booted content_size accessibility-extra-extra-extra-large   # Dynamic Type lớn nhất
xcrun simctl ui booted content_size large           # reset
xcrun simctl boot "iPad Pro 11-inch (M4)"           # tên thiết bị tuỳ máy; xem `simctl list devices`
```

Với iOS, kích thước vùng chạm/nhãn accessibility được kiểm bằng Accessibility Inspector hoặc XCUITest — nếu không chạy được, ghi `medium`.

### Flutter / React Native

- Flutter: `flutter run -d <device>`; widget inspector; `flutter test` golden tests với nhiều kích thước (`tester.view.physicalSize`), `MediaQuery` override cho `textScaler`.
- React Native: chạy bằng emulator như trên; kiểm `useWindowDimensions` tại nhiều kích thước; Dynamic Type/font scale đặt ở hệ điều hành.

### Quy trình chụp có hệ thống

1. Đặt thiết bị về trạng thái chuẩn (light, font 1.0, kích thước P-M).
2. Chạy từng flow, chụp mỗi bước, lưu theo `evidence/<thiết bị>/<flow>-<bước>.png`.
3. Lặp lại với các biến thể ở `platform-checks.md` (P-S, T-P, T-L, font 2.0, dark).
4. Với mỗi biến thể, ghi lại ngay các lỗi phát hiện, đừng đợi cuối.
5. **Reset thiết bị** về cài đặt gốc sau khi xong (size/density/font_scale), để không làm hỏng môi trường của người dùng.

### Đo hiệu năng cảm nhận (`performance_perceived`)

Chỉ chấm trên 3.0–3.5 khi đã **đo**, không phải đoán. Tên lệnh/đầu ra có thể khác chút theo phiên bản công cụ — nếu lệnh không chạy, ghi `medium`/`low` và nói rõ vì sao.

```bash
# Android — khởi động nguội (thay PKG/ACTIVITY)
PKG=com.example.app; ACT=.MainActivity
adb shell am force-stop $PKG
adb shell am start -W -n $PKG/$ACT                 # xem TotalTime (ms) = cold start

# Android — độ mượt khi cuộn/thao tác luồng chính
adb shell dumpsys gfxinfo $PKG reset
#   ... cuộn danh sách chính, chuyển màn trong 30–60 giây ...
adb shell dumpsys gfxinfo $PKG | grep -E "Total frames|Janky frames|percentile"

# Android — bộ nhớ
adb shell dumpsys meminfo $PKG | grep -E "TOTAL|Java Heap|Native Heap"

# Mạng chập chờn / offline (Wi-Fi emulator)
adb shell svc wifi disable        # offline;  svc wifi enable để bật lại
```

- **Flutter:** `flutter run --profile` rồi mở DevTools → Performance (frame > 16ms ở 60Hz là rớt); `flutter run --profile --trace-startup` ghi thời gian tới frame đầu vào `build/start_up_info.json`.
- **React Native:** Perf Monitor trong dev menu, React DevTools Profiler, Hermes profiler; chạy bản release để số đo có nghĩa.
- **iOS:** Instruments → Animation Hitches / Time Profiler; Network Link Conditioner để giả lập mạng chậm; MetricKit nếu có dữ liệu thật.
- **Compose:** Macrobenchmark (`StartupTimingMetric`, `FrameTimingMetric`) nếu dự án có sẵn.
- **Dữ liệu cực trị:** nạp 0 / 1 / 10.000 mục, chuỗi rất dài, ảnh rất lớn; nhìn xem có treo, cuộn giật hay tràn bộ nhớ.
- **Tablet:** lặp lại phép đo cuộn và kéo đổi kích thước/xoay trên emulator tablet, vì màn lớn dựng nhiều thứ hơn.

### Chụp dark mode (`theming_dark_mode`)

Chụp cùng các màn hình ở light và dark, **cả mobile lẫn tablet**, kể cả dialog, bottom sheet, thanh trạng thái, splash, màn có ảnh/logo, chart/WebView/bản đồ. Đổi theme lúc app đang chạy để kiểm tra không nháy trắng và không mất state.

---

## 5. Chế độ D — Figma / mockup

- Chỉ đánh giá được thiết kế, không phải sản phẩm cuối. Hạ `confidence` về `medium` cho các mục phụ thuộc hành vi (feedback, motion, adaptive thật).
- Kiểm tra: có đủ frame cho cả phone và tablet không (thiếu → ghi "không có thiết kế tablet" — bản thân đó là phát hiện cho `adaptive_responsive`); có đủ trạng thái (empty/error/loading) không; component/variables có được dùng không; auto-layout/constraints có cho thấy ý định responsive không.
- Contrast: lấy mã màu từ style/fill → `contrast.py`.

---

## 6. Gán ID bằng chứng

Dùng tiền tố để dễ truy vết:

| Tiền tố | Ý nghĩa | Ví dụ |
|---|---|---|
| `S-` | Screenshot | `S-cart-P-S` (màn Cart, phone nhỏ) |
| `C-` | Code (`file:dòng`) | `C-lib/theme.dart:41` |
| `R-` | Kết quả chạy/đo (uiautomator, script) | `R-uiautomator-home: 5 element clickable thiếu content-desc` |
| `F-` | Figma/mockup | `F-frame-Checkout-Tablet` |
| `X-` | Kết quả `contrast.py` | `X-caption-gray-on-white: 2.9:1` |

Trong scorecard, mỗi mục `evidence` là một chuỗi ngắn bắt đầu bằng ID rồi nêu quan sát.

---

## 7. Bảng "đo được gì, tin được đến đâu"

| Tiêu chí | Screenshot | Code | Chạy thật | Figma |
|---|---|---|---|---|
| Hierarchy & layout | ★★★ | ★ | ★★★ | ★★ |
| Typography | ★★★ | ★★ | ★★★ | ★★ |
| Color & contrast | ★★ (lấy mẫu pixel) | ★★★ (token) | ★★★ | ★★★ |
| Navigation & IA | ★★ | ★★ | ★★★ | ★★ |
| Touch & interaction | ★ | ★★ | ★★★ (uiautomator) | ★ |
| Feedback / states / motion | ★ | ★★ | ★★★ | ★ |
| Accessibility | ★ | ★★ | ★★★ | ★ |
| Consistency / design system | ★★ | ★★★ | ★★ | ★★★ |
| Content & microcopy | ★★★ | ★★ | ★★★ | ★★★ |
| Adaptive / responsive | ★ (chỉ thấy cái được chụp) | ★★ | ★★★ | ★ |
| Hiệu năng cảm nhận | ★ | ★★ (virtualization, ảnh, rebuild) | ★★★ (số đo thật) | ★ |
| Theming & dark mode | ★★★ (nếu có ảnh dark) | ★★★ (token vs hardcode) | ★★★ | ★★ |

★★★ = đủ để `high`; ★★ = tối đa `medium` trừ khi bổ sung bằng chứng khác; ★ = `low` nếu đây là nguồn duy nhất.
