# 01. Bài toán, học tự giám sát (SSL), tổng quát hóa miền (DG)

## 1. Bài toán là gì?

**Bối cảnh.** Bệnh võng mạc tiểu đường (Diabetic Retinopathy, DR) là biến chứng ở mắt của người bị tiểu đường, có thể gây mù nếu phát hiện muộn. Bác sĩ chụp ảnh đáy mắt (fundus photograph) rồi chấm **5 mức** theo thang ICDR:

| Mức | Ý nghĩa |
|---|---|
| 0 | Không bệnh |
| 1 | Nhẹ |
| 2 | Trung bình |
| 3 | Nặng |
| 4 | Tăng sinh (rất nặng) |

Mức ≥ 2 thường được coi là **"cần chuyển khám chuyên khoa"** (referable DR).

**Nhiệm vụ của mô hình:** nhận 1 ảnh đáy mắt → dự đoán mức 0–4. Đây là bài toán **phân loại có thứ tự** (nhầm 0 thành 4 tệ hơn nhầm 2 thành 3), nên ngoài accuracy ta dùng thêm QWK (xem file 05).

**Vấn đề thật sự của đề tài không phải là "chấm bệnh", mà là "chấm bệnh ở nơi khác".**

Một mô hình train bằng ảnh của bệnh viện A (máy chụp A, ánh sáng A, dân số A) thường đạt kết quả rất tốt trên chính dữ liệu đó. Đem sang bệnh viện B (máy khác, ánh sáng khác, nhóm bệnh nhân khác, người chấm khác) thì độ chính xác tụt mạnh. Hiện tượng này gọi là **domain shift** (dịch chuyển miền). Nguyên nhân gồm:

- **Covariate shift:** ảnh nhìn khác nhau (màu, độ sáng, độ phân giải, trường nhìn, nhiễu, viền đen, thiết bị).
- **Label/prior shift:** tỉ lệ các mức bệnh khác nhau giữa hai bộ (ví dụ EyePACS có khoảng 73% mức 0, DDR có tỉ lệ mức 2 cao hơn nhiều).
- **Annotation shift:** tiêu chuẩn và người chấm khác nhau (EyePACS: một người chấm mỗi ảnh; DDR: 7 người chấm được đào tạo).

Mô hình dễ học "đường tắt" (shortcut): nhận ra **máy chụp** thay vì **tổn thương** — ví dụ ảnh từ máy X thường có nhiều ca bệnh, nên mô hình gắn "dấu hiệu máy X" với "có bệnh". Khi đổi máy, đường tắt hỏng.

**Câu hỏi nghiên cứu:**
> Học tự giám sát trên ảnh võng mạc (RETFound) và augmentation mô phỏng domain shift có giúp mô hình giữ được hiệu năng khi chuyển từ EyePACS sang DDR hay không, và giúp bao nhiêu?

---

## 2. Học tự giám sát (Self-Supervised Learning, SSL) là gì?

Học có giám sát thường cần **nhãn** (do bác sĩ chấm — đắt và chậm). Ảnh đáy mắt **không nhãn** thì có rất nhiều. SSL tạo ra một **bài toán phụ tự sinh nhãn từ chính dữ liệu**, để mô hình học được "ảnh này trông như thế nào" mà không cần bác sĩ.

**Ví dụ dùng trong đề tài: MAE (Masked Autoencoder).**
1. Chia ảnh thành các mảnh vuông nhỏ (patch 16×16).
2. **Che ngẫu nhiên khoảng 75%** số patch.
3. Cho encoder (ViT) nhìn 25% còn lại, decoder phải **tái tạo lại các patch bị che**.
4. Để làm được, encoder buộc phải hiểu cấu trúc võng mạc: đĩa thị, hoàng điểm, mạch máu, vị trí tương đối giữa các thành phần.

Sau tiền huấn luyện, bỏ decoder, giữ encoder, thêm một "đầu phân loại" và **fine-tune** bằng ít nhãn hơn.

**Vì sao SSL có thể giúp bền vững hơn?** (đây là *giả thuyết* của đề tài, phải kiểm chứng bằng thực nghiệm)
- Biểu diễn học từ hàng trăm nghìn ảnh từ **nhiều nguồn** ít bị gắn với một máy chụp duy nhất.
- Không bị "kéo" theo nhãn nhiễu của một bộ dữ liệu cụ thể.
- Đã thấy nhiều biến thể ánh sáng/màu sắc trước khi bắt đầu học chấm bệnh.

---

## 3. Tổng quát hóa miền (Domain Generalization, DG) là gì?

**DG** là bài toán: huấn luyện trên một hoặc nhiều miền **nguồn**, rồi chạy tốt trên miền **đích chưa từng thấy** (và **không được** dùng dữ liệu miền đích khi huấn luyện, kể cả không nhãn). Khác với *domain adaptation* (được nhìn trước dữ liệu đích).

Các nhóm kỹ thuật DG phổ biến:
- **Tăng cường dữ liệu (data augmentation)** mô phỏng các khác biệt có thể gặp (màu, gamma, blur, nhiễu, chất lượng ảnh) — đây là hướng của **FundusAug** trong GDRNet.
- Học đặc trưng bất biến (domain-invariant): CORAL, DANN, IRM… (cần nhiều miền nguồn có nhãn miền).
- Chuẩn hóa/biến đổi kiểu thống kê đặc trưng, meta-learning…

Đề tài có **một miền nguồn chính** (EyePACS, dù bên trong nhiều loại máy nhưng không có nhãn máy) nên chọn hướng **augmentation** (thực tế và khả thi), và dùng **giao thức đánh giá DG chuẩn**: train ở nguồn, test ở đích chưa thấy.

---

## 4. Ánh xạ vào đề tài: hai vấn đề được giải quyết ở đâu?

| Thành phần | Nằm ở đâu trong pipeline | Vai trò |
|---|---|---|
| **SSL** | **Trọng số RETFound** (ViT-L, MAE trên ảnh võng mạc không nhãn) → dùng làm khởi tạo cho M1 và M2 | Cung cấp biểu diễn võng mạc bền vững *trước khi* học chấm bệnh |
| **Đối chứng SSL** | **B2** (ViT-L MAE tiền huấn luyện trên ImageNet) và **B1** (ResNet-50 ImageNet có giám sát) | Cô lập tác động của "SSL **trên ảnh võng mạc**": cùng kiến trúc với M1 nhưng khác dữ liệu tiền huấn luyện |
| **DG – phương pháp** | **M2** = M1 + augmentation mô phỏng domain shift (khối augmentation trong pipeline huấn luyện) | Ép mô hình bỏ "đường tắt" gắn với máy chụp |
| **DG – giao thức** | **Train EyePACS → Test DDR chưa thấy**, DDR không được dùng cho chọn checkpoint/siêu tham số | Đo đúng khả năng tổng quát hóa miền |
| **Chẩn đoán lý do** | Grad-CAM, t-SNE theo bộ dữ liệu, độ giảm in → out | Xem mô hình nhìn vào tổn thương hay vào đặc điểm máy; xem hai miền có tách cụm không |

**Cách nói trung thực trong báo cáo:**
- Phần SSL **do RETFound đã thực hiện sẵn** (không phải nhóm pretrain). Đóng góp của nhóm là **thiết kế so sánh có kiểm soát** (B1, B2, M1, M2) và **phân tích** domain shift.
- DG ở đây chỉ gồm augmentation (single-source DG); không có kỹ thuật học đặc trưng bất biến. Nêu rõ đây là giới hạn.
- Nếu M2 không hơn M1 thì đó vẫn là một kết quả trung thực và đáng bàn.
