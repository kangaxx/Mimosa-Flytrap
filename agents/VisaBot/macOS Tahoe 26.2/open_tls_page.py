#!/usr/bin/env python3
import argparse
import base64
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

DEFAULT_TLS_FR_URL = "https://fr.tlscontact.com"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Open a TLS (HTTPS) webpage using Playwright")
    parser.add_argument(
        "--url",
        default=os.getenv("TLS_URL", DEFAULT_TLS_FR_URL),
        help=(
            "Target URL to open (default: TLS_URL env or "
            f"{DEFAULT_TLS_FR_URL})"
        ),
    )
    parser.add_argument(
        "--headless",
        action=argparse.BooleanOptionalAction,
        default=os.getenv("HEADLESS", "1") not in {"0", "false", "False"},
        help="Run browser headless (default: true; set --no-headless to show UI)",
    )
    parser.add_argument(
        "--manual-verify",
        action=argparse.BooleanOptionalAction,
        default=os.getenv("MANUAL_VERIFY", "1") not in {"0", "false", "False"},
        help=(
            "Wait for you to manually finish bot verification/CAPTCHA before continuing "
            "(default: true)"
        ),
    )
    parser.add_argument(
        "--manual-timeout-ms",
        type=int,
        default=int(os.getenv("MANUAL_TIMEOUT_MS", "900000")),
        help="Max time to wait for manual verification (ms). Default: 900000 (15 min)",
    )
    parser.add_argument(
        "--auto-select-city",
        action=argparse.BooleanOptionalAction,
        default=os.getenv("AUTO_SELECT_CITY", "1") not in {"0", "false", "False"},
        help="After manual verification, attempt to select a city (default: true)",
    )
    parser.add_argument(
        "--city",
        default=os.getenv("TLS_CITY", "Shanghai"),
        help="City name to select (default: Shanghai; can also work with 上海)",
    )
    parser.add_argument(
        "--wait-ms",
        type=int,
        default=int(os.getenv("WAIT_MS", "5000")),
        help="Extra wait after navigation (ms). Default: 5000",
    )
    parser.add_argument(
        "--wait-until",
        default=os.getenv("WAIT_UNTIL", "commit"),
        choices=["commit", "domcontentloaded", "load", "networkidle"],
        help="Playwright waitUntil strategy. Default: commit",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=int(os.getenv("TIMEOUT_MS", "60000")),
        help="Navigation timeout (ms). Default: 60000",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=int(os.getenv("RETRIES", "2")),
        help="Retry count on navigation timeout/error. Default: 2",
    )
    parser.add_argument(
        "--retry-delay-ms",
        type=int,
        default=int(os.getenv("RETRY_DELAY_MS", "800")),
        help="Delay between retries (ms). Default: 800",
    )
    parser.add_argument(
        "--screenshot",
        default=os.getenv("SCREENSHOT", ""),
        help="If set, save a screenshot to this path (e.g. tls.png)",
    )
    parser.add_argument(
        "--screenshot-timeout-ms",
        type=int,
        default=int(os.getenv("SCREENSHOT_TIMEOUT_MS", "90000")),
        help="Screenshot timeout (ms). Default: 90000",
    )
    parser.add_argument(
        "--full-page",
        action=argparse.BooleanOptionalAction,
        default=os.getenv("FULL_PAGE", "1") not in {"0", "false", "False"},
        help="Capture full page in screenshot (default: true)",
    )
    return parser.parse_args()


def _is_interactive() -> bool:
    try:
        return sys.stdin.isatty()
    except Exception:
        return False


def wait_for_manual_verification(page, timeout_ms: int) -> None:
    print("\nManual step required:")
    print("- Complete the bot verification / CAPTCHA in the opened browser window.")
    print("- After you reach the page where you can choose a city (e.g., Shanghai), return here.")
    try:
        page.bring_to_front()
    except Exception:
        pass

    if _is_interactive():
        input("Press Enter to continue after verification...")
        return

    print(f"Non-interactive shell detected; waiting up to {timeout_ms}ms...")
    page.wait_for_timeout(timeout_ms)


