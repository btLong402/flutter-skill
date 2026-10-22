# Rubric chấm điểm UI/UX Mobile + Tablet (v2 — 12 tiêu chí)

## Mục lục
1. Thang điểm và cách hiệu chỉnh
2. Bảng trọng số
3. Chi tiết 12 tiêu chí
4. Mức độ nghiêm trọng của lỗi
5. Trần điểm (caps) và hạng
6. Tên gọi khác (alias) và cách ghi khoảng trống rubric
7. Lịch sử phiên bản

---

## 1. Thang điểm và cách hiệu chỉnh

Mỗi tiêu chí chấm **0–5, bước 0.5**, riêng cho từng nền tảng (mobile, tablet).

| Điểm | Ý nghĩa |
|---|---|
| 0 | Không có hoặc hỏng hoàn toàn (vd: không thể đọc/không thể chạm) |
| 1 | Nhiều lỗi nghiêm trọng, ảnh hưởng hoàn thành tác vụ chính |
| 2 | Dùng được nhưng lỗi rõ ràng, lặp lại ở nhiều màn hình |
| 3 | **Mức tối thiểu chấp nhận được.** Đúng cơ bản, còn lỗi nhỏ lặp lại. Đây là điểm mặc định khi chưa đủ bằng chứng |
| 4 | Tốt. Chỉ còn lỗi nhỏ lẻ tẻ, không ảnh hưởng tác vụ |
| 5 | Xuất sắc. Đã kiểm chứng trên cả ma trận thiết bị, soi kỹ vẫn không tìm ra lỗi đáng kể |

**Hiệu chỉnh:** app thương mại trung bình ≈ 3.0–3.5. App được khen về UX ≈ 4.0–4.5. Điểm 5 chỉ dành cho thứ thực sự không tìm ra lỗi.

**Giới hạn theo độ tin cậy (script tự áp):** `confidence: low` → tối đa 3.5; `medium` → tối đa 4.0; `high` → không giới hạn.
- `high`: đã nhìn thấy/đo trực tiếp trên thiết bị hoặc screenshot thật, hoặc đọc đúng code quyết định hành vi đó.
- `medium`: suy ra từ code/design mà chưa thấy kết quả render, hoặc chỉ thấy một phần các trạng thái.
- `low`: suy đoán, hoặc nền tảng đó không có bằng chứng.

---

## 2. Bảng trọng số (tổng 100, rubric v2)

| Key | Tiêu chí | Trọng số |
|---|---|---|
| `visual_hierarchy_layout` | Thứ bậc thị giác & bố cục | 10 |
| `typography` | Typography | 7 |
| `color_contrast` | Màu sắc & độ tương phản | 7 |
| `navigation_ia` | Điều hướng & kiến trúc thông tin | 11 |
| `touch_interaction` | Tương tác chạm & công thái học | 11 |
| `feedback_states_motion` | Phản hồi, trạng thái & chuyển động | 9 |
| `accessibility` | Khả năng tiếp cận | 14 |
| `consistency_design_system` | Nhất quán & design system | 7 |
| `content_microcopy` | Nội dung & microcopy | 5 |
| `adaptive_responsive` | Thích ứng đa kích thước (phone↔tablet, hướng, split view) | 10 |
| `performance_perceived` | Hiệu năng cảm nhận & độ mượt (mới ở v2) | 5 |
| `theming_dark_mode` | Theming & Dark mode (mới ở v2) | 4 |

Điểm nền tảng = Σ (trọng số × điểm/5). Điểm tổng = trung bình có trọng số của các nền tảng (mặc định 50/50).

---

## 3. Chi tiết 12 tiêu chí

Mỗi tiêu chí có: mốc 1 / 3 / 5 để neo điểm, và checklist để soi. Điểm 2 và 4 nằm giữa các mốc; điểm .5 dùng khi hai mức đều đúng một phần.

### 3.1 Thứ bậc thị giác & bố cục (10) — `visual_hierarchy_layout`

