# 04. Có nên train mô hình khác? File mẫu của nhóm khác? Có cần tải dataset về?

## 1. Có nên train mô hình khác để so sánh không?

**Có, nhưng ít và có chủ đích.** Một kết quả "M1 đạt QWK X trên DDR" tự nó không nói gì. Nó chỉ có nghĩa khi đặt cạnh các mô hình đối chứng, mỗi mô hình trả lời đúng **một câu hỏi**:

| Mã | Mô hình | Câu hỏi nó trả lời | Chi phí |
|---|---|---|---|
| **B1** | ResNet-50, ImageNet có giám sát | Mô hình thông thường bị tụt bao nhiêu khi đổi miền? | Thấp (khoảng 0,5 giờ/run, ước lượng) |
| **B2** | ViT-L, MAE tiền huấn luyện trên ImageNet | Cùng kiến trúc và cùng kiểu SSL, chỉ khác dữ liệu: SSL **trên ảnh võng mạc** có thực sự đáng giá? | Cao (cỡ M1) |
| **M1** | RETFound fine-tune | Mô hình chính | Cao |
| **M2** | M1 + augmentation mô phỏng domain shift | Augmentation DG có giúp thêm không? | Cao |

**Đề xuất bổ sung (rẻ, nhiều thông tin) — cần bạn duyệt:**
- **Linear probe (LP)** cho RETFound và B2: đóng băng toàn bộ backbone, chỉ train đầu phân loại trên đặc trưng đã trích sẵn. Chỉ cần **một lượt suy luận** để trích đặc trưng (không backprop ViT-L), nên rẻ. Cho biết **chất lượng biểu diễn thô** của SSL võng mạc so với ImageNet, tách khỏi tác động của fine-tune. Đặc trưng đó cũng dùng luôn cho t-SNE.
- **Ablation augmentation của M2** (1 seed, nếu còn giờ): từng nhóm augmentation (màu / blur / nhiễu / chất lượng) để biết nhóm nào có ích.

**Không đề xuất:**
- Train thêm nhiều kiến trúc (EfficientNet, Swin, ConvNeXt…): tốn giờ GPU, không thêm câu hỏi nghiên cứu mới, dễ làm báo cáo loãng.
- Tự pretrain SSL trên EyePACS: không đủ 30 giờ GPU (xem file 03).

**Số run dự kiến:** B1 ×3 seed, B2 ×1–3 seed, M1 ×3 seed, M2 ×3 seed, LP ×2 (rẻ). Quyết định số seed của B2 sau khi đo tốc độ thật.

---

## 2. File mẫu của nhóm khác: `Group3_SIC_AI_N02-signed.pdf`

**Đã đọc** (41 trang, đề tài phát hiện vượt đèn đỏ). Chỉ học **cách trình bày**, không sao chép nội dung. (Lưu ý: nhóm đó cũng tên "Group 3", lớp SIC-AI-N02, nên cần tránh trùng câu chữ.)

**Những điều rút ra để áp dụng:**

