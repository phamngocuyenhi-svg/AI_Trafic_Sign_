# Metrics Summary

## 1. Mục tiêu

Tài liệu này tổng hợp các chỉ số đánh giá hiệu năng của hệ thống nhận diện biển báo giao thông sử dụng YOLO và CNN.

---

## 2. Kết quả đánh giá mô hình

| Chỉ số | Giá trị | Nguồn dữ liệu | Ghi chú |
|---------|----------|---------------|---------|
| Accuracy | | CNN Evaluation | Độ chính xác tổng thể |
| Precision | | CNN Classification Report | Độ chính xác của dự đoán dương |
| Recall | | CNN Classification Report | Khả năng phát hiện đúng |
| F1-score | | CNN Classification Report | Trung bình điều hòa của Precision và Recall |

---

## 3. Hiệu năng thời gian thực

| Chỉ số | Giá trị | Ghi chú |
|---------|----------|---------|
| FPS | | Số khung hình xử lý mỗi giây |
| Latency | | Thời gian xử lý trung bình mỗi khung hình |
| CPU Usage | | Mức sử dụng CPU |
| RAM Usage | | Mức sử dụng bộ nhớ |

---

## 4. Confusion Matrix

> Chèn hình Confusion Matrix sau khi hoàn thành huấn luyện mô hình CNN.

Ví dụ:

![Confusion Matrix](images/confusion_matrix.png)

---

## 5. Nhận xét

- Accuracy càng cao càng tốt.
- Precision cao giúp giảm nhận diện sai.
- Recall cao giúp phát hiện được nhiều biển báo hơn.
- F1-score phản ánh hiệu năng tổng thể của mô hình.
- FPS càng lớn, hệ thống xử lý càng mượt.
- Latency càng thấp, hệ thống phản hồi càng nhanh.

---

## 6. Kết luận

Sau khi hoàn thành huấn luyện và kiểm thử, cập nhật toàn bộ các chỉ số vào bảng trên để đánh giá chất lượng của hệ thống.