- **1:** Mọi thứ cùng "độ to"; không biết nhìn đâu trước; CTA chính lẫn trong nội dung; khoảng cách lộn xộn.
- **3:** Có một điểm nhấn chính mỗi màn hình; nhóm nội dung rõ nhưng spacing còn lệch ở vài chỗ; còn màn hình hơi chật hoặc hơi trống.
- **5:** Mắt đi đúng thứ tự ưu tiên trong 3 giây; mỗi màn hình có đúng một hành động chính nổi bật; spacing theo scale nhất quán; nhóm bằng proximity/whitespace thay vì viền thừa.

Checklist:
- [ ] Mỗi màn hình có **một** primary action rõ ràng (không 2–3 nút cùng nổi).
- [ ] Squint test: làm mờ screenshot, vẫn thấy thứ quan trọng nhất.
- [ ] Spacing theo thang (4/8dp), không có giá trị lẻ ngẫu nhiên (13, 17, 22…).
- [ ] Căn lề nhất quán (cùng một lề trái/phải cho nội dung cùng cấp).
- [ ] Mật độ phù hợp: không nhồi quá nhiều lựa chọn; danh sách dài có nhóm/section.
- [ ] Nội dung không bị che bởi status bar, notch, home indicator, bàn phím (safe area).
- [ ] Ảnh/icon không vỡ tỉ lệ, không bị cắt mất phần quan trọng.

### 3.2 Typography (7) — `typography`

- **1:** Chữ quá nhỏ (<11), >5 cỡ chữ lộn xộn, dòng dày đặc không ngắt đoạn, chữ cắt/chồng.
- **3:** Có thang cỡ chữ cơ bản; body đọc được; còn vài chỗ caption/label quá nhỏ hoặc line-height chật.
- **5:** Thang type rõ (3–6 cấp) dùng nhất quán qua token; body ≥ 16sp/17pt; line-height 1.4–1.6; độ dài dòng 45–75 ký tự; dùng Dynamic Type/font scale; tiếng Việt có dấu không bị cắt.

Checklist:
- [ ] Body ≥ 16sp (Android) / 17pt (iOS); chữ nội dung tối thiểu 12; không dùng chữ <11 cho thông tin cần đọc.
- [ ] Tối đa 2 font family; trọng lượng chữ (weight) phân cấp rõ, không chỉ dựa vào màu.
- [ ] Line-height ≥ 1.4 cho body (với tiếng Việt: ≥ 1.4 để dấu không bị cắt/chạm dòng trên).
- [ ] Tablet: nội dung đọc dài không trải hết chiều ngang (giới hạn ~ 600–720dp, 45–75 ký tự/dòng).
- [ ] Căn lề trái cho đoạn văn (không justify/center cho đoạn dài).
- [ ] Số liệu/tiền tệ/ngày giờ căn chỉnh, dùng tabular figures khi so sánh cột.
- [ ] Truncation có chủ đích (ellipsis + cách xem đầy đủ), không cắt ở thông tin then chốt (giá, tên).

### 3.3 Màu sắc & độ tương phản (7) — `color_contrast`

- **1:** Nhiều văn bản/nút không đạt contrast; dùng màu là cách duy nhất truyền tải trạng thái.
- **3:** Text chính đạt 4.5:1; placeholder/caption/disabled còn vài chỗ yếu; có màu ngữ nghĩa nhưng chưa thật nhất quán.
- **5:** Mọi text ≥ 4.5:1 (large text ≥ 3:1), thành phần UI/viền input/focus ≥ 3:1; palette có vai trò rõ (primary/surface/on-surface/error…); trạng thái luôn có thêm icon/chữ ngoài màu; đạt chuẩn ở **cả hai theme** (light và dark). Chất lượng dark mode về mặt thiết kế chấm ở 3.12.

