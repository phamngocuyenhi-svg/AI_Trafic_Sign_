# Demo Script - AI Traffic Sign Recognition

## 1. Giới thiệu

Xin chào thầy/cô và các bạn.

Nhóm chúng em xin trình bày đồ án **AI Traffic Sign Recognition**, xây dựng hệ thống nhận diện biển báo giao thông sử dụng mô hình YOLO kết hợp CNN.

---

## 2. Mục tiêu

Hệ thống có khả năng:

- Phát hiện biển báo giao thông.
- Phân loại biển báo.
- Hiển thị kết quả theo thời gian thực.
- Hỗ trợ camera hoặc webcam.

---

## 3. Chuẩn bị

Trước khi chạy chương trình cần:

- Cài đặt Python.
- Cài đặt các thư viện trong `requirements.txt`.
- Chuẩn bị webcam.
- Chuẩn bị mô hình YOLO và CNN đã huấn luyện.

---

## 4. Chạy chương trình

Mở Terminal và chạy:

```bash
python detect.py
```

Hoặc:

```bash
python realtime_pipeline.py
```

---

## 5. Thực hiện Demo

### Bước 1

Khởi động chương trình.

Kết quả mong muốn:

- Camera được mở.
- Không xuất hiện lỗi.

---

### Bước 2

Đưa một biển báo vào trước camera.

Kết quả mong muốn:

- YOLO phát hiện vị trí biển báo.
- Hiển thị Bounding Box.

---

### Bước 3

CNN phân loại biển báo.

Kết quả mong muốn:

Ví dụ:

```
Speed Limit 40
Confidence: 98%
```

---

### Bước 4

Thử nhiều biển báo khác nhau.

Ví dụ:

- Stop
- No Entry
- Speed Limit
- Turn Left
- Turn Right

---

### Bước 5

Đưa hai biển báo cùng lúc.

Kết quả mong muốn:

- Hệ thống phát hiện cả hai biển báo.

---

### Bước 6

Kiểm tra trong điều kiện ánh sáng yếu.

Quan sát:

- Độ chính xác.
- FPS.

---

### Bước 7

Nhấn phím **Q** để thoát.

---

## 6. Kết quả mong đợi

- Camera hoạt động ổn định.
- Nhận diện đúng biển báo.
- Hiển thị tên biển báo.
- Hiển thị Confidence.
- Hệ thống chạy thời gian thực.

---

## 7. Kết luận

Hệ thống đáp ứng yêu cầu phát hiện và phân loại biển báo giao thông trong thời gian thực bằng mô hình YOLO kết hợp CNN.
