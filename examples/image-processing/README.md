# Image Processing Examples

Practical examples for image processing agents.

## Basic Examples

### 1. Image Generation from Text

```python
from agents.image_processing.generator import ImageGenerator

# Initialize generator
generator = ImageGenerator(model="stable-diffusion-xl")

# Generate image
image = generator.generate(
    prompt="A serene mountain landscape at sunset, photorealistic",
    negative_prompt="blurry, low quality, distorted",
    width=1024,
    height=768,
    steps=50,
    guidance_scale=7.5
)

# Save image
image.save("output/landscape.png")
```

### 2. Object Detection

```python
from agents.image_processing.detector import ObjectDetector

detector = ObjectDetector(model="yolov8")

# Detect objects
detections = detector.detect(
    image_path="images/street.jpg",
    confidence_threshold=0.5
)

# Print results
for detection in detections:
    print(f"{detection['class']}: {detection['confidence']:.2%}")
    print(f"  Location: {detection['bbox']}")

# Save annotated image
detector.save_annotated("images/street_annotated.jpg")
```

**Output:**
```
car: 98.5%
  Location: [120, 200, 350, 450]
person: 95.2%
  Location: [450, 100, 550, 400]
traffic_light: 87.3%
  Location: [600, 50, 650, 150]
```

### 3. Background Removal

```python
from agents.image_processing.background_remover import BackgroundRemover

remover = BackgroundRemover()

# Remove background
result = remover.remove_background(
    input_path="images/product.jpg",
    output_path="images/product_nobg.png"
)

print(f"Background removed successfully")
print(f"Processing time: {result['processing_time']:.2f}s")
```

### 4. Image Enhancement

```python
from agents.image_processing.enhancer import ImageEnhancer

enhancer = ImageEnhancer()

# Enhance image
enhanced = enhancer.enhance(
    image_path="images/old_photo.jpg",
    operations=[
        "denoise",
        "sharpen",
        "color_correction",
        "upscale_2x"
    ]
)

enhanced.save("images/old_photo_enhanced.jpg")
```

## Advanced Examples

### 5. Style Transfer

```python
from agents.image_processing.style_transfer import StyleTransfer

transfer = StyleTransfer()

# Apply artistic style
stylized = transfer.apply_style(
    content_image="images/photo.jpg",
    style_image="images/van_gogh.jpg",
    strength=0.8
)

stylized.save("images/photo_stylized.jpg")
```

### 6. Image Segmentation

```python
from agents.image_processing.segmenter import ImageSegmenter

segmenter = ImageSegmenter(model="segment-anything")

# Segment image
segments = segmenter.segment(
    image_path="images/scene.jpg",
    mode="automatic"
)

# Save each segment
for i, segment in enumerate(segments):
    segment.save(f"output/segment_{i}.png")

# Or segment specific object
mask = segmenter.segment_by_prompt(
    image_path="images/scene.jpg",
    prompt="the red car"
)
mask.save("output/car_mask.png")
```

### 7. Image Inpainting

```python
from agents.image_processing.inpainter import ImageInpainter

inpainter = ImageInpainter()

# Remove unwanted objects
result = inpainter.inpaint(
    image_path="images/photo.jpg",
    mask_path="images/mask.png",
    prompt="clear sky background"
)

result.save("images/photo_inpainted.jpg")
```

### 8. Batch Processing

```python
from agents.image_processing.batch_processor import BatchProcessor
import glob

processor = BatchProcessor()

# Process all images in directory
images = glob.glob("input/*.jpg")

results = processor.process_batch(
    images=images,
    operations=[
        {"type": "resize", "width": 800, "height": 600},
        {"type": "enhance", "auto": True},
        {"type": "watermark", "text": "© 2024", "position": "bottom-right"}
    ],
    output_dir="output/",
    parallel=True,
    max_workers=4
)

print(f"Processed {len(results)} images")
```

## AI-Powered Examples

### 9. Image Captioning

