#!/usr/bin/env python3
"""Tkinter GUI to call the local Ollama demo (02_ollama_local_demo.py).

This is a single-module, cleaned version. It prints startup/shutdown messages
so running it from a terminal shows the prints.
"""

import sys
import threading
import queue
import json
import traceback
from pathlib import Path
import importlib.util
import logging
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import tempfile
import subprocess
import os


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
        # main model used for Q&A (Ollama server). Keep default as server model.
        self.model_var = tk.StringVar(value=(getattr(self.mod, 'DEFAULT_MODEL', 'deepseek-r1:8b') if self.mod else 'deepseek-r1:8b'))

        # STT model (faster-whisper) — default to a known local path if present
        default_local_model = '/Users/huangxuling/models/faster-whisper-small'
        self.stt_model_var = tk.StringVar(value=default_local_model if Path(default_local_model).exists() else '')
        ttk.Entry(frm, textvariable=self.model_var, width=30).grid(row=2, column=1, sticky="w")

        ttk.Label(frm, text="Temperature:").grid(row=2, column=2, sticky="w")
        self.temp_var = tk.DoubleVar(value=0.7)
        ttk.Entry(frm, textvariable=self.temp_var, width=8).grid(row=2, column=3, sticky="w")

        ttk.Label(frm, text="Max tokens:").grid(row=3, column=0, sticky="w")
        self.max_var = tk.IntVar(value=2000)
        ttk.Entry(frm, textvariable=self.max_var, width=10).grid(row=3, column=1, sticky="w")

        ttk.Label(frm, text="Timeout (s):").grid(row=3, column=2, sticky="w")
        self.timeout_var = tk.IntVar(value=120)
        ttk.Entry(frm, textvariable=self.timeout_var, width=10).grid(row=3, column=3, sticky="w")

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

        # recording state
        self.recording = False
        self.record_file = Path(tempfile.gettempdir()) / "ollama_record.wav"
        self.transcription_file = Path(tempfile.gettempdir()) / "ollama_transcription.txt"

        # add voice controls (record/transcribe/speak)
        try:
            self.add_voice_controls(frm)
        except Exception:
            # non-fatal: keep GUI working even if voice controls fail to build
            logging.exception('Failed to add voice controls')
        # automatic behaviours (defaults: side layout chosen earlier)
        self.auto_transcribe = True
        self.auto_speak = True
        # last generated content (for speaking)
        self._last_generated = None

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
            # determine timeout (ensure at least 1 second)
            try:
                timeout = int(max(1, int(self.timeout_var.get())))
            except Exception:
                timeout = 120

            # log payload for debugging
            try:
                self.q.put("Request payload: " + json.dumps(payload, ensure_ascii=False))
            except Exception:
                pass

            if not use_curl:
                try:
                    res = self.mod.call_with_requests(endpoint, headers, payload, timeout=timeout)
                except TypeError:
                    # older demo module may not accept timeout param
                    res = self.mod.call_with_requests(endpoint, headers, payload)
                except Exception as e:
                    self.q.put(f"requests failed: {e}; falling back to curl")
                    try:
                        res = self.mod.call_with_curl(endpoint, headers, payload, timeout=timeout)
                    except TypeError:
                        res = self.mod.call_with_curl(endpoint, headers, payload)
            else:
                try:
                    res = self.mod.call_with_curl(endpoint, headers, payload, timeout=timeout)
                except TypeError:
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
                    # store last generated and auto-speak if enabled
                    try:
                        self._last_generated = content
                        auto_s = self.auto_speak_var.get() if getattr(self, 'auto_speak_var', None) is not None else getattr(self, 'auto_speak', False)
                        if auto_s:
                            self.root.after(0, lambda c=content: self._play_text(c))
                    except Exception:
                        pass
                else:
                    self.q.put(json.dumps(res, indent=2, ensure_ascii=False))
            else:
                self.q.put(json.dumps(res, indent=2, ensure_ascii=False))
        except Exception as e:
            self.q.put(f"Request error: {e}")
            self.q.put(traceback.format_exc())
        finally:
            self.root.after(0, lambda: self.send_btn.config(state=tk.NORMAL))

    # --- STT/TTS helpers -------------------------------------------------
    def add_voice_controls(self, parent: ttk.Frame):
        # Buttons layout beside the prompt area
        btn_frm = ttk.Frame(parent)
        btn_frm.grid(row=1, column=4, rowspan=3, sticky="ne", padx=(8, 0))

        self.record_btn = ttk.Button(btn_frm, text="Record", command=self.toggle_record)
        self.record_btn.grid(row=0, column=0, pady=(0, 4))

        self.transcribe_btn = ttk.Button(btn_frm, text="Transcribe", command=self.transcribe_recording)
        self.transcribe_btn.grid(row=1, column=0, pady=(0, 4))

        self.speak_btn = ttk.Button(btn_frm, text="Speak Response", command=self.speak_response)
        self.speak_btn.grid(row=2, column=0, pady=(0, 4))

        # STT model display + browse
        ttk.Label(btn_frm, text="STT model:").grid(row=7, column=0, sticky='w', pady=(6, 0))
        self.stt_model_entry = ttk.Entry(btn_frm, textvariable=self.stt_model_var, width=30)
        self.stt_model_entry.grid(row=8, column=0, pady=(2, 4))
        def _browse_stt():
            d = filedialog.askdirectory(initialdir=str(Path(self.stt_model_var.get()) or Path.home()))
            if d:
                self.stt_model_var.set(d)
        ttk.Button(btn_frm, text="Browse", command=_browse_stt).grid(row=9, column=0, pady=(0,4))

        # Auto toggles
        self.auto_transcribe_var = tk.BooleanVar(value=getattr(self, 'auto_transcribe', True))
        self.auto_speak_var = tk.BooleanVar(value=getattr(self, 'auto_speak', True))
        ttk.Checkbutton(btn_frm, text="Auto Transcribe", variable=self.auto_transcribe_var).grid(row=3, column=0, sticky='w')
        ttk.Checkbutton(btn_frm, text="Auto Speak", variable=self.auto_speak_var).grid(row=4, column=0, sticky='w')

        # store refs on self for later use
        self._voice_btn_frame = btn_frm

        # status + re-check
        self.voice_status_label = ttk.Label(btn_frm, text="Voice: checking...")
        self.voice_status_label.grid(row=5, column=0, pady=(6, 0), sticky='w')
        self.voice_recheck_btn = ttk.Button(btn_frm, text="Re-check", command=self.check_voice_deps)
        self.voice_recheck_btn.grid(row=6, column=0, pady=(4, 0), sticky='w')

        # run dependency check to enable/disable voice features
        try:
            self.check_voice_deps()
        except Exception:
            logging.exception('Voice dependency check failed')

    def check_voice_deps(self) -> None:
        """Check if required voice/STT/TTS packages are importable and update UI accordingly."""
        miss = []
        for pkg in ('sounddevice','soundfile','numpy'):
            try:
                __import__(pkg)
            except Exception:
                miss.append(pkg)

        # faster-whisper used at transcribe time; pyttsx3 used at tts time
        try:
            __import__('faster_whisper')
        except Exception:
            miss.append('faster_whisper')
        try:
            __import__('pyttsx3')
        except Exception:
            miss.append('pyttsx3')

        if miss:
            self.q.put('Voice features disabled — missing: ' + ', '.join(miss))
            # disable buttons
            try:
                self.record_btn.config(state=tk.DISABLED)
                self.transcribe_btn.config(state=tk.DISABLED)
                self.speak_btn.config(state=tk.DISABLED)
            except Exception:
                pass
            self.voice_deps_ok = False
            try:
                if getattr(self, 'voice_status_label', None):
                    self.voice_status_label.config(text='Voice: missing: ' + ', '.join(miss))
            except Exception:
                pass
        else:
            self.voice_deps_ok = True
            try:
                if getattr(self, 'voice_status_label', None):
                    self.voice_status_label.config(text='Voice: available')
                # enable buttons
                self.record_btn.config(state=tk.NORMAL)
                self.transcribe_btn.config(state=tk.NORMAL)
                self.speak_btn.config(state=tk.NORMAL)
            except Exception:
                pass

    def _local_transcribe(self, model_size: str, input_path: str, output_path: str, device: str = "cpu") -> None:
        """Transcribe an audio file using faster-whisper (inlined helper).

        model_size may be a known identifier (tiny, base, small, medium, large)
        or it may be a local path to a model directory.
        """
        try:
            from faster_whisper import WhisperModel
        except Exception as e:
            raise RuntimeError("faster-whisper is not installed") from e

        model = WhisperModel(model_size, device=device)
        segments, info = model.transcribe(input_path, beam_size=5)

        text = ""
        for segment in segments:
            text += segment.text

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text.strip())

        self.q.put(f"Saved transcription to: {output_path}")

    def toggle_record(self):
        if not self.recording:
            try:
                import sounddevice as sd  # type: ignore
                import soundfile as sf  # type: ignore
            except Exception:
                messagebox.showerror("Missing dependency", "Recording requires 'sounddevice' and 'soundfile'.\nInstall with: pip install sounddevice soundfile")
                return

            self.recording = True
            self.record_btn.config(text="Stop")

            def record_thread():
                try:
                    samplerate = 44100
                    channels = 1
                    frames = []

                    def callback(indata, frames_count, time, status):
                        if status:
                            self.q.put(f"Record status: {status}")
                        frames.append(indata.copy())

                    with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback):
                        self.q.put("Recording... press Stop to finish")
                        while self.recording:
                            sd.sleep(100)

                    # write to wav
                    import numpy as np  # type: ignore
                    data = np.concatenate(frames, axis=0) if frames else np.zeros((0, channels))
                    sf.write(str(self.record_file), data, samplerate)
                    self.q.put(f"Saved recording to: {self.record_file}")
                    # auto-transcribe if enabled (use UI checkbox if present)
                    try:
                        auto = self.auto_transcribe_var.get() if getattr(self, 'auto_transcribe_var', None) is not None else getattr(self, 'auto_transcribe', False)
                    except Exception:
                        auto = getattr(self, 'auto_transcribe', False)
                    if auto:
                        # schedule a pre-transcribe notification on the main loop
                        self.root.after(100, lambda: self._notify_before_stt())
                except Exception as e:
                    self.q.put(f"Recording error: {e}")
                    self.q.put(traceback.format_exc())
                finally:
                    self.recording = False
                    self.root.after(0, lambda: self.record_btn.config(text="Record"))

            threading.Thread(target=record_thread, daemon=True).start()
        else:
            self.recording = False

    def transcribe_recording(self):
        if not self.record_file.exists():
            messagebox.showwarning("No recording", "No recording found. Please record audio first.")
            return

        # ensure faster-whisper is available (we use the inlined helper)
        try:
            __import__('faster_whisper')
        except Exception:
            messagebox.showerror("Missing dependency", "STT integration requires the 'faster-whisper' package.\nInstall with: pip install faster-whisper")
            return

        # Decide STT model to pass to faster-whisper: prefer explicit small/base/medium/large names
        # but allow a local path set in the STT Model field (self.stt_model_var).
        model_size = 'small'
        try:
            mv = self.stt_model_var.get() if getattr(self, 'stt_model_var', None) is not None else ''
            if not mv:
                mv = self.model_var.get() if getattr(self, 'model_var', None) is not None else ''
            mv_l = mv.split(':')[0].lower().strip() if mv else ''
            # common whisper model names
            if mv_l in ('tiny', 'tiny.en', 'base', 'small', 'medium', 'large'):
                model_size = mv_l
            else:
                # if the field is a local path to a model, use it
                from pathlib import Path as _P
                if mv and _P(mv).exists():
                    model_size = mv
        except Exception:
            pass

        self.transcribe_btn.config(state=tk.DISABLED)
        def tthread():
            try:
                # use the inlined faster-whisper helper
                self._local_transcribe(model_size, str(self.record_file), str(self.transcription_file))
                if self.transcription_file.exists():
                    txt = self.transcription_file.read_text(encoding='utf-8')
                    self.root.after(0, lambda: self.prompt.delete('1.0', tk.END))
                    self.root.after(0, lambda: self.prompt.insert(tk.END, txt))
                    self.q.put("Transcription inserted into Prompt.")
                else:
                    self.q.put("Transcription file not found after transcribe.")
            except Exception as e:
                self.q.put(f"Transcription failed: {e}")
                self.q.put(traceback.format_exc())
            finally:
                self.root.after(0, lambda: self.transcribe_btn.config(state=tk.NORMAL))

        threading.Thread(target=tthread, daemon=True).start()
    def _notify_before_stt(self):
        """Run on the main thread: inform the user that recording was saved before starting STT."""
        try:
            messagebox.showinfo("Recording saved", f"Saved recording to: {self.record_file}\nStarting transcription...")
        except Exception:
            pass
        try:
            auto = self.auto_transcribe_var.get() if getattr(self, 'auto_transcribe_var', None) is not None else getattr(self, 'auto_transcribe', False)
        except Exception:
            auto = getattr(self, 'auto_transcribe', False)
        if auto:
            # kick off transcription
            self.transcribe_recording()
        

    def speak_response(self):
        # speak currently selected/generated text
        text = self.output.get('1.0', tk.END).strip()
        if not text:
            messagebox.showwarning("No text", "No response text to speak.")
            return
        self._play_text(text)

    def _play_text(self, text: str) -> None:
        try:
            from agents.whisper import tts_pyttsx3 as tts_mod
            use_pyttsx3 = True
        except Exception:
            use_pyttsx3 = False

        out_wav = Path(tempfile.gettempdir()) / 'ollama_tts_out.wav'

        def tts_thread():
            try:
                if use_pyttsx3:
                    try:
                        tts_mod.synthesize(text, str(out_wav))
                        if sys.platform == 'darwin':
                            subprocess.run(['afplay', str(out_wav)])
                        else:
                            try:
                                from playsound import playsound  # type: ignore
                                playsound(str(out_wav))
                            except Exception:
                                self.q.put('TTS saved to ' + str(out_wav))
                    except Exception as e:
                        self.q.put(f"pyttsx3 error: {e}")
                        self.q.put(traceback.format_exc())
                else:
                    if sys.platform == 'darwin':
                        subprocess.run(['say', text])
                    else:
                        self.q.put('No TTS available; install pyttsx3 or use macOS say')
            except Exception as e:
                self.q.put(f"TTS error: {e}")

        threading.Thread(target=tts_thread, daemon=True).start()


def main():
    # configure logging to file so double-click launches can be diagnosed
    logging.basicConfig(
        filename='/tmp/ollama_gui_run.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
    )
    # also mirror to stdout when available
    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setLevel(logging.INFO)
    logging.getLogger().addHandler(sh)

    logging.info('Starting Ollama GUI...')
    try:
        root = tk.Tk()
        app = OllamaGUI(root)
        root.mainloop()
        logging.info('Ollama GUI exited.')
    except Exception:
        logging.exception('Unhandled exception in GUI')
        try:
            # attempt to show an error dialog (requires a Tk root)
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror('GUI Error', 'An unexpected error occurred. See /tmp/ollama_gui_run.log for details.')
        except Exception:
            pass


if __name__ == "__main__":
    main()
