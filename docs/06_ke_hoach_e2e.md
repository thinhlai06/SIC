# 06. Kế hoạch end-to-end (bản 2, đã thêm giai đoạn viết báo cáo lần 1)

Ký hiệu: **[Claude]** tôi làm, **[Nhóm]** nhóm làm. **GPU** = tốn giờ quota Kaggle (30 giờ), **CPU** = không tốn GPU.
🚦 = điểm dừng để chốt với bạn trước khi đi tiếp.

## Nguyên tắc viết báo cáo: "làm đến đâu viết đến đấy"

Báo cáo không để đến cuối mới viết. Sau mỗi mốc lớn có một **đợt viết (W)**:
- Phần nào **đã chốt hoặc đã biết** thì viết ngay bằng nội dung thật.
- Phần nào **chưa có kết quả** thì để vị trí trống có đánh dấu `% [PENDING: ...]` trong file `.tex`, **không điền số giả**. Các số mẫu của template (ví dụ bảng kết quả 3.3) sẽ được thay bằng ô "TBD".
- Nếu phát hiện vấn đề (dữ liệu, kết quả bất thường) thì **sửa lại phần đã viết** ngay đợt đó, không dồn đến cuối.

| Đợt | Sau giai đoạn | Viết gì |
|---|---|---|
| **W1** | GĐ1 (dữ liệu) | Chương 1; 2.1; lý thuyết 2.2; workflow 2.3; 3.1 và 3.2 (có số thật từ probe/EDA); danh sách viết tắt; khởi tạo references |
| **W2** | GĐ4 (huấn luyện) | Cấu hình train thật (2.2), đường cong train, bảng siêu tham số, phụ lục A/B |
| **W3** | GĐ5–6 (đánh giá và phân tích) | 3.3 (kết quả), phân tích Grad-CAM/t-SNE, 3.5 |
| **W4** | GĐ7–9 | 3.4 (demo), 2.4 (system design), chương 4, hoàn thiện references, ngày nộp |

Luôn tuân thủ: giữ nguyên mọi `\section` gốc; chỉ thêm `\subsection`; không `\subsubsection`.

---

## GĐ0. Thiết lập (CPU)
| # | Việc | Ai | Kết quả |
|---|---|---|---|
| 0.1 | Cài `kaggle` CLI, đặt token qua biến môi trường, kiểm tra kết nối và tài khoản Kaggle (GPU, internet trong notebook) | Claude | `kaggle` chạy được |
| 0.2 | Xác nhận quyền dữ liệu EyePACS, tìm bản DDR trên Kaggle | Claude | Danh sách dataset gắn vào notebook |
| 0.3 | Lấy trọng số RETFound từ Hugging Face (Chrome MCP, bạn đã đăng nhập sẵn), đưa lên Kaggle dùng được trong notebook | Claude | Trọng số trong `/kaggle/input` |
| 0.4 | Đẩy repo lên GitHub để thành viên khác đọc | Claude | Repo `thinhlai06/SIC` |

## GĐ1. Dữ liệu (CPU)
| # | Việc | Kết quả |
|---|---|---|
| 1.1 | Notebook **probe**: cấu trúc, nhãn, split Public/Private, id bệnh nhân, kích thước ảnh, ảnh mẫu | `probe_report.md`, hình mẫu |
| 1.2 | Tiền xử lý: cắt viền đen → vuông → 224×224 → cache; kiểm tra ảnh trùng EyePACS↔DDR | Dataset cache trên Kaggle |
| 1.3 | EDA: phân bố lớp, kích thước, màu/độ sáng, ảnh mẫu, ảnh trước/sau xử lý | `evidence_figures/01_data`, `02_preprocessing` |
| 🚦 | Duyệt kết quả probe/EDA (split, rò rỉ bệnh nhân, ảnh trùng) | |

## GĐ2. Viết báo cáo lần 1 (W1) (CPU, mới)
Viết ngay những gì đã chốt. Có thể bắt đầu từ trước khi GĐ1 xong với phần không phụ thuộc dữ liệu.

| # | Việc | Trạng thái nội dung |
|---|---|---|
| 2.1 | `metadata.tex`: tên đề tài EN, Group 3, 2 thành viên (**ngày nộp để trống đến cuối**); bỏ 3 slot thừa ở bìa, mục 1.3, chương 5; mở rộng viết tắt (20–25 mục) | Chốt |
| 2.2 | **Chương 1:** 1.1 bối cảnh (DR, sàng lọc hiện nay, học sâu/ViT/SSL, domain shift); 1.2 động lực và mục tiêu đo được; 1.3 bảng 2 thành viên; 1.4 lịch Weeks 1–10 (trạng thái thực tế) | Chốt |
| 2.3 | **2.1 Data Acquisition:** nguồn, thu thập, gán nhãn, thống kê, chia tập (EyePACS, DDR), hạn chế | Số thật từ probe |
| 2.4 | **2.2 Training Methodology (phần lý thuyết và kế hoạch):** MAE, ViT, RETFound, augmentation, loss, optimizer, chỉ số, công thức đánh số | Lý thuyết chốt; số cấu hình để `[PENDING]` |
| 2.5 | **2.3 Workflow:** mô tả pipeline (kèm sơ đồ khi có) | Chốt (có thể chỉnh sau) |
| 2.6 | **3.1 Preprocessing, 3.2 EDA:** viết bằng số và hình thật từ GĐ1 | Số thật |
| 2.7 | `references.bib`: khoảng 8–10 nguồn nền tảng đầu tiên, đã xác minh qua Google Scholar/web; bỏ `\nocite{*}` | Xác minh từng mục |
| 2.8 | Dọn các số/nội dung mẫu của template (bảng 3.3 → TBD, ô hình placeholder giữ nhãn rõ) | |
| 🚦 | Bạn đọc bản W1 (đặc biệt chương 1, 2.1), góp ý | |

