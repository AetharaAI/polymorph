'''
# Aether Skill

## Description

This skill enables the Aether agent, a semi-autonomous AI assistant with advanced capabilities, including a Redis-based mutable memory system, NVIDIA Kimik2.5 integration, and a Fleet Manager Control Plane (FMC) for orchestration. It provides a set of commands to manage the agent's autonomy, memory, and fleet integration.

**Patent Claims:**
- Novel method for AI agent memory mutation via distributed caches (Redis).
- System for hybrid human-AI autonomy with client-server fleet orchestration.

## Commands

The Aether skill introduces the following commands, accessible via the `/aether` prefix:

-   `/aether browse <url> [purpose]`: Navigates to a URL and provides a vision-powered understanding of the page content based on your purpose.

-   `/aether toggle auto`: Switches the agent to **autonomous mode**, allowing it to execute tasks without requiring human approval for most actions.
-   `/aether toggle semi`: Switches the agent to **semi-autonomous mode**, where it will ask for approval before executing potentially risky actions.
-   `/aether checkpoint <name>`: Creates a snapshot of the agent's current memory state. An optional `name` can be provided for easy identification.
-   `/aether rollback <checkpoint_id>`: Reverts the agent's memory to a previously created checkpoint.
-   `/aether fleet status`: Displays the current status of the Aether pod within the Fleet Manager, including health metrics and resource usage.
-   `/aether heartbeat`: Manually triggers a heartbeat to the Fleet Manager to report the latest health stats.
-   `/aether stats`: Shows statistics about the agent's memory usage, such as the number of daily logs, long-term memory size, and available checkpoints.

## Tools

This skill provides a set of custom tools that are used by the Aether agent to perform its functions. These tools are designed to be used by the agent itself and are not typically invoked directly by the user.

-   `smart_navigate`: Navigates to a URL with intelligent purpose understanding.
-   `smart_click`: Clicks an element by description instead of index.
-   `smart_extract`: Extracts information intelligently from a page.

-   `aether_memory_search`: Performs a semantic search over the agent's Redis-based memory.
-   `aether_checkpoint`: Creates a snapshot of the agent's memory.
-   `aether_rollback`: Restores the agent's memory from a snapshot.
-   `fleet_report`: Sends a health report to the Fleet Manager.
-   `nvidia_kimik_complete`: Interacts with the NVIDIA Kimik2.5 model for advanced reasoning and content generation.

## Installation and Configuration

To use this skill, you need to have the Aether agent installed and configured in your OpenClaw environment. This includes:

1.  Installing the Aether Python package.
2.  Configuring the `config_patches.yaml` to integrate Aether with your OpenClaw gateway.
3.  Ensuring that the Aether workspace and necessary environment variables are set up correctly.

For detailed installation instructions, please refer to the `README.md` file in the Aether project documentation.
'''))িনারਾ- I have created the `aether.skill.md` file, which defines the Aether skill for OpenClaw. This file describes the skill, its commands, and the tools it provides, making Aether
