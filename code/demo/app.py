"""Gradio demo: upload a fundus photograph -> DR grade, class probabilities, referable flag, Grad-CAM overlay.

Runs locally on CPU.  Usage:
  python app.py --ckpt path/to/M1_best.pt [--port 7860] [--share]
The same preprocessing as in training (crop retina -> square -> 224x224) is applied.
Research prototype for a student project; NOT a medical device.
"""
import argparse
import os
import sys

import gradio as gr
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gradcam import gradcam_vit, load_vit, overlay, preprocess  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--ckpt", required=True)
ap.add_argument("--arch", default="vit_large_patch16_224")
ap.add_argument("--port", type=int, default=7860)
ap.add_argument("--share", action="store_true")
args = ap.parse_args()

torch.set_num_threads(max(1, (os.cpu_count() or 4) - 1))
MODEL = load_vit(args.ckpt, args.arch)
NAMES = ["0 - No DR", "1 - Mild", "2 - Moderate", "3 - Severe", "4 - Proliferative"]


def predict(img):
    if img is None:
        return None, None, "Please upload a fundus image.", None
    im224, x = preprocess(img)
    probs, top, cam = gradcam_vit(MODEL, x)
    referable = float(probs[2:].sum())
    verdict = (f"**Predicted grade: {NAMES[top]}**  \n"
               f"Probability of referable DR (grade >= 2): **{referable:.1%}** -> "
               + ("**refer to an ophthalmologist**" if referable >= 0.5 else "routine follow-up"))
    return {n: float(p) for n, p in zip(NAMES, probs)}, im224, verdict, overlay(im224, cam)


with gr.Blocks(title="DR grading demo") as demo:
    gr.Markdown("# Diabetic retinopathy grading from fundus photographs\n"
                "Model: RETFound (ViT-L) fine-tuned on EyePACS. Upload a colour fundus photograph.  \n"
                "*Research prototype of the SIC capstone project - not a medical device.*")
    with gr.Row():
        with gr.Column():
            inp = gr.Image(type="pil", label="Fundus image")
            btn = gr.Button("Grade image", variant="primary")
        with gr.Column():
            verdict = gr.Markdown()
            lab = gr.Label(num_top_classes=5, label="Class probabilities")
    with gr.Row():
        pre = gr.Image(label="Preprocessed input (224x224)")
        cam = gr.Image(label="Grad-CAM: regions that influenced the decision")
    btn.click(predict, inp, [lab, pre, verdict, cam])

if __name__ == "__main__":
    demo.launch(server_port=args.port, share=args.share)
