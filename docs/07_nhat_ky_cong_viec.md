# 07. Nhật ký công việc (work log)

File này ghi lại **việc đã làm, mục đích, và lý do** ở từng giai đoạn, để nhóm và các thành viên khác đọc lại được. Sẽ được **cập nhật tiếp** sau mỗi giai đoạn. Ngày ghi theo máy: 2026-11-24.

Quy ước mỗi mục: **Làm gì** → **Mục đích** → **Vì sao làm vậy** → **Kết quả**.

---

## Giai đoạn chuẩn bị: đọc hiểu dự án (trước GĐ0)

### P1. Đọc toàn bộ file trong dự án
- **Làm gì:** Đọc `Capstone-Project_latex/` (main, 6 chương, appendices, metadata, preamble, references, README), `SIC.docx` (đề bài, 2 bộ dữ liệu, mô hình, luồng tổng quát), `apikey_kaggle.txt`, và file Word mẫu của Samsung.
- **Mục đích:** Nắm cấu trúc template, các mục bắt buộc giữ nguyên, và đề tài của nhóm.
- **Vì sao:** Mọi quyết định sau (chỉ thêm `\subsection`, giữ các `\section` gốc, thiết kế thí nghiệm) phải bám đúng template và đề bài, không đoán.
- **Kết quả:** Hiểu quy tắc: 6 chương cố định, chỉ thêm mục con dạng x.y.z, không đi sâu hơn. Template còn nhiều nội dung mẫu (số giả ở bảng 3.3, code mẫu ở phụ lục, tài liệu tham khảo mẫu) cần thay.
- **Sai sót của tôi:** Khi đọc `apikey_kaggle.txt`, lệnh che token không hoạt động nên **token Kaggle bị in ra log phiên này**. Từ đó tôi chỉ đọc token vào biến môi trường và không in ra. Bạn nên **tạo lại token Kaggle** cho an toàn.

### P2. Hỏi đáp để chốt yêu cầu
- **Làm gì:** Hỏi về ngôn ngữ, độ dài, thành viên, tên đề tài, ngân sách GPU, demo, trích dẫn; sau đó chốt: tiếng Anh, 40–50 trang, 2 thành viên (Lai Van Thinh, Tran Thuy Duyen), Group 3, chỉ dùng EyePACS + DDR, demo web chạy local.
- **Mục đích:** Tránh làm sai hướng rồi phải làm lại.
- **Vì sao:** Đề tài và template có nhiều chỗ mơ hồ (ví dụ SIC.docx nhắc APTOS nhưng sau đó bạn chốt chỉ 2 bộ).
- **Kết quả:** Ghi trong `PROJECT_CONTEXT.md`.

### P3. Tạo `PROJECT_CONTEXT.md`
- **Làm gì:** Viết một file tổng hợp mọi điều đã chốt và hiểu biết về đề tài.
- **Mục đích:** Không mất ngữ cảnh khi phiên làm việc dài hoặc đổi phiên.
- **Vì sao:** Bạn yêu cầu rõ để tránh quên context.

### P4. Viết 5 tài liệu giải thích (`docs/01`–`05`) và đọc file mẫu của nhóm khác
- **Làm gì:** Giải thích bài toán, SSL, DG; hai bộ dữ liệu và lý do train/test; vì sao chọn RETFound; có nên train mô hình khác, rút bài học từ `Group3_SIC_AI_N02-signed.pdf`; tiền xử lý, huấn luyện, đánh giá.
- **Mục đích:** Giúp bạn (không chuyên học máy) hiểu và đồng ý với các quyết định kỹ thuật trước khi tốn giờ GPU.
- **Vì sao:** Các lựa chọn (dùng EyePACS để train, DDR chỉ test, baseline B1/B2, chọn checkpoint chỉ theo EyePACS-val) quyết định tính hợp lệ của kết luận nghiên cứu.
- **Kết quả:** 5 file trong `docs/`. Từ file mẫu rút ra: cấu trúc `x.y.z`, phụ lục A/B, caption bảng ở trên, caption hình ở dưới, công thức đánh số có giải thích. Chỉ học bố cục, không sao chép nội dung.