## GĐ3. Code huấn luyện và đo tốc độ (GPU ngắn)
| # | Việc | Kết quả |
|---|---|---|
| 3.1 | Viết code: dataset, augmentation M1/M2, weighted sampler, ViT-L RETFound, ResNet-50, AMP, layer-wise LR decay, lưu/resume checkpoint (session tối đa 12 giờ), log CSV + xuất đường cong | Thư mục `code/` |
| 3.2 | Chạy thử **1 epoch** để đo tốc độ, bộ nhớ, kiểm tra tải trọng số RETFound | Số liệu tốc độ thật |
| 🚦 | **Chốt ngân sách GPU:** số epoch, số seed từng mô hình (tôi chọn mặc định tốt nhất và báo lại bạn) | |

## GĐ4. Huấn luyện (GPU)
Chạy 2 run song song, mỗi run một GPU.
| # | Việc |
|---|---|
| 4.1 | B1 ResNet-50 ×3 seed (rẻ, chạy trước để kiểm tra pipeline) |
| 4.2 | M1 RETFound ×3 seed |
| 4.3 | M2 (M1 + augmentation DG) ×3 seed |
| 4.4 | B2 ViT-L MAE ImageNet ×1 seed (thêm seed nếu còn giờ) |
| 4.5 | Linear probe RETFound và B2 (đã chọn làm) |
| Mỗi run | Log từng epoch, đường cong loss/QWK, chọn checkpoint theo **QWK trên EyePACS-val** (`evidence_figures/03_training`, `logs/`) |
| 🚦 | Duyệt checkpoint đã chốt **trước khi** chạm DDR. Sau đó viết **W2** |

## GĐ5. Đánh giá cuối (GPU, chạy đúng một lần)
| # | Việc |
|---|---|
| 5.1 | EyePACS-test (42.670) và DDR-test (3.759) với checkpoint đã chốt, cho mọi mô hình |
| 5.2 | QWK, Acc, Macro-F1, AUC, recall từng lớp, AUC referable, ΔQWK; bootstrap 95% CI và paired bootstrap |

## GĐ6. Phân tích (GPU nhẹ)
Grad-CAM (ca đúng/sai); t-SNE theo bộ dữ liệu và theo mức bệnh; ablation augmentation M2 và reliability diagram nếu còn giờ; rút kết luận. Sau đó viết **W3**.

## GĐ7. Demo web (CPU, local)
Gradio: upload ảnh → mức DR, xác suất, Grad-CAM; giao diện tiếng Anh; chụp ảnh vào `evidence_figures/07_demo`.

## GĐ8. Hình sơ đồ (CPU, làm được song song khi train)
Pipeline, system design, kiến trúc MAE/RETFound (vẽ bằng Python) → `evidence_figures/06_diagrams`.

## GĐ9. Tài liệu tham khảo (CPU, song song)
Nâng từ 8–10 lên khoảng 15–18 nguồn đã xác minh; mỗi nguồn được trích dẫn có chủ đích.

## GĐ10. Hoàn thiện báo cáo (W4)
Hoàn thiện 3.4, 2.4, chương 4, phụ lục A/B (code và siêu tham số thật), mỗi hình có caption + mô tả, mỗi công thức đánh số + giải thích. **Điền ngày nộp** khi nhóm biết.

## GĐ11. Kiểm tra cuối
| # | Việc | Ai |
|---|---|---|
| 11.1 | Đối chiếu mọi số trong báo cáo với `logs/` và hình | Claude |
| 11.2 | Kiểm tra quy tắc: DDR chỉ chạm ở GĐ5; không `\subsubsection`; các `\section` gốc còn nguyên; không còn số/giả định mẫu của template | Claude |
| 11.3 | Biên dịch trên **Overleaf**, kiểm tra 40–50 trang, lỗi biên dịch | Nhóm (Claude sửa theo log lỗi) |
| 11.4 | Ảnh nhóm, nhận xét thành viên (chương 5), chữ ký/nhận xét giảng viên (chương 6) | Nhóm |

---

## Đường găng, rủi ro, việc song song

- **Đường găng:** 0.3 (trọng số) → 1.2 (cache) → 3.2 (đo tốc độ) → 4 (huấn luyện) → 5 (đánh giá) → W3.
- **Song song khi GPU đang train:** GĐ2 (báo cáo W1), 7, 8, 9.
- **Rủi ro chính:**
  1. **Hết quota GPU** → giảm epoch/seed ở 🚦 sau 3.2.
  2. **Session Kaggle tối đa 12 giờ** → lưu/resume checkpoint từ đầu.
  3. **Trọng số RETFound bị khóa hoặc lệch phiên bản thư viện** → kiểm tra sớm ở 0.3 và 3.2.
  4. **Rò rỉ bệnh nhân hoặc ảnh trùng** → phát hiện ở 1.1/1.2.
  5. **Mức 3 rất hiếm trong DDR** → CI rộng, nói rõ trong báo cáo.
  6. **Không biên dịch được LaTeX trên máy này** → kiểm tra cú pháp cẩn thận; nhóm biên dịch trên Overleaf và gửi log lỗi nếu có.
- **Mô tả trung thực:** SSL là của RETFound; DG ở đây chỉ là augmentation; kết luận chỉ cho cặp EyePACS → DDR.
