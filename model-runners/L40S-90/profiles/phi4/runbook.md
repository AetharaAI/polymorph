# Phi-4 Runner Runbook

## Purpose

Known-good local runner definition for `phi-4-instruct` on `L40S-90`.

This runner is intended for direct multimodal chat with:
- text
- image
- audio

The harness should use this model for direct microphone/audio turns without
transcribing through ASR first.

## Served Model Contract

- Served model name: `phi-4-instruct`
- OpenAI-compatible route: `/v1/chat/completions`
- Base URL on node: `http://<host>:8101`
- External router target: `https://api.aetherpro.tech/v1`

## Model-Specific Notes

- Requires audio and vision LoRAs to be loaded.
- Maximum satisfactory audio length should stay within the Phi-4 model-card guidance.
- Force `--chat-template-content-format openai` on the runner. Auto-detect
  may incorrectly choose `string`, which breaks OpenAI-style multimodal content
  arrays for `input_audio`.
- The harness direct-audio path should send:
  - a text block
  - an audio block (`input_audio` preferred, `audio_url` secondary)
- This path must bypass the ASR transcription pipeline.

## Operational Checks

1. `docker compose up -d`
2. `docker compose logs -f`
3. Verify startup shows:
   - `Loaded new LoRA adapter: name 'audio'`
   - `Loaded new LoRA adapter: name 'image'`
   - `/v1/chat/completions` route present
4. Smoke test text-only chat.
5. Smoke test direct audio multimodal chat through the router.

## Troubleshooting

- If `/v1/chat/completions` returns `404` externally, check the upstream gateway path and domain mapping first.
- If direct audio returns `400 Bad Request`, check the runner logs for:
  - `Detected the chat template content format to be 'string'`
  - missing `--chat-template-content-format openai`
  - LoRA load lines for both `audio` and `image`
- If the harness falls back to ASR, inspect `DIRECT_AUDIO_*` / `PHI_4_INSTRUCT_*` env config in the harness.