### P5. Tạo thư mục minh chứng `evidence_figures/` và `logs/`
- **Làm gì:** Tạo 7 thư mục con (data, preprocessing, training, evaluation, analysis, diagrams, demo) kèm `README.md` quy ước tên.
- **Mục đích:** Mọi hình sinh ra khi train có chỗ lưu cố định để đưa vào báo cáo.
- **Vì sao:** Bạn yêu cầu báo cáo phải có biểu đồ minh chứng, không chỉ bảng số.

### P6. Lập kế hoạch end-to-end (`docs/06`) và thêm đợt viết báo cáo lần 1
- **Làm gì:** Chia 12 giai đoạn (GĐ0–GĐ11), thêm GĐ2 "Báo cáo lần 1" và 4 đợt viết W1–W4, đánh dấu 4 điểm dừng cần bạn duyệt.
- **Mục đích:** Có bản đồ toàn cục, và viết báo cáo song song với công việc thay vì dồn cuối.
- **Vì sao:** Bạn muốn "làm đến đâu viết đến đấy"; phần chưa có kết quả để `% [PENDING]`, không điền số giả.

### P7. Đẩy toàn bộ lên GitHub
- **Làm gì:** `git init`, nối `https://github.com/thinhlai06/SIC.git`, thêm `.gitignore`, commit và push (commit `cbf1596`).
- **Mục đích:** Thành viên khác đọc được.
- **Vì sao và các quyết định:** Repo là **public**, nên tôi **không push `apikey_kaggle.txt`** (chứa token) và **không push `Group3_SIC_AI_N02-signed.pdf`** (báo cáo có chữ ký của nhóm khác). Khôi phục `README.md` gốc của repo thay vì xóa nó. Thêm `.gitkeep` để giữ thư mục rỗng. Đã kiểm tra lại trên GitHub: không có file nhạy cảm.

---

## GĐ0. Thiết lập

### 0.1 Cài Kaggle CLI và kiểm tra token
- **Làm gì:** `pip install kaggle` (bản 2.2.5), đọc token từ file vào biến môi trường `KAGGLE_API_TOKEN`, chạy thử liệt kê cuộc thi và dataset.
- **Mục đích:** Điều khiển Kaggle từ máy này (xem dữ liệu, đẩy notebook, tải kết quả) thay vì thao tác tay.
- **Vì sao:** Máy local không có GPU; huấn luyện chạy trên Kaggle. Cần chắc token hoạt động trước khi viết code.
- **Kết quả:** Hoạt động, tài khoản `thinhlai`. Truy cập được cuộc thi `diabetic-retinopathy-detection` (đã accept luật).

### 0.2 Xác định nguồn dữ liệu EyePACS và DDR, kiểm chứng số liệu
- **Làm gì:** Liệt kê file của cuộc thi, tìm các bản resize và bản DDR trên Kaggle, tải **chỉ các file nhãn nhỏ** (`trainLabels15.csv`, `testLabels15.csv`, `DR_grading/test.txt`) và phân tích.
- **Mục đích:** Kiểm tra những con số nhóm đang giả định (split, số ảnh, phân bố lớp) trước khi đưa vào báo cáo và thiết kế thí nghiệm.
- **Vì sao:** Cuộc thi gốc **không có nhãn test**, ảnh là file zip chia nhỏ khoảng 89 GB nên không tiện dùng. Cần một bản có nhãn test và đã resize. Chỉ tải file nhãn (vài MB) để không phải tải hàng chục GB.
- **Kết quả (đã xác minh):**
  - EyePACS: train 35.126; val (Public) 10.906; test (Private) 42.670. **Không có bệnh nhân trùng** giữa các tập, nên không rò rỉ. Nguồn dùng: `benjaminwarner/resized-2015-2019-blindness-detection-images`.
  - DDR-test: 4.105 ảnh, bỏ ungradable còn 3.759. Mức 3 chỉ có **71 ảnh** (CI sẽ rộng). Nguồn dùng: `samriddhibagchi/ddr-dataset-credits-to-authors`.
  - **Label shift:** EyePACS mức 0 khoảng 74%, DDR-test khoảng 50% mức 0 và 36% mức 2, nên không so Accuracy trực tiếp giữa hai bộ; ưu tiên QWK, macro-F1.
  - Đã cập nhật `docs/02_dataset.md` và `logs/gd0_findings.md`.

