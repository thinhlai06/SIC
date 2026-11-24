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
