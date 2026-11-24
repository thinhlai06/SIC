# 02. Hai bộ dữ liệu: EyePACS và DDR

> Các con số dưới đây là từ tài liệu `SIC.docx` và từ hiểu biết của tôi về các bộ này. Những chỗ có ⚠ sẽ được **kiểm tra lại bằng notebook "probe" trên Kaggle** trước khi đưa vào báo cáo.

## 1. EyePACS (Kaggle Diabetic Retinopathy Detection, 2015)

**Là gì.** Dữ liệu của nền tảng sàng lọc võng mạc EyePACS (Mỹ), được công bố qua cuộc thi Kaggle năm 2015. Ảnh chụp ở nhiều phòng khám, bằng nhiều loại máy (Centervue DRS, Optovue iCam, Canon CR1/DGi/CR2, Topcon NW) — vì vậy bản thân EyePACS đã có nhiều "miền con".

**Trong đó có gì.**
- Ảnh `.jpeg`, đặt tên `<id>_left` / `<id>_right` (mắt trái/phải của cùng một người).
- File nhãn: `trainLabels.csv` (và file nhãn tập test).
- Nhãn 5 mức 0–4.
- Kích thước ảnh rất không đồng đều (từ vài trăm đến khoảng 4000 px). Dung lượng gốc khoảng 89 GiB.
- Split dùng trong đề tài: **train 35.126 / val 10.906 / test 42.670**. ✅ **Đã xác minh (GĐ0):** 10.906 + 42.670 = 53.576 là tập test gốc của cuộc thi; file `testLabels15.csv` có cột `Usage`: **Public = 10.906 (dùng làm val)**, **Private = 42.670 (dùng làm test)**. Cuộc thi trên Kaggle chỉ có `trainLabels.csv`, nhãn test lấy từ bản resize của `benjaminwarner/resized-2015-2019-blindness-detection-images`.

**Phân bố lớp (✅ đã xác minh từ file nhãn):**

| Tập | Tổng | Mức 0 | Mức 1 | Mức 2 | Mức 3 | Mức 4 |
|---|---|---|---|---|---|---|
| Train | 35.126 | 25.810 (73,5%) | 2.443 | 5.292 | 873 | 708 |
| Val (Public) | 10.906 | 8.130 | 720 | 1.579 | 237 | 240 |
| Test (Private) | 42.670 | 31.403 | 3.042 | 6.282 | 977 | 966 |

Mất cân bằng nặng (lớp 0 chiếm khoảng 73–74% ở mọi tập).

**Điểm yếu (phải nêu trong báo cáo):**
- Nhãn nhiễu (một người chấm mỗi ảnh); nhiều ảnh không chấm được lại bị gán mức 0.
- Mất cân bằng lớp.
- ✅ **Không rò rỉ bệnh nhân (đã kiểm tra theo id):** train có 17.563 bệnh nhân, test 26.788; **0 bệnh nhân trùng** giữa train và test, và **0 bệnh nhân trùng** giữa Public (val) và Private (test). Mắt trái/phải của cùng một người luôn nằm cùng một tập.

**Vì sao chọn EyePACS làm miền nguồn (train):**
1. **Lớn nhất** (35k ảnh có nhãn): đủ để fine-tune mô hình 300 triệu tham số mà không quá khớp.
2. **Đa dạng bên trong** (nhiều máy, nhiều phòng khám): tốt cho DG vì mô hình thấy nhiều biến thể.
3. **Có split chính thức** sẵn, tái lập được.
4. Là chuẩn de-facto của cộng đồng DR; RETFound cũng dùng EyePACS để tiền huấn luyện **(không dùng nhãn)** → dùng EyePACS cho fine-tune là tự nhiên và công bằng cho cả B1, B2, M1, M2 (cùng train trên EyePACS).

## 2. DDR (Diabetic Retinopathy Detection and Grading dataset)

**Là gì.** Đại học Nankai (Trung Quốc) công bố năm 2019. **13.673 ảnh** từ **147 bệnh viện** ở **23 tỉnh**, chụp 2016–2018, do **7 người chấm** đã được đào tạo gán nhãn theo thang ICDR.

**Trong đó có gì.**
- Nhãn mức bệnh **6 lớp**: 0–4 và lớp 5 "ungradable" (ảnh chất lượng kém, không chấm được).
- Có thêm nhãn mức pixel và bounding box cho vi phình mạch, xuất huyết, xuất tiết cứng/mềm (đề tài **không dùng** phần này).
- Split chính thức: train 6.835 / val 2.733 / test 4.105. Bỏ lớp ungradable (thông lệ): 6.320 / 2.503 / **3.759**.
- ✅ **Đã xác minh từ `DR_grading/test.txt` (4.105 dòng):** mức 0 = 1.880, mức 1 = 189, mức 2 = 1.344, **mức 3 = 71**, mức 4 = 275, ungradable (5) = 346. Bỏ lớp 5 còn **3.759** ảnh. Mức 3 chỉ có **71 ảnh** → recall/F1 của mức 3 sẽ **dao động mạnh**, bắt buộc báo cáo bootstrap CI.
- So với EyePACS (mức 0 khoảng 74%): DDR-test có mức 0 khoảng 50% và mức 2 khoảng 36% → **label shift** rõ rệt, nên Accuracy giữa hai bộ không so sánh trực tiếp được.
- Nguồn dùng: Kaggle `samriddhibagchi/ddr-dataset-credits-to-authors` (giữ cấu trúc gốc, giấy phép MIT).

