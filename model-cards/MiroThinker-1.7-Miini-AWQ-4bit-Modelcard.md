 MiroThinker

Agents Paper

Github Discord Website
Introduction

Our new MiroThinker family represents a significant leap in building reliable agents for long-chain tasks. Engineered with enhanced post-training pipeline, our MiroThinker-1.7 family achieve SOTA performance in deep research tasks among open-source models.

Key Features

    MiroThinker-1.7 supports a 256K context window, long-horizon reasoning, and deep multi-step analysis.
    Handles up to 300 tool calls per task, now with more accurate stepwise reasoning and decision-making.
    Released in 30B and 235B parameter scales, accompanied by a comprehensive suite of tools and workflows to flexibly support diverse research settings and compute budgets.
    Our proprietary agent, MiroThinker-H1 provides promising evidence for long-chain verifiable reasoning — reasoning processes that are step-verifiable and globally verifiable, improving the performance of complex agentic workflows.

Model Name 	Parameters 	Max Context 	Max Tool Calls 	HF Link
MiroThinker-1.7-mini 	30B 	256K 	300 	🤗 link
MiroThinker-1.7 	235B 	256K 	300 	🤗 link

MiroThinker-1.7 demonstrates strong general-research performance across a broad range of benchmarks, achieving 74.0%, 75.3%, 82.7% and 42.9% accuracy on BrowseComp, BrowseComp-ZH, GAIA-Val-165 and HLE-Text, respectively. MiroThinker-1.7 achieves SOTA performance on BrowseComp-ZH.

image

More details can be found in our technical report (coming soon).
Try MiroThinker Online

Welcome to try out MiroThinker which offers agentic general QA experience better than OpenAI DeepResearch.

    Note: This online service is not intended for BrowseComp evaluation. Each query is limited to 100 tool calls for latency and stability. BrowseComp involves long-horizon tasks that typically require over 200 tool calls for our agent, which is outside the scope of this demo.

Performance

    To prevent potential information leakage (e.g., retrieving benchmark answers from HuggingFace), we blocked access to certain websites during evaluation.

MiroThinker
Quick Start

For optimal usage, we recommend using MiroThinker with our tool-enabled agent framework and thinking mode enabled. Please refer to our GitHub repository for installation instructions, examples, and full documentation:

👉 https://github.com/MiroMindAI/MiroThinker
Local Deployment

It is recommended to use SGLang or vLLM for deploying the agent:

SGLang
python -m sglang.launch_server --model-path miromind-ai/MiroThinker-1.7-mini --tp 8 --host 0.0.0.0 --port 1234
vLLM
vllm serve miromind-ai/MiroThinker-1.7-mini --tensor-parallel-size 8 --max-model-len 262144 --enable-reasoning

For optimal performance in agentic tasks, we recommend the following inference parameters:

temperature: 1.0
top_p: 0.95
repetition_penalty: 1.05
max_context_length: 262144
max_tokens: 16384

Recommended System Prompt

We use this unified XML-wrapped JSON format to describe and organize all tools. If you have additional tools, please document them using the same structure and formatting to ensure consistent parsing, compatibility, and optimal performance across the environment.
Click to expand system prompt example

Minimal Runnable Example

The following example shows how to run a MCP-style tool-calling workflow, including system prompt generation, agent invocation, tool execution, and final response generation.

Before running the script, make sure to set the required environment variables:

export OPENAI_API_KEY="your-api-key-here"
export BASE_URL="https://your-agent-endpoint.example.com/v1"

Click to expand python code example

import json
import os
import inspect
import re
from openai import OpenAI
from json_repair import repair_json
def get_weather(location: str, unit: str = "celsius") -> str:
    """
    Get weather information for a specified location (simulated)
    
    Args:
        location: Location name
        unit: Temperature unit, either celsius or fahrenheit
    
    Returns:
        JSON string with weather information
    """
    weather_data = {
        "London": {"temperature": 15, "condition": "sunny", "humidity": 45},
        "New York": {"temperature": 20, "condition": "cloudy", "humidity": 60},
        "Tokyo": {"temperature": 25, "condition": "rainy", "humidity": 75},
    }
    weather = weather_data.get(location, {"temperature": 18, "condition": "unknown", "humidity": 50})
    if unit == "fahrenheit":
        weather["temperature"] = weather["temperature"] * 9/5 + 32
        weather["unit"] = "°F"
    else:
        weather["unit"] = "°C"
    return json.dumps(weather, ensure_ascii=False)