```python
from agents.image_processing.captioner import ImageCaptioner

captioner = ImageCaptioner(model="blip-2")

# Generate caption
caption = captioner.generate_caption(
    image_path="images/photo.jpg",
    max_length=50
)

print(f"Caption: {caption}")

# Generate detailed description
description = captioner.describe(
    image_path="images/photo.jpg",
    detail_level="high"
)

print(f"Description: {description}")
```

### 10. Visual Question Answering

```python
from agents.image_processing.vqa import VisualQuestionAnswering

vqa = VisualQuestionAnswering()

# Ask questions about image
answers = vqa.ask(
    image_path="images/scene.jpg",
    questions=[
        "How many people are in the image?",
        "What is the weather like?",
        "What colors are prominent?"
    ]
)

for question, answer in answers.items():
    print(f"Q: {question}")
    print(f"A: {answer}\n")
```

### 11. Image-to-Image Translation

```python
from agents.image_processing.translator import ImageTranslator

translator = ImageTranslator()

# Transform image
result = translator.translate(
    image_path="images/daytime.jpg",
    transformation="day_to_night",
    strength=0.7
)

result.save("images/nighttime.jpg")

# Or custom transformation
result = translator.translate_with_prompt(
    image_path="images/photo.jpg",
    prompt="transform to watercolor painting style"
)
```

## OCR Examples

### 12. Text Extraction from Images

```python
from agents.image_processing.ocr import ImageOCR

ocr = ImageOCR(engine="paddleocr")

# Extract text
text = ocr.extract_text(
    image_path="images/document.jpg",
    languages=["en", "zh"]
)

print(f"Extracted text:\n{text}")

# Extract with positions
result = ocr.extract_with_positions(
    image_path="images/document.jpg"
)

for block in result['blocks']:
    print(f"Text: {block['text']}")
    print(f"Position: {block['bbox']}")
    print(f"Confidence: {block['confidence']:.2%}\n")
```

## Integration Examples

### 13. Image Processing Pipeline

```python
from agents.image_processing.pipeline import ImagePipeline

# Create processing pipeline
pipeline = ImagePipeline([
    ("load", {}),
    ("detect_faces", {"draw_boxes": True}),
    ("blur_faces", {"intensity": 20}),
    ("resize", {"width": 1200, "maintain_aspect": True}),
    ("compress", {"quality": 85}),
    ("save", {"format": "jpg"})
])

# Process image
result = pipeline.process("input/group_photo.jpg", "output/anonymous.jpg")
print(f"Pipeline completed in {result['time']:.2f}s")
```

### 14. Real-time Processing

```python
from agents.image_processing.realtime import RealtimeProcessor

processor = RealtimeProcessor()

# Process video stream
processor.process_stream(
    source=0,  # Webcam
    operations=["face_detection", "emotion_recognition"],
    display=True,
    fps=30
)

# Or process video file
processor.process_video(
    input_path="video.mp4",
    output_path="video_processed.mp4",
    operations=["object_detection", "tracking"]
)
```

## Running Examples

```bash
# Install dependencies
pip install -r agents/image-processing/requirements.txt

# For GPU support
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Run example
python examples/image-processing/01_image_generation.py

# Run with custom model
python examples/image-processing/generate.py \
  --prompt "mountain landscape" \
  --model sdxl \
  --steps 50

# Batch process images
python examples/image-processing/batch_process.py \
  --input images/ \
  --output processed/ \
  --operation enhance
```

## Sample Images

Test images available in `examples/image-processing/samples/`:
- Various resolutions and formats
- Sample masks for inpainting
- Reference style images
- Test documents for OCR

## Configuration

Configuration examples in `docs/configuration/image-processing/`.

## Performance Tips

- Use GPU for faster processing
- Enable batch processing for multiple images
- Adjust quality settings based on needs
- Cache models to avoid reloading
- Use quantization for lower memory usage

## Next Steps

- Experiment with different models
- Try combining multiple operations
- Explore style transfer variations
- Build custom processing workflows
