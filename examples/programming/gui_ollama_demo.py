#!/usr/bin/env python3
"""Simple Tkinter GUI to call the local Ollama demo (02_ollama_local_demo.py).

The GUI dynamically loads the demo module by path and runs its request
functions in a background thread so the UI remains responsive.
"""

import os
import sys
import threading
import queue
import json
import traceback
from pathlib import Path
import importlib.util
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox


def load_demo_module() -> object:
    # Locate the demo module by relative path to this file
    base = Path(__file__).parent
    demo_path = base / "02_ollama_local_demo.py"
    if not demo_path.exists():
        raise FileNotFoundError(f"Demo module not found at {demo_path}")
    spec = importlib.util.spec_from_file_location("ollama_demo", str(demo_path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)  # type: ignore
    return mod


class OllamaGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Ollama Local Demo")

        self.mod = None
        try:
            self.mod = load_demo_module()
        except Exception as e:
            messagebox.showerror("Module load error", f"Failed to load demo module:\n{e}")

        frm = ttk.Frame(root, padding=12)
        frm.grid(sticky="nsew")

        ttk.Label(frm, text="Prompt:").grid(row=0, column=0, sticky="w")
        self.prompt = tk.Text(frm, height=6, width=80)
        self.prompt.grid(row=1, column=0, columnspan=4, sticky="we", pady=(0, 8))

        ttk.Label(frm, text="Model:").grid(row=2, column=0, sticky="w")
        self.model_var = tk.StringVar(value=(getattr(self.mod, 'DEFAULT_MODEL', 'deepseek-r1:8b') if self.mod else 'deepseek-r1:8b'))
        ttk.Entry(frm, textvariable=self.model_var, width=30).grid(row=2, column=1, sticky="w")

        ttk.Label(frm, text="Temperature:").grid(row=2, column=2, sticky="w")
        self.temp_var = tk.DoubleVar(value=0.7)
        ttk.Entry(frm, textvariable=self.temp_var, width=8).grid(row=2, column=3, sticky="w")

        ttk.Label(frm, text="Max tokens:").grid(row=3, column=0, sticky="w")
        self.max_var = tk.IntVar(value=2000)
        ttk.Entry(frm, textvariable=self.max_var, width=10).grid(row=3, column=1, sticky="w")

        self.use_curl = tk.BooleanVar(value=False)
        ttk.Checkbutton(frm, text="Force curl", variable=self.use_curl).grid(row=3, column=2, sticky="w")

        self.send_btn = ttk.Button(frm, text="Send", command=self.on_send)
        self.send_btn.grid(row=3, column=3, sticky="e")

        ttk.Label(frm, text="Response:").grid(row=4, column=0, sticky="w", pady=(8, 0))
        self.output = scrolledtext.ScrolledText(frm, height=20, width=100)
        self.output.grid(row=5, column=0, columnspan=4, sticky="nsew")

        # make UI expand
        root.columnconfigure(0, weight=1)
        #!/usr/bin/env python3
        """Simple Tkinter GUI to call the local Ollama demo (02_ollama_local_demo.py).

        The GUI dynamically loads the demo module by path and runs its request
        functions in a background thread so the UI remains responsive.
        """

        import sys
        import threading
        import queue
        import json
        import traceback
        from pathlib import Path
        import importlib.util
        import tkinter as tk
        from tkinter import ttk, scrolledtext, messagebox


        def load_demo_module() -> object:
            base = Path(__file__).parent
            demo_path = base / "02_ollama_local_demo.py"
            if not demo_path.exists():
                raise FileNotFoundError(f"Demo module not found at {demo_path}")
            spec = importlib.util.spec_from_file_location("ollama_demo", str(demo_path))
            mod = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = mod
            spec.loader.exec_module(mod)  # type: ignore
            return mod


        class OllamaGUI:
            def __init__(self, root: tk.Tk):
                self.root = root
                root.title("Ollama Local Demo")

                self.mod = None
                try:
                    self.mod = load_demo_module()
                except Exception as e:
                    messagebox.showerror("Module load error", f"Failed to load demo module:\n{e}")

                frm = ttk.Frame(root, padding=12)
                frm.grid(sticky="nsew")

                ttk.Label(frm, text="Prompt:").grid(row=0, column=0, sticky="w")
                self.prompt = tk.Text(frm, height=6, width=80)
                self.prompt.grid(row=1, column=0, columnspan=4, sticky="we", pady=(0, 8))

                ttk.Label(frm, text="Model:").grid(row=2, column=0, sticky="w")
                self.model_var = tk.StringVar(value=(getattr(self.mod, 'DEFAULT_MODEL', 'deepseek-r1:8b') if self.mod else 'deepseek-r1:8b'))
                ttk.Entry(frm, textvariable=self.model_var, width=30).grid(row=2, column=1, sticky="w")

                ttk.Label(frm, text="Temperature:").grid(row=2, column=2, sticky="w")
                self.temp_var = tk.DoubleVar(value=0.7)
                ttk.Entry(frm, textvariable=self.temp_var, width=8).grid(row=2, column=3, sticky="w")

                ttk.Label(frm, text="Max tokens:").grid(row=3, column=0, sticky="w")
                self.max_var = tk.IntVar(value=2000)
                ttk.Entry(frm, textvariable=self.max_var, width=10).grid(row=3, column=1, sticky="w")

                self.use_curl = tk.BooleanVar(value=False)
                ttk.Checkbutton(frm, text="Force curl", variable=self.use_curl).grid(row=3, column=2, sticky="w")

                self.send_btn = ttk.Button(frm, text="Send", command=self.on_send)
                self.send_btn.grid(row=3, column=3, sticky="e")

                ttk.Label(frm, text="Response:").grid(row=4, column=0, sticky="w", pady=(8, 0))
                self.output = scrolledtext.ScrolledText(frm, height=20, width=100)
                self.output.grid(row=5, column=0, columnspan=4, sticky="nsew")

                # make UI expand
                root.columnconfigure(0, weight=1)
                root.rowconfigure(0, weight=1)
                frm.columnconfigure(0, weight=1)

                self.q = queue.Queue()
                self.poll_queue()

            def poll_queue(self):
                try:
                    while True:
                        msg = self.q.get_nowait()
                        self.append_output(msg)
                except queue.Empty:
                    pass
                self.root.after(100, self.poll_queue)

            def append_output(self, text: str) -> None:
                self.output.insert(tk.END, text + "\n")
                self.output.see(tk.END)

            def on_send(self) -> None:
                if not self.mod:
                    messagebox.showerror("Not loaded", "Demo module not loaded; cannot send request.")
                    return
                prompt = self.prompt.get("1.0", tk.END).strip()
                if not prompt:
                    messagebox.showwarning("Empty prompt", "Please enter a prompt.")
                    return
                model = self.model_var.get().strip() or getattr(self.mod, 'DEFAULT_MODEL', 'deepseek-r1:8b')
                temp = float(self.temp_var.get())
                max_tokens = int(self.max_var.get())
                use_curl = bool(self.use_curl.get())

                self.send_btn.config(state=tk.DISABLED)
                threading.Thread(target=self.worker, args=(prompt, model, temp, max_tokens, use_curl), daemon=True).start()

            def worker(self, prompt: str, model: str, temperature: float, max_tokens: int, use_curl: bool) -> None:
                try:
                    payload = self.mod.build_payload(prompt, model, temperature, max_tokens)
                    endpoint = f"{getattr(self.mod, 'DEFAULT_BASE', 'http://127.0.0.1:11434').rstrip('/')}/v1/chat/completions"
                    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {getattr(self.mod, 'DEFAULT_KEY', 'ollama') }"}
                except Exception as e:
                    self.q.put(f"Error preparing request: {e}")
                    self.q.put(traceback.format_exc())
                    self.q.put("---")
                    self.root.after(0, lambda: self.send_btn.config(state=tk.NORMAL))
                    return

                try:
                    if not use_curl:
                        try:
                            res = self.mod.call_with_requests(endpoint, headers, payload)
                        except Exception as e:
                            self.q.put(f"requests failed: {e}; falling back to curl")
                            res = self.mod.call_with_curl(endpoint, headers, payload)
                    else:
                        res = self.mod.call_with_curl(endpoint, headers, payload)

                    # Pretty-format response
                    if isinstance(res, dict) and "choices" in res:
                        choice = res["choices"][0]
                        content = None
                        if isinstance(choice, dict):
                            content = choice.get("message", {}).get("content") or choice.get("text")
                        if content:
                            self.q.put("=== Generated content ===")
                            self.q.put(content)
                        else:
                            self.q.put(json.dumps(res, indent=2, ensure_ascii=False))
                    else:
                        self.q.put(json.dumps(res, indent=2, ensure_ascii=False))
                except Exception as e:
                    self.q.put(f"Request error: {e}")
                    self.q.put(traceback.format_exc())
                finally:
                    self.root.after(0, lambda: self.send_btn.config(state=tk.NORMAL))


        def main():
            root = tk.Tk()
            app = OllamaGUI(root)
            root.mainloop()


        if __name__ == "__main__":
            main()
            main()