Checklist (**đo bằng `scripts/contrast.py`**, không ước lượng):
- [ ] Text thường ≥ 4.5:1; text lớn (≥ 24px, hoặc ≥ 18.66px đậm) ≥ 3:1.
- [ ] Placeholder, caption, link, text trên ảnh/gradient cũng đạt.
- [ ] Viền input, icon chức năng, focus indicator ≥ 3:1 so với nền kề.
- [ ] Không chỉ dùng màu để phân biệt (đỏ/xanh → thêm icon, nhãn).
- [ ] Số màu nhấn có kiểm soát (thường 1 accent chính + màu ngữ nghĩa).
- [ ] Chạy lại phép đo contrast cho **từng theme** (light, dark, và high-contrast nếu có) — kết quả đạt ở theme này không suy ra cho theme kia. (Thiết kế dark mode: xem 3.12.)
- [ ] Màu error/success/warning đạt contrast trên nền thực tế của chúng.

### 3.4 Điều hướng & kiến trúc thông tin (11) — `navigation_ia`

- **1:** Không biết mình đang ở đâu; không quay lại được; tính năng quan trọng bị chôn sâu; nhãn mơ hồ.
- **3:** Cấu trúc điều hướng chuẩn (tab/stack); biết mình đang ở đâu; còn vài chỗ vào/ra gượng hoặc nhãn chưa rõ.
- **5:** Việc chính ≤ 3 chạm từ màn hình chủ; trạng thái hiện tại luôn rõ; back/gesture hành xử đúng chuẩn nền tảng; deep link/khôi phục trạng thái ổn; điều hướng tablet tận dụng không gian (rail/sidebar, list-detail).

Checklist:
- [ ] 3–5 đích chính ở thanh điều hướng cấp cao nhất (bottom bar/rail/sidebar); không nhồi >5.
- [ ] Mục đang chọn được đánh dấu rõ (không chỉ bằng đổi màu nhẹ).
- [ ] Nút/cử chỉ Back luôn đưa về đúng nơi người dùng mong đợi (iOS swipe-back, Android system back/predictive back).
- [ ] Việc thường làm nhất ≤ 3 chạm; không có ngõ cụt (dead-end).
- [ ] Nhãn điều hướng là từ người dùng hiểu, không phải thuật ngữ nội bộ.
- [ ] Modal/bottom sheet có cách đóng rõ ràng, không kẹt người dùng.
- [ ] Quay lại màn hình trước giữ nguyên scroll/filter/form đang nhập.
- [ ] Tìm kiếm có mặt khi nội dung nhiều; kết quả rỗng có hướng dẫn.
- [ ] Onboarding/đăng nhập: không bắt đăng ký trước khi cho thấy giá trị (nếu phù hợp), có "bỏ qua".

### 3.5 Tương tác chạm & công thái học (11) — `touch_interaction`

- **1:** Vùng chạm nhỏ (<32), nút sát nhau gây bấm nhầm; hành động chính ở chỗ khó với; thao tác phá hủy không có bảo vệ.
- **3:** Hầu hết target ≥ 44/48; vài icon-button nhỏ hoặc sát nhau; có thể với được hành động chính nhưng chưa tối ưu.
- **5:** Mọi target ≥ 48dp (Android) / 44pt (iOS) và cách nhau ≥ 8dp; hành động chính trong tầm ngón cái; gesture có thay thế bằng nút; thao tác phá hủy có undo hoặc xác nhận; form dùng đúng loại bàn phím/autofill.

Checklist:
- [ ] Vùng chạm ≥ 48×48dp / 44×44pt (có thể dùng hit-slop mở rộng cho icon nhỏ). Mức sàn WCAG 2.2 AA: 24×24 CSS px.
- [ ] Khoảng cách giữa các target liền kề ≥ 8dp.
- [ ] Hành động chính ở nửa dưới màn hình / vùng với tới bằng ngón cái (đặc biệt phone lớn). Hành động phá hủy tránh nằm ngay chỗ dễ bấm nhầm.
- [ ] Gesture ẩn (swipe, long-press) luôn có đường thay thế hiển thị (nút/menu).
- [ ] Thao tác phá hủy: undo (snackbar) tốt hơn hộp thoại xác nhận; xác nhận chỉ khi không thể hoàn tác.
- [ ] Form: bàn phím đúng loại (email, number, phone), `autofill`/`textContentType`, nút Next/Done, scroll để input không bị bàn phím che.
- [ ] Không bắt người dùng gõ lại thứ app đã biết; dùng picker/stepper/segmented thay vì gõ khi hợp lý.
- [ ] Tablet: target không bị phình quá to một cách vô nghĩa; hỗ trợ hover/pointer và phím (Tab, Enter, Esc) khi dùng bàn phím/chuột.
- [ ] Không có vùng chạm chồng lấn với cử chỉ hệ thống (mép màn hình, home indicator).

