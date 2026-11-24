# evidence_figures: ảnh và minh chứng cho báo cáo

Mọi hình sinh ra khi chạy trên Kaggle (`/kaggle/working`) sẽ được tải về và đặt vào đây, **đúng thư mục và đúng tên** dưới đây. Sau đó được copy vào `Capstone-Project_latex/figures/` khi viết báo cáo. Log số liệu thô (CSV/JSON) đặt ở `../logs/`.

Quy ước tên: `<mã_hình>_<mô_tả>[_<mô_hình>][_seed<N>].png` (độ phân giải ≥ 200 dpi, nền trắng, nhãn trục rõ, chữ đủ to khi thu nhỏ vào trang A4).

| Thư mục | Nội dung | Ví dụ tên file | Dùng ở mục |
|---|---|---|---|
| `01_data/` | Phân bố lớp EyePACS (train/val/test) và DDR-test; phân bố kích thước ảnh; ảnh mẫu mỗi mức 0–4 của từng bộ; thống kê màu/độ sáng trung bình của hai bộ | `d01_class_dist_eyepacs.png`, `d02_class_dist_ddr.png`, `d03_samples_per_grade.png`, `d04_color_stats_domain_gap.png` | 2.1, 3.2 |
| `02_preprocessing/` | Ảnh gốc vs sau cắt viền/resize; ví dụ kiểm tra trùng (perceptual hash) | `p01_before_after_crop.png`, `p02_phash_check.png` | 3.1 |
| `03_training/` | Đường cong loss, QWK, LR theo epoch từng run; gộp 3 seed; ảnh batch augmentation M1 vs M2 | `t01_curves_M1_seed0.png`, `t02_curves_all_models.png`, `t03_augmentation_M1_vs_M2.png` | 2.2, 3.3 |
| `04_evaluation/` | Confusion matrix, ROC (referable), recall từng lớp, biểu đồ cột QWK trong miền và ngoài miền (kèm CI), bootstrap CI | `e01_confusion_M1_ddr.png`, `e02_roc_referable.png`, `e03_perclass_recall.png`, `e04_in_vs_out_qwk.png`, `e05_bootstrap_ci.png` | 3.3, 3.5 |
| `05_analysis/` | Grad-CAM (ca đúng/sai, theo bộ), t-SNE đặc trưng tô màu theo bộ và theo mức, (tùy chọn) reliability diagram, ablation augmentation | `a01_gradcam_correct.png`, `a02_gradcam_error.png`, `a03_tsne_domain.png`, `a04_tsne_grade.png`, `a05_ablation_aug.png` | 3.3, 3.5 |
| `06_diagrams/` | Sơ đồ pipeline tổng thể, system design, sơ đồ kiến trúc RETFound/MAE | `g01_pipeline.png`, `g02_system_design.png`, `g03_mae_retfound.png` | 2.3, 2.4, 2.2 |
| `07_demo/` | Ảnh chụp demo web (upload, kết quả, Grad-CAM) | `u01_demo_upload.png`, `u02_demo_result.png` | 3.4 |

**Nguyên tắc:** không đưa vào báo cáo bất kỳ con số nào mà không có file log (CSV/JSON) tương ứng trong `../logs/` và ít nhất một hình minh chứng.
