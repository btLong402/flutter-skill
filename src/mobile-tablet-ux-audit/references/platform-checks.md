# Kiểm tra riêng theo nền tảng: Mobile & Tablet

## Mục lục
1. Ma trận thiết bị tối thiểu
2. Ma trận trạng thái cần chụp
3. Kiểm tra riêng cho Mobile
4. Kiểm tra riêng cho Tablet
5. Quy ước iOS vs Android
6. Kiểm tra cho nội dung tiếng Việt

---

## 1. Ma trận thiết bị tối thiểu

Chọn **theo kích thước viewport**, không theo tên model — mục tiêu là phủ các điểm gãy bố cục.

| Mã | Loại | Viewport (dp/pt) | Vì sao |
|---|---|---|---|
| P-S | Phone nhỏ | 360×640 – 375×667 | Ca xấu nhất cho nội dung chật, bàn phím che form |
| P-M | Phone chuẩn | 390×844 | Điểm tham chiếu phổ biến |
| P-L | Phone lớn | 430×932 | Kiểm tra thumb zone, khoảng trống thừa |
| P-LS | Phone ngang | 844×390 | Form + bàn phím, safe area ngang |
| T-P | Tablet dọc | 768×1024 – 834×1194 | Medium window class (600–839dp) |
| T-L | Tablet ngang | 1024×768 – 1194×834 | Expanded (≥840dp): list-detail, sidebar |
| T-S3 | Tablet split 1/3 | ~ 320–400 rộng | Phải co về bố cục compact |
| T-S2 | Tablet split 1/2 | ~ 500–600 rộng | Ngưỡng giữa compact và medium |

Nếu ngân sách ít: tối thiểu **P-S, P-L, T-P, T-L**. Ghi rõ những cái đã bỏ qua và chấm `confidence` tương ứng.

Cạnh đó, kiểm tra **cho cả hai nền tảng** (chọn ít nhất một màn quan trọng):
- Font scale lớn nhất (Android 2.0×; iOS accessibility XXXL).
- Dark mode.
- Ngôn ngữ chuỗi dài (tiếng Việt/Đức), hoặc pseudo-localization (+40% độ dài).

## 2. Ma trận trạng thái cần chụp

Với mỗi flow chính, cố gắng có đủ:

| Trạng thái | Cách tạo |
|---|---|
| Bình thường (dữ liệu điển hình) | Dữ liệu mẫu thực tế |
| Dữ liệu cực trị | Tên rất dài, danh sách 0/1/200 mục, số tiền lớn, ảnh thiếu |
| Loading | Throttle mạng / delay giả |
| Empty | Tài khoản mới / xóa dữ liệu |
| Error | Tắt mạng / trả lỗi 500 / validate sai |
| Quyền bị từ chối | Từ chối camera/location/notification |
| Bàn phím mở | Focus vào input cuối form |
| Đang xoay / đổi kích thước cửa sổ | Xoay hoặc kéo split |

Không có đủ các trạng thái này, đừng chấm `feedback_states_motion` hay `adaptive_responsive` quá 3.5.

---

## 3. Kiểm tra riêng cho Mobile

**Thumb zone & công thái học**
- Hành động chính và điều hướng cấp cao nằm ở nửa dưới (bottom nav, bottom sheet, FAB) — đặc biệt phone ≥ 6.5".
- Tiêu đề/nút Back ở trên cùng khó với: phải có cử chỉ thay thế (swipe-back/predictive back).
- Không đặt nút phá hủy cạnh nút chính trong vùng dễ chạm.

**Màn hình & hệ thống**
- Safe area: status bar, notch/dynamic island, home indicator, gesture nav bar (Android edge-to-edge) không đè nội dung/nút.
- Bàn phím: input đang focus luôn nhìn thấy; nút gửi/tiếp tục không bị che; có cách đóng bàn phím.
- Xoay ngang: nếu app cho phép, form và nội dung vẫn dùng được.

