import os
from rembg import remove
from PIL import Image

INPUT_ROOT = "./images_binned"
OUTPUT_ROOT = "./images_rembg"
VALID_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp")

os.makedirs(OUTPUT_ROOT, exist_ok=True)

def process_image_file(in_path: str, out_path: str):
    img = Image.open(in_path)
    out = remove(img)
    out.save(out_path)

processed = 0
skipped = 0

for subject in sorted(os.listdir(INPUT_ROOT)):
    subject_in_dir = os.path.join(INPUT_ROOT, subject)
    if not os.path.isdir(subject_in_dir):
        continue
    subject_out_dir = os.path.join(OUTPUT_ROOT, subject)
    os.makedirs(subject_out_dir, exist_ok=True)

    for name in sorted(os.listdir(subject_in_dir)):
        base, ext = os.path.splitext(name)
        if ext.lower() not in VALID_EXTS:
            skipped += 1
            continue
        in_path = os.path.join(subject_in_dir, name)
        out_path = os.path.join(subject_out_dir, base + ".png")  # preserve alpha; save as PNG
        if os.path.exists(out_path):
            continue
        try:
            process_image_file(in_path, out_path)
            processed += 1
        except Exception:
            skipped += 1

print(f"Saved {processed} background-removed images to '{OUTPUT_ROOT}'. Skipped {skipped} files.")


