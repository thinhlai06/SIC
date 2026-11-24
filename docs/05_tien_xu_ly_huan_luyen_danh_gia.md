# 05. Tiền xử lý, quy trình huấn luyện, đánh giá

> Các số về tốc độ/giờ GPU là **ước lượng sơ bộ**, sẽ đo thật bằng notebook thử trước khi cam kết.

## 1. Tiền xử lý dữ liệu: làm gì và vì sao

Mục tiêu: **cùng một quy trình cho mọi bộ và mọi mô hình**, để chênh lệch kết quả đến từ mô hình/miền chứ không đến từ cách xử lý.

| Bước | Làm gì | Vì sao |
|---|---|---|
| 1. Đọc nhãn, kiểm tra | Đọc CSV, loại ảnh lỗi/không mở được; DDR bỏ lớp 5 (ungradable) → 3.759 ảnh test | Giữ đúng giao thức đã chốt; ảnh không chấm được không có nhãn đáng tin |
| 2. Cắt viền đen | Ngưỡng độ sáng để tìm vùng võng mạc (hình tròn), cắt theo hộp bao | Viền đen khác nhau giữa các máy (một dấu hiệu "đường tắt" của máy chụp); cắt đi để mô hình tập trung vào võng mạc |
| 3. Đưa về hình vuông | Thêm viền cho vuông (không méo) rồi **resize 224×224** (nội suy `INTER_AREA`) | RETFound/ViT-L nhận 224×224; giữ tỉ lệ để không làm méo đĩa thị/hoàng điểm |
| 4. Chuẩn hóa | Trừ mean/chia std (⚠ xác nhận mean/std dùng trong code chính thức của RETFound, nhiều khả năng là mean/std ImageNet) | Đúng với cách trọng số được tiền huấn luyện |
| 5. Cache | Lưu ảnh 224×224 dạng JPEG chất lượng cao (khoảng 2 GB cho ~92 nghìn ảnh) | Mọi run sau đọc nhanh, không phải xử lý lại ảnh gốc 89 GiB |
| 6. Kiểm tra trùng | **Perceptual hash** giữa EyePACS và DDR (và trong EyePACS) | Đảm bảo DDR thật sự là miền chưa thấy; phát hiện rò rỉ |

**Cái tôi cố ý KHÔNG làm:**
- **Không** dùng chuẩn hóa màu kiểu Ben Graham (trừ nền cục bộ) làm mặc định: nó tự là một phép "chuẩn hóa miền", làm lệch nghiên cứu về DG và lệch phân phối so với lúc RETFound pretrain.
- **Không** dùng thông tin DDR (thống kê màu, mean/std) để chỉnh tiền xử lý EyePACS.
- **Không** áp dụng tiền xử lý riêng cho từng mô hình.

**Mất cân bằng lớp (EyePACS):** dùng **weighted sampler** (lấy mẫu cân bằng theo lớp) hoặc weighted loss, vì lớp 0 chiếm khoảng 73%. Mặc định: **weighted cross-entropy + weighted sampler** (nhẹ), đã nêu trong `PROJECT_CONTEXT.md`.

**Augmentation (chỉ trên tập train):**
- **M1 (và B1, B2):** augmentation chuẩn: lật ngang/dọc, xoay, co giãn nhẹ, jitter độ sáng/tương phản nhẹ.
- **M2:** M1 + augmentation mô phỏng domain shift: thay đổi màu (hue/saturation/channel gain), gamma, blur Gaussian, nhiễu, giảm chất lượng (JPEG nén), thay đổi độ sáng/tương phản mạnh, che cục bộ. Mỗi phép áp dụng với xác suất; cường độ chọn theo **EyePACS-val**, **không dùng DDR**.

---

## 2. Quy trình huấn luyện

**Môi trường:** Kaggle notebook, GPU T4 ×2, **30 giờ** quota.

**Cấu hình đề xuất (chỉnh sau khi đo tốc độ):**

