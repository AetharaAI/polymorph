> ## Documentation Index
> Fetch the complete documentation index at: https://platform.minimax.io/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Text Generation

> MiniMax text models, supporting multilingual programming, Agent workflows and complex task scenarios.

<Note>
  Subscribe to [Coding Plan](https://platform.minimax.io/subscribe/coding-plan) to use MiniMax text models at ultra-low prices!
</Note>

## Model Overview

MiniMax offers multiple text models to meet different scenario requirements. **MiniMax-M2.5** achieves or sets new SOTA benchmarks in programming, tool calling and search, office productivity and other scenarios, while **MiniMax-M2** is built for efficient coding and Agent workflows.

### Supported Models

| Model Name             | Context Window | Description                                                                                                                                   |
| :--------------------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| MiniMax-M2.5           | 204,800        | **Peak Performance. Ultimate Value. Master the Complex (output speed approximately 60 tps)**                                                  |
| MiniMax-M2.5-highspeed | 204,800        | **M2.5 highspeed: Same performance, faster and more agile (output speed approximately 100 tps)**                                              |
| MiniMax-M2.1           | 204,800        | **Powerful Multi-Language Programming Capabilities with Comprehensively Enhanced Programming Experience (output speed approximately 60 tps)** |
| MiniMax-M2.1-highspeed | 204,800        | **Faster and More Agile (output speed approximately 100 tps)**                                                                                |
| MiniMax-M2             | 204,800        | **Agentic capabilities, Advanced reasoning**                                                                                                  |

<Note>
  For details on how tps (Tokens Per Second) is calculated, please refer to [FAQ > About APIs](/faq/about-apis#q-how-is-tps-tokens-per-second-calculated-for-text-models).
</Note>

### **MiniMax M2.5** Key Highlights

<AccordionGroup>
  <Accordion title="Programming: Think and Build Like an Architect">
    M2.5 has been trained on over 10 languages (including GO, C, C++, TS, Rust, Kotlin, Python, Java, JS, PHP, Lua, Dart, Ruby) across hundreds of thousands of real-world environments. The model has evolved native Spec behavior: before writing code, it proactively decomposes functionality, structure, and UI design from an architect's perspective, enabling comprehensive upfront planning.
  </Accordion>

  <Accordion title="Office Productivity: Deliverable Quality in Word, PPT, and Excel Financial Modeling">
    M2.5 deeply integrates real-world needs and tacit knowledge from experts in finance, law, and social sciences, building professional evaluation systems and cost monitoring frameworks. In advanced office scenarios such as Word, PPT, and financial modeling, it delivers high-quality, quantifiable, and scalable professional output.
  </Accordion>

  <Accordion title="Efficiency: Faster Decomposition, Faster Execution, Faster Delivery">
    With 100TPS inference speed, reinforcement learning-optimized complex task decomposition, and improved token efficiency, M2.5 significantly reduces end-to-end time for complex tasks—on SWE-Bench Verified, average time decreased from 31.3 minutes to 22.8 minutes, achieving 37% speedup and entering the mainstream top-tier model efficiency range.
  </Accordion>

  <Accordion title="Cost: Making Complex Agents Truly Sustainable for Long-Term Operation">
    M2.5 delivers high-performance output at highly competitive pricing—continuous operation at 100TPS costs only about \$1 per hour, with even lower costs for the 50TPS version. This makes long-term, multi-agent, year-round scaled deployment a reality, ushering agents into an era of "economic sustainability."
  </Accordion>
</AccordionGroup>

<Note>
  For more model details, please refer to [MiniMax M2.5](https://minimax.io/news/minimax-m25)
</Note>

***

## Calling Example

<Steps>
  <Step title="Install Anthropic SDK (Recommended)">
    <CodeGroup>
      ```bash Python theme={null}
      pip install anthropic
      ```

      ```bash Node.js theme={null}
      npm install @anthropic-ai/sdk
      ```
    </CodeGroup>
  </Step>

  <Step title="Set Environment Variables">
    ```bash  theme={null}
    export ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic
    export ANTHROPIC_API_KEY=${YOUR_API_KEY}
    ```
  </Step>

  <Step title="Call MiniMax-M2.5">
    ```python Python theme={null}
    import anthropic

    client = anthropic.Anthropic()

    message = client.messages.create(
        model="MiniMax-M2.5",
        max_tokens=1000,
        system="You are a helpful assistant.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Hi, how are you?"
                    }
                ]
            }
        ]
    )

    for block in message.content:
        if block.type == "thinking":
            print(f"Thinking:\n{block.thinking}\n")
        elif block.type == "text":
            print(f"Text:\n{block.text}\n")
    ```
  </Step>

  <Step title="Example Output">
    ```json  theme={null}
    {
      "thinking": "The user is just greeting me casually. I should respond in a friendly, professional manner.",
      "text": "Hi there! I'm doing well, thanks for asking. I'm ready to help you with whatever you need today—whether it's coding, answering questions, brainstorming ideas, or just chatting. What can I do for you?"
    }
    ```
  </Step>
</Steps>

***

## API Reference

<Columns cols={2}>
  <Card title="Anthropic API Compatible (Recommended)" icon="book-open" href="/api-reference/text-anthropic-api" cta="View Docs">
    Call MiniMax models via Anthropic SDK, supporting streaming output and Interleaved Thinking
  </Card>

  <Card title="OpenAI API Compatible" icon="book-open" href="/api-reference/text-openai-api" cta="View Docs">
    Call MiniMax models via OpenAI SDK
  </Card>

  <Card title="Text Generation" icon="file-text" href="/api-reference/text-post" cta="View Docs">
    Call text generation API directly via HTTP requests
  </Card>

  <Card title="Using M2.5 in AI Coding Tools" icon="code" href="/guides/text-ai-coding-tools" cta="View Docs">
    Use M2.5 in Claude Code, Cursor, Cline and other tools
  </Card>
</Columns>

***

## Contact Us

If you encounter any issues while using MiniMax models:

* Contact our technical support team through official channels such as email [Model@minimax.io](mailto:Model@minimax.io)
* Submit an Issue on our [Github](https://github.com/MiniMax-AI/MiniMax-M2.5/issues) repository

## Related Links

* [Anthropic SDK Documentation](https://docs.anthropic.com/en/api/client-sdks)
* [OpenAI SDK Documentation](https://platform.openai.com/docs/libraries)
* [MiniMax M2.5](https://minimax.io/news/minimax-m25)
