@echo off

if exist venv_downloader (
    echo Virtual environment already exists. Skipping creation...
) else (
    echo Creating virtual environment...
    python -m venv venv_downloader
)

call .\venv_downloader\Scripts\activate.bat

python -m pip install --upgrade pip

pip install -U gradio==5.35.0 huggingface_hub hf_transfer hf_xet

set HF_XET_CHUNK_CACHE_SIZE_BYTES=90737418240

set HUGGING_FACE_HUB_TOKEN=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
python -W ignore Downloader_Gradio_App.py

pause