### 0.3 Lấy trọng số RETFound
- **Làm gì:**
  1. Kiểm tra giấy phép và hướng dẫn qua GitHub và API công khai: giấy phép **CC BY-NC 4.0** (phi thương mại); repo Hugging Face bị khóa kiểu `auto`.
  2. Thử dùng Chrome để bấm đồng ý điều khoản, nhưng công cụ Chrome không kết nối được. Bạn tự bấm đồng ý và đưa token Hugging Face (lưu trong `apikey_kaggle.txt`, file bị git chặn).
  3. Kiểm tra token: tài khoản `thinhv`, đã có quyền tải `RETFound_mae_natureCFP.pth` (3,95 GB). Tải về `data/retfound/` (thư mục bị git chặn) chạy nền.
- **Mục đích:** Có trọng số SSL tiền huấn luyện để fine-tune M1 và M2.
- **Vì sao:** Đọc giấy phép trước khi tải vì repo yêu cầu đồng ý điều khoản; đồ án học thuật là phi thương mại nên hợp lệ. Trọng số **không được đưa lên GitHub public**; sẽ chỉ để trong Kaggle dataset **private**.
- **Việc cần xác minh sau (ghi để không quên):** Model card Hugging Face ghi tiêu đề "RETFound_MAE_MEH" và `config.json` ghi `"dataset": "MEH MIDAS"`, trong khi tôi nhớ bài Nature nói bản ảnh đáy mắt (CFP) tiền huấn luyện trên MEH-MIDAS **và** Kaggle EyePACS. Điều này ảnh hưởng đến lời cảnh báo "RETFound đã thấy EyePACS khi pretrain". **Sẽ đối chiếu với bài báo Nature** ở bước tìm tài liệu tham khảo trước khi viết câu này vào báo cáo.
- **Trạng thái:** đang tải; sau đó upload thành Kaggle dataset private.

### 0.4 GitHub
- Xem P7. Sau đó có thêm commit `ee578a7` ghi kết quả GĐ0 và `.gitignore` chặn `hf_token.txt`.

---

## Các lưu ý và sai sót cần nhớ

| Mục | Ghi chú |
|---|---|
| Token Kaggle bị in ra log | Lỗi của tôi ở P1. Khuyến nghị tạo lại token. |
| `apikey_kaggle.txt` chứa cả token Kaggle và Hugging Face | Đã bị git chặn, nhưng nên xem xét đổi token nếu từng chia sẻ file này. Có thể tách token HF sang file riêng `hf_token.txt` (cũng bị chặn). |
| Công cụ Chrome không kết nối | Đã đi đường vòng bằng token. Nếu sau này cần thao tác web, cần bật extension. |
| Số liệu ước lượng giờ GPU | Vẫn là ước lượng, chưa đo; sẽ đo ở GĐ3. |

---

## Viết báo cáo đợt 1 (W1) trong lúc chờ kernel đóng gói (2026-11-24)

> Kernel `sic-dr-package` (CPU) chạy từ khoảng 19:07 và đến 21:04 vẫn `RUNNING`; Kaggle không cho xem log khi đang chạy. Trong lúc chờ làm các việc **không phụ thuộc kết quả đóng gói** và **không đụng GPU**.

