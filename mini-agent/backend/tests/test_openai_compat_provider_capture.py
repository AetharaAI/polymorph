import unittest

from backend.agent.providers.openai_compat_provider import OpenAICompatProvider
from backend.agent.providers.base import LLMUsage


class OpenAICompatProviderCaptureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.provider = OpenAICompatProvider(
            base_url="https://openrouter.ai/api/v1",
            api_key="test-key",
            model_name="xiaomi/mimo-v2.5",
            provider_name="delegated_vision",
        )

    def test_normalize_message_content_from_plain_string(self) -> None:
        text, meta = self.provider._normalize_message_content("Visible text here.")  # noqa: SLF001
        self.assertEqual(text, "Visible text here.")
        self.assertEqual(meta["raw_content_type"], "str")

    def test_normalize_message_content_from_text_block_array(self) -> None:
        text, meta = self.provider._normalize_message_content(  # noqa: SLF001
            [{"type": "text", "text": "First line"}, {"type": "output_text", "text": "Second line"}]
        )
        self.assertEqual(text, "First line\nSecond line")
        self.assertEqual(meta["raw_content_type"], "list")

    def test_build_blocks_from_message_recovers_thinking_only(self) -> None:
        blocks = self.provider._build_blocks_from_message(  # noqa: SLF001
            {"reasoning_content": "Reasoning only", "content": ""}
        )
        self.assertEqual([block.type for block in blocks], ["thinking"])

    def test_build_blocks_from_message_uses_output_text_fallback(self) -> None:
        blocks = self.provider._build_blocks_from_message(  # noqa: SLF001
            {"content": "", "output_text": "Recovered output text"}
        )
        self.assertEqual([block.type for block in blocks], ["text"])
        self.assertEqual(blocks[0].text, "Recovered output text")

    def test_empty_response_diagnostics_capture_empty_choices(self) -> None:
        diagnostics = self.provider._empty_response_diagnostics(  # noqa: SLF001
            request_id="req-empty",
            status_code=200,
            data={"id": "resp_1", "choices": [], "usage": {"prompt_tokens": 1, "completion_tokens": 0}},
            message={},
            finish_reason="stop",
            usage=LLMUsage(input_tokens=1, output_tokens=0),
            blocks=[],
            stream_requested=False,
            enable_thinking=False,
        )
        self.assertEqual(diagnostics["kind"], "empty_provider_response")
        self.assertEqual(diagnostics["provider_response_id"], "resp_1")
        self.assertEqual(diagnostics["choices_count"], 0)

    def test_empty_response_diagnostics_capture_empty_content_array(self) -> None:
        diagnostics = self.provider._empty_response_diagnostics(  # noqa: SLF001
            request_id="req-empty-content",
            status_code=200,
            data={
                "id": "resp_2",
                "choices": [{"message": {"content": []}, "finish_reason": "stop"}],
                "usage": {"prompt_tokens": 2, "completion_tokens": 0},
            },
            message={"content": []},
            finish_reason="stop",
            usage=LLMUsage(input_tokens=2, output_tokens=0),
            blocks=[],
            stream_requested=False,
            enable_thinking=False,
        )
        self.assertEqual(diagnostics["raw_message_content_type"], "list")
        self.assertEqual(diagnostics["raw_content_length"], 0)

    def test_build_blocks_from_message_uses_refusal_when_no_content(self) -> None:
        blocks = self.provider._build_blocks_from_message(  # noqa: SLF001
            {"content": "", "refusal": "I can't analyze this image."}
        )
        self.assertEqual([block.type for block in blocks], ["text"])
        self.assertIn("can't analyze", blocks[0].text or "")

    def test_normalize_message_content_from_object_like_message(self) -> None:
        class Message:
            def __init__(self) -> None:
                self.content = [{"type": "text", "text": "Object-backed text"}]

        blocks = self.provider._build_blocks_from_message(Message())  # noqa: SLF001
        self.assertEqual([block.type for block in blocks], ["text"])
        self.assertEqual(blocks[0].text, "Object-backed text")


if __name__ == "__main__":
    unittest.main()