### 3.6 Phản hồi, trạng thái & chuyển động (9) — `feedback_states_motion`

- **1:** Bấm không biết có ăn không; màn hình trắng khi tải; lỗi im lặng hoặc chỉ "Đã xảy ra lỗi"; animation giật hoặc chặn thao tác.
- **3:** Có loading/spinner và thông báo lỗi cơ bản; empty state còn sơ sài; chuyển động không gây hại nhưng chưa có chủ đích.
- **5:** Mọi hành động có phản hồi < 100ms (pressed state); loading dùng skeleton khi > 1s, progress thật khi dài; empty/error/offline/success đều được thiết kế, có hướng đi tiếp; chuyển động ngắn (150–300ms), giải thích quan hệ không gian, tôn trọng "reduce motion".

Checklist:
- [ ] Pressed/focus/disabled state hiển thị rõ cho mọi phần tử tương tác.
- [ ] **4 trạng thái cho mỗi màn dữ liệu:** loading, empty, error, success — đã thiết kế đủ.
- [ ] Lỗi nêu: chuyện gì xảy ra + cách khắc phục + nút thử lại; giữ lại dữ liệu người dùng đã nhập.
- [ ] Offline/mạng yếu: có thông báo và hành vi hợp lý (cache, hàng đợi).
- [ ] Loading > 1s dùng skeleton/progress; > 10s dùng progress xác định + hủy được.
- [ ] Optimistic update cho thao tác nhẹ (like, bật/tắt), rollback có thông báo khi thất bại.
- [ ] Animation 150–300ms (chuyển màn ≤ 400ms), không chặn input; dùng easing tự nhiên; không nhấp nháy >3 lần/giây.
- [ ] Tôn trọng cài đặt Reduce Motion / Remove animations.
- [ ] Haptic dùng tiết chế, đúng chỗ (xác nhận, lỗi), không lạm dụng.

### 3.7 Khả năng tiếp cận (14) — `accessibility`

- **1:** Screen reader không dùng được (nút không nhãn, thứ tự lung tung); chữ không phóng to được; thông tin chỉ bằng màu.
- **3:** Phần lớn control có nhãn; font scale 130–150% còn dùng được; contrast cơ bản đạt; còn vài chỗ thứ tự focus/nhãn kém.
- **5:** Dùng được trọn vẹn bằng VoiceOver/TalkBack; font scale 200% không mất chức năng; contrast đạt; hỗ trợ bàn phím/switch; reduce motion; không phụ thuộc màu/âm thanh/cử chỉ đơn lẻ.

Checklist:
- [ ] Mọi control có tên truy cập có nghĩa (`accessibilityLabel` / `contentDescription` / `Semantics`), role đúng, trạng thái (đã chọn, bật/tắt, mở/đóng) được đọc ra.
- [ ] Icon trang trí được ẩn khỏi screen reader; icon chức năng có nhãn mô tả hành động ("Xóa", không phải "thùng rác").
- [ ] Thứ tự đọc/focus đúng với thứ tự thị giác; nhóm hợp lý (card = một đối tượng, không đọc 6 mảnh rời).
- [ ] **Font scale 200% / Dynamic Type lớn nhất:** không cắt cụt, không đè chữ, không mất nút; layout co giãn hoặc cuộn.
- [ ] Contrast & target size đạt (tham chiếu 3.3, 3.5).
- [ ] Lỗi form gắn với field và được đọc ra; không chỉ dựa vào màu đỏ.
- [ ] Thay đổi động (toast, cập nhật nội dung) được thông báo (live region / announcement).
- [ ] Không có timeout ngắn gây mất dữ liệu; gesture phức tạp có phương án đơn giản.
- [ ] Hỗ trợ bàn phím ngoài / Full Keyboard Access / Switch Control: focus nhìn thấy được và tab theo thứ tự hợp lý (rất quan trọng trên tablet).
- [ ] Video/audio có phụ đề/transcript khi có nội dung quan trọng.

