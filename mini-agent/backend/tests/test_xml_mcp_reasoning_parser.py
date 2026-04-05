import unittest

from backend.agent.providers.compat.xml_mcp_reasoning import parse_xml_mcp_reasoning_output


class XMLMCPReasoningParserTests(unittest.TestCase):
    def test_think_only_output(self) -> None:
        text = "<think>plan quietly</think>Final answer only."
        parsed = parse_xml_mcp_reasoning_output(
            text,
            available_tool_names={"web_search"},
            allowed_server_names={"my-tools"},
        )
        self.assertEqual(parsed.reasoning_channel, "plan quietly")
        self.assertEqual(parsed.final_answer_channel, "Final answer only.")
        self.assertEqual(len(parsed.tool_call_channel), 0)

    def test_think_plus_tool_call_output(self) -> None:
        text = (
            "<think>Need lookup</think>"
            "<use_mcp_tool>"
            "<server_name>My-Tools</server_name>"
            "<tool_name>web_search</tool_name>"
            "<arguments>{\"query\":\"weather\"}</arguments>"
            "</use_mcp_tool>"
            "I'll call a tool now."
        )
        parsed = parse_xml_mcp_reasoning_output(
            text,
            available_tool_names={"web_search"},
            allowed_server_names={"my-tools"},
        )
        self.assertEqual(parsed.reasoning_channel, "Need lookup")
        self.assertEqual(len(parsed.tool_call_channel), 1)
        self.assertTrue(parsed.tool_call_channel[0].allowed)
        self.assertEqual(parsed.tool_call_channel[0].tool_name, "web_search")
        self.assertEqual(parsed.tool_call_channel[0].arguments, {"query": "weather"})
        self.assertEqual(parsed.final_answer_channel, "I'll call a tool now.")

    def test_malformed_xml(self) -> None:
        text = (
            "<use_mcp_tool>"
            "<server_name>my-tools</server_name>"
            "<tool_name>web_search</tool_name>"
            # missing arguments tag and closing use tag
        )
        parsed = parse_xml_mcp_reasoning_output(
            text,
            available_tool_names={"web_search"},
            allowed_server_names={"my-tools"},
        )
        self.assertEqual(len(parsed.tool_call_channel), 0)
        self.assertIn("<use_mcp_tool>", parsed.final_answer_channel)

    def test_malformed_json_arguments(self) -> None:
        text = (
            "<use_mcp_tool>"
            "<server_name>my-tools</server_name>"
            "<tool_name>web_search</tool_name>"
            "<arguments>{\"query\": weather}</arguments>"
            "</use_mcp_tool>"
        )
        parsed = parse_xml_mcp_reasoning_output(
            text,
            available_tool_names={"web_search"},
            allowed_server_names={"my-tools"},
        )
        self.assertEqual(len(parsed.tool_call_channel), 1)
        self.assertFalse(parsed.tool_call_channel[0].allowed)
        self.assertIsNotNone(parsed.tool_call_channel[0].parse_error)
        self.assertGreaterEqual(len(parsed.parse_errors), 1)

    def test_plain_final_answer_no_tags(self) -> None:
        text = "Plain answer with no tags."
        parsed = parse_xml_mcp_reasoning_output(
            text,
            available_tool_names={"web_search"},
            allowed_server_names={"my-tools"},
        )
        self.assertEqual(parsed.reasoning_channel, "")
        self.assertEqual(parsed.final_answer_channel, "Plain answer with no tags.")
        self.assertEqual(len(parsed.tool_call_channel), 0)

    def test_generic_tool_block_json_payload_is_recovered(self) -> None:
        text = (
            "<tool>"
            "{\"name\":\"write_file\",\"arguments\":{\"filename\":\"00_run_journal.md\",\"content\":\"ok\"}}"
            "</tool_call>"
            "Done."
        )
        parsed = parse_xml_mcp_reasoning_output(
            text,
            available_tool_names={"write_file"},
            allowed_server_names={"harness"},
        )
        self.assertEqual(len(parsed.tool_call_channel), 1)
        call = parsed.tool_call_channel[0]
        self.assertTrue(call.allowed)
        self.assertEqual(call.server_name, "harness")
        self.assertEqual(call.tool_name, "write_file")
        self.assertEqual(call.arguments, {"filename": "00_run_journal.md", "content": "ok"})
        self.assertEqual(parsed.final_answer_channel, "Done.")

    def test_missing_server_name_defaults_to_harness(self) -> None:
        text = (
            "<use_mcp_tool>"
            "<tool_name>list_files</tool_name>"
            "<arguments>{}</arguments>"
            "</use_mcp_tool>"
        )
        parsed = parse_xml_mcp_reasoning_output(
            text,
            available_tool_names={"list_files"},
            allowed_server_names={"harness"},
        )
        self.assertEqual(len(parsed.tool_call_channel), 1)
        call = parsed.tool_call_channel[0]
        self.assertTrue(call.allowed)
        self.assertEqual(call.server_name, "harness")
        self.assertEqual(call.tool_name, "list_files")
        self.assertEqual(call.arguments, {})


if __name__ == "__main__":
    unittest.main()