| Mục | Giá trị |
|---|---|
| Input | 224×224 |
| Optimizer | AdamW (weight decay khoảng 0,05) |
| Learning rate | Cosine schedule, warmup vài epoch; **layer-wise LR decay ≈ 0,65** cho ViT-L (lớp sâu học nhanh hơn lớp nông) |
| Batch | Nhỏ (8–16 mỗi GPU) + gradient accumulation để đạt batch hiệu dụng khoảng 64 |
| Độ chính xác số | AMP fp16 |
| Epoch | Khoảng 10–15 (quyết định sau khi đo) |
| Loss | Weighted cross-entropy |
| Chọn checkpoint | **QWK cao nhất trên EyePACS-val** |
| Seed | 3 seed (mean ± std) cho M1, M2, B1; B2 theo ngân sách |
| Early stopping | Theo QWK val |

**Mẹo tiết kiệm giờ (quan trọng):** Kaggle tính quota theo **thời gian chạy của notebook**, không theo số GPU. Với 2×T4 nên **chạy hai run độc lập song song, mỗi run trên một GPU** (ví dụ hai seed khác nhau cùng lúc) thay vì DataParallel/DDP cho một run → gần gấp đôi thông lượng trên cùng số giờ quota, không tốn chi phí giao tiếp giữa GPU.

**Ước lượng giờ GPU (⚠ chưa đo):**

| Hạng mục | Ước lượng |
|---|---|
| Probe (CPU), tiền xử lý + cache (CPU/GPU nhẹ) | 2–3 giờ |
| ViT-L/run (M1, M2, B2): 10–15 epoch × 35k ảnh, khoảng 20 phút/epoch/GPU | khoảng 3–5 giờ/run |
| 9 run ViT-L (3 mô hình × 3 seed), 2 run song song | khoảng 15–22 giờ |
| B1 ResNet-50 ×3 | khoảng 1,5–2 giờ |
| Suy luận (EyePACS-test 42.670 + DDR-test 3.759) + Grad-CAM + t-SNE + LP | khoảng 3–4 giờ |
| **Tổng** | khoảng 22–30 giờ → **sát quota** |

Nếu đo thực tế chậm hơn: giảm epoch, giảm seed của B2 xuống 1, đóng băng bớt layer đầu, hoặc dùng subsample nhỏ để chọn siêu tham số.

**Quy tắc tránh rò rỉ trong huấn luyện:**
- Mọi lựa chọn (epoch, LR, mức augmentation, checkpoint) **chỉ dựa trên EyePACS-val**.
- **DDR và EyePACS-test chạy đúng một lần ở cuối**, với checkpoint đã chốt.

**Minh chứng sinh ra trong khi train** (lưu vào `evidence_figures/03_training/` và `logs/`):
- Log từng epoch (CSV): train loss, val loss, val QWK, val acc, LR, thời gian, bộ nhớ GPU.
- Đường cong loss và QWK theo epoch cho mỗi run (và gộp 3 seed).
- Ảnh batch augmentation (M1 so với M2).

---

## 3. Đánh giá: theo tiêu chí gì?

**Chỉ số chính:** **QWK (Quadratic Weighted Kappa)** trên DDR-test.
- Với phân loại có thứ tự, QWK phạt nặng hơn khi nhầm xa (0 ↔ 4) so với nhầm gần (2 ↔ 3). Là chỉ số chuẩn của cuộc thi Kaggle DR và các bài báo DR.

**Chỉ số phụ:**

| Chỉ số | Vì sao dùng |
|---|---|
| **Accuracy** | Dễ hiểu, nhưng **dễ đánh lừa** khi lớp 0 chiếm đa số |
| **Macro-F1** | Trung bình F1 các lớp → công bằng với lớp hiếm |
| **AUC macro (OvR)** | Chất lượng xếp hạng không phụ thuộc ngưỡng |
| **Recall từng lớp** | Mô hình bỏ sót lớp nào (đặc biệt mức 3, 4) |
| **AUC nhị phân "referable" (≥ 2)** | Gần với ca dùng thực tế: sàng lọc có cần chuyển khám không; kèm sensitivity/specificity |
| **Confusion matrix** | Xem lỗi nhầm giữa các mức kề nhau |

**Chỉ số về độ bền vững (cốt lõi của đề tài):**
- **ΔQWK = QWK(EyePACS-test) − QWK(DDR-test)** cho từng mô hình: mô hình nào **tụt ít hơn** là bền vững hơn.
- **Tỉ lệ giữ hiệu năng** = QWK(DDR) / QWK(EyePACS-test).