### W1.1 Xác minh tài liệu tham khảo và viết `references.bib`
- **Làm gì:** Tìm kiếm web để đối chiếu thông tin các nguồn (RETFound Nature 2023, DDR/Information Sciences 2019, GDRNet/MICCAI 2023, Domain Generalization survey/TPAMI 2023, MAE/CVPR 2022, EyePACS/J Diabetes Sci Technol 2009, thang ICDR/Ophthalmology 2003); các nguồn kinh điển còn lại (ViT, ResNet, ImageNet, AdamW, SGDR, AMP, label smoothing, Cohen kappa, Bootstrap, Grad-CAM, t-SNE, Gulshan 2016) ghi theo thông tin chuẩn đã biết. Tổng **20 nguồn**, mỗi nguồn đều được `\cite` ít nhất một lần; đã bỏ `\nocite{*}`.
- **Mục đích:** Có tài liệu tham khảo thật để trích dẫn trong chương 1–3.
- **Kết quả đáng chú ý (đã đối chiếu bài Nature):** RETFound bản ảnh đáy mắt tiền huấn luyện trên **904.170** ảnh, ~90,2% MEH-MIDAS và ~9,8% **Kaggle EyePACS**, không nhãn (1,6 triệu là tổng cả OCT). → Việc "RETFound đã thấy EyePACS khi pretrain" là đúng, nên số in-domain của M1 có thể hơi lạc quan; DDR không nằm trong dữ liệu pretrain. (Lưu ý: `config.json` trên Hugging Face ghi `"dataset": "MEH MIDAS"`; bài Nature là nguồn chính thức cho bản natureCFP.)
- **Cần soát tay trước khi nộp (không bịa, nhưng chưa đối chiếu từng chữ trên Google Scholar):** thứ tự tác giả DDR (Li, Gao, Wang, Guo, Liu, Kang), số trang MICCAI của GDRNet (đang để trống, chỉ ghi arXiv:2307.04378), danh sách đầy đủ tác giả RETFound (đang rút gọn bằng "and others").

### W1.2 Sơ đồ (vẽ bằng Python: `code/figures/make_diagrams.py`)
- `g01_pipeline.png` (mục 2.3), `g02_system_design.png` (mục 2.4), `g03_mae_retfound.png` (mục 2.2). Lưu ở `evidence_figures/06_diagrams/`, bản dùng cho báo cáo ở `Capstone-Project_latex/figures/`.

### W1.3 Nội dung LaTeX đã viết
- `metadata.tex` (tên đề tài EN, Group 3, 2 thành viên; **ngày nộp để trống đến cuối**); bỏ 3 slot thành viên thừa ở bìa (`sicaireport.cls`) và chương 5; bảng viết tắt; bỏ `\nocite{*}`.
- Chương 1 (4 section, 15 subsection x.y.z, 3 giả thuyết H1–H3), chương 2 (2.1 dữ liệu với bảng số liệu đã xác minh; 2.2 phương pháp huấn luyện với **7 công thức đánh số** MAE, sampler, CE nhãn làm mượt, LLRD, cosine, QWK, ΔQWK; 2.3 workflow; 2.4 system design), chương 3 (3.1 tiền xử lý; 3.2 EDA với 5 hình d01–d05; 3.3–3.5 để `% [PENDING: ...]`), phụ lục A/B bằng code và siêu tham số thật (đánh dấu "planned" những giá trị chờ đo tốc độ).
- Không có con số kết quả mô hình nào được bịa; bảng kết quả giả của template đã bị xóa.
- Kiểm tra tĩnh bằng `code/figures/check_tex.py` (không cần LaTeX): nhãn/tham chiếu khớp, mọi `\cite` có trong bib, môi trường cân bằng, không có `\subsubsection`, đủ file hình. **Chưa biên dịch thật** (máy không có LaTeX) → cần bạn biên dịch trên Overleaf và báo lỗi nếu có.

### Còn chờ (phụ thuộc kernel đóng gói)
- Mục 3.1: kết quả QA, hình trước/sau cắt viền, kết quả kiểm tra ảnh trùng dHash (đang là `% [PENDING]`).

