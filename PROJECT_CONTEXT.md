# SIC Capstone – Project Context (tổng hợp những gì đã chốt)

> File này lưu lại toàn bộ context đã thống nhất giữa nhóm và Claude để tránh mất thông tin giữa các phiên làm việc.
> **Không ghi API token vào file này.** Token Kaggle nằm riêng trong `c:\SIC\apikey_kaggle.txt`.

---

## 1. Thông tin chung

| Mục | Giá trị |
|---|---|
| Chương trình | Samsung Innovation Campus – AI Course (Capstone Project Final Report) |
| Lớp / Giảng viên | SIC-AI-N02 / TS. Trần Quang Quý (đã có sẵn trong `metadata.tex`) |
| Team name | Group 3 |
| Thành viên (2 người) | **Lai Van Thinh**, **Tran Thuy Duyen** |
| Vai trò (đã đồng ý) | Lai Van Thinh: mô hình & huấn luyện. Tran Thuy Duyen: dữ liệu, đánh giá, demo web |
| Ngôn ngữ báo cáo | **Tiếng Anh** |
| Độ dài báo cáo | **> 40 và < 50 trang** (tính cả bìa, mục lục, phụ lục; nội dung chính nhắm khoảng 38–42 trang) |
| Trình biên dịch | Overleaf (XeLaTeX + Biber). Máy local không có LaTeX và không có GPU |
| Huấn luyện | Hoàn toàn trên Kaggle, **còn 30 giờ GPU** (T4) |

**Tên đề tài gốc (VI):** Học tự giám sát và tổng quát hóa miền nhằm nâng cao độ bền vững của mô hình phân loại bệnh võng mạc tiểu đường trên các bộ dữ liệu ảnh đáy mắt khác nhau.

**Tên đề tài (EN, đã chốt):**
> Self-Supervised Learning and Domain Generalization for Improving the Robustness of Diabetic Retinopathy Grading Across Fundus Image Datasets

**Còn thiếu / chưa chốt:**
- Ngày nộp báo cáo (DD/MM/YY) và deadline của nhóm.
- Loss: mặc định weighted cross-entropy + weighted sampler (chưa có phản hồi thay đổi).
- Ngân sách GPU chi tiết (chốt sau khi đo tốc độ thật).

---

## 2. Quy tắc viết LaTeX (bắt buộc)

