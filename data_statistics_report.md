# Báo cáo Thống kê Dữ liệu Biển báo Giao thông
Báo cáo chi tiết số lượng ảnh qua các giai đoạn xử lý trong pipeline (làm sạch -> tăng cường/cân bằng -> chia tập dữ liệu).

## 1. Tóm tắt Dữ liệu
- **Tổng số lớp học (Classes):** 7
- **Tỷ lệ chia dữ liệu (Train/Val/Test):** 70% / 15% / 15%
- **Đường dẫn dữ liệu kiểm thử (YOLO format):** Được cấu hình trong [data.yaml](file:///C:/Users/PC/.gemini/antigravity/scratch/traffic_sign_pipeline/data.yaml)

## 2. Bảng Phân bố Dữ liệu Qua Các Giai Đoạn

| Tên Lớp | Dữ liệu gốc (Raw) | Sau làm sạch (Cleaned) | Cân bằng & Tăng cường (Balanced) | Huấn luyện (Train) | Phát triển (Val) | Kiểm thử (Test) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| class_0 | 152 | 3 | 100 | 70 | 15 | 15 |
| class_1 | 80 | 25 | 100 | 70 | 15 | 15 |
| class_2 | 10 | 4 | 100 | 70 | 15 | 15 |
| class_3 | 44 | 3 | 100 | 70 | 15 | 15 |
| class_4 | 3 | 2 | 100 | 70 | 15 | 15 |
| class_5 | 4 | 4 | 100 | 70 | 15 | 15 |
| class_6 | 8 | 3 | 100 | 70 | 15 | 15 |
| **TỔNG CỘNG** | **301** | **44** | **700** | **490** | **105** | **105** |

## 3. Biểu đồ Phân bố Dữ liệu Cuối cùng (Train Set)
```text
class_0    | ████████████████████████████████████████ | 70 ảnh
class_1    | ████████████████████████████████████████ | 70 ảnh
class_2    | ████████████████████████████████████████ | 70 ảnh
class_3    | ████████████████████████████████████████ | 70 ảnh
class_4    | ████████████████████████████████████████ | 70 ảnh
class_5    | ████████████████████████████████████████ | 70 ảnh
class_6    | ████████████████████████████████████████ | 70 ảnh
```

## 4. Giải thích Tiến trình Pipeline
1. **Làm sạch (Cleaning):** Loại bỏ các file hỏng, phát hiện và xóa ảnh mờ (ngưỡng Laplacian < 100), loại bỏ các ảnh trùng lặp gần tuyệt đối sử dụng thuật toán băm nhận thức 64-bit dhash.
2. **Cân bằng & Tăng cường (Augmentation):** Để tránh mất cân bằng lớp (Class Imbalance) có hại cho việc huấn luyện, hệ thống đã tăng cường ảnh cho các lớp thiểu số bằng các phép quay ngẫu nhiên, thay đổi độ sáng, độ tương phản và thêm nhiễu Gauss.
3. **Phân chia dữ liệu (Splitting):** Dữ liệu được chia ngẫu nhiên thành 3 tập riêng biệt để đảm bảo tính đánh giá khách quan của mô hình.
