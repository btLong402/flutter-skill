---
description: Tiêu chuẩn Tuân thủ Google Play (Compliance), Đánh giá Nội dung (IARC), Data Safety, Chính sách Quyền riêng tư
globs: docs/play_store/**,play_store_metadata/**,android/app/src/main/AndroidManifest.xml
---

# Rule: Google Play Compliance & Data Safety

> Kích hoạt: Khi người dùng yêu cầu cấu hình Content Rating, Data Safety, Privacy Policy, khai báo quyền Android hoặc checklist chuẩn bị release

## 1. Đánh Giá Phân Loại Nội Dung (Content Rating / IARC)

- Trả lời bảng câu hỏi IARC hoàn toàn dựa trên tính năng thực tế đang có của ứng dụng.
- Nếu ứng dụng có tính năng người dùng tương tác (UGC - User Generated Content), bắt buộc phải có cơ chế **báo cáo (Report)**, **chặn (Block)** và **kiểm duyệt nội dung (Moderation)**.
- Nếu ứng dụng sử dụng vị trí: Phải phân biệt rõ ràng giữa vị trí tương đối (Approximate Location) và vị trí chính xác (Precise Location).
- Tuyệt đối không phỏng đoán mơ hồ; các mục chưa rõ phải đánh dấu cần xác minh với Product Owner.

---

## 2. Khai Báo An Toàn Dữ Liệu (Data Safety Section)

- **Nguyên tắc trung thực:** Chỉ khai báo những loại dữ liệu mà ứng dụng thực tế thu thập hoặc chia sẻ với bên thứ ba (qua SDK như Firebase, AdMob, AppsFlyer...).
- Nếu có thu thập dữ liệu cá nhân (Email, số điện thoại, tên): Phải giải thích rõ mục đích sử dụng (Xác thực tài khoản, cá nhân hóa...).
- Bắt buộc khai báo dữ liệu được mã hóa trong quá trình truyền tải (**Encrypted in transit** qua HTTPS/TLS).
- Cung cấp đường dẫn và quy trình cho phép người dùng yêu cầu xóa tài khoản và dữ liệu cá nhân (**Account & Data Deletion URL**).

---

## 3. Chính Sách Quyền Riêng Tư (Privacy Policy)

- Phải có một URL hoạt động ổn định, có thể truy cập công khai mà không cần đăng nhập.
- Nội dung Privacy Policy phải liệt kê chi tiết: Loại dữ liệu thu thập, mục đích, thời gian lưu trữ (retention), chính sách chia sẻ bên thứ ba và thông tin liên hệ hỗ trợ.
- Email liên hệ hỗ trợ phải khớp với tên miền của sản phẩm hoặc tổ chức phát hành.

---

## 4. Cổng Kiểm Soát Cuối Cùng (Final Compliance Gate)

Trước khi xuất kết quả cho người dùng, AI phải tự kiểm tra 4 điểm cốt tử:
1. Đánh giá Content Rating có trung thực với ứng dụng không?
2. Khai báo Data Safety có khớp hoàn toàn với các quyền trong `AndroidManifest.xml` không?
3. Đường link Privacy Policy có hợp lệ và đầy đủ điều khoản không?
4. Đã có hướng dẫn xóa tài khoản theo chính sách mới của Google Play chưa?

> 🔴 **CẢNH BÁO:** Bất kỳ sai lệch nào trong Data Safety hoặc Content Rating đều có thể dẫn đến việc ứng dụng bị **Reject hoặc Gỡ bỏ (Suspension)** khỏi Google Play Store.