import re

import boto3
import structlog
from mypy_boto3_bedrock_runtime import BedrockRuntimeClient

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.dev.ConsoleRenderer(colors=True),
    ]
)

log = structlog.get_logger(__name__)


def bedrock_client() -> BedrockRuntimeClient:
    return boto3.client("bedrock-runtime", region_name="us-east-2")  # pyright: ignore[reportUnknownMemberType]


def color(text: str, color: str = "yellow") -> str:
    color_codes = {
        "yellow": "\033[33m",
        "green": "\033[32m",
        "red": "\033[31m",
        "blue": "\033[34m",
    }
    reset = "\033[0m"
    return f"{color_codes[color]}{text}{reset}"


def print_output(output: str):
    """
    Prints the output from the agent, extracting and displaying any thought process
    contained within <thinking> tags before showing the final output.

    Args:
        output (str): The raw output string from the agent, which may contain
                     thought process within <thinking> tags
    """
    thinking_pattern = r"<thinking>(.*?)</thinking>"
    agent_thought = re.search(thinking_pattern, output, re.DOTALL)

    if agent_thought:
        print(color(f"Thought » {agent_thought.group(1).strip()}", color="yellow"))
        # Remove the thinking tags and content
        output = re.sub(thinking_pattern, "", output, flags=re.DOTALL)

    print(color(f"Output »\n{output.strip()}", color="green"))
