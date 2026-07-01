# Test Cases

## Mục tiêu

Kiểm thử các chức năng của hệ thống nhận diện biển báo giao thông.

| TC | Nội dung kiểm thử | Dữ liệu đầu vào | Kết quả mong muốn | Kết quả thực tế | Trạng thái |
|----|-------------------|-----------------|-------------------|-----------------|------------|
| TC01 | Khởi động chương trình | detect.py | Chương trình chạy thành công | | |
| TC02 | Mở webcam | Webcam | Camera hoạt động | | |
| TC03 | Không có biển báo | Khung hình trống | Không phát hiện biển báo | | |
| TC04 | Một biển báo | 1 biển báo | Phát hiện đúng biển báo | | |
| TC05 | Hai biển báo | 2 biển báo | Phát hiện cả hai | | |
| TC06 | Biển ở gần camera | Khoảng cách gần | Phát hiện đúng | | |
| TC07 | Biển ở xa camera | Khoảng cách xa | Phát hiện nếu đủ rõ | | |
| TC08 | Biển nghiêng | Xoay khoảng 20° | Vẫn nhận diện được | | |
| TC09 | Ánh sáng yếu | Phòng tối | Hệ thống vẫn hoạt động | | |
| TC10 | Ánh sáng mạnh | Ngoài trời | Nhận diện đúng | | |
| TC11 | Biển bị che một phần | Che 30% | Có thể nhận diện hoặc confidence giảm | | |
| TC12 | Biển mờ | Ảnh mờ | Độ chính xác giảm | | |
| TC13 | Webcam bị tắt | Ngắt webcam | Hiển thị thông báo lỗi phù hợp | | |
| TC14 | Thoát chương trình | Nhấn Q | Chương trình đóng bình thường | | |
