# mouse_work.py
import time
import random
import math
from playwright.sync_api import Mouse

class MouseWork:
    """鼠标操作处理类"""
    
    def __init__(self, slow_mo: int = 80, max_auto_retry: int = 2):
        """
        初始化鼠标操作处理器
        :param slow_mo: 操作延迟（毫秒），模拟人类速度
        :param max_auto_retry: 自动验证最大重试次数
        """
        self.slow_mo = slow_mo
        self.max_auto_retry = max_auto_retry

    def simulate_human_mouse_slide(self, page, start_x: float, start_y: float, end_x: float, end_y: float) -> bool:
        """模拟人类滑块滑动轨迹"""
        try:
            speed_curve = [0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 0.8, 0.6, 0.4, 0.2, 0.1]
            steps = random.randint(15, 25)
            
            page.mouse.move(start_x + random.uniform(-2, 2), start_y + random.uniform(-2, 2))
            time.sleep(random.uniform(0.3, 0.7))
            
            page.mouse.down(button=Mouse.LEFT)
            time.sleep(random.uniform(0.05, 0.15))
            
            for i in range(steps):
                ratio = i / steps
                speed = speed_curve[min(int(ratio * len(speed_curve)), len(speed_curve)-1)]
                current_x = start_x + (end_x - start_x) * ratio * speed + random.uniform(-4, 4)
                current_y = start_y + random.uniform(-4, 4)
                page.mouse.move(current_x, current_y)
                time.sleep(random.uniform(0.03, 0.08))
            
            final_x = end_x + random.uniform(-5, 5)
            final_y = end_y + random.uniform(-2, 2)
            page.mouse.move(final_x, final_y)
            time.sleep(random.uniform(0.1, 0.3))
            page.mouse.up(button=Mouse.LEFT)
            time.sleep(random.uniform(0.5, 0.8))
            
            page.wait_for_selector(
                "div#challenge-stage div.success, div.challenge-success, div.recaptcha-success",
                timeout=8000
            )
            return True
        except Exception as e:
            print(f"❌ 滑块滑动失败：{str(e)}")
            return False

    def mouse_draw_circles(self, page, center_x: float = None, center_y: float = None, num_circles: int = 3) -> None:
        """
        让鼠标指针画随机圆圈（模拟人类操作）
        :param page: Playwright 页面对象
        :param center_x: 画圈中心点X坐标（默认页面居中）
        :param center_y: 画圈中心点Y坐标（默认页面70%高度）
        :param num_circles: 画圈数量
        """
        if not center_x or not center_y:
            viewport = page.viewport_size
            center_x = viewport["width"] / 2 if viewport else 500
            center_y = viewport["height"] * 0.7 if viewport else 600

        print(f"\n🎨 开始画 {num_circles} 个随机圆圈（中心：{center_x:.0f}, {center_y:.0f}）...")
        
        page.mouse.move(center_x + random.uniform(-10, 10), center_y + random.uniform(-10, 10))
        time.sleep(random.uniform(0.5, 1.0))
        
        for circle_idx in range(num_circles):
            radius = random.randint(50, 150)
            steps = random.randint(30, 60)
            speed = random.uniform(0.02, 0.05)
            rotation = random.choice([-1, 1])
            offset_x = random.randint(-30, 30)
            offset_y = random.randint(-30, 30)
            
            print(f"🔵 第 {circle_idx+1} 个圈：半径 {radius}px，{'顺时针' if rotation == 1 else '逆时针'}")
            
            for step in range(steps):
                angle = rotation * 2 * math.pi * (step / steps)
                current_x = center_x + offset_x + radius * math.cos(angle)
                current_y = center_y + offset_y + radius * math.sin(angle)
                page.mouse.move(
                    current_x + random.uniform(-3, 3),
                    current_y + random.uniform(-3, 3)
                )
                time.sleep(speed)
            
            page.mouse.move(
                center_x + random.uniform(-50, 50),
                center_y + random.uniform(-50, 50)
            )
            time.sleep(random.uniform(0.3, 0.8))
        
        page.mouse.move(center_x + random.uniform(-20, 20), center_y + random.uniform(-20, 20))
        time.sleep(random.uniform(0.5, 1.0))
        print("🎨 鼠标画圈完成！")

    def auto_handle_verification(self, page) -> bool:
        """自动处理验证（滑块/点选）"""
        for retry in range(self.max_auto_retry):
            try:
                print(f"🤖 第{retry+1}次尝试自动验证...")
                
                slider = page.query_selector("div.ctp-slider-bar, div.g-recaptcha-slider, div.slider-track")
                if slider:
                    slider_bbox = slider.bounding_box()
                    if not slider_bbox:
                        continue
                    start_x = slider_bbox["x"] + random.uniform(8, 15)
                    start_y = slider_bbox["y"] + slider_bbox["height"] / 2 + random.uniform(-3, 3)
                    end_x = slider_bbox["x"] + slider_bbox["width"] - random.uniform(8, 15)
                    end_y = start_y
                    
                    if self.simulate_human_mouse_slide(page, start_x, start_y, end_x, end_y):
                        print("✅ 自动滑块验证通过！")
                        return True
                
                check_box = page.query_selector("input[type='checkbox'][id*='recaptcha'], div.recaptcha-checkbox-border")
                if check_box:
                    check_box_bbox = check_box.bounding_box()
                    click_x = check_box_bbox["x"] + random.uniform(5, 20)
                    click_y = check_box_bbox["y"] + random.uniform(5, 20)
                    
                    page.mouse.move(click_x, click_y)
                    time.sleep(random.uniform(0.2, 0.5))
                    page.mouse.click(click_x, click_y, button=Mouse.LEFT, delay=random.uniform(0.1, 0.3))
                    page.wait_for_selector("div.recaptcha-checkbox-checked", timeout=5000)
                    print("✅ 自动点选验证通过！")
                    return True
                
                print("✅ 无需验证，直接通过！")
                return True
            
            except Exception as e:
                print(f"❌ 自动验证重试失败：{str(e)}")
                page.reload()
                time.sleep(random.uniform(1, 2))
        
        print("❌ 多次自动验证失败，建议人工处理！")
        return False

    def open_page_with_operation(self, page, url: str, keep_open_ms: int = 30000, manual_timeout_ms: int = 900000) -> str:
        """
        打开页面并执行鼠标操作（完整流程）
        :param page: Playwright 页面对象
        :param url: 目标URL
        :param keep_open_ms: 页面停留时间（毫秒）
        :param manual_timeout_ms: 人工验证超时时间（毫秒）
        :return: 页面URL
        """
        try:
            print(f"🌐 正在打开页面：{url}")
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)

            self.mouse_draw_circles(page, num_circles=random.randint(3, 5))

            selectors = [
                "div#challenge-stage",
                "iframe[src*='turnstile']",
                "iframe[src*='challenges']",
                "div.g-recaptcha",
                "text=/verify you are human/i",
            ]
            has_challenge = False
            for sel in selectors:
                try:
                    if page.query_selector(sel):
                        has_challenge = True
                        break
                except Exception:
                    continue

            if has_challenge:
                if not self.auto_handle_verification(page):
                    print("\n⚠️ 自动验证失败，请手动完成验证！")
                    input("✅ 完成验证后按 Enter 继续...")

            stay_seconds = keep_open_ms / 1000
            print(f"\n✅ 页面已打开，将停留 {stay_seconds} 秒...")
            page.wait_for_timeout(keep_open_ms)
            
            return f"成功打开页面：{page.url}"
        except Exception as e:
            raise Exception(f"页面打开失败：{str(e)}")