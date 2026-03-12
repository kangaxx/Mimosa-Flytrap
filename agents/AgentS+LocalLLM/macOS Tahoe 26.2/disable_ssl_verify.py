# disable_ssl_verify.py
import ssl
import requests
import warnings
import os

# ========== 1. 禁用 Python 全局 SSL 证书验证（最底层） ==========
# 覆盖 ssl 模块的默认上下文，强制不验证证书
ssl._create_default_https_context = ssl._create_unverified_context
# 修复：过滤正确的 Warning 子类（忽略所有 SSL 相关警告）
warnings.filterwarnings("ignore", category=UserWarning, module="ssl")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="ssl")

# ========== 2. 禁用 requests 库的 SSL 验证 ==========
# 禁用 urllib3 的 SSL 警告（正确的警告类别）
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)
# 重写 requests.Session.request 方法，强制关闭验证
old_request = requests.Session.request
def new_request(self, method, url, *args, **kwargs):
    # 强制设置 verify=False，跳过证书验证
    kwargs['verify'] = False
    # 禁用重定向中的 SSL 验证（额外兜底）
    kwargs['allow_redirects'] = True
    return old_request(self, method, url, *args, **kwargs)
requests.Session.request = new_request

# ========== 3. 适配 huggingface-hub（兼容所有版本） ==========
try:
    import huggingface_hub
    # 通用方案：通过环境变量禁用 SSL（所有版本都支持）
    os.environ["HUGGINGFACE_HUB_DISABLE_SSL"] = "true"
    os.environ["HF_HUB_DISABLE_SSL"] = "true"  # 兼容旧版本的环境变量名
    # 可选：调用官方禁用方法（仅当方法存在时执行）
    if hasattr(huggingface_hub, "disable_ssl_verification"):
        huggingface_hub.disable_ssl_verification()
    elif hasattr(huggingface_hub.utils, "_ssl_verify") and hasattr(huggingface_hub.utils._ssl_verify, "disable_ssl_verification"):
        huggingface_hub.utils._ssl_verify.disable_ssl_verification()
except ImportError:
    # 未安装 huggingface-hub 时跳过
    print("⚠️ 未检测到 huggingface-hub，跳过相关 SSL 配置")
except Exception as e:
    # 捕获所有其他异常，仅警告不中断
    print(f"⚠️ huggingface-hub SSL 配置警告：{str(e)}，已通过环境变量禁用 SSL")

print("✅ 全局 SSL 验证已完全禁用，即将启动 vLLM 服务...")
