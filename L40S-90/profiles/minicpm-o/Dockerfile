FROM vllm/vllm-openai:nightly
RUN pip install vllm[video] vllm[audio] --no-deps 2>/dev/null; pip install librosa soundfile opencv-python-headless