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


if __name__ == "__main__":
    unittest.main()
