# GĐ0: kết quả kiểm tra thiết lập (2026-11-24)

## Kaggle
- `kaggle` CLI 2.2.5 cài xong; token qua biến môi trường `KAGGLE_API_TOKEN` hoạt động. Tài khoản: `thinhlai`.
- Cuộc thi `diabetic-retinopathy-detection` truy cập được (đã accept luật). **Chỉ có `trainLabels.csv`, không có nhãn test**; ảnh là các file zip chia nhỏ (train 5 phần, test 7 phần, ~89 GB) nên không tiện dùng trực tiếp.

## EyePACS (nguồn dùng): `benjaminwarner/resized-2015-2019-blindness-detection-images`
- Có `labels/trainLabels15.csv` (35.126 dòng), `labels/testLabels15.csv` (53.576 dòng, có cột `Usage`), thư mục `resized train 15`, `resized test 15` (ảnh `.jpg` tên `<id>_left/right`).
- Kích thước và việc đã cắt viền hay chưa: **chưa kiểm tra**, làm ở probe GĐ1.
- Phân bố và rò rỉ: xem `docs/02_dataset.md` (đã xác minh).

## DDR (nguồn dùng): `samriddhibagchi/ddr-dataset-credits-to-authors`
- `DDR-dataset/DR_grading/test.txt` (4.105 dòng, định dạng `tên_ảnh nhãn`) và thư mục `DR_grading/test/` (ảnh gốc độ phân giải cao, vài trăm KB đến hơn 1 MB mỗi ảnh).
- Số lượng và phân bố: xem `docs/02_dataset.md` (đã xác minh).

## RETFound
- Có nhiều biến thể trên Hugging Face (`YukunZhou/...`). **Bản dùng: `RETFound_mae_natureCFP`** (bài Nature 2023, ảnh đáy mắt, ViT-L, MAE).
- Repo bị khóa kiểu `gated: auto`: phải đăng nhập và đồng ý điều khoản thì được cấp quyền ngay.
- Giấy phép code: **CC BY-NC 4.0** (phi thương mại). Đồ án học thuật dùng được; **không đưa trọng số lên repo công khai**, chỉ để trong Kaggle dataset **private**.
- Ghi chú: biến thể `RETFound_mae_meh` chỉ tiền huấn luyện trên dữ liệu Moorfields, không có EyePACS. Có thể là phân tích phụ nếu còn giờ GPU, **chưa đưa vào kế hoạch**.
- Code chính thức (`rmaphoh/RETFound_MAE`): fine-tune mặc định ảnh 224, `--global_pool`, `--nb_classes`, hỗ trợ `--adaptation finetune|lp` (linear probe).

## Trạng thái
- [x] 0.1 Kaggle CLI và token
- [x] 0.2 Dữ liệu EyePACS (kèm nhãn test) và DDR đã xác định nguồn
- [ ] 0.3 Trọng số RETFound: **chờ bấm đồng ý điều khoản Hugging Face** (công cụ Chrome không kết nối được trong phiên này)
- [x] 0.4 GitHub
