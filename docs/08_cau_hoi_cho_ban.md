# 08. Câu hỏi cần bạn chốt (gom lại để trả lời một lượt vào buổi sáng)

> File này do Claude cập nhật trong lúc tự chạy. Mỗi mục có **mặc định tôi đã chọn** (nếu bạn không trả lời, tôi giữ mặc định). Đánh dấu ✅ khi bạn đã trả lời.

## A. Việc chỉ bạn làm được (báo cáo chưa hoàn chỉnh nếu thiếu)

1. **Ảnh nhóm** cho chương 5 (hộp "ATTACH A TEAM PICTURE HERE"). Mặc định: để hộp trống. Cách làm: bạn gửi file, tôi chèn vào `figures/team_photo.png`.
2. **Nhận xét của từng thành viên** (chương 5, 2 dòng: Lai Van Thinh, Tran Thuy Duyen). Mặc định: để trống (biểu mẫu Samsung, thành viên tự viết).
3. **Ngày nộp báo cáo (DD/MM/YY)**. Mặc định: giữ placeholder `< Date (DD/MM/YY) >` trên bìa.
4. **Chương 6 (rubric giảng viên):** để nguyên, giảng viên tự điền.

## B. Câu hỏi cần xác nhận

5. **Tên giảng viên** trên bìa hiện là `TS. Trần Quang Quý` (mặc định của template). Bạn đã đổi lớp từ N02 sang **N05**; giảng viên lớp N05 có đúng là người này không? Mặc định: giữ nguyên.
6. **Ghi chú sử dụng công cụ AI** (trong báo cáo/lời cảm ơn): chương trình có yêu cầu khai báo việc dùng trợ lý AI khi viết code/báo cáo không? Mặc định: **không thêm** câu nào; nếu cần, bạn cho tôi nội dung.
7. **Lịch Weeks 1–10 (mục 1.4):** cột trạng thái hiện là "Completed / In Progress / Pending". Tôi sẽ đổi hết thành "Completed" khi báo cáo xong. Nếu bạn muốn khác, ghi lại.

## C. Rủi ro tôi đã tính và cách xử lý tự động

- **Kết quả không như giả thuyết** (ví dụ M1 không hơn B2, M2 không hơn M1): vẫn báo cáo trung thực, phân tích nguyên nhân, không chỉnh số.
- **Số epoch thấp:** xem log ở `docs/07`. Quy tắc: nếu QWK val còn tăng dốc ở epoch cuối thì chạy lại với số epoch lớn hơn (còn thời gian); nếu đã đi ngang thì giữ.
- **Kaggle:** chỉ chạy được một phiên 2 GPU một lúc, có thể phải xếp hàng. Tôi chạy nối tiếp tự động; mốc dừng thí nghiệm khoảng 05:30, sau đó chỉ viết báo cáo.
- **Số trang:** mục tiêu 40–50 trang. Nếu thiếu/thừa tôi chỉnh nội dung hợp lý.
- **Chưa đối chiếu từng chữ trên Google Scholar:** thứ tự tác giả bài DDR, trang MICCAI của GDRNet, danh sách tác giả đầy đủ RETFound (xem `docs/07`).
- **Kaggle token:** không lưu trong repo; nếu bạn từng chia sẻ file `apikey_kaggle.txt`, nên tạo lại token.

## Đã trả lời (25/11, nửa đêm)

- ✅ Ảnh nhóm: người dùng gửi sau (để hộp trống đến khi có file).
- ✅ Nhận xét thành viên: không cần (để trống).
- ✅ Ngày nộp: **25/11/26** (đã điền vào `metadata.tex`).
- ✅ Tên giảng viên: giữ nguyên.
- ✅ Ghi chú AI: không thêm.
- ✅ Thí nghiệm có thể kéo dài đến khoảng 07:00–08:00 nếu cần; phần còn lại chỉ viết/duyệt/sửa.
- ✅ Tài liệu tham khảo: tôi tự kiểm chứng trên mạng. Kết quả: thứ tự tác giả DDR **đúng** (Li, Gao, Wang, Guo, Liu, Kang); GDRNet có số trang **430–440**, DOI 10.1007/978-3-031-43904-9_42 (đã thêm vào bib; số tập LNCS không xác minh được nên không ghi); RETFound: số 7981, trang 156–163, thứ tự 9 tác giả đầu **đúng**.

## D. Còn lại trước khi nộp (25/11, sau kết quả 15 epoch)

1. **Ảnh nhóm** (chương 5) vẫn chờ bạn gửi file.
2. **Kết quả:** QWK trên DDR 0.67–0.71 (tối đa 0.734 với giải mã thứ bậc), thấp hơn mục tiêu 0.85; H1 không được ủng hộ. Báo cáo ghi đúng như đo được.
3. **Số trang:** PDF 51 trang gồm cả bìa, mục lục, danh mục, tài liệu tham khảo và phụ lục. Nếu giảng viên đếm toàn bộ và yêu cầu ≤ 50 thì cần rút gọn.
4. **Bảng 1.3:** giai đoạn 5 (nộp báo cáo và thuyết trình) đang ghi "In progress".
5. **Một seed** cho B2 và M1 (B1 có 2 seed): đã nêu là hạn chế.