### GĐ1 hoàn tất (2026-11-24 21:21)
- Kernel `sic-dr-package` chạy khoảng 2 giờ 36 phút (đọc lại 92.000 file nhỏ rất chậm), kết thúc COMPLETE. Tải về `logs/_pkg/` (4 file tar khoảng 1,8 GB + báo cáo; thư mục này bị `.gitignore`); báo cáo và hình đã chép vào `logs/` và `evidence_figures/02_preprocessing/`.
- Kết quả QA và kiểm tra trùng: xem `docs/02_dataset.md` (mục "Kết quả tiền xử lý và kiểm tra ảnh trùng").
- Bước dHash trên Kaggle cho kết quả gây hiểu lầm (94% "gần trùng"); đã viết `code/preprocess/dup_check_local.py` chạy trên máy (CPU, đọc trực tiếp các file tar) để kiểm tra lại bằng bộ mô tả chặt hơn, có tự kiểm chứng bằng bản sao bị làm hỏng. Kết luận: không có ảnh trùng.
- Overleaf: bản nháp biên dịch báo "hết thời gian" (0 lỗi, 3 cảnh báo). Đã giảm ảnh `d03` (3,1 MB → 217 KB, đổi sang JPG), sửa bảng `tab:experiments` (cảnh báo tabularx), bỏ chữ đậm trong listing (cảnh báo font). Nguyên nhân chính khả dĩ: lần biên dịch đầu của XeLaTeX phải dựng cache font; gói miễn phí giới hạn thời gian.
- Báo cáo: đã điền kết quả GĐ1 vào mục 3.1 (kết quả tiền xử lý, hình trước/sau cắt viền, kiểm tra trùng).

---

## GĐ1 duyệt, chuẩn bị GĐ3 (benchmark GPU) và MiKTeX (2026-11-24 đêm)

> Người dùng duyệt GĐ1. Thời gian còn lại để hoàn thiện báo cáo: khoảng 12 giờ (đến khoảng 10:00 ngày 25/11), nên chỉ làm những việc cần thiết cho báo cáo.

### MiKTeX (biên dịch PDF tại máy, không phụ thuộc Overleaf)
- **Làm gì:** cài MiKTeX 25.12 bằng `winget install MiKTeX.MiKTeX --source winget --scope user` (lần đầu lỗi vì nguồn `msstore`), cập nhật cơ sở dữ liệu tên file (`initexmf --update-fndb`) vì `geometry.sty` ở trạng thái "đã cài nhưng không tìm thấy". Viết `code/figures/build_pdf.sh` (xelatex → biber → xelatex ×2).
- **Kết quả:** biên dịch thành công `Capstone-Project_latex/main.pdf` (37 trang), đúng cấu trúc template (bìa, mục lục, danh mục hình/bảng, chương 1–6, tài liệu tham khảo, phụ lục). Chỉ còn 1 cảnh báo overfull nhỏ (13 pt). Bảng 2.3 từng tràn lề đã sửa.
- **Lưu ý:** lúc chạy lần đầu tôi chạy hai chuỗi biên dịch chồng nhau và phải dừng các tiến trình TeX bằng tay.

### Chuẩn bị benchmark / huấn luyện
- Trọng số B1 (ResNet-50 torchvision v1 qua timm) và B2 (ViT-L MAE ImageNet của Meta) tải về, **đã kiểm tra nạp được trên CPU**: ViT: thiếu `fc_norm`/`head` (khởi tạo mới, đúng công thức chính thức), thừa `norm` (bỏ); ResNet: chỉ thiếu `fc`. Upload thành Kaggle dataset private `thinhlai/sic-dr-imagenet-weights`.
- `train_lib.py`: thêm hàng đợi theo GPU (nhiều job tuần tự trên mỗi GPU), `resolve_path` (tìm file trọng số theo tên trong `/kaggle/input`), và `final_eval()` — đánh giá EyePACS-test và DDR-test **đúng một lần** trên checkpoint tốt nhất theo EyePACS-val (lưu logits + đặc trưng vào `.npz`). Đã kiểm thử CPU với dữ liệu giả.
- `code/eval/analyze.py`: tính QWK, macro-F1, AUC referable, recall từng mức, bootstrap CI 1000 lần (dùng chung mẫu lại để so sánh cặp), hình e01–e05, t-SNE a03/a04, và bảng LaTeX tự sinh từ `results.json` (tránh chép số tay). Kiểm thử bằng dữ liệu giả (không phải kết quả thật).
- `code/demo/gradcam.py` và `app.py` (Gradio, giao diện tiếng Anh) kiểm thử với mô hình ngẫu nhiên nhỏ.
- Benchmark `thinhlai/sic-dr-bench` đã đẩy lên Kaggle (M1 và B2 ViT-L song song trên 2 GPU, rồi B1), đang xếp hàng chờ GPU.