**Độ tin cậy thống kê:**
- 3 seed → báo cáo **trung bình ± độ lệch chuẩn**.
- **Bootstrap 95% CI** (khoảng 1000 lần lấy mẫu lại) trên DDR-test cho từng chỉ số; **paired bootstrap** để so sánh hai mô hình (M1 so với B2, M2 so với M1…). Do mức 3 rất hiếm trong DDR nên CI của recall/F1 mức 3 sẽ rộng — cần nói rõ.
- Không kết luận "tốt hơn" khi hai CI chồng lấn nhiều.

**Phân tích định tính / chẩn đoán:**
- **Grad-CAM**: mô hình nhìn vào tổn thương (xuất huyết, xuất tiết, vi phình mạch) hay vào rìa ảnh/đặc điểm máy? Chọn ca đúng và ca sai.
- **t-SNE** đặc trưng, tô màu theo **bộ dữ liệu** và theo **mức bệnh**: hai miền có bị tách cụm không? SSL (M1) có làm các miền trộn lẫn hơn B1/B2 không?
- (tùy chọn) Reliability diagram / ECE: độ hiệu chuẩn xác suất khi đổi miền.

**Cảnh báo cần ghi trong báo cáo:**
- **Label shift** (tỉ lệ lớp khác nhau) làm Accuracy giữa hai bộ không so sánh trực tiếp được; ưu tiên QWK, macro-F1 và recall từng lớp.
- Kết luận chỉ áp dụng cho cặp EyePACS → DDR.

**Danh sách hình đầu ra** (lưu vào `evidence_figures/`): xem `evidence_figures/README.md`.

---

## 4. Giải thích dễ hiểu: QWK, B1/B2/M1/M2, và thế nào là "tốt"

### 4.1 QWK là gì, đo cái gì?

**QWK (Quadratic Weighted Kappa)** đo mức độ **đồng thuận giữa mô hình và bác sĩ** khi chấm các mức bệnh **có thứ tự** (0 → 4), có tính đến **khoảng cách** của lỗi.

- **Hình dung:** chấm điểm một bài thi. Máy chấm 3, bác sĩ chấm 2: lệch ít, bị phạt nhẹ. Máy chấm 0, bác sĩ chấm 4: lệch rất xa, bị phạt rất nặng. Phạt tăng theo **bình phương** khoảng cách (nhầm xa 2 mức bị phạt gấp 4 lần nhầm xa 1 mức).
- **Thang đo:** **1** = trùng khít bác sĩ; **0** = không hơn gì đoán ngẫu nhiên; **âm** = tệ hơn đoán ngẫu nhiên.
- **Điểm mạnh:** đã trừ phần "trùng hợp do may rủi", nên không bị lớp đông (mức 0) làm đẹp số.
- **Cách đọc tham khảo** (thang Landis-Koch, dùng cho kappa nói chung): 0,61–0,80 khá tốt; 0,81–1,00 gần như hoàn hảo. Đây chỉ là mốc tham khảo, **không phải ngưỡng đạt/không đạt**.

### 4.2 B1, B2, M1, M2 là gì?

**B = Baseline** (mốc đối chứng). **M = Main** (mô hình của đề tài). Cả bốn đều huấn luyện trên **cùng dữ liệu EyePACS** với cùng quy trình, chỉ khác "bộ não khởi đầu".

| Mã | Mô hình | Hình dung dễ hiểu |
|---|---|---|
| **B1** | ResNet-50, học trước trên ảnh thường (ImageNet) | Người giỏi nhận đồ vật nói chung, chưa từng thấy võng mạc, học chấm bệnh gần như từ đầu |
| **B2** | ViT-L, học trước trên ảnh thường bằng MAE | Cùng loại "bộ não" với RETFound nhưng chưa từng thấy võng mạc |
| **M1** | **RETFound**, đã học trước trên hàng trăm nghìn ảnh võng mạc | Đã "xem" rất nhiều võng mạc trước khi học chấm bệnh |
| **M2** | M1 cộng augmentation mô phỏng máy chụp khác (đổi màu, độ sáng, làm mờ, nhiễu) | Như M1 nhưng được luyện chịu được ảnh từ nhiều kiểu máy |

