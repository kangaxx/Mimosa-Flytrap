# main.py
import asyncio
import json
import os
import sys
from typing import Any, AsyncGenerator, Mapping, Sequence, Union

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from mouse_work import MouseWork

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core._cancellation_token import CancellationToken
from autogen_core._types import FunctionCall
from autogen_core.models import ChatCompletionClient, CreateResult, RequestUsage
from autogen_core.models._types import LLMMessage
from autogen_core.tools import FunctionTool, Tool, ToolSchema

load_dotenv()

def open_tls_and_wait(url: str) -> str:
    """调用 MouseWork 打开页面并执行鼠标操作"""
    mouse_worker = MouseWork(slow_mo=80, max_auto_retry=2)
    
    with sync_playwright() as p:
        browser = p.webkit.launch(
            headless=False,
            slow_mo=mouse_worker.slow_mo,
        )
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "Version/17.4.1 Safari/605.1.15"
            ),
            viewport=None,
            locale="en-GB",
            timezone_id="Europe/London",
            geolocation={"latitude": 51.5074, "longitude": -0.1278},
        )
        context.add_init_script(
            """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-GB', 'en-US', 'en']});
            Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
            """
        )
        page = context.new_page()
        
        try:
            result = mouse_worker.open_page_with_operation(
                page=page,
                url=url,
                keep_open_ms=300000,
                manual_timeout_ms=900000
            )
            return result
        finally:
            browser.close()
            print("\n🔚 浏览器已关闭")

class DummyChatCompletionClient(ChatCompletionClient):
    """Minimal ChatCompletionClient for Autogen"""
    def __init__(self, url: str) -> None:
        self._url = url
        self._total_usage = RequestUsage(prompt_tokens=0, completion_tokens=0)
        self._actual_usage = RequestUsage(prompt_tokens=0, completion_tokens=0)
        self._model_info = {
            "model": "dummy-tool-caller",
            "max_tokens": 8192,
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": "any",
            "structured_output": False,
            "multiple_system_messages": True,
        }
        self._capabilities = {
            "vision": False,
            "function_calling": True,
            "json_output": False,
        }

    @property
    def capabilities(self) -> dict[str, bool]:
        return self._capabilities

    @property
    def model_info(self) -> dict[str, Any]:
        return self._model_info

    @property
    def total_usage(self) -> RequestUsage:
        return self._total_usage

    @property
    def actual_usage(self) -> RequestUsage:
        return self._actual_usage

    def count_tokens(self, messages: Sequence[LLMMessage], *, tools: Sequence[Tool | ToolSchema] = ()) -> int:
        total = 0
        for msg in messages:
            content = getattr(msg, "content", "")
            total += len(content) if isinstance(content, str) else 1
        return total

    def remaining_tokens(self, messages: Sequence[LLMMessage], *, tools: Sequence[Tool | ToolSchema] = ()) -> int:
        return max(0, int(self._model_info.get("max_tokens", 0)) - self.count_tokens(messages, tools=tools))

    async def create(
        self,
        messages: Sequence[LLMMessage],
        *,
        tools: Sequence[Tool | ToolSchema] = (),
        tool_choice: Union[Tool, str] = "auto",
        json_output: Union[bool, type[Any], None] = None,
        extra_create_args: Mapping[str, Any] = (),
        cancellation_token: CancellationToken | None = None,
    ) -> CreateResult:
        if any(getattr(m, "type", None) == "FunctionExecutionResultMessage" for m in messages):
            return CreateResult(
                finish_reason="stop",
                content="TERMINATE",
                usage=RequestUsage(prompt_tokens=0, completion_tokens=len("TERMINATE")),
                cached=False,
                logprobs=None,
                thought=None,
            )

        fc = FunctionCall(
            id="call_1",
            name="open_tls_and_wait",
            arguments=json.dumps({"url": self._url}, ensure_ascii=False),
        )
        return CreateResult(
            finish_reason="function_calls",
            content=[fc],
            usage=RequestUsage(prompt_tokens=0, completion_tokens=0),
            cached=False,
            logprobs=None,
            thought=None,
        )

    async def create_stream(
        self,
        messages: Sequence[LLMMessage],
        *,
        tools: Sequence[Tool | ToolSchema] = (),
        tool_choice: Union[Tool, str] = "auto",
        json_output: Union[bool, type[Any], None] = None,
        extra_create_args: Mapping[str, Any] = (),
        cancellation_token: CancellationToken | None = None,
    ) -> AsyncGenerator[Union[str, CreateResult], None]:
        yield await self.create(
            messages, tools=tools, tool_choice=tool_choice, json_output=json_output,
            extra_create_args=extra_create_args, cancellation_token=cancellation_token
        )

    def close(self) -> None:
        return None

async def main(target_url: str = "https://visas-fr.tlscontact.com/") -> None:
    """主程序：Autogen 框架调用 MouseWork 模块"""
    tool = FunctionTool(
        open_tls_and_wait,
        name="open_tls_and_wait",
        description="Open TLSContact URL, handle verification (auto + manual fallback).",
    )

    assistant = AssistantAgent(
        name="TLSOpener",
        model_client=DummyChatCompletionClient(target_url),
        tools=[tool],
        system_message="Use open_tls_and_wait tool to open the page. Reply TERMINATE when done.",
        max_tool_iterations=2,
    )

    team = RoundRobinGroupChat(
        participants=[assistant],
        termination_condition=TextMentionTermination("TERMINATE"),
        max_turns=3,
    )

    print(f"🚀 启动 TLSContact 页面工具：{target_url}")
    await Console(team.run_stream(task=f"打开页面并处理验证：{target_url}"))

if __name__ == "__main__":
    if os.name == "posix":
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    asyncio.run(main())