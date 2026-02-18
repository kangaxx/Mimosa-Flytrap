#!/usr/bin/env python3
from pathlib import Path
import tempfile
import sys

rec = Path(tempfile.gettempdir()) / 'ollama_record.wav'
out = Path(tempfile.gettempdir()) / 'ollama_transcription.txt'
print('record:', rec)
print('out:', out)

if not rec.exists():
    print('Record file not found', file=sys.stderr)
    sys.exit(2)

try:
    from agents.whisper import stt_faster_whisper as stt_mod
except Exception as e:
    print('Cannot import stt module:', e, file=sys.stderr)
    sys.exit(3)

try:
    print('Starting transcribe...')
    stt_mod.transcribe('small', str(rec), str(out), device='cpu')
    print('Transcribe finished')
    if out.exists():
        print('--- transcription content ---')
        print(out.read_text(encoding='utf-8'))
    else:
        print('Transcription file not created', file=sys.stderr)
        sys.exit(4)
except Exception as e:
    print('Transcription error:', e, file=sys.stderr)
    raise