---

## Quyết định về huấn luyện (25/11, 00:50) — ghi ngắn, có lý do

**Kết quả K1 (M1 và B2, 5 epoch, 1 seed, mỗi lần chạy 113 phút):**

| Mô hình | QWK val (epoch 1→5) | QWK EyePACS-test | QWK DDR-test |
|---|---|---|---|
| M1 (RETFound) | 0,587 → 0,662 → 0,671 → 0,678 → **0,694** | 0,680 | 0,691 |
| B2 (ViT-L ImageNet) | 0,533 → 0,607 → 0,638 → 0,658 → **0,668** | 0,654 | 0,722 |

- **Nhận xét:** QWK val **còn tăng ở epoch 5** (M1 +0,016, B2 +0,010 ở epoch cuối), loss train vẫn giảm → 5 epoch **chưa hội tụ hoàn toàn**. Một epoch thực tế mất 21,3 phút (benchmark ước 18 phút).
- **Quan sát đáng chú ý (không chỉnh, sẽ báo cáo trung thực):** B2 cao hơn M1 trên DDR (0,722 so với 0,691; chênh lệch cặp −0,031, khoảng tin cậy 95% [−0,051; −0,013]), nhưng M1 cao hơn B2 trên EyePACS-test (0,680 so với 0,654). Cả hai có QWK trên DDR không thấp hơn trong miền; nguyên nhân khả dĩ là phân bố mức bệnh khác nhau và nhãn DDR sạch hơn, nên tôi thêm chỉ số **ΔQWK khớp phân bố** (lấy mẫu EyePACS-test theo tỉ lệ mức bệnh của DDR) để loại yếu tố label shift: M1: +0,009 [−0,019; 0,036], B2: −0,061 [−0,088; −0,033].
- t-SNE (kNN khác bộ dữ liệu): M1 0,03–0,06, B2 0,22–0,28 (0,5 là trộn hoàn toàn) → đặc trưng RETFound **tách hai bộ rõ hơn** B2, trái với giả thuyết "SSL võng mạc trộn miền hơn".

**Quyết định (quy tắc đã báo: còn tăng dốc thì chạy thêm epoch, nhưng ưu tiên có bộ kết quả đầy đủ trước):**
1. **K2 (đã đẩy lúc 00:50):** M2 seed 0 (5 epoch) song song B1 ba seed (5 epoch). *Lý do:* hoàn tất bộ so sánh 4 mô hình với **cùng ngân sách 5 epoch** (B2 so với M1 so với M2 công bằng), xong khoảng 02:50, nên có kết quả đầy đủ sớm, an toàn nếu sau này có sự cố.
2. **K3 (tự đẩy khi K2 xong, xong khoảng 06:00):** M1 và B2 chạy **8 epoch** (seed 0). *Lý do:* kiểm tra xem kết luận (đặc biệt "B2 hơn M1 trên DDR") có đổi khi huấn luyện lâu hơn không, đúng mối lo "5 epoch quá thấp". 8 epoch (không phải 10) để còn đệm thời gian trước mốc 07:00–08:00.
3. **Không chạy thêm seed ViT-L** (không đủ thời gian): độ tin cậy dựa trên bootstrap 95% CI; B1 có 3 seed. Sẽ nói rõ trong báo cáo.
4. Linear probe đã bỏ.