### 3.8 Nhất quán & design system (7) — `consistency_design_system`

- **1:** Mỗi màn hình một kiểu nút/màu/khoảng cách; hành vi khác nhau cho cùng một việc.
- **3:** Có palette/component cơ bản, đa số màn hình thống nhất; còn component "mồ côi" và giá trị hardcode.
- **5:** Token (màu, spacing, radius, type, elevation) dùng xuyên suốt, không hardcode; component tái sử dụng; hành vi nhất quán; tuân thủ quy ước nền tảng (HIG / Material) ở chỗ người dùng kỳ vọng.

Checklist:
- [ ] Cùng một vai trò → cùng một component (mọi primary button giống nhau).
- [ ] Màu/spacing/radius/font lấy từ token/theme; ít hardcode (grep được trong code).
- [ ] Icon cùng một bộ, cùng độ dày nét, cùng kích thước theo ngữ cảnh.
- [ ] Thuật ngữ nhất quán (đã chọn "Giỏ hàng" thì không lẫn "Túi", "Cart").
- [ ] Hành vi tương đương (xóa, lưu, chia sẻ) giống nhau mọi nơi.
- [ ] Tôn trọng quy ước nền tảng: vị trí back, kiểu picker, dialog, share sheet, settings. Khác biệt có chủ đích và có lý do.
- [ ] Mobile và tablet cùng một ngôn ngữ thiết kế (chỉ khác bố cục, không khác "tính cách").

### 3.9 Nội dung & microcopy (5) — `content_microcopy`

- **1:** Nhãn mơ hồ, thuật ngữ kỹ thuật, thông báo lỗi vô nghĩa; văn phong lộn xộn; chữ cứng không dịch được.
- **3:** Nhãn nút và thông báo hiểu được; giọng điệu tạm ổn; còn vài chỗ chung chung hoặc dài dòng.
- **5:** Nhãn nút là động từ cụ thể ("Lưu thay đổi"); lỗi nói rõ nguyên nhân + cách sửa; giọng điệu nhất quán; có thể dịch/mở rộng chuỗi mà layout không vỡ; không có chữ thừa.

Checklist:
- [ ] Nút dùng động từ cụ thể, không "OK/Submit/Tiếp tục" mơ hồ khi có lựa chọn tốt hơn.
- [ ] Thông báo lỗi: nguyên nhân + việc cần làm; không đổ lỗi người dùng; không mã lỗi trần.
- [ ] Empty state giải thích + gợi ý hành động đầu tiên.
- [ ] Giọng điệu thống nhất (xưng hô, mức trang trọng) toàn app.
- [ ] Không lặp ý giữa tiêu đề/mô tả/nút; mỗi chuỗi chỉ nói điều cần.
- [ ] Chuỗi không hardcode trong layout; chịu được mở rộng ~30–40% khi dịch; tiếng Việt kiểm tra riêng (dấu, từ dài).
- [ ] Định dạng ngày/giờ/tiền/số theo locale (vd: `15/10/2026`, `1.250.000 ₫`).
- [ ] Quyền (permission) có giải thích lý do trước khi xin, đúng thời điểm cần.

### 3.10 Thích ứng đa kích thước (10) — `adaptive_responsive`

- **1:** Layout vỡ/lệch khi đổi cỡ màn hình, xoay, hoặc split view; tablet là UI phone bị kéo giãn, thừa khoảng trắng khổng lồ.
- **3:** Chạy được đúng trên phone và tablet, xoay không vỡ; tablet có tối ưu nhẹ (max-width, lưới nhiều cột) nhưng chưa tận dụng điều hướng/bố cục kiểu tablet.
- **5:** Bố cục thích ứng theo **window size class** (không theo model thiết bị): compact → điều hướng dưới, medium/expanded → rail/sidebar, list-detail/supporting pane khi đủ rộng; hỗ trợ xoay, split view/slide over/cửa sổ nhiều kích thước, font scale lớn; state được giữ qua thay đổi cấu hình.