Thư mục template: `c:\SIC\Capstone-Project_latex\` (bắt nguồn từ `SIC_AI_Capstone Project_Final Report.docx` của Samsung).

1. **Giữ nguyên** 6 chương và mọi `\section` đã có:
   - 1 Introduction: 1.1 Background Information, 1.2 Motivation and Objective, 1.3 Members and Role Assignments, 1.4 Schedule and Milestones
   - 2 Project Execution: 2.1 Data Acquisition, 2.2 Training Methodology, 2.3 Workflow, 2.4 System Design
   - 3 Results: 3.1 Data Preprocessing, 3.2 Exploratory Data Analysis (EDA), 3.3 Modeling, 3.4 User Interface, 3.5 Testing and Improvements
   - 4 Projected Impact: 4.1 Accomplishments and Benefits, 4.2 Future Improvements
   - 5 Team Member Review and Comment, 6 Instructor Review and Comment (biểu mẫu Samsung, không đổi cấu trúc)
2. **Chỉ thêm nội dung bằng `\subsection`** (dạng 2.1.1, 2.1.2, …). **Không dùng `\subsubsection`** (không có 2.1.1.1).
3. Lịch ở mục 1.4: **giữ nguyên các mốc Weeks 1–10** của template.
4. Template có 5 slot thành viên, nhóm chỉ có 2 người → bỏ 3 slot thừa ở bìa (`metadata.tex`), mục 1.3 và chương 5.
5. **Hình ảnh:** mỗi hình có `\begin{figure}`, `\includegraphics`, `\caption`, `\label`, kèm đoạn mô tả trong thân bài, tham chiếu bằng `Figure~\ref{}` và nêu hình cho thấy điều gì. Đặt file ảnh trong `figures/`.
6. **Công thức:** dùng `equation` có đánh số, sau mỗi công thức giải thích ý nghĩa từng ký hiệu. Không lạm dụng, khoảng 6–8 công thức (MAE reconstruction loss, weighted cross-entropy, QWK, F1, layer-wise LR decay, cosine schedule, bootstrap CI).
7. **Trích dẫn:** tìm bằng Google Scholar / web search, lấy BibTeX thật, đưa vào `references.bib`, dùng `\cite{}`. Khoảng **15–18 nguồn**, chỉ giữ nguồn xác minh được, không bịa. Bỏ các mục mẫu và bỏ `\nocite{*}` trong `main.tex`. Mỗi nguồn phải được trích dẫn có chủ đích.
8. Cần thay các nội dung mẫu của template: placeholder trong `metadata.tex`, bảng kết quả giả ở mục 3.3, code và siêu tham số mẫu ở phụ lục A/B, các hộp placeholder hình.
9. Tạo thêm ảnh **pipeline** và **system diagram** (PNG, vẽ bằng Python) cho mục 2.3 và 2.4.

---

## 3. Bài toán

**Bệnh võng mạc tiểu đường (DR)** là biến chứng mắt của người bị tiểu đường, có thể gây mù. Ảnh đáy mắt được chấm theo 5 mức (thang ICDR): 0 không bệnh, 1 nhẹ, 2 trung bình, 3 nặng, 4 tăng sinh.

**Vấn đề:** mô hình train trên dữ liệu của một nơi (máy chụp, ánh sáng, dân số khác nhau) thường tốt trên chính dữ liệu đó nhưng giảm mạnh khi sang nơi khác (domain shift).

**Hai công cụ:**
- **Học tự giám sát (SSL):** học biểu diễn võng mạc từ ảnh không nhãn (che ảnh rồi tái tạo – MAE), nên ít phụ thuộc đặc điểm của một máy chụp.
- **Tổng quát hóa miền (DG):** train trên miền nguồn, kiểm tra trên miền đích chưa từng thấy, kèm augmentation mô phỏng khác biệt máy chụp (ý tưởng FundusAug của GDRNet).

**Câu hỏi nghiên cứu:** SSL trên ảnh võng mạc (RETFound) và augmentation mô phỏng domain shift có giúp mô hình giữ được hiệu năng khi chuyển từ EyePACS sang DDR hay không?

---

## 4. Dữ liệu (chỉ dùng 2 bộ)

**Quyết định: chỉ dùng EyePACS và DDR. Không dùng APTOS, Messidor-2 hay bộ nào khác.**

### 4.1 EyePACS (miền nguồn – huấn luyện)
- Kaggle *Diabetic Retinopathy Detection* (2015): https://www.kaggle.com/c/diabetic-retinopathy-detection/data
- Nền tảng sàng lọc võng mạc của Mỹ, nhiều loại máy (Centervue DRS, Optovue iCam, Canon CR1/DGi/CR2, Topcon NW) → bản thân đã có nhiều miền con.
- Nhãn 5 mức; ảnh `.jpeg` tên `<id>_left/right`, file `trainLabels.csv`. Dữ liệu gốc khoảng 89 GiB; có bản btgraham-300 khoảng 3,65 GiB và các bản resize trên Kaggle (nên dùng bản nhỏ).
- **Split:** train 35.126 / val 10.906 / test 42.670 (10.906 + 42.670 = 53.576 ảnh test gốc của cuộc thi, khớp split của RETFound).
- **Điểm yếu cần nêu trong báo cáo:** nhãn nhiễu, nhiều ảnh không chấm được bị gán DR0, mỗi ảnh một người chấm, mất cân bằng nặng (lớp 0 khoảng 73%).
- Nhóm đã chấp nhận luật cuộc thi trên Kaggle.

### 4.2 DDR (miền đích – kiểm tra)
- Đại học Nankai (2019), bệnh nhân Trung Quốc, 13.673 ảnh từ 147 bệnh viện, 23 tỉnh, chụp 2016–2018, 7 người chấm được đào tạo, thang ICDR.
- Nhãn 6 lớp (có "ungradable"). Thông lệ bỏ ungradable.
- **Chỉ dùng tập test: 3.759 ảnh (đã bỏ ungradable).** DDR train/val **không dùng**.
- Nguồn: Google Drive của tác giả, GitHub `nkicsl/DDR-dataset`, bản trên Kaggle/HuggingFace.
- Có nhãn pixel/bounding box nhưng không dùng trong đề tài này.

### 4.3 Quy tắc đánh giá (cứng)
- **DDR không được dùng cho bất kỳ việc gì trước khi test cuối**, kể cả chọn checkpoint hay chỉnh siêu tham số. Mọi lựa chọn chỉ dựa trên **EyePACS-val**.
- Test chính trên **DDR (out-of-domain, kết quả chính)**. EyePACS-test là mốc in-domain tham chiếu.
- Ghi chú trong báo cáo: RETFound đã thấy ảnh EyePACS (không nhãn) khi tiền huấn luyện nên số in-domain có thể hơi lạc quan. RETFound bản gốc chưa từng thấy DDR nên kết quả DDR là trung thực.

---

## 5. Mô hình và thí nghiệm

| Mã | Mô hình | Mục đích |
|---|---|---|
| **B1** | ResNet-50 pretrain ImageNet | Baseline thông thường |
| **B2** | ViT-L MAE pretrain ImageNet | Cùng kiến trúc với RETFound, tách riêng tác dụng của SSL trên ảnh võng mạc |
| **M1** | RETFound (ViT-L, MAE, 307M tham số, bản ảnh đáy mắt CFP tiền huấn luyện trên 904.170 ảnh không nhãn, ~90,2% từ MEH-MIDAS và ~9,8% từ Kaggle EyePACS (đã đối chiếu bài Nature 2023; con số 1,6 triệu gồm cả ảnh OCT), UCL + Moorfields) fine-tune trên EyePACS-train | Mô hình chính |
| **M2** | M1 + augmentation mô phỏng domain shift (màu, gamma, blur, nhiễu, giảm chất lượng) | Phần mở rộng DG |

**Cấu hình đề xuất:**
- Input 224×224, AdamW, layer-wise LR decay khoảng 0.65, cosine schedule có warmup, fp16, khoảng 10–15 epoch (tuỳ tốc độ đo thực tế), có thể đóng băng bớt layer đầu.
- Loss: weighted cross-entropy + weighted sampler (xử lý mất cân bằng).
- Chọn checkpoint theo **QWK trên EyePACS-val**.
- **3 seed** cho M1, M2, B1; B2 có thể chạy 1 seed nếu thiếu giờ GPU. Báo cáo trung bình ± độ lệch chuẩn.
- Có thể thêm ablation nhỏ (1 seed) cho từng loại augmentation của M2 nếu còn giờ.

**Cách nói trong báo cáo (không nói quá):** phần SSL do RETFound đã thực hiện sẵn; đóng góp của nhóm là so sánh có kiểm soát (B1, B2, M1, M2) và phân tích domain shift. DG ở đây chỉ gồm augmentation, vì khi huấn luyện không có miền đích. Nêu rõ giới hạn này.

**Chỉ số:** QWK, AUC macro (one-vs-rest), Macro-F1, Accuracy, recall từng lớp, AUC nhị phân "cần chuyển khám" (mức ≥ 2). Thêm **bootstrap 95% CI** trên DDR-test.

---

## 6. Pipeline tổng quát

1. **Chuẩn bị dữ liệu:** EyePACS (split có sẵn), DDR chỉ test (bỏ ungradable → 3.759 ảnh).
2. **Tiền xử lý thống nhất:** cắt viền đen → resize 224×224 → chuẩn hóa; cache ra file nhỏ để dùng lại; kiểm tra ảnh trùng giữa EyePACS và DDR bằng perceptual hash.
3. **Baseline:** B1, B2.
4. **Mô hình chính:** M1, M2; xử lý mất cân bằng nhãn; chọn checkpoint theo QWK trên EyePACS-val.
5. **Đánh giá (chạy một lần ở cuối):** EyePACS-test (in-domain) và DDR-test (out-of-domain, kết quả chính); 3 seed; bootstrap CI.
6. **Phân tích:** độ giảm hiệu năng in → out của từng mô hình; Grad-CAM (mô hình nhìn vào tổn thương hay đặc điểm máy chụp); t-SNE đặc trưng tô màu theo bộ dữ liệu.

---

## 7. Minh chứng bằng hình ảnh (bắt buộc khi train)

Không chỉ xuất bảng số cuối. Mỗi run lưu log từng epoch (CSV/JSON) và xuất hình vào Kaggle output, sau đó đưa vào `figures/`:

- Phân bố lớp của EyePACS và DDR.
- Ảnh mẫu từng mức bệnh; ảnh trước/sau tiền xử lý.
- Ảnh minh họa augmentation của M2.
- Đường cong loss và QWK theo epoch (train/val).
- Confusion matrix và ROC cho EyePACS-test và DDR-test.
- Recall từng lớp.
- Biểu đồ cột độ giảm hiệu năng in → out cho B1, B2, M1, M2, kèm CI.
- Grad-CAM (ca đúng và ca sai).
- t-SNE tô màu theo bộ dữ liệu.
- Sơ đồ pipeline và system diagram (vẽ bằng Python).
- Ảnh chụp demo web.

---

## 8. Demo web (mục 3.4 User Interface)

- Gradio (hoặc Streamlit), **chạy local**, chụp ảnh đưa vào báo cáo (không cần deploy công khai).
- Chức năng: upload ảnh đáy mắt → mức DR dự đoán, xác suất từng lớp, Grad-CAM.
- Suy luận trên CPU; trọng số tải từ Kaggle về sau khi train.

---

## 9. Kaggle và môi trường

- Token Kaggle dạng `KGAT_…` dùng qua biến môi trường `KAGGLE_API_TOKEN` (hoặc `~/.kaggle/access_token`). Token nằm trong `c:\SIC\apikey_kaggle.txt`. Không sao chép vào file khác.
- Ưu tiên làm qua API (`kaggle` CLI, đẩy notebook lên Kaggle). Việc nào API không làm được (ví dụ xin quyền trọng số RETFound trên Hugging Face) thì dùng Chrome MCP; cần đăng nhập sẵn Kaggle và Hugging Face trong Chrome.
- Máy local: Python 3.11.9, không có GPU, không có LaTeX, không có pandoc. Báo cáo xem và biên dịch trên Overleaf.
- **Ngân sách 30 giờ GPU (sơ bộ, chỉnh sau khi đo thật):**
  - khoảng 2–3 giờ: tiền xử lý và đo tốc độ;
  - khoảng 22–24 giờ: các run huấn luyện;
  - phần còn lại: đánh giá, Grad-CAM, t-SNE.
- Ước lượng sơ bộ ViT-L trên T4 fp16: khoảng 10–20 phút mỗi epoch trên 35k ảnh (cần đo thật). Mỗi session Kaggle tối đa 12 giờ. Đủ 12 run (4 mô hình × 3 seed) có thể vượt hạn mức → ưu tiên theo thứ tự: đo tốc độ → 3 seed cho M1, M2, B1 → B2 1 seed nếu thiếu giờ.
- Trọng số RETFound: dùng bản CFP (`RETFound_mae_natureCFP`, trên Hugging Face / GitHub), có thể cần xin quyền hoặc chấp nhận điều khoản. Cần kiểm tra khi bắt đầu.

---

## 10. Cấu trúc báo cáo dự kiến (40–50 trang)

- **Ch.1:** bối cảnh DR, động lực (domain shift), mục tiêu, bảng 2 thành viên, lịch Weeks 1–10.
- **Ch.2:**
  - 2.1: nguồn dữ liệu, thống kê, hạn chế;
  - 2.2: SSL/MAE, ViT, RETFound, augmentation, loss, optimizer, môi trường Kaggle;
  - 2.3: workflow (có ảnh pipeline);
  - 2.4: system design (có ảnh system diagram).
- **Ch.3:** tiền xử lý; EDA; kết quả B1/B2/M1/M2; bootstrap CI; in → out drop; Grad-CAM; t-SNE; demo web; ablation, phân tích lỗi, cải tiến.
- **Ch.4:** thành tựu và lợi ích (sàng lọc DR hỗ trợ tuyến cơ sở), hạn chế và hướng phát triển (thêm miền, TTA, pretrain SSL tiếp trên miền đích không nhãn, v.v.).
- **Ch.5–6:** biểu mẫu Samsung (ảnh nhóm, nhận xét thành viên, rubric giảng viên).
- **References:** khoảng 15–18 nguồn (RETFound, MAE, ViT, ResNet, DDR, EyePACS/Kaggle DR, GDRNet/FundusAug, SSiT, DG survey, QWK, Grad-CAM, t-SNE, AdamW, v.v. — chỉ giữ nguồn xác minh được).
- **Appendix A/B:** code huấn luyện và bảng siêu tham số thật của nhóm.

---

## 10b. Quyết định bổ sung (sau các phiên thảo luận)

- **Ủy quyền kỹ thuật:** người dùng không chuyên học máy/học sâu → Claude **chọn hướng tốt nhất theo điều kiện hiện có** và báo lại. Khi cần ý kiến về học máy/học sâu, Claude phải **giải thích dễ hiểu** (tránh thuật ngữ trần, ví dụ thực tế) rồi mới hỏi.
- **Ngày nộp:** để **đến cuối** mới điền (nhóm chưa biết ngày). `metadata.tex` giữ placeholder ngày đến lúc đó.
- **Hugging Face:** người dùng đã đăng nhập sẵn trên Chrome (dùng Chrome MCP khi cần lấy trọng số RETFound).
- **Chọn mặc định:** có làm linear probe (RETFound, B2); B2 chạy 1 seed trước, thêm nếu còn giờ GPU; loss = weighted cross-entropy + weighted sampler; demo giao diện tiếng Anh.
- **Viết báo cáo theo đợt (W1–W4):** "làm đến đâu viết đến đấy". Phần đã chốt viết bằng nội dung thật; phần chưa có kết quả để `% [PENDING: ...]`, không điền số giả. Chi tiết trong `docs/06_ke_hoach_e2e.md`.
- **Các tài liệu giải thích** nằm trong `docs/` (01–06). **Ảnh minh chứng** lưu trong `evidence_figures/` (xem README ở đó), log số liệu thô trong `logs/`.
- **GitHub:** repo `https://github.com/thinhlai06/SIC` (public) để thành viên khác đọc. **Không bao giờ commit** `apikey_kaggle.txt` (đã có trong `.gitignore`).

---

## 11. Trạng thái công việc

- [x] Đọc và hiểu template LaTeX, `SIC.docx`, API Kaggle.
- [x] Chốt ngôn ngữ, độ dài, thành viên, tên đề tài EN, 2 bộ dữ liệu, mô hình, cách trích dẫn, demo local.
- [ ] Chốt ngày nộp, deadline, ngân sách GPU (sau khi đo tốc độ).
- [ ] Thiết lập Kaggle (API, dataset EyePACS, DDR test, trọng số RETFound).
- [ ] Tiền xử lý và cache dữ liệu; EDA.
- [ ] Huấn luyện B1, B2, M1, M2 (xuất log và hình).
- [ ] Đánh giá, Grad-CAM, t-SNE, bootstrap CI.
- [ ] Demo web và ảnh chụp.
- [ ] Cập nhật `metadata.tex`, viết nội dung LaTeX, `references.bib`, ảnh pipeline.
- [ ] Biên dịch trên Overleaf, kiểm tra 40–50 trang.
