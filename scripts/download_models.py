"""
Supreme Feng Shui AGI System - Direct File-by-File Model Downloader
Downloads all files from hemsinath/khmer-supreme-feng-shui into local models/ folder.
"""

import os
import sys
import shutil
from pathlib import Path
from huggingface_hub import hf_hub_download

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

sys.path.insert(0, str(BASE_DIR))
from config import config

HF_TOKEN = config.HF_TOKEN or os.getenv("HF_TOKEN", "")
REPO_ID = os.getenv("HF_MODEL_TRAINED", "hemsinath/khmer-supreme-feng-shui")

FILES_TO_DOWNLOAD = [
    "zenith_metadata.json",
    "zenith_rag_index/index.faiss",
    "zenith_rag_index/index.pkl",
    "zenith_tokenizer/chat_template.jinja",
    "zenith_tokenizer/tokenizer.json",
    "zenith_tokenizer/tokenizer_config.json",
    "zenith_weights/README.md",
    "zenith_weights/adapter_config.json",
    "zenith_weights/adapter_model.safetensors"
]


def download_models():
    print("=" * 80)
    print(f"[DOWNLOAD] Direct Hub Downloader: {REPO_ID}")
    print("=" * 80)

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    for rfilename in FILES_TO_DOWNLOAD:
        target_path = MODELS_DIR / rfilename
        target_path.parent.mkdir(parents=True, exist_ok=True)

        if target_path.exists() and target_path.stat().st_size > 0:
            print(f"[EXISTS] {rfilename} ({target_path.stat().st_size / 1024:.1f} KB)")
            continue

        print(f"[DOWNLOADING] {rfilename}...")
        try:
            cached_file = hf_hub_download(
                repo_id=REPO_ID,
                filename=rfilename,
                token=HF_TOKEN,
                force_download=False
            )
            shutil.copyfile(cached_file, target_path)
            print(f"[SAVED] {rfilename} ({target_path.stat().st_size / 1024:.1f} KB)")
        except Exception as e:
            print(f"[ERROR] Failed to download {rfilename}: {e}")

    print("\n" + "=" * 80)
    print("[SUCCESS] All Model Components Successfully Downloaded to models/!")
    print("=" * 80)
    for root, dirs, files in os.walk(MODELS_DIR):
        for file in files:
            p = Path(root, file)
            print(f"  * {p.relative_to(MODELS_DIR)} ({p.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    download_models()