Checklist:
- [ ] Kiểm tra theo ma trận thiết bị (xem `platform-checks.md`): phone nhỏ, phone lớn, tablet dọc/ngang, split view 1/3 & 1/2.
- [ ] Dùng window size class (Compact <600dp, Medium 600–839dp, Expanded ≥840dp) hoặc size class tương đương iOS, thay vì hardcode theo thiết bị.
- [ ] Tablet: tận dụng không gian (list-detail, nhiều cột, sidebar/rail), không chỉ phóng to phone UI.
- [ ] Giới hạn chiều rộng nội dung đọc/form trên màn lớn (không form kéo hết 1200dp).
- [ ] Xoay màn hình không mất state, không crash, không bố cục lệch; phone landscape vẫn dùng được (đặc biệt form + bàn phím).
- [ ] Split View / Slide Over (iPad), multi-window/resizable (Android) không vỡ ở độ rộng hẹp.
- [ ] Ảnh/video có tỉ lệ & độ phân giải phù hợp cho màn lớn (không mờ).
- [ ] Font scale lớn + màn nhỏ (360dp) + chuỗi dài không làm vỡ layout.
- [ ] Safe area/notch/dynamic island/gesture bar/foldable hinge được xử lý ở mọi hướng.

### 3.11 Hiệu năng cảm nhận & độ mượt (5) — `performance_perceived`

Chấm **cảm giác của người dùng** (đứng hình, giật, chờ lâu, treo ở dữ liệu cực trị), không phải benchmark kỹ thuật thuần túy. Đây là tiêu chí bằng chứng dựa nhiều vào đo/chạy thật; xem bảng đo ở `evidence-collection.md`.

- **1:** Khởi động > 5s màn trắng; cuộn giật rõ; tương tác trễ > 300ms; treo/ANR/crash khi dữ liệu lớn, ảnh lớn hoặc mạng chậm.
- **3:** Cold start ~2–4s có splash/skeleton; cuộn mượt với dữ liệu thường nhưng giật ở danh sách dài/ảnh nặng; vài thao tác trễ nhẹ; chưa kiểm thiết bị yếu/mạng chậm.
- **5:** Thấy nội dung hữu ích < 2s (cache/skeleton); frame ổn định (60fps, 90/120Hz nếu màn cao), tỉ lệ janky frame thấp ở các luồng chính; phản hồi chạm < 100ms; chịu tốt dữ liệu cực trị (0 / 1 / 10.000 mục, ảnh lớn, mạng 3G/offline) và thiết bị cấu hình thấp; xoay/resize không giật.

Checklist:
- [ ] **Khởi động:** cold start và warm start đo được; có nội dung/skeleton trước khi dữ liệu mạng về; không màn trắng.
- [ ] **Cuộn:** danh sách dài dùng virtualization/lazy (`ListView.builder`, `FlatList`/`FlashList`, `LazyColumn`, `LazyVStack`/`List`); không dựng toàn bộ item.
- [ ] **Ảnh:** có cache, thu nhỏ đúng kích thước hiển thị (không tải ảnh 4000px để hiện 100px), placeholder khi tải, giải mã ngoài main thread.
- [ ] **Phản hồi:** thao tác chạm đổi trạng thái < 100ms; tác vụ nặng không chạy trên main/UI thread.
- [ ] **Dữ liệu cực trị (edge cases):** 0 mục, 1 mục, rất nhiều mục (≥ 10k), chuỗi rất dài, ảnh rất lớn, payload lớn — không treo, không tràn bộ nhớ, giao diện vẫn đúng.
- [ ] **Mạng/thiết bị:** mạng chậm/chập chờn/offline xử lý êm (timeout hợp lý, hủy được, không khoá UI); thử trên thiết bị tầm thấp hoặc emulator hạn chế CPU/RAM nếu có.
- [ ] **Animation:** không rớt frame khi chạy chuyển cảnh/animation; hiệu ứng nặng (blur, shadow lớn, nhiều lớp trong suốt) không phá frame rate.
- [ ] **Rebuild thừa:** không rebuild/recompose cả màn hình cho thay đổi nhỏ (theo dõi qua profiler hoặc đọc code).
- [ ] **Tablet:** màn lớn render nhiều pane/cột/ảnh hơn → đo lại; kéo đổi kích thước cửa sổ và xoay không giật, không tải lại dữ liệu vô cớ.
- [ ] **Pin/nhiệt (nếu đo được):** không loop làm nóng máy, không polling dày khi nền.

