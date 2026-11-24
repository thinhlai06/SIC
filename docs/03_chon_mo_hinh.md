# 03. Vì sao chọn RETFound (ViT-Large, MAE) mà không phải mô hình khác?

## 1. RETFound là gì?

- **Foundation model cho ảnh võng mạc**, đăng trên *Nature* (2023), do UCL và Bệnh viện Mắt Moorfields phát triển.
- **Kiến trúc:** Vision Transformer cỡ Large (ViT-L/16), khoảng **307 triệu tham số**, input 224×224.
- **Tiền huấn luyện tự giám sát bằng MAE** trên ~1,6 triệu ảnh võng mạc **không nhãn** (gồm ảnh đáy mắt và OCT; ✅ đã đối chiếu bài Nature: bản ảnh đáy mắt tiền huấn luyện trên **904.170** ảnh, khoảng 90,2% từ MEH-MIDAS và 9,8% từ Kaggle EyePACS; khởi tạo từ trọng số MAE-ImageNet rồi huấn luyện tiếp trên ảnh võng mạc).
- Sau đó **fine-tune** cho từng bài toán có nhãn (DR, glaucoma, bệnh tim mạch tiên lượng…).
- Trọng số và code **công khai** (GitHub; trọng số bản ảnh đáy mắt cũng có trên Hugging Face — ⚠ có thể phải chấp nhận điều khoản).

## 2. Lý do chọn

1. **Phủ cả hai vế của đề tài.** RETFound chính là "học tự giám sát trên ảnh võng mạc" (vế SSL). Thêm augmentation mô phỏng máy chụp là vế DG. Các mô hình khác thường chỉ phủ một vế.
2. **Có thể kiểm soát thí nghiệm (ablation sạch).** RETFound dùng đúng kiến trúc ViT-L/MAE. Nếu so với một ViT-L MAE tiền huấn luyện trên **ImageNet** (B2), hai mô hình **chỉ khác nhau ở dữ liệu tiền huấn luyện** (ảnh võng mạc vs ảnh tự nhiên). Chênh lệch kết quả → quy được về "SSL trên ảnh võng mạc". Đây là thiết kế so sánh mạnh nhất có thể trong 30 giờ GPU.
3. **DDR là miền "sạch".** RETFound bản gốc không tiền huấn luyện/fine-tune trên DDR (⚠ kiểm tra lại), nên test trên DDR phản ánh đúng khả năng tổng quát hóa.
4. **Trọng số + code công khai** → tái lập được, trích dẫn được, nhóm không phải tự pretrain (điều bất khả thi với 30 giờ T4).
5. **Khả thi về tính toán:** ViT-L fine-tune được trên 2×T4 với fp16, batch nhỏ, ảnh 224×224 (xem file 05 cho ngân sách).
6. **Uy tín học thuật:** đăng trên Nature, được trích dẫn rộng → báo cáo có cơ sở.

## 3. Vì sao không chọn mô hình khác?

| Lựa chọn khác | Vì sao không chọn làm mô hình chính |
|---|---|
| **GDRNet** (FundusAug, ResNet-50) | Chỉ phủ vế DG, nền là ResNet-50 ImageNet có giám sát. Không có SSL võng mạc. Ý tưởng FundusAug vẫn được dùng làm M2. |
| **ResNet-50 / ViT ImageNet thông thường** | Dùng làm **baseline** (B1, B2), không phải mô hình chính: không có tri thức võng mạc. |
| **SimCLR / MoCo / DINO tự pretrain trên EyePACS** | Cần nhiều tuần GPU để pretrain tử tế; 30 giờ T4 không đủ. Kết quả có thể không bằng RETFound (đã pretrain 900k+ ảnh). Có thể ghi vào "hướng phát triển". |
| **VisionFM, FLAIR, UrFound…** (⚠ các foundation model võng mạc khác) | Một số dùng dữ liệu đa phương thức hoặc có nhãn/văn bản trong tiền huấn luyện nên **không phải SSL thuần**, hoặc khó tái lập, trọng số khó lấy; làm mất tính "so sánh sạch". |
| **DERETFound** (⚠) | Là biến thể sau RETFound; DDR xuất hiện trong dữ liệu của biến thể này → DDR không còn "chưa thấy", làm hỏng giao thức. |
| **DINOv2 / CLIP ViT tổng quát** | Không có tri thức võng mạc; dùng được làm baseline phụ, nhưng B2 (MAE ImageNet) đã đủ để đối chứng và cùng họ với RETFound. |
| **Mô hình nhỏ (RETFound-Green, ViT-B)** ⚠ | Có thể là hướng thay thế nếu ViT-L quá nặng. Hiện **chưa cần**; sẽ cân nhắc nếu đo tốc độ cho thấy ngân sách GPU không đủ. |

## 4. Điểm cần cân nhắc / rủi ro (nêu trung thực trong báo cáo)

- **ViT-L nặng**: cần AMP fp16, batch nhỏ + gradient accumulation, có thể đóng băng bớt layer đầu hoặc dùng layer-wise LR decay.
- **RETFound đã thấy ảnh EyePACS (không nhãn)** khi tiền huấn luyện → số **in-domain** (EyePACS-test) có thể hơi lạc quan; **DDR mới là kết quả chính**.
- **Độ phân giải 224×224** làm mất chi tiết nhỏ (vi phình mạch). Đây là giới hạn của RETFound (và tiêu chuẩn của ViT); vẫn đủ để so sánh các mô hình với nhau cùng điều kiện.
- **Đóng góp SSL là của RETFound**, không phải của nhóm. Báo cáo ghi rõ đóng góp của nhóm là so sánh có kiểm soát, DG bằng augmentation, và phân tích.