| Khía cạnh | Mẫu làm thế nào | Áp dụng cho nhóm mình |
|---|---|---|
| **Độ dài** | 41 trang: 8 trang đầu (bìa, mục lục, danh mục hình/bảng, viết tắt), chương 1–4 khoảng 22 trang, chương 5–6 khoảng 2 trang, tài liệu tham khảo 2 trang, phụ lục khoảng 6 trang | Mình cần 40–50 trang → chương 2 và 3 dài hơn và nhiều hình minh chứng hơn mẫu |
| **Cấu trúc** | Mỗi `\section` chia thành `x.y.z` (không sâu hơn). Ví dụ 1.1 có 4 mục con, 2.1 có 6 mục con, 2.2 có 7 mục con, 2.3 có 8 mục con | Đúng quy tắc đã chốt: chỉ `\subsection` |
| **Mục 1.1** | Tình hình → thực tế hiện nay → công nghệ nền tảng → thách thức kỹ thuật | DR → hệ thống sàng lọc hiện nay → học sâu/ViT/SSL → domain shift |
| **Mục 1.2** | Tách *Motivation* và *Objectives* (mục tiêu đánh số 1–6) | Làm tương tự, mục tiêu đo được (QWK, ΔQWK…) |
| **Mục 2.1** | Nguồn dữ liệu, thu thập, gán nhãn, thống kê, chia tập, … | Giữ khung này cho EyePACS và DDR, thêm bảng thống kê |
| **Mục 2.2** | Chỉ rõ mô hình, siêu tham số (bảng), augmentation (gạch đầu dòng), loss và chỉ số, quá trình train và **chọn checkpoint kèm hình đường cong** | Đúng ý bạn: có hình loss/QWK theo epoch |
| **Mục 2.3 / 2.4** | Sơ đồ pipeline (hộp + mũi tên), sơ đồ kiến trúc nguyên trang | Mình vẽ pipeline và system diagram bằng Python |
| **Mục 3.x** | Bảng chuẩn bị dữ liệu từng bước, hình EDA, bảng kết quả (tổng + từng lớp), hình định tính, ảnh UI, bảng test | Thêm confusion matrix, ROC, Grad-CAM, t-SNE, CI |
| **Công thức** | Ít, đánh số (2.1), (3.1), có giải thích ký hiệu ngay sau | Khoảng 6–8 công thức |
| **Bảng/hình** | Caption bảng ở **trên**, caption hình ở **dưới**; caption dài, nêu rõ nội dung | Giữ phong cách này |
| **Tiêu đề mục** | Dạng "nhãn in đậm + câu giải thích" (run-in) cho các ý nhỏ | Dùng `\textbf{...}` mở đoạn |
| **Phụ lục** | A: mã nguồn chính; B: bảng siêu tham số (train, augmentation, suy luận) | A: vòng lặp train + tính QWK; B: siêu tham số thật |
| **Viết tắt** | Bảng dài (khoảng 20+ mục) | Mở rộng từ 10 mục mẫu của template lên khoảng 20–25 |
| **Tài liệu tham khảo** | khoảng 16 nguồn, IEEE | Khoảng 15–18 nguồn đã xác minh |

**Điểm mình nên làm tốt hơn mẫu:**
- Chương 3 của mẫu chỉ khoảng 7 trang và thiên về bảng số; mình có **nhiều minh chứng đồ thị** (đúng yêu cầu của bạn).
- Chương 3 của mình cần phần **phân tích** (vì sao in → out giảm, mô hình nhìn vào đâu) chứ không chỉ liệt kê số.

---

## 3. Có cần tải dataset về cho tôi đọc trước không?

**Không cần tải đầy đủ về máy.** Lý do:

- EyePACS gốc khoảng **89 GiB**; không hợp lý và không cần thiết tải về máy local. Huấn luyện chạy hoàn toàn trên Kaggle và dữ liệu cuộc thi được gắn sẵn vào notebook (`/kaggle/input`).
- Việc "đọc dữ liệu" (EDA, thống kê) sẽ **chạy trong notebook Kaggle**, xuất kết quả (CSV + hình) ra `/kaggle/working`, rồi tôi tải **chỉ các file kết quả nhỏ** về `evidence_figures/` và `logs/`.

**Thay vào đó, tôi đề xuất một bước "probe" rất nhẹ trước khi train:**

1. Notebook Kaggle **chỉ dùng CPU** (**không tốn giờ GPU**).
2. Liệt kê cấu trúc thư mục, đọc file nhãn: số ảnh, phân bố lớp, kiểm tra Public/Private (val/test), đếm id bệnh nhân (kiểm tra rò rỉ trái/phải).
3. Lấy mẫu vài chục ảnh: kích thước, viền đen, màu sắc; lưu 12–20 ảnh mẫu.
4. Với DDR: xác nhận tập test, số ảnh sau khi bỏ lớp 5, định dạng nhãn.
5. Xuất `probe_report.md` + vài hình nhỏ → tôi tải về và đọc.

Như vậy tôi **đọc được dữ liệu thật** mà không phải tải hàng chục GB. Chỉ khi probe cho thấy cần (ví dụ DDR-test chỉ vài GB và cần kiểm tra thủ công) tôi mới đề nghị tải riêng phần đó, và sẽ hỏi bạn trước.
