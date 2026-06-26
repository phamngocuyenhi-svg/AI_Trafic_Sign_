import os
import urllib.request
import zipfile
import argparse

# URL chính thức của bộ dữ liệu GTSRB
GTSRB_TRAIN_URL = "https://sid.erda.dk/public/archives/da4667553b3afc9641203b57e1b991f4/GTSRB_Final_Training_Images.zip"
GTSRB_TEST_URL = "https://sid.erda.dk/public/archives/da4667553b3afc9641203b57e1b991f4/GTSRB_Final_Test_Images.zip"

# URL của BTSC (mẫu hoặc toàn bộ)
BTSC_URL = "https://bcs.fit.vutbr.cz/data/ref-app.zip" # Bản đồ/bộ mẫu từ ĐH Brno

def download_progress(block_num, block_size, total_size):
    """
    Hiển thị phần trăm tiến trình tải xuống.
    """
    downloaded = block_num * block_size
    percent = min(100, (downloaded / total_size) * 100) if total_size > 0 else 0
    print(f"\rTải dữ liệu: {percent:.2f}% ({downloaded // (1024*1024)}MB / {total_size // (1024*1024)}MB)", end="")

def download_and_extract(url, output_dir):
    """
    Tải file zip từ URL và giải nén vào thư mục đích.
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = url.split('/')[-1]
    zip_path = os.path.join(output_dir, filename)
    
    if not os.path.exists(zip_path):
        print(f"\nBắt đầu tải từ: {url}")
        try:
            urllib.request.urlretrieve(url, zip_path, download_progress)
            print(f"\nTải xuống thành công! Lưu tại: {zip_path}")
        except Exception as e:
            print(f"\nLỗi khi tải từ {url}: {e}")
            return False
    else:
        print(f"\nFile đã tồn tại: {zip_path}, bỏ qua tải xuống.")

    print(f"Đang giải nén {filename}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        print("Giải nén hoàn tất!")
        return True
    except Exception as e:
        print(f"Lỗi khi giải nén {zip_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Script tải dữ liệu biển báo giao thông GTSRB và BTSC.")
    parser.add_argument("--gtsrb", action="store_true", help="Tải bộ dữ liệu huấn luyện GTSRB (~263MB)")
    parser.add_argument("--btsc", action="store_true", help="Tải bộ dữ liệu BTSC mẫu")
    parser.add_argument("--all", action="store_true", help="Tải toàn bộ tất cả các bộ dữ liệu")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")

    if not (args.gtsrb or args.btsc or args.all):
        print("Vui lòng chỉ định bộ dữ liệu muốn tải.")
        print("Ví dụ:")
        print("  python download_data.py --gtsrb     (để tải GTSRB)")
        print("  python download_data.py --all       (để tải toàn bộ)")
        print("Hoặc bạn có thể chạy mock_data_generator.py để sinh dữ liệu giả lập ngay lập tức.")
        return

    if args.gtsrb or args.all:
        gtsrb_dir = os.path.join(raw_dir, "gtsrb")
        print("\n--- Tải dữ liệu GTSRB ---")
        download_and_extract(GTSRB_TRAIN_URL, gtsrb_dir)
        
    if args.btsc or args.all:
        btsc_dir = os.path.join(raw_dir, "btsc")
        print("\n--- Tải dữ liệu BTSC ---")
        download_and_extract(BTSC_URL, btsc_dir)

if __name__ == "__main__":
    main()
