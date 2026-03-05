import asyncio
import json
import os
import sys
from typing import Any, AsyncGenerator, Mapping, Sequence, Union

from playwright.sync_api import sync_playwright

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core._cancellation_token import CancellationToken
from autogen_core._types import FunctionCall
from autogen_core.models import (
    ChatCompletionClient,
    CreateResult,
    RequestUsage,
)
from autogen_core.models._types import LLMMessage
from autogen_core.tools import FunctionTool, Tool, ToolSchema


def open_baidu_and_type(query: str) -> str:
    """Open https://www.baidu.com and type the query into the search box."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        page.goto("https://www.baidu.com", wait_until="domcontentloaded")
        try:
            page.wait_for_load_state("networkidle", timeout=15_000)
        except Exception:
            pass

        # Baidu sometimes keeps multiple inputs in DOM; pick a visible one.
        candidates = [
            "#kw:visible",
            "input[name='wd']:visible",
            "input#kw",
            "input[name='wd']",
        ]

        search_input = None
        last_error: Exception | None = None
        for sel in candidates:
            try:
                loc = page.locator(sel).first
                loc.wait_for(state="visible", timeout=5_000)
                try:
                    loc.scroll_into_view_if_needed(timeout=2_000)
                except Exception:
                    pass
                loc.click(timeout=2_000)
                search_input = loc
                break
            except Exception as exc:
                last_error = exc
                continue

        if search_input is not None:
            search_input.fill(query, timeout=10_000)
            page.keyboard.press("Enter")
            page.wait_for_timeout(1500)
        else:
            # Fallback: some Baidu variants keep the input in DOM but hidden for automation.
            hidden = page.locator("input[name='wd'], #kw").first
            try:
                hidden.wait_for(state="attached", timeout=5_000)
                hidden.fill(query, timeout=10_000, force=True)
                submitted = page.evaluate(
                    """(q) => {
                        const el = document.querySelector('#kw') || document.querySelector("input[name='wd']");
                        if (!el) return false;
                        el.value = q;
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                        if (el.form) { el.form.submit(); return true; }
                        return false;
                    }""",
                    query,
                )
                if not submitted:
                    page.goto(
                        "https://www.baidu.com/s?wd=" + query,
                        wait_until="domcontentloaded",
                    )
                page.wait_for_timeout(1500)
            except Exception as exc:
                raise RuntimeError(f"Failed to fill Baidu search box even with fallback: {exc}")

        keep_open_ms = int(os.getenv("KEEP_OPEN_MS", "10000"))
        page.wait_for_timeout(keep_open_ms)

        context.close()
        browser.close()

    return f"Opened baidu.com and typed query: {query}"


class DummyChatCompletionClient(ChatCompletionClient):
    """A minimal ChatCompletionClient for AutoGen that always calls the tool once.

    This keeps the script runnable even without configuring an external LLM.
    """

    def __init__(self) -> None:
        self._total_usage = RequestUsage(prompt_tokens=0, completion_tokens=0)
        self._actual_usage = RequestUsage(prompt_tokens=0, completion_tokens=0)
        # NOTE: In this AutoGen version, AssistantAgent expects `model_info` to be a dict
        # with top-level keys like "function_calling".
        self._capabilities: dict[str, bool] = {
            "vision": False,
            "function_calling": True,
            "json_output": False,
        }
        self._model_info: dict[str, Any] = {
            "model": "dummy-tool-caller",
            "max_tokens": 8192,
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": "any",
            "structured_output": False,
            "multiple_system_messages": True,
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
        # Very rough estimate; good enough for a dummy client.
        total = 0
        for msg in messages:
            content = getattr(msg, "content", "")
            if isinstance(content, str):
                total += len(content)
            else:
                total += 1
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
        extra_create_args: Mapping[str, Any] = {},
        cancellation_token: CancellationToken | None = None,
    ) -> CreateResult:
        # If the tool already ran, terminate.
        if any(getattr(m, "type", None) == "FunctionExecutionResultMessage" for m in messages):
            content = "TERMINATE"
            usage = RequestUsage(prompt_tokens=0, completion_tokens=len(content))
            return CreateResult(
                finish_reason="stop",
                content=content,
                usage=usage,
                cached=False,
                logprobs=None,
                thought=None,
            )

        fc = FunctionCall(
            id="call_1",
            name="open_baidu_and_type",
            arguments=json.dumps({"query": "顾欣欣"}, ensure_ascii=False),
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
        extra_create_args: Mapping[str, Any] = {},
        cancellation_token: CancellationToken | None = None,
    ) -> AsyncGenerator[Union[str, CreateResult], None]:
        yield await self.create(
            messages,
            tools=tools,
            tool_choice=tool_choice,
            json_output=json_output,
            extra_create_args=extra_create_args,
            cancellation_token=cancellation_token,
        )

    def close(self) -> None:
        return None


async def main() -> None:
    tool = FunctionTool(
        open_baidu_and_type,
        name="open_baidu_and_type",
        description="Open baidu.com and type a query into the search box.",
    )

    assistant = AssistantAgent(
        name="BaiduAssistant",
        model_client=DummyChatCompletionClient(),
        tools=[tool],
        system_message="Use tools to complete the task. Reply with TERMINATE when done.",
        max_tool_iterations=2,
    )

    team = RoundRobinGroupChat(
        participants=[assistant],
        termination_condition=TextMentionTermination("TERMINATE"),
        max_turns=3,
    )

    await Console(team.run_stream(task="打开百度，并在搜索框输入：顾欣欣"))


if __name__ == "__main__":
    asyncio.run(main())