def try_select_city(page, city: str) -> bool:
    city_variants = [city]
    if city.lower() != city:
        city_variants.append(city.lower())
    if city.upper() != city:
        city_variants.append(city.upper())
    if city == "Shanghai":
        city_variants.extend(["上海", "SHANGHAI"])

    def click_first_match(locator) -> bool:
        try:
            if locator.count() <= 0:
                return False
            locator.first.click(timeout=5000)
            return True
        except Exception:
            return False

    # Strategy 1: click visible option/text directly.
    for v in city_variants:
        if click_first_match(page.get_by_role("option", name=v)):
            return True
        if click_first_match(page.get_by_text(v, exact=False)):
            return True

    # Strategy 2: open any combobox then click an option.
    try:
        comboboxes = page.get_by_role("combobox")
        for i in range(min(comboboxes.count(), 5)):
            try:
                comboboxes.nth(i).click(timeout=2000)
                for v in city_variants:
                    if click_first_match(page.get_by_role("option", name=v)):
                        return True
                    if click_first_match(page.get_by_text(v, exact=False)):
                        return True
            except Exception:
                continue
    except Exception:
        pass

    return False


def main() -> None:
    args = parse_args()

    if args.manual_verify and args.headless:
        print("manual_verify=true requires a visible browser window; forcing --no-headless")
        args.headless = False

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        context = browser.new_context(
            ignore_https_errors=False,
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()

        out_path = None
        if args.screenshot:
            out_path = Path(args.screenshot).expanduser().resolve()
            out_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"Opening: {args.url}")
        print(f"headless={args.headless} wait_until={args.wait_until} timeout_ms={args.timeout_ms}")

        last_error: Exception | None = None
        for attempt in range(1, max(1, args.retries) + 1):
            try:
                response = page.goto(args.url, wait_until=args.wait_until, timeout=args.timeout_ms)
                status = getattr(response, "status", None)
                if callable(status):
                    print(f"HTTP status: {response.status()}")
                break
            except (PlaywrightTimeoutError, Exception) as exc:
                last_error = exc
                print(f"Attempt {attempt} failed: {type(exc).__name__}: {exc}")
                if attempt >= args.retries:
                    break
                time.sleep(args.retry_delay_ms / 1000.0)

        if last_error is not None:
            print("Navigation did not fully succeed; continuing to report page info.")

        try:
            page.wait_for_timeout(args.wait_ms)
        except Exception:
            pass

        if args.manual_verify:
            wait_for_manual_verification(page, args.manual_timeout_ms)
            try:
                page.wait_for_timeout(800)
            except Exception:
                pass

        if args.auto_select_city:
            print(f"\nAttempting to select city: {args.city}")
            ok = try_select_city(page, args.city)
            print(f"City selection result: {'OK' if ok else 'NOT FOUND'}")
            try:
                page.wait_for_timeout(1000)
            except Exception:
                pass

        try:
            title = page.title()
        except Exception:
            title = ""

        print(f"Title: {title!r}")
        print(f"Final URL: {page.url}")

        if "tlscontact error" in (title or "").strip().lower():
            print(
                "Hint: TLScontact may block headless/automation sessions. "
                "Use --no-headless and --manual-verify to complete verification in the browser window."
            )

        if out_path is not None:
            try:
                page.screenshot(
                    path=str(out_path),
                    full_page=args.full_page,
                    timeout=args.screenshot_timeout_ms,
                    animations="disabled",
                )
                print(f"Saved screenshot: {out_path}")
            except PlaywrightTimeoutError as exc:
                print(f"Screenshot timed out, trying Chromium CDP fallback: {exc}")
                try:
                    cdp = context.new_cdp_session(page)
                    result = cdp.send(
                        "Page.captureScreenshot",
                        {
                            "format": "png",
                            "captureBeyondViewport": bool(args.full_page),
                        },
                    )
                    png_b64 = result.get("data", "")
                    if not png_b64:
                        raise RuntimeError("CDP did not return screenshot data")
                    out_path.write_bytes(base64.b64decode(png_b64))
                    print(f"Saved screenshot (CDP): {out_path}")
                except Exception as exc2:
                    print(f"CDP screenshot failed: {type(exc2).__name__}: {exc2}")
            except Exception as exc:
                print(f"Screenshot failed: {type(exc).__name__}: {exc}")

        context.close()
        browser.close()


if __name__ == "__main__":
    main()
