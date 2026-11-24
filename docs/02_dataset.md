# 02. Hai bộ dữ liệu: EyePACS và DDR

> Các con số dưới đây là từ tài liệu `SIC.docx` và từ hiểu biết của tôi về các bộ này. Những chỗ có ⚠ sẽ được **kiểm tra lại bằng notebook "probe" trên Kaggle** trước khi đưa vào báo cáo.

## 1. EyePACS (Kaggle Diabetic Retinopathy Detection, 2015)

**Là gì.** Dữ liệu của nền tảng sàng lọc võng mạc EyePACS (Mỹ), được công bố qua cuộc thi Kaggle năm 2015. Ảnh chụp ở nhiều phòng khám, bằng nhiều loại máy (Centervue DRS, Optovue iCam, Canon CR1/DGi/CR2, Topcon NW) — vì vậy bản thân EyePACS đã có nhiều "miền con".

**Trong đó có gì.**
- Ảnh `.jpeg`, đặt tên `<id>_left` / `<id>_right` (mắt trái/phải của cùng một người).
- File nhãn: `trainLabels.csv` (và file nhãn tập test).
- Nhãn 5 mức 0–4.
- Kích thước ảnh rất không đồng đều (từ vài trăm đến khoảng 4000 px). Dung lượng gốc khoảng 89 GiB.
- Split dùng trong đề tài: **train 35.126 / val 10.906 / test 42.670**. ⚠ Tôi nhớ 10.906 + 42.670 = 53.576 chính là tập test gốc của cuộc thi, chia theo Public/Private leaderboard; sẽ xác nhận trong file nhãn.

**Phân bố lớp (tập train, xấp xỉ ⚠):** mức 0 ≈ 73%, mức 1 ≈ 7%, mức 2 ≈ 15%, mức 3 ≈ 2,5%, mức 4 ≈ 2%. Mất cân bằng nặng.

**Điểm yếu (phải nêu trong báo cáo):**
- Nhãn nhiễu (một người chấm mỗi ảnh); nhiều ảnh không chấm được lại bị gán mức 0.
- Mất cân bằng lớp.
- ⚠ Rủi ro rò rỉ bệnh nhân: nếu val và test cắt theo ảnh mà không theo bệnh nhân thì mắt trái/phải cùng một người có thể nằm ở cả hai. Sẽ kiểm tra bằng id trong probe; chọn checkpoint theo val chỉ có hại nhẹ, nhưng cần ghi nhận.

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
- Mức 3 rất hiếm trong DDR (⚠ vài trăm ảnh toàn bộ bộ, chỉ khoảng một trăm trong test) → recall/F1 của mức 3 sẽ **dao động mạnh**, cần bootstrap CI.

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

Các hình EDA sẽ được lưu vào `evidence_figures/01_data/` (phân bố lớp, kích thước ảnh, ảnh mẫu mỗi mức, thống kê màu/độ sáng trung bình để thấy khoảng cách miền).