def calculate(expression: str) -> str:
    """
    Calculate a mathematical expression
    
    Args:
        expression: Mathematical expression, e.g., "2 + 3 * 4"
    
    Returns:
        Calculation result
    """
    try:
        result = eval(expression)
        return json.dumps({"result": result, "expression": expression}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)
tools = [
    {"type": "function", "function": {"name": "get_weather", "parameters": {"type": "object", "properties": {"location": {"type": "string", "description": "Location name"}, "unit": {"type": "string", "enum": ["celsius", "fahrenheit"], "description": "Temperature unit, default is celsius"}}, "required": ["location"]}}},
    {"type": "function", "function": {"name": "calculate", "parameters": {"type": "object", "properties": {"expression": {"type": "string", "description": "Mathematical expression to calculate, e.g., '2 + 3 * 4'"}}, "required": ["expression"]}}}
]
available_functions = {"get_weather": get_weather, "calculate": calculate}
def parse_mcp_tool_call(response_text: str):
    """Parse MCP-style tool call from model response. Returns first tool call or None."""
    match = re.search(r'<use_mcp_tool>(.*?)</use_mcp_tool>', response_text, re.DOTALL)
    if not match:
        return None
    content = match.group(1)
    server_match = re.search(r'<server_name>(.*?)</server_name>', content, re.DOTALL)
    tool_match = re.search(r'<tool_name>(.*?)</tool_name>', content, re.DOTALL)
    args_match = re.search(r'<arguments>(.*?)</arguments>', content, re.DOTALL)
    server_name = server_match.group(1).strip() if server_match else None
    tool_name = tool_match.group(1).strip() if tool_match else None
    if args_match:
        try:
            arguments = json.loads(args_match.group(1).strip())
        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: Failed to parse arguments JSON: {e}, attempting to repair...")
            try:
                repaired = repair_json(args_match.group(1).strip())
                arguments = json.loads(repaired)
                print(f"✅  Successfully repaired JSON")
            except Exception as repair_error:
                print(f"❌  Failed to repair JSON: {repair_error}")
                arguments = {}
    else:
        arguments = {}
    if server_name and tool_name:
        return {"server_name": server_name, "tool_name": tool_name, "arguments": arguments}
    return None