### 3.12 Theming & Dark mode (4) — `theming_dark_mode`

Chấm **chất lượng hệ thống theme**: dark mode, khả năng đổi theme, và độ phủ trên mọi thành phần. (Contrast đo ở 3.3; ở đây chấm thiết kế và độ phủ.)

- **1:** Không có dark mode, hoặc có nhưng hỏng (chữ vô hình, nền trắng chói lẫn vào, nhiều màn hardcode màu sáng); không theo cài đặt hệ thống.
- **3:** Theo cài đặt hệ thống; đa số màn hình ổn; còn sót thành phần chưa đổi theme (dialog, bottom sheet, status/nav bar, ảnh/logo, chart, WebView, bản đồ); chưa kiểm contrast ở dark.
- **5:** Light/Dark dùng token ngữ nghĩa (`surface`, `onSurface`, `primary`…) thay vì màu cố định; surface phân tầng theo độ cao; mọi thành phần và nội dung nhúng thích ứng; đổi theme tức thời không mất state, không nháy trắng; có tùy chọn trong app (Hệ thống / Sáng / Tối); hỗ trợ Increase Contrast/high contrast; mobile và tablet cùng một theme nhất quán.

Checklist:
- [ ] Theo `prefers-color-scheme`/chế độ hệ thống mặc định; đổi lúc đang chạy không cần khởi động lại.
- [ ] Không dùng màu cố định cho nền/chữ ngoài token (grep hex hardcode — xem `evidence-collection.md`).
- [ ] Dark surface không phải `#000` thuần cho mọi lớp; dùng phân tầng elevation (lớp cao sáng hơn); chữ không trắng `#FFF` chói trên nền đen — ưu tiên on-surface ~87% độ sáng.
- [ ] Giảm độ bão hòa màu nhấn trong dark; kiểm lại màu ngữ nghĩa (error/success/warning).
- [ ] Ảnh, logo, minh họa, icon có biến thể dark hoặc nền trung tính; ảnh sáng không chói; ảnh PNG nền trong suốt không biến mất.
- [ ] Status bar / navigation bar / splash / launch screen / keyboard appearance đổi theo theme.
- [ ] Thành phần nhúng: chart, bản đồ, WebView, PDF viewer, date picker hệ thống đều theo theme.
- [ ] Skeleton/shimmer, divider, shadow, trạng thái pressed/focus/disabled đều đọc được ở cả hai theme.
- [ ] Có tuỳ chọn theme trong Settings và nhớ lựa chọn; (Android) dynamic color nếu app chọn hỗ trợ; (iOS) tôn trọng tint/accent hệ thống ở chỗ hợp lý.
- [ ] Cả hai theme được chụp ở **cả mobile và tablet** — không giả định dark đúng chỉ vì light đúng.

---

## 4. Mức độ nghiêm trọng của lỗi

| Mức | Định nghĩa | Ví dụ |
|---|---|---|
| `blocker` | Chặn hoàn thành luồng chính, hoặc loại trừ cả nhóm người dùng | CTA thanh toán bị bàn phím che không cuộn được; nút không có nhãn trong flow chính với screen reader; layout tablet vỡ khiến không bấm được nút; ANR/crash khi mở danh sách lớn |
| `major` | Gây sai/mất thời gian rõ rệt, nhiều người gặp | Target chính 32dp; contrast 2.5:1 ở text chính; không có trạng thái lỗi khi mất mạng; cuộn danh sách chính rớt frame rõ; dark mode có màn chữ trùng màu nền |
| `minor` | Gây khó chịu nhưng có cách vượt qua | Spacing lệch giữa hai màn; icon không nhất quán; caption hơi nhỏ |
| `polish` | Tinh chỉnh, không ảnh hưởng chức năng | Easing chưa mượt; ảnh empty state chưa đẹp |

