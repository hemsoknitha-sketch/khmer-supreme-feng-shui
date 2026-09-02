"""
Hugging Face Models Downloader & Local Cache Provisioner
========================================================
Tool for downloading and caching full models, tokenizers, or weights
from Hugging Face to local PC disk (`./models/` or HF cache).
"""

import os
import sys
import argparse
import logging
from typing import Optional, List
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("HFDownloader")

DEFAULT_MODELS = [
    "Qwen/Qwen2.5-72B-Instruct",
    "meta-llama/Llama-3.3-70B-Instruct",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    "mistralai/Mistral-Small-24B-Instruct-2501",
    "BAAI/bge-m3"
]

def download_model(model_id: str, local_dir: Optional[str] = None, token: Optional[str] = None):
    """
    Download a model repository from Hugging Face.
    """
    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        logger.error("huggingface_hub is not installed. Please run: pip install huggingface_hub")
        return False

    hf_token = token or os.environ.get("HUGGINGFACE_API_TOKEN") or os.environ.get("HF_TOKEN")
    logger.info(f"Starting download for model: {model_id}...")
    
    try:
        download_path = snapshot_download(
            repo_id=model_id,
            local_dir=local_dir,
            token=hf_token,
            resume_download=True
        )
        logger.info(f"✅ Successfully downloaded/cached '{model_id}' at: {download_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to download '{model_id}': {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Supreme Feng Shui Hugging Face Model Downloader")
    parser.add_argument("--model", type=str, default=None, help="Specific model repo ID (e.g., Qwen/Qwen2.5-72B-Instruct)")
    parser.add_argument("--all", action="store_true", help="Download all default Supreme Feng Shui models")
    parser.add_argument("--dest", type=str, default="./models", help="Destination local directory")
    parser.add_argument("--token", type=str, default=None, help="Hugging Face User Access Token")
    args = parser.parse_args()

    dest_dir = Path(args.dest)
    dest_dir.mkdir(parents=True, exist_ok=True)

    if args.model:
        models_to_download = [args.model]
    elif args.all:
        models_to_download = DEFAULT_MODELS
    else:
        logger.info("Available Supreme Feng Shui Model Matrix:")
        for idx, m in enumerate(DEFAULT_MODELS, 1):
            logger.info(f"  {idx}. {m}")
        logger.info("\nUsage: python deploy/download_hf_models.py --model <REPO_ID> or --all")
        return

    for m in models_to_download:
        safe_name = m.replace("/", "_")
        target_local_path = str(dest_dir / safe_name)
        download_model(m, local_dir=target_local_path, token=args.token)

if __name__ == "__main__":
    main()
