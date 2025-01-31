import json
from decimal import Decimal
from typing import Sequence

from mypy_boto3_bedrock_runtime.type_defs import (
    ConverseOutputTypeDef,
    InferenceConfigurationTypeDef,
    MessageTypeDef,
    SystemContentBlockTypeDef,
    ToolResultBlockOutputTypeDef,
    ToolUseBlockOutputTypeDef,
)

from amzn_bedrock_demo.tools import (
    add_subtract_multiply_divide,
    calculate_percentage_change,
    get_stock_price,
    is_trading_day,
    tool_config,
)
from amzn_bedrock_demo.util import bedrock_client, print_output

_MODEL_ID = "us.amazon.nova-lite-v1:0"

# Prompt inspired by https://smith.langchain.com/hub/cpatrickalves/react-chat-agent
_SYSTEM_PROMPT = """
You are designed to help with a variety of tasks, from answering questions to
providing summaries to other types of analyses. This may require breaking the
task into subtasks and using different tools to complete each subtask. You
follow the following rules:

- You break down the individual steps required to complete the task.
- You describe your plan for completing the task.
- You NEVER perform any math on your own. You ALWAYS use the tools provided to
you. If a question requires math and you don't have the tools to perform the
math, say so and ask the user to rephrase the question.

## Tools
You have access to a wide variety of tools. You are responsible for using the
tools in any sequence you deem appropriate to complete the task at hand.  This
may require breaking the task into subtasks and using different tools to
complete each subtask.
"""


def handle_assistant_output(
    output: ConverseOutputTypeDef, messages: Sequence[MessageTypeDef]
) -> Sequence[MessageTypeDef]:
    updated_messages: Sequence[MessageTypeDef] = list(messages)
    tool_results: list[ToolResultBlockOutputTypeDef] = []

    if "message" in output:
        updated_messages.append(
            {
                "role": output["message"]["role"],
                "content": output["message"]["content"],
            }
        )

        for content in output["message"]["content"]:
            if "text" in content:
                output_text = content["text"]
                print_output(output_text)
            elif "toolUse" in content:
                result = handle_tool_use(content["toolUse"])
                if result is not None:
                    tool_results.append(result)

    updated_messages.append(
        {"role": "user", "content": [{"toolResult": result} for result in tool_results]}
    )
    return updated_messages


def handle_tool_use(
    tool_use: ToolUseBlockOutputTypeDef,
) -> ToolResultBlockOutputTypeDef | None:
    tool_use_id = tool_use["toolUseId"]
    tool_name = tool_use["name"]

    if tool_name == "get_stock_price":
        symbol = str(tool_use["input"]["symbol"])
        date = str(tool_use["input"]["date"])
        stock_price = get_stock_price(symbol, date)
        if stock_price is not None:
            return {
                "toolUseId": tool_use_id,
                "status": "success",
                "content": [{"json": json.loads(stock_price.model_dump_json())}],
            }
    elif tool_name == "is_trading_day":
        date = str(tool_use["input"]["date"])
        return {
            "toolUseId": tool_use_id,
            "status": "success",
            "content": [{"json": {"result": is_trading_day(date)}}],
        }
    elif tool_name == "add_subtract_multiply_divide":
        first_num = Decimal(tool_use["input"]["first_num"])
        second_num = Decimal(tool_use["input"]["second_num"])
        operation = str(tool_use["input"]["operation"])
        try:
            result = add_subtract_multiply_divide(operation, first_num, second_num)
            if result is not None:
                return {
                    "toolUseId": tool_use_id,
                    "status": "success",
                    "content": [{"json": {"result": float(result)}}],
                }
            else:
                raise ValueError(f"Invalid operation '{operation}'")
        except ValueError:
            return {
                "toolUseId": tool_use_id,
                "status": "error",
                "content": [{"text": "Invalid operation"}],
            }
    elif tool_name == "calculate_percentage_change":
        first_num = Decimal(tool_use["input"]["first_num"])
        second_num = Decimal(tool_use["input"]["second_num"])
        pct_change = calculate_percentage_change(first_num, second_num)
        return {
            "toolUseId": tool_use_id,
            "status": "success",
            "content": [{"json": {"result": float(pct_change)}}],
        }


def agent_loop():
    client = bedrock_client()
    tools = tool_config()

    inf_params: InferenceConfigurationTypeDef = {
        "maxTokens": 5_120,
        "topP": 0.9,
        "temperature": 0.7,
        "stopSequences": [],
    }

    system_list: Sequence[SystemContentBlockTypeDef] = [
        {
            "text": _SYSTEM_PROMPT,
        }
    ]

    prompt = input("Enter a prompt: ")
    print()
    messages: Sequence[MessageTypeDef] = [
        {"role": "user", "content": [{"text": prompt}]}
    ]

    cont = True
    while cont:
        # Uncomment to see the raw messages
        # print(json.dumps(messages, indent=2))
        response = client.converse(
            modelId=_MODEL_ID,
            inferenceConfig=inf_params,
            system=system_list,
            messages=messages,
            toolConfig=tools,
        )
        # Uncomment to see the raw response
        # print(json.dumps(response, indent=2))

        messages = handle_assistant_output(response["output"], messages)
        stop_reason = response["stopReason"]
        cont = stop_reason != "end_turn"