Khi chưa chắc, chọn mức **thấp hơn một bậc** nhưng ghi rõ lý do — tránh báo động giả làm nhiễu backlog.

---

## 5. Trần điểm (caps) và hạng

`score.py` áp các trần sau cho từng nền tảng (lấy giá trị thấp nhất nếu nhiều trần cùng áp):

| Điều kiện | Trần điểm nền tảng |
|---|---|
| Có ≥ 1 issue `blocker` còn mở (`status` ≠ fixed/wontfix) chạm nền tảng đó | **59** |
| Có tiêu chí điểm hiệu lực ≤ 1.5 | **69** |
| Tiêu chí `accessibility` < 3 | **79** |

Lý do: một lỗi chặn hoặc một tiêu chí sụp đổ không được "bù" bằng các tiêu chí khác; app không dùng được với screen reader thì không nên được gọi là "tốt" dù đẹp.

| Điểm | Hạng |
|---|---|
| 90–100 | Xuất sắc |
| 80–89 | Tốt |
| 70–79 | Đạt |
| 60–69 | Cần cải thiện |
| < 60 | Kém |

---

## 6. Tên gọi khác (alias) và cách ghi khoảng trống rubric

Agent đôi khi gọi tiêu chí bằng tên riêng. `score.py` tự quy các tên sau về khoá chuẩn (và nhắc trong phần Cảnh báo) — nhưng hãy dùng khoá chuẩn ở bảng trọng số.

| Tên hay gặp | Khoá chuẩn |
|---|---|
| `tablet_adaptive`, `responsive_tablet`, `responsive`, `adaptive`, `tablet_layout` | `adaptive_responsive` |
| `consistency_standards`, `consistency`, `design_system` | `consistency_design_system` |
| `feedback_status`, `feedback`, `states`, `motion` | `feedback_states_motion` |
| `performance_smoothness`, `performance_edge_cases`, `performance`, `smoothness` | `performance_perceived` |
| `dark_mode_theming`, `dark_mode`, `theming`, `theme` | `theming_dark_mode` |

Khi quy nhiều tên về cùng một khoá chuẩn (ví dụ `performance_smoothness` và `performance_edge_cases`), script lấy **điểm thấp hơn** cho mỗi nền tảng để không che lỗi.

**Nếu thấy một khía cạnh thực sự chưa có trong rubric:** đừng tạo khoá mới trong `scores` (nó sẽ bị bỏ qua). Hãy ghi vào mảng `rubric_gaps` của scorecard:

```json
"rubric_gaps": [
  {"name": "tên ngắn của khía cạnh", "platform": "tablet", "reason": "vì sao không tiêu chí nào hiện có chứa nó, ví dụ cụ thể"}
]
```

Báo cáo sẽ hiển thị mục này ở phần "Đề xuất bổ sung rubric" để người dùng quyết định có thêm vào rubric hay không. Lúc chấm vẫn xếp lỗi liên quan vào tiêu chí gần nhất.

## 7. Lịch sử phiên bản

| Phiên bản | Thay đổi |
|---|---|
| v1 | 10 tiêu chí |
| v2 | Thêm `performance_perceived` (5) và `theming_dark_mode` (4); giảm nhẹ trọng số các tiêu chí khác để tổng giữ 100; chuyển phần đánh giá dark mode khỏi `color_contrast` sang `theming_dark_mode` (contrast từng theme vẫn đo ở 3.3); thêm bảng alias và cơ chế `rubric_gaps`. Nguồn: báo cáo khoảng trống thu thập từ agent khi chạy skill (`export.csv`). |

Scorecard cũ (v1) vẫn chạy được: `score.py` nhận ra thiếu `rubric_version` và chấm theo trọng số v1. Điểm tổng giữa v1 và v2 **không so sánh trực tiếp** được; chấm lại một vòng theo v2 làm mốc mới.
