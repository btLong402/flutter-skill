---
description: Tiêu chuẩn Hình ảnh Google Play (Screenshots, Feature Graphic, Icon Guidance)
globs: assets/store/**,docs/store/**,fastlane/metadata/**
---

# Rule: Google Play Visual Assets

> Kích hoạt: Khi người dùng yêu cầu hướng dẫn thiết kế ảnh chụp màn hình (Screenshots), Feature Graphic, App Icon hoặc bộ tài nguyên hình ảnh phát hành

## 1. Nguyên Tắc Thiết Kế Ảnh Chụp Màn Hình (Screenshots)

- **Ảnh đầu tiên là quan trọng nhất:** Bắt buộc phải thể hiện tính năng cốt lõi hoặc giá trị lớn nhất của ứng dụng ngay ở tấm ảnh đầu tiên (trong 3 giây đầu tiên của người dùng).
- **Luồng kể chuyện (Visual Storytelling):** Sắp xếp thứ tự ảnh theo phễu tâm lý:  
  $$\text{Giá trị độc bản (Value)} \longrightarrow \text{Tính năng chủ đạo (Feature)} \longrightarrow \text{Uy tín & Đánh giá (Trust)} \longrightarrow \text{Kêu gọi hành động (CTA)}$$
- **Thiết bị Mockup:** Sử dụng khung thiết bị viền mỏng hiện đại; tuyệt đối không dùng mockup thiết bị cũ có nút Home vật lý lỗi thời.
- **Văn bản mô tả (Text Caption):** Ngắn gọn, cỡ chữ lớn, tối đa 1-2 dòng, tương phản cao trên nền để người dùng dễ đọc trên màn hình điện thoại nhỏ.

---

## 2. Đồ Họa Nổi Bật (Feature Graphic - $1024 \times 500\,\text{px}$)

- Đúng một thông điệp chính và một tâm điểm thị giác (Focal Point) rõ ràng.
- Giữ vùng an toàn (Safe Area): Tránh đặt logo hoặc chữ sát mép biên hoặc góc dưới bên trái (nơi hiển thị nút Play/Cài đặt).
- Tránh đưa quá nhiều chi tiết rối mắt; ưu tiên phong cách tối giản, tinh tế.

---

## 3. Biểu Tượng Ứng Dụng (App Icon - $512 \times 512\,\text{px}$)

- Tuyệt đối không sử dụng nhãn hiệu hoặc logo của bên thứ ba mà chưa có bản quyền.
- Màu sắc nhận diện phải đồng nhất với màu chủ đạo trong Design System của ứng dụng.
- Ưu tiên hình khối hình học rõ ràng, dễ nhận biết ngay cả khi thu nhỏ trên màn hình chính.

---

## 4. Cổng Kiểm Định Chất Lượng Hình Ảnh (Quality Gate)

- [ ] Ảnh chụp màn hình số 1 đã thể hiện ngay tính năng cốt lõi chưa?
- [ ] Kích thước và tỉ lệ khung hình có đúng chuẩn Play Console (Tối thiểu 1080p, tỉ lệ 16:9 hoặc 9:16) không?
- [ ] Hình ảnh có trung thực với giao diện thực tế của ứng dụng không (tránh vi phạm chính sách hiển thị sai lệch)?