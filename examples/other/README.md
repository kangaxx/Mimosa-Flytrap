# Other AI Agent Examples

Examples for various AI agents beyond the main categories.

## Audio Processing Examples

### 1. Speech-to-Text

```python
from agents.other.audio.transcriber import AudioTranscriber

transcriber = AudioTranscriber(model="whisper-large-v3")

# Transcribe audio file
result = transcriber.transcribe(
    audio_path="audio/meeting.mp3",
    language="en",
    timestamps=True
)

print(f"Transcript:\n{result['text']}\n")

# Print with timestamps
for segment in result['segments']:
    print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s]: {segment['text']}")
```

### 2. Text-to-Speech

```python
from agents.other.audio.synthesizer import TextToSpeech

tts = TextToSpeech(model="elevenlabs")

# Generate speech
audio = tts.synthesize(
    text="Hello, this is a demonstration of text to speech.",
    voice="professional_male",
    language="en-US"
)

audio.save("output/speech.mp3")
```

## Video Processing Examples

### 3. Video Summarization

```python
from agents.other.video.summarizer import VideoSummarizer

summarizer = VideoSummarizer()

# Summarize video
summary = summarizer.summarize(
    video_path="videos/lecture.mp4",
    max_clips=5,
    clip_duration=30
)

# Save summary video
summary.save("output/lecture_summary.mp4")

# Generate text summary
text_summary = summary.get_text_summary()
print(text_summary)
```

### 4. Action Recognition

```python
from agents.other.video.action_recognizer import ActionRecognizer

recognizer = ActionRecognizer()

# Detect actions in video
actions = recognizer.recognize(
    video_path="videos/sports.mp4",
    top_k=3
)

for timestamp, detected_actions in actions.items():
    print(f"\nAt {timestamp}:")
    for action in detected_actions:
        print(f"  - {action['name']}: {action['confidence']:.2%}")
```

## Data Analysis Examples

### 5. Data Visualization

```python
from agents.other.data_analysis.visualizer import DataVisualizer

visualizer = DataVisualizer()

# Load data
data = visualizer.load_data("data/sales.csv")

# Generate visualizations
charts = visualizer.create_dashboard(
    data=data,
    charts=[
        {"type": "line", "x": "date", "y": "revenue"},
        {"type": "bar", "x": "product", "y": "sales"},
        {"type": "pie", "values": "category_distribution"}
    ]
)

# Save as HTML dashboard
charts.save("output/dashboard.html")
```

### 6. Anomaly Detection

```python
from agents.other.data_analysis.anomaly_detector import AnomalyDetector

detector = AnomalyDetector()

# Detect anomalies in time series
anomalies = detector.detect(
    data="data/metrics.csv",
    column="value",
    method="isolation_forest",
    sensitivity=0.8
)

print(f"Found {len(anomalies)} anomalies:")
for anomaly in anomalies:
    print(f"  - {anomaly['timestamp']}: {anomaly['value']} (score: {anomaly['score']})")
```

## Web Automation Examples

### 7. Web Scraping

```python
from agents.other.web.scraper import WebScraper

scraper = WebScraper()

# Scrape website
data = scraper.scrape(
    url="https://example.com/products",
    selectors={
        "title": ".product-title",
        "price": ".product-price",
        "description": ".product-desc"
    }
)

# Save to JSON
scraper.save_json(data, "output/products.json")
```

### 8. Browser Automation

```python
from agents.other.web.automator import BrowserAutomator

automator = BrowserAutomator()

# Automate form submission
automator.navigate("https://example.com/form")
automator.fill_field("name", "John Doe")
automator.fill_field("email", "john@example.com")
automator.click_button("Submit")

# Take screenshot
automator.screenshot("output/confirmation.png")
```

## Conversational AI Examples

### 9. Chatbot

```python
from agents.other.conversational.chatbot import Chatbot

bot = Chatbot(
    model="gpt-4",
    personality="helpful and friendly",
    memory_enabled=True
)

# Interactive conversation
bot.start_conversation()

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    
    response = bot.respond(user_input)
    print(f"Bot: {response}")

# Save conversation history
bot.save_history("output/conversation.json")
```

### 10. Virtual Assistant