def generate_mcp_system_prompt(openai_tools: list, available_functions: dict = None, server_name: str = "default", date: str = "2025-11-27") -> str:
    """Generate MCP-style system prompt from OpenAI tools format."""
    prefix = f"""
In this environment you have access to a set of tools you can use to answer the user's question.
You only have access to the tools provided below. You can only use one tool per message, and will receive the result of that tool in the user's next response. You use tools step-by-step to accomplish a given task, with each tool-use informed by the result of the previous tool-use. Today is: {date}
# Tool-Use Formatting Instructions
Tool-use is formatted using XML-style tags. The tool-use is enclosed in <use_mcp_tool></use_mcp_tool> and each parameter is similarly enclosed within its own set of tags.
The Model Context Protocol (MCP) connects to servers that provide additional tools and resources to extend your capabilities. You can use the server's tools via the `use_mcp_tool`.
Description:
Request to use a tool provided by a MCP server. Each MCP server can provide multiple tools with different capabilities. Tools have defined input schemas that specify required and optional parameters.
Parameters:
- server_name: (required) The name of the MCP server providing the tool
- tool_name: (required) The name of the tool to execute
- arguments: (required) A JSON object containing the tool's input parameters, following the tool's input schema, quotes within string must be properly escaped, ensure it's valid JSON
Usage:
<use_mcp_tool>
<server_name>server name here</server_name>
<tool_name>tool name here</tool_name>
<arguments>
{{
  "param1": "value1",
  "param2": "value2 \\"escaped string\\""
}}
</arguments>
</use_mcp_tool>
Important Notes:
- Tool-use must be placed **at the end** of your response, **top-level**, and not nested within other tags.
- Always adhere to this format for the tool use to ensure proper parsing and execution.
String and scalar parameters should be specified as is, while lists and objects should use JSON format. Note that spaces for string values are not stripped. The output is not expected to be valid XML and is parsed with regular expressions.
Here are the functions available in JSONSchema format:
## Server name: {server_name}
"""
    tools_section = []
    for i, tool in enumerate(openai_tools):
        if tool.get("type") == "function":
            func = tool["function"]
            tool_name = func["name"]
            func_obj = available_functions[tool_name]
            full_description = inspect.getdoc(func_obj) or func.get("description", "")
            if i > 0:
                tools_section.append("\n")
            tools_section.append(f"### Tool name: {tool_name}\nDescription: {full_description}\n\nInput JSON schema: {json.dumps(func['parameters'], ensure_ascii=False)}\n")
    suffix = "\n# General Objective\n\nYou accomplish a given task iteratively, breaking it down into clear steps and working through them methodically."
    return prefix + ''.join(tools_section) + suffix
def run_conversation(user_query: str, model: str = "MiroThinker"):
    """Run a complete conversation with tool calling"""
    system_prompt = generate_mcp_system_prompt(openai_tools=tools, available_functions=available_functions, server_name="My-Tools", date="2025-12-01")
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key-here"), base_url=os.environ.get("BASE_URL", "your-base-url-here"))
    print(f"\n{'='*60}\nUser Query: {user_query}\n{'='*60}\n")
    messages = [{'role': 'system', 'content': system_prompt}, {"role": "user", "content": user_query}]
    print("📤 Sending request to model...")
    response = client.chat.completions.create(model=model, messages=messages)
    response_message = response.choices[0].message
    response_content = response_message.content
    tool_call = parse_mcp_tool_call(response_content)
    print(f"📝 Model response:\n{response_content}\n")
    messages.append(response_message)
    if tool_call:
        server_name = tool_call["server_name"]
        tool_name = tool_call["tool_name"]
        function_args = tool_call["arguments"]
        print(f"\n🔧 Model decided to call tool:\n  - Server: {server_name}\n    Tool: {tool_name}\n    Args: {json.dumps(function_args, ensure_ascii=False)}")
        function_response = available_functions[tool_name](**function_args)
        print(f"    Result: {function_response}\n")
        messages.append({"role": "user", "content": function_response})
        print("📤 Requesting model to generate final response based on tool results...\n")
        second_response = client.chat.completions.create(model=model, messages=messages)
        final_message = second_response.choices[0].message.content
        print(f"💬 Final Response:\n{final_message}\n")
        return final_message
    else:
        print(f"💬 Model Response (no tool calls):\n{response_message.content}\n")
        return response_message.content
def main():
    """Run multiple examples"""
    run_conversation("What's the weather like in London?")
    # run_conversation("Calculate (25 + 15) * 3 - 10")
if __name__ == "__main__":
    main()

License

MiroThinker-1.7 is released under Apache 2.0.
Citation

If you find this project useful in your research, please consider citing:

@article{miromind2025mirothinker,
  title={MiroThinker: Pushing the Performance Boundaries of Open-Source Research Agents via Model, Context, and Interactive Scaling},
  author={MiroMind Team and Bai, Song and Bing, Lidong and Chen, Carson and Chen, Guanzheng and Chen, Yuntao and Chen, Zhe and Chen, Ziyi and Dong, Xuan and others},
  journal={arXiv preprint arXiv:2511.11793},
  year={2025}
}

Contact Us

MiroThinker is developed by the MiroMind AI Team. If you would like to leave us a message, feel free to get in touch. In addition to GitHub, Discord, you can also reach us via email at service@miromind.ai.