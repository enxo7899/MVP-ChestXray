---
title: Chest X-ray Pathology Classifier
emoji: 🫁
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# Chest X-ray Pathology Classifier

Proposal-stage prototype built for Albania's Ministry of Health: upload a chest X-ray and get likelihood scores for 18 pathologies in about 2–3 seconds, with an Albanian clinician-facing interface.

**Live demo:** https://huggingface.co/spaces/enxo7899/MVP_MSH

> **Medical disclaimer:** research and educational prototype. Results are suggestions, not diagnoses. Every case must be reviewed by a qualified radiologist; do not use for clinical decisions without medical supervision.

## How it works

- **Model:** DenseNet-121 from [TorchXRayVision](https://github.com/mlmed/torchxrayvision) (`densenet121-res224-all`), pretrained on multiple public chest X-ray datasets.
- **Findings:** 18 pathologies, e.g. pneumonia, cardiomegaly, pleural effusion.
- **Serving:** Flask app (`app.py`) with a `/predict` endpoint; inference in `engine_chest.py`; Albanian labels in `translations.py`.
- **Deployment:** Docker image on Hugging Face Spaces (port 7860).

## Run locally

```bash
docker build -t chest-xray .
docker run -p 7860:7860 chest-xray   # then open http://localhost:7860
```

or

```bash
pip install -r requirements.txt
python app.py
```

## Project structure

```
app.py            # Flask server: UI and /predict endpoint
engine_chest.py   # DenseNet-121 inference
translations.py   # Albanian pathology names
templates/        # clinician-facing UI
Dockerfile
```

---
*Shqip:* Klasifikues prototip i patologjive në radiografitë e gjoksit, i zhvilluar për Ministrinë e Shëndetësisë. Rezultatet janë sugjerime dhe duhet të vlerësohen nga një radiolog i kualifikuar.