Mỗi cặp so sánh trả lời **một câu hỏi**:
- **B2 so với M1:** học trước trên *ảnh võng mạc* có thực sự giúp, hay chỉ do kiến trúc ViT-L?
- **M1 so với M2:** augmentation mô phỏng domain shift có giúp thêm không?
- **B1 so với M1:** mô hình thông thường so với mô hình của đề tài.

### 4.3 Làm sao biết mô hình đang "tốt lên" trong lúc huấn luyện?

Sau mỗi epoch ta tính và vẽ biểu đồ trên **EyePACS-val** (không bao giờ nhìn DDR):

| Dấu hiệu | Ý nghĩa | Việc làm |
|---|---|---|
| Train loss giảm **và** val QWK tăng | Đang học thật, tốt lên | Tiếp tục |
| Train loss vẫn giảm nhưng val QWK **đứng yên hoặc giảm** | **Overfitting** (học thuộc dữ liệu train, không tổng quát) | Dừng, lấy checkpoint có val QWK cao nhất |
| Train loss **không giảm** | Cấu hình có vấn đề (tốc độ học quá lớn/nhỏ, lỗi dữ liệu) | Kiểm tra lại, chỉnh |
| Val QWK **dao động mạnh** | Chưa ổn định | Giảm tốc độ học, chạy thêm seed |

Checkpoint tốt nhất được chọn theo **QWK cao nhất trên EyePACS-val**. Biểu đồ loss/QWK theo epoch là minh chứng, lưu ở `evidence_figures/03_training/`.

### 4.4 Tiêu chí "tốt" và vì sao dùng chúng

"Tốt" **không có một con số tuyệt đối**; nó là so sánh có kiểm soát theo các tiêu chí sau:

| Tiêu chí | Trả lời câu hỏi | Vì sao dùng |
|---|---|---|
| **QWK** (chính) | Chấm mức bệnh gần bác sĩ đến đâu? | Hợp với nhãn có thứ tự; đã hiệu chỉnh theo may rủi; là chuẩn của cộng đồng DR |
| **Macro-F1** | Có làm tốt **đều** ở mọi mức, kể cả mức hiếm? | Trung bình các lớp ngang nhau, không để lớp đông át |
| **Recall từng lớp** | Bắt được bao nhiêu ca bệnh **thật** ở từng mức? | Bỏ sót ca nặng nguy hiểm hơn báo nhầm |
| **AUC "referable" (mức ≥ 2)** | Có phân biệt được ca cần chuyển khám không? | Gần với ca dùng thực tế (sàng lọc) |
| **Accuracy** (phụ) | Tỉ lệ đoán đúng | Dễ hiểu, nhưng **dễ đánh lừa** (xem ví dụ dưới) |
| **ΔQWK = QWK(EyePACS-test) − QWK(DDR-test)** | Đổi sang miền mới thì tụt bao nhiêu? | **Đo trực tiếp độ bền vững**, là câu hỏi cốt lõi của đề tài |
| **Khoảng tin cậy 95% (bootstrap)** | Chênh lệch có thật hay chỉ do ngẫu nhiên? | DDR mức 3 chỉ có 71 ảnh nên số rất dao động |

**Ví dụ vì sao Accuracy đánh lừa:** một "mô hình ngốc" luôn đoán *"không bệnh"* sẽ đạt Accuracy khoảng **73,6%** trên EyePACS-test (31.403/42.670 ca là mức 0), nhưng **QWK = 0** và Macro-F1 chỉ khoảng **0,17**, tức không bắt được ca bệnh nào. Trên DDR-test, mô hình đó đạt Accuracy khoảng 50,0% (1.880/3.759). Hai con số Accuracy khác nhau chỉ vì tỉ lệ lớp khác nhau (label shift), không liên quan chất lượng mô hình.

**Đề tài coi mô hình là "tốt" khi (cả ba ý):**
1. Trên **DDR**, M1 (hoặc M2) có QWK **cao hơn** B1 và B2, và khoảng tin cậy không chồng lấn nhiều.
2. **ΔQWK nhỏ hơn**, tức mô hình tụt ít hơn khi đổi miền.
3. Recall các mức nặng (3, 4) **không sụp** (không đạt thì QWK cao cũng chưa đáng tin).

Nếu kết quả không như kỳ vọng (ví dụ M2 không hơn M1), đó **vẫn là kết quả hợp lệ** và được báo cáo trung thực cùng phân tích nguyên nhân.
