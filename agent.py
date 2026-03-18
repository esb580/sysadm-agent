import os
import anthropic
from tools import check_disk_usage

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

MODEL = "claude-haiku-4-5-20251001"

# Tool definitions tell the model what tools exist and how to call them
TOOLS = [
    {
        "name": "check_disk_usage",
        "description": "Check disk usage on the system using df -h. Returns a table showing filesystem, size, used, available, and mount points.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]


def run_tool(name, tool_input):
    """Dispatch a tool call by name and return the result as a string."""
    if name == "check_disk_usage":
        return check_disk_usage()
    return f"Unknown tool: {name}"


def run_agent(user_message):
    """
    Run the agent loop for a single user message.

    The loop:
      1. Send message to the model
      2. If the model wants to call a tool, run it and feed the result back
      3. Repeat until the model gives a final text response
    """
    print(f"\nYou: {user_message}")

    messages = [
        {"role": "user", "content": user_message}
    ]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=TOOLS,
            messages=messages
        )

        # Append the assistant's response to the conversation history
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            # Model is done — print the final text response
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"\nAgent: {block.text}")
            break

        elif response.stop_reason == "tool_use":
            # Model wants to call one or more tools
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"\n[calling tool: {block.name}]")
                    result = run_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            # Feed the tool results back as a user message
            messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    print("Sysadmin Agent — type 'quit' to exit")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if user_input:
            run_agent(user_input)