**Hiệu năng cảm nhận**
- Khởi động có splash/skeleton hợp lý, không màn hình trắng.
- Cuộn mượt: không giật khi danh sách dài (60fps cảm nhận); ảnh lazy load có placeholder.

**Nội dung & cấu trúc**
- Một cột là chính; tránh bảng ngang cần cuộn ngang.
- Dùng bottom sheet/full-screen modal cho tác vụ ngắn thay vì dialog nhỏ nhiều nút.
- Form dài: chia bước hoặc nhóm section; hiển thị tiến độ.

---

## 4. Kiểm tra riêng cho Tablet

Đây là nơi hầu hết app mất điểm. Hãy soi kỹ.

**4.1 Bố cục — không chỉ phóng to phone**
- [ ] Có **bố cục tablet riêng** (list-detail, supporting pane, sidebar + content, lưới nhiều cột) khi width ≥ 600dp; không phải một cột trải hết ngang với chữ/nút khổng lồ.
- [ ] Nội dung đọc/form có `max-width` (~ 600–840dp) và căn giữa hoặc đặt cạnh pane khác — không dòng chữ dài 150 ký tự.
- [ ] Khoảng trắng hai bên có chủ đích; không bị "đảo nhỏ" nội dung giữa biển trống.
- [ ] Ảnh/hero độ phân giải đủ cho màn lớn (không mờ khi phóng).
- [ ] Master-detail: chọn mục ở list thì detail cập nhật tại chỗ, không đẩy sang màn mới; trạng thái chọn nhìn rõ; ở compact thì thu về navigation stack.

**4.2 Điều hướng**
- [ ] Medium/Expanded dùng **navigation rail / sidebar** thay vì bottom bar rộng 1000dp+ (Material: bottom bar cho compact; rail cho medium; rail hoặc drawer cho expanded; iOS: sidebar/`TabView` dạng sidebar trên iPad).
- [ ] Hành động không chỉ ở góc dưới phải/trái xa tầm với khi cầm bằng hai tay ở chế độ dọc; ở ngang thì cạnh hai bên mới dễ với.
- [ ] Chuyển giữa các kích cỡ (xoay/split) giữ nguyên đích đang xem, vị trí cuộn, và dữ liệu form.

**4.3 Đa nhiệm & cửa sổ**
- [ ] Split View / Slide Over (iPad), multi-window, free-form window (Android/ChromeOS) — layout chuyển mượt về compact khi cửa sổ hẹp, không vỡ ở độ rộng bất kỳ.
- [ ] Không khóa orientation trừ khi có lý do chính đáng (camera, game); khóa dọc trên tablet là lỗi thường gặp (Android khuyến nghị không giới hạn orientation cho màn lớn).
- [ ] Hỗ trợ thay đổi kích cỡ động (kéo cửa sổ), không giả định "tablet = ngang".
- [ ] Foldable (nếu nhắm tới): tôn trọng hinge/fold, tabletop posture, không đặt nội dung then chốt đè lên nếp gập.

**4.4 Nhập liệu**
- [ ] Hoạt động tốt với bàn phím ngoài: Tab/Shift-Tab, Enter gửi, Esc đóng, phím tắt cho hành động chính (iPad: menu bar/`keyboardShortcut`; Android: `onKeyEvent`/shortcut helper).
- [ ] Chuột/trackpad: hover state, con trỏ đổi theo ngữ cảnh, chuột phải/long-press mở menu ngữ cảnh.
- [ ] Bút (nếu app có vẽ/ghi chú): vùng vẽ, palm rejection, hover của Pencil.
- [ ] Drag & drop giữa các cửa sổ/ứng dụng (nếu phù hợp với nội dung).

