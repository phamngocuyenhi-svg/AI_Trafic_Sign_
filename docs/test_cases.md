# Test Cases - AI Traffic Sign Recognition System

## Mục tiêu

Kiểm thử các chức năng của hệ thống nhận diện biển báo giao thông sử dụng YOLO và CNN.

| TC | Nội dung kiểm thử | Dữ liệu đầu vào | Kết quả mong muốn | Kết quả thực tế | Trạng thái |
|----|-------------------|-----------------|-------------------|-----------------|------------|
| TC01 | Khởi động chương trình | detect.py | Chương trình chạy thành công | | |
| TC02 | Mở webcam | Webcam laptop | Camera hoạt động bình thường | | |
| TC03 | Không có biển báo | Khung hình trống | Không phát hiện biển báo | | |
| TC04 | Một biển báo | 1 biển báo rõ nét | Phát hiện đúng vị trí và tên biển báo | | |
| TC05 | Hai biển báo | 2 biển báo khác nhau | Phát hiện cả hai biển báo | | |
| TC06 | Ba biển báo | 3 biển báo | Phát hiện đầy đủ các biển báo | | |
| TC07 | Biển báo ở gần | Khoảng cách < 50 cm | Nhận diện đúng | | |
| TC08 | Biển báo ở xa | Khoảng cách > 2 m | Vẫn phát hiện nếu đủ rõ | | |
| TC09 | Biển báo nghiêng | Xoay khoảng 20° | Vẫn nhận diện đúng | | |
| TC10 | Biển báo xoay 45° | Ảnh biển báo | Nhận diện hoặc giảm confidence | | |
| TC11 | Biển báo bị che một phần | Che khoảng 30% | Có thể nhận diện hoặc confidence giảm | | |
| TC12 | Biển báo bị mờ | Ảnh mờ | Độ chính xác giảm nhưng không crash | | |
| TC13 | Ánh sáng yếu | Phòng tối | Hệ thống vẫn hoạt động | | |
| TC14 | Ánh sáng mạnh | Ngoài trời | Nhận diện đúng | | |
| TC15 | Camera rung | Di chuyển webcam | Hệ thống vẫn hoạt động | | |
| TC16 | Biển báo kích thước nhỏ | Biển nhỏ trong khung hình | Detect nếu đủ pixel | | |
| TC17 | Biển báo kích thước lớn | Chiếm phần lớn khung hình | Detect đúng | | |
| TC18 | Biển không thuộc dataset | Biển lạ | Không phân loại sai nghiêm trọng | | |
| TC19 | Đổi biển báo liên tục | Thay biển sau mỗi 2 giây | Hệ thống cập nhật kết quả đúng | | |
| TC20 | Webcam bị ngắt | Rút webcam hoặc tắt camera | Hiển thị thông báo lỗi phù hợp | | |
| TC21 | Chạy liên tục 5 phút | Webcam | Không bị treo | | |
| TC22 | Chạy liên tục 30 phút | Webcam | Hoạt động ổn định | | |
| TC23 | Chạy liên tục 1 giờ | Webcam | Không crash | | |
| TC24 | Thoát chương trình | Nhấn phím Q | Chương trình đóng bình thường | | |
| TC25 | Khởi động lại chương trình | Mở lại detect.py | Chạy bình thường sau khi khởi động lại | | |

## Ghi chú

- Kết quả thực tế và trạng thái (Pass/Fail) sẽ được cập nhật sau khi hoàn thành quá trình kiểm thử.
- Các trường hợp kiểm thử được thực hiện trên hệ thống nhận diện biển báo giao thông bằng YOLO và CNN.