**Vì sao chọn DDR làm miền đích (test):**
1. **Khác EyePACS thật sự**: dân số Trung Quốc vs Mỹ, máy/bệnh viện khác, người chấm khác, tỉ lệ mức bệnh khác → đúng loại domain shift đề tài muốn đo.
2. **Nhãn sạch hơn**: 7 người chấm đã đào tạo, tiêu chuẩn ICDR rõ ràng.
3. **RETFound bản gốc chưa tiền huấn luyện trên DDR** (⚠ sẽ kiểm tra lại trong bài báo Nature; DDR có xuất hiện ở một số biến thể khác như DERETFound) → kết quả test trên DDR là **trung thực**.
4. **Cỡ test đủ lớn** (3.759 ảnh) để có CI khá hẹp.
5. **Có sẵn trên Kaggle/GitHub/HuggingFace** (dễ lấy).

## 3. Vì sao chia: một bộ train, một bộ test?

> Nếu train và test đều trên EyePACS thì chỉ chứng minh được mô hình tốt **trong cùng miền**. Đề tài hỏi về **độ bền vững khi đổi miền**, nên phải test ở bộ **khác miền**.

- **EyePACS-test (in-domain)** vẫn báo cáo làm mốc tham chiếu. Khoảng chênh **in-domain − out-of-domain** cho thấy mô hình mất bao nhiêu khi đổi miền. Ghi chú: RETFound đã thấy ảnh EyePACS (không nhãn) lúc tiền huấn luyện nên số in-domain có thể hơi lạc quan.
- **DDR-test (out-of-domain)** là **kết quả chính**.
- **Quy tắc cứng:** DDR **không được** dùng để chọn checkpoint, chỉnh siêu tham số, hay chọn augmentation. Mọi lựa chọn chỉ dựa trên **EyePACS-val**. DDR chỉ được "nhìn" ở bước đánh giá cuối.
- **Không dùng DDR-train/val**: nếu có (dù chỉ để chỉnh), DDR không còn là miền chưa thấy. Đây là quyết định đã chốt (chỉ dùng 2 bộ, DDR chỉ test).
- Vì chỉ có một miền đích nên kết luận chỉ áp dụng cho cặp EyePACS → DDR. Phải nói rõ giới hạn này trong báo cáo (không khái quát hóa sang mọi bệnh viện).

## 4. Điểm khác biệt giữa hai bộ cần nêu trong báo cáo (EDA)

| Khía cạnh | EyePACS | DDR |
|---|---|---|
| Nguồn | Phòng khám Mỹ (sàng lọc) | 147 bệnh viện Trung Quốc |
| Số ảnh dùng | 35.126 / 10.906 / 42.670 | 3.759 (test) |
| Người chấm | 1 người/ảnh, nhiễu | 7 người đào tạo |
| Phân bố lớp | Rất lệch về mức 0 | Ít lệch hơn nhưng mức 3 hiếm |
| Kích thước ảnh | Rất đa dạng | Đa dạng |
| Vai trò | Train / val / test in-domain | Test out-of-domain (kết quả chính) |

### Kết quả probe trên Kaggle (CPU, đã chạy xong)

Số liệu thô: `logs/probe_report.json`; hình: `evidence_figures/01_data/d01`–`d05`; thống kê mẫu 400 ảnh mỗi bộ: `logs/stats_*_sample.csv`.

- **Toàn vẹn:** EyePACS không thiếu file nào (35.126 train, 53.576 test); DDR đủ 4.105 file. Số liệu khớp 100% với phân tích nhãn ở trên.
- **Khung hình (domain gap thứ nhất):** võng mạc chiếm khoảng **83%** diện tích ảnh EyePACS (bản resize, đã cắt khá sát) nhưng chỉ khoảng **52%** ở DDR (viền đen rộng). Cần **cắt theo vùng võng mạc** trước khi resize về 224×224, nếu không võng mạc DDR sẽ chỉ chiếm nửa ảnh đầu vào.
- **Kích thước:** EyePACS (resize) cạnh dài tối đa 1024 px, trung vị khoảng 1024×946; DDR rất lớn, trung vị khoảng 2736×1824, tối đa 5184×3456. Hình dạng vùng võng mạc của DDR hay là hình **elip** (không tròn như EyePACS).
- **Màu (domain gap thứ hai):** trung bình trong vùng võng mạc, kênh xanh dương: EyePACS khoảng 67, DDR khoảng 38; kênh xanh lá và đỏ cũng lệch. DDR ngả **cam/vàng**, EyePACS sáng và nhiều xanh hơn. Đây là bằng chứng định lượng cho việc dùng augmentation màu ở M2.
- **Phân bố lớp:** giống hệt kết quả phân tích nhãn (lớp 0 khoảng 74% ở EyePACS, DDR-test khoảng 50% lớp 0 và 36% lớp 2).

Các hình EDA sẽ được lưu vào `evidence_figures/01_data/` (phân bố lớp, kích thước ảnh, ảnh mẫu mỗi mức, thống kê màu/độ sáng trung bình để thấy khoảng cách miền).