**4.5 Hạt nhỏ cần soi**
- [ ] Dialog/popover: trên tablet dùng popover/anchored dialog kích cỡ vừa phải, không full-width 1000dp.
- [ ] Bàn phím ảo trên tablet ngang chiếm nửa màn hình — input vẫn nhìn thấy; bàn phím nổi/tách (iPad) không làm hỏng layout.
- [ ] Bảng/dữ liệu: dùng không gian để hiện nhiều cột hơn thay vì phóng to cột.
- [ ] Target không phình quá mức (nút 88dp trông kỳ cục) nhưng vẫn ≥ 48dp.

---

## 5. Quy ước iOS vs Android

Không ép cùng một kiểu trên hai nền tảng; người dùng mỗi bên có kỳ vọng riêng. Cross-platform app chỉ cần **không vi phạm** quy ước mà người dùng cảm nhận rõ.

| Hạng mục | iOS (HIG) | Android (Material 3) |
|---|---|---|
| Vùng chạm tối thiểu | 44×44pt | 48×48dp |
| Quay lại | Nút Back góc trên trái + swipe từ mép trái | Nút/cử chỉ Back hệ thống (predictive back) |
| Điều hướng chính | Tab bar dưới (≤5); sidebar trên iPad | Navigation bar dưới (3–5) / rail / drawer |
| Hành động nổi bật | Nút trong navigation bar hoặc trong nội dung | FAB hoặc extended FAB |
| Hộp thoại/lựa chọn | Action sheet, alert ngắn | Dialog, bottom sheet, menu |
| Cỡ chữ cơ sở | 17pt body, hỗ trợ Dynamic Type | 14–16sp body, hỗ trợ font scale |
| Phản hồi | Haptic nhẹ tiết chế | Ripple + haptic nhẹ |
| Chế độ hệ thống | Dark mode, Dynamic Type, Reduce Motion, Bold Text | Dark theme, font size, Remove animations, Dynamic color |
| Màn hình lớn | Size classes, Split View, Stage Manager | Window size classes, canonical layouts, multi-window |

---

## 6. Kiểm tra cho nội dung tiếng Việt

Chỉ áp dụng khi app hiển thị tiếng Việt, nhưng rất hay bị bỏ sót:

- **Dấu bị cắt:** dấu chồng (ệ, ữ, ẳ, Ấ…) bị cắt ở đầu/đáy dòng khi `line-height` quá chật hoặc `height` cố định → body line-height ≥ 1.4, tiêu đề ≥ 1.25, không đặt `height` cứng cho Text.
- **Font hỗ trợ đủ glyph tiếng Việt** (kiểm tra cả weight đậm, in nghiêng); không rơi về font hệ thống làm lệch thẩm mỹ.
- **Độ dài chuỗi:** tiếng Việt thường dài hơn tiếng Anh khoảng 15–30% — nút, tab, nhãn có đủ chỗ hay bị cắt "Thanh toá…"?
- **Tách từ khi xuống dòng:** tránh ngắt giữa âm tiết trong từ ghép ngắn khi có thể (dùng non-breaking space cho cụm như "10 000 ₫" hoặc "Điều khoản & Điều kiện" nếu cần).
- **Định dạng:** ngày `dd/MM/yyyy`, số dùng dấu chấm ngăn nghìn `1.250.000`, tiền `₫` đặt sau số; múi giờ nhất quán.
- **Nhập liệu:** ô tìm kiếm tìm được cả khi gõ không dấu ("ha noi" khớp "Hà Nội"); bàn phím có Telex/VNI không bị app cản trở (không can thiệp ký tự đang compose, nhất là trên ô có validate/format realtime).
- **Giọng điệu & xưng hô:** thống nhất xưng hô ("bạn" / "quý khách"), tránh dịch máy sống sượng, tránh trộn Anh–Việt ngẫu nhiên trong cùng một nhãn.
- **Screen reader:** VoiceOver/TalkBack đọc tiếng Việt đúng khi ngôn ngữ nội dung được khai báo (`lang`/`accessibilityLanguage`).