```python
from agents.other.conversational.assistant import VirtualAssistant

assistant = VirtualAssistant()

# Execute commands
commands = [
    "Schedule a meeting for tomorrow at 2 PM",
    "Send an email to john@example.com",
    "What's the weather like today?"
]

for command in commands:
    result = assistant.execute(command)
    print(f"Command: {command}")
    print(f"Result: {result}\n")
```

## Workflow Automation Examples

### 11. Task Scheduler

```python
from agents.other.workflow.scheduler import TaskScheduler

scheduler = TaskScheduler()

# Schedule tasks
scheduler.schedule_task(
    name="daily_backup",
    function=backup_database,
    trigger="cron",
    hour=2,
    minute=0
)

scheduler.schedule_task(
    name="generate_report",
    function=generate_weekly_report,
    trigger="interval",
    days=7
)

# Start scheduler
scheduler.start()
```

### 12. Process Orchestration

```python
from agents.other.workflow.orchestrator import ProcessOrchestrator

orchestrator = ProcessOrchestrator()

# Define workflow
workflow = orchestrator.create_workflow("data_pipeline")

workflow.add_step("extract", extract_data, {"source": "api"})
workflow.add_step("transform", transform_data, depends_on="extract")
workflow.add_step("validate", validate_data, depends_on="transform")
workflow.add_step("load", load_to_database, depends_on="validate")

# Execute workflow
result = workflow.execute()
print(f"Workflow status: {result['status']}")
```

## Email Processing Examples

### 13. Email Automation

```python
from agents.other.email.processor import EmailProcessor

processor = EmailProcessor()

# Process incoming emails
processor.connect(
    imap_server="imap.gmail.com",
    email="your@email.com",
    password="your_password"
)

# Auto-categorize emails
emails = processor.fetch_unread()
for email in emails:
    category = processor.categorize(email)
    processor.apply_label(email, category)
    
    # Auto-respond if needed
    if category == "support":
        processor.auto_respond(email, template="support_response")
```

## Security Examples

### 14. Content Filtering

```python
from agents.other.security.content_filter import ContentFilter

filter = ContentFilter()

# Check content safety
text = "Some user-generated content"
result = filter.check_text(text)

if result['is_safe']:
    print("Content is safe")
else:
    print(f"Content flagged: {result['categories']}")
    print(f"Severity: {result['severity']}")
```

### 15. Privacy Protection

```python
from agents.other.security.privacy import PrivacyProtector

protector = PrivacyProtector()

# Anonymize sensitive data
data = """
Contact John Smith at john.smith@company.com 
or call 555-123-4567. 
Credit card: 4532-1234-5678-9012
"""

anonymized = protector.anonymize(
    text=data,
    entities=["email", "phone", "credit_card", "person"]
)

print(anonymized)
```

**Output:**
```
Contact [PERSON_1] at [EMAIL_1]
or call [PHONE_1].
Credit card: [CREDIT_CARD_1]
```

## Running Examples

```bash
# Install dependencies
pip install -r agents/other/requirements.txt

# Run audio example
python examples/other/audio/transcribe.py \
  --input audio.mp3 \
  --model whisper-large

# Run video example
python examples/other/video/summarize.py \
  --input video.mp4 \
  --output summary.mp4

# Run automation
python examples/other/automation/scraper.py \
  --url https://example.com \
  --output data.json
```

## Integration Examples

### 16. Multi-Agent System

```python
from agents.other.orchestrator import MultiAgentSystem

system = MultiAgentSystem()

# Register agents
system.register("transcriber", AudioTranscriber())
system.register("summarizer", TextSummarizer())
system.register("translator", TextTranslator())

# Create pipeline
pipeline = system.create_pipeline([
    ("transcriber", {"audio": "meeting.mp3"}),
    ("summarizer", {"text": "{{transcriber.output}}"}),
    ("translator", {"text": "{{summarizer.output}}", "target": "es"})
])

# Execute
result = pipeline.execute()
print(result['translator']['output'])
```

## Configuration

Configuration files in `docs/configuration/other/`.

## Next Steps

- Explore agent combinations
- Build custom workflows
- Integrate with existing systems
- Scale for production use
