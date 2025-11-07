import os
import re
from typing import List
from PIL import Image

INPUT_ROOT = "./images_rembg"
OUTPUT_ROOT = "./gifs"
VALID_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp")

# GIF options
FPS = 6                   # frames per second
DURATION_MS = int(1000 / FPS)
LOOP = 0                  # 0 = infinite loop

os.makedirs(OUTPUT_ROOT, exist_ok=True)

number_suffix_re = re.compile(r".*\((\d+)\)$")

def natural_key(filename_base: str) -> int:
    m = number_suffix_re.match(filename_base)
    return int(m.group(1)) if m else 0

def list_subjects(root: str) -> List[str]:
    return sorted([d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))])

def load_subject_frames(subject_dir: str) -> List[Image.Image]:
    files = [f for f in os.listdir(subject_dir) if os.path.splitext(f)[1].lower() in VALID_EXTS]
    files.sort(key=lambda f: natural_key(os.path.splitext(os.path.basename(f))[0]))
    frames: List[Image.Image] = []
    for name in files:
        path = os.path.join(subject_dir, name)
        try:
            img = Image.open(path)
            # Composite alpha onto white so transparent bg becomes white, then convert to RGB
            if img.mode in ("RGBA", "LA") or ("A" in img.getbands()):
                bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
                composed = Image.alpha_composite(bg, img.convert("RGBA")).convert("RGB")
                frames.append(composed)
            else:
                frames.append(img.convert("RGB"))
        except Exception:
            continue
    return frames

def normalize_sizes(frames: List[Image.Image]) -> List[Image.Image]:
    if not frames:
        return frames
    base_size = frames[0].size
    if all(f.size == base_size for f in frames):
        return frames
    resized = [f.resize(base_size, Image.LANCZOS) for f in frames]
    return resized

processed = 0
skipped = 0

for subject in list_subjects(INPUT_ROOT):
    subject_dir = os.path.join(INPUT_ROOT, subject)
    out_path = os.path.join(OUTPUT_ROOT, f"{subject}.gif")
    frames = load_subject_frames(subject_dir)
    if len(frames) < 2:
        skipped += 1
        continue
    frames = normalize_sizes(frames)
    try:
        frames[0].save(
            out_path,
            save_all=True,
            append_images=frames[1:],
            duration=DURATION_MS,
            loop=LOOP,
            optimize=False,
            disposal=2,
        )
        processed += 1
    except Exception:
        skipped += 1

print(f"Created {processed} GIFs in '{OUTPUT_ROOT}'. Skipped {skipped} subjects.")