## 25/11 06:00–06:30 — K2 xong, phân tích 5 epoch
- K2 (M2_s0 + B1×3) xong 04:24; K3 (M1 và B2, 8 epoch) tự đẩy lúc 04:24, đang chạy.
- Phân tích đầy đủ 5 epoch (`results/main_5ep/`): QWK DDR argmax B1 0.701, B2 0.722, M1 0.691, M2 0.734; ΔQWK B1 -0.015, B2 -0.068, M1 -0.010, M2 -0.076.
- Biến thể ordinal (ngưỡng chỉ fit trên EyePACS-val): DDR B2 0.744, M1 0.727, M2 0.753.
- Nhận xét trung thực: giả thuyết M1 > B2 trên DDR KHÔNG được ủng hộ ở 5 epoch; RETFound giữ QWK ổn định giữa hai miền (ΔQWK ≈ 0 khớp prior) nhưng không cao hơn tuyệt đối. QWK val vẫn tăng ở epoch 5 → chờ K3 (8 epoch) để xem độ nhạy.
- Grad-CAM (a01), curves (t_curves_all), t-SNE, confusion, ROC, recall, bootstrap đã tạo.

## 25/11 06:30–07:00 — viết báo cáo phần kết quả
- Quyết định: bộ so sánh chính = 5 epoch cho cả 4 mô hình (cùng ngân sách); 8 epoch (K3) chỉ là kiểm tra độ nhạy cho M1/B2.
- Đã sửa cho khớp thực tế: g01/g02 (số seed, đánh giá cuối nằm trong kernel huấn luyện, phân tích chạy local, MiKTeX), bảng ma trận thí nghiệm (bỏ linear probe, B1 3 seed, còn lại 1 seed), Mục tiêu 1.2.3, Phụ lục B (epoch, seed), mục 2.2.3 (độ dài huấn luyện), mục 2.2.5 thêm hình augmentation, 2.4.1 (kiến trúc).
- Đã viết: 3.3 (động học huấn luyện, kết quả chính, so sánh khớp tỉ lệ nhãn, từng mức, ROC, biến thể ordinal, Grad-CAM/t-SNE, bảng tóm tắt giả thuyết), 3.4 (demo, ảnh chụp thật với M1), 3.5 phân tích lỗi, chương 4.
- Phát hiện trung thực: H1, H2, H3 không được ủng hộ ở 5 epoch; M1 lỗi nghiêng về chấm quá cao (ít bỏ sót) còn B2/M2 chấm thấp hơn thực tế.
- Còn chờ K3: mục 3.3.8, câu hạn chế về ngân sách huấn luyện, 1 câu ở chương 4.

## 25/11 07:00–07:30 — K3 bị hủy, chốt báo cáo
- K3 (M1, B2 với 8 epoch) bị Kaggle hủy sau ~2,5 giờ (chưa chạm giới hạn 240 phút của script, không có lý do). Chỉ còn đường cong validation (B2 đến epoch 7, M1 đến epoch 6), không có kết quả test.
- Quyết định: KHÔNG chạy lại (cần ~3 giờ, sát hạn nộp). Báo cáo mục 3.3.8 mô tả đúng sự việc, chỉ dùng đường cong validation (hình t02), không đưa vào bảng nào; thêm giới hạn "ngân sách huấn luyện" ở 3.5.5 và chương 4.
- PDF: 52 trang tổng (bìa/mục lục/danh mục 9 trang; chương 1–6 ~37 trang; tài liệu tham khảo + phụ lục ~6 trang).

## 25/11 07:05 — K5: huấn luyện tiếp 3 epoch từ checkpoint 5 epoch (trả lời lo ngại "điểm thấp")
- Lý do: K3 bị hủy; chạy lại 8 epoch từ đầu (~3 h) không kịp. Phương án rẻ hơn: tiếp tục 3 epoch từ best.pt của M1, B2, B1 (seed 0), tổng 8 epoch hiệu dụng. Quy tắc cố định TRƯỚC khi xem kết quả: blr 2e-3 (ViT-L) / lr 4e-5 (ResNet-50), warm-up 0,25 epoch, cosine về 1e-6, aug chuẩn, seed 100, chọn checkpoint theo QWK EyePACS-val, không dùng DDR.
- Code: thêm `init_ckpt` vào train_lib (đã test load trên CPU), jobs_k5.json, dataset `sic-dr-ckpt5` (3 checkpoint), kernel `sic-dr-run-k5` đẩy 07:07 (GPU0: M1; GPU1: B2 rồi B1).
- Kế hoạch: xong dự kiến 08:30–08:45. Nếu chưa xong lúc 09:15 thì giữ nguyên báo cáo hiện tại (đã nhất quán). M2 không có bản tiếp tục (thiếu GPU).

## 25/11 08:22 — Quyết định mới: huấn luyện lại từ đầu 15 epoch, 3 mô hình
- Người dùng không chấp nhận QWK ~0.70 và không muốn huấn luyện nối tiếp (5+3). Hạn nộp dời đến 16:00 (viết báo cáo chỉ còn ~1 giờ cuối).
- Đã dừng K5 (xóa kernel), K6 chưa từng đẩy. Nguyên nhân K3 bị hủy: tôi đẩy với `-t 9000` (150 phút) → từ nay luôn `-t 43200`.
- Chốt: M1 (RETFound), B2 (ViT-L ImageNet MAE), B1 (ResNet-50, 2 seed), 15 epoch, warm-up 2 epoch, một mạch. Bỏ M2 (thiếu GPU cho ViT-L thứ ba): mất H3, giữ H1 và H2. Kernel `sic-dr-run-e15` đẩy 08:22; ETA M1/B2 ~13:45, B1 ~14:35 (GPU0: M1→B1_s0; GPU1: B2→B1_s1).
- Mọi kết quả 5 epoch cũ (K1, K2, K3, K5) bị LOẠI khỏi báo cáo; bản cũ giữ ở git tag `report-5ep-v1`.
- QWK >= 0.85 là mong muốn của người dùng; tôi đã nói rõ không thể đảm bảo (ảnh 224 px, nhãn nhiễu) và không chỉnh gì theo DDR.

## 25/11 15:18–15:35 — Kết quả 15 epoch và hoàn thiện báo cáo
- Kernel `sic-dr-run-e15` COMPLETE (tải lúc 15:18). Thời gian chạy: M1 356 phút, B2 328 phút, B1 50 và 48 phút.
- QWK arg-max (EyePACS-test / DDR-test): B1 0.672 / 0.669; B2 0.686 / 0.713; M1 0.670 / 0.682. Giải mã thứ bậc (ngưỡng fit trên EyePACS-val): DDR 0.709 / 0.734 / 0.707.
- H1 không được ủng hộ (M1 − B2 = −0.031, KTC 95% [−0.051, −0.009]); H2 không phân biệt được. Mục tiêu 0.85 KHÔNG đạt. Huấn luyện dài hơn không giúp: val QWK tốt nhất ở epoch 5–6 (M1, B1) và 11 (B2).
- Demo dùng checkpoint B2 (val QWK cao nhất, không chọn theo test).
- Đã viết mục 3.3, 3.4, 3.5.4, phát hiện chính chương 4; PDF 51 trang, không còn ghi chú PENDING.

## 25/11 15:50 - Quay lai ban 5 epoch lam chinh (nguoi dung chon phuong an B)
- Them muc 3.3.8 so sanh voi lan train lai 15 epoch (ca hai ket qua deu cong bo). Ban 15 epoch day du: git tag report-15ep.
- Chen anh thanh vien, dien chuong 5 (Role, Tasks; Self-review va Peer comment de trong). PDF 52 trang.
- Anh ca nhan va main.pdf (co anh) KHONG day len GitHub vi repo cong khai.
