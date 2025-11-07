import cv2 as cv
import os

# Directories
input_dir = "./images"
output_dir = "./images_resized"
os.makedirs(output_dir, exist_ok=True)

# Resize settings
max_dim = 1024  # adjust to 640–1200 depending on your feature detector
valid_exts = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp", ".JPG", ".JPEG", ".PNG", ".BMP", ".TIF", ".TIFF", ".WEBP"}

processed = 0
skipped = 0

for name in sorted(os.listdir(input_dir)):
    in_path = os.path.join(input_dir, name)
    if not os.path.isfile(in_path):
        continue
    base, ext = os.path.splitext(name)
    if ext not in valid_exts:
        skipped += 1
        continue

    img = cv.imread(in_path)
    if img is None:
        skipped += 1
        continue

    h, w = img.shape[:2]
    scale = min(max_dim / max(h, w), 1.0)
    new_w, new_h = int(round(w * scale)), int(round(h * scale))
    resized = cv.resize(img, (new_w, new_h), interpolation=cv.INTER_AREA)

    out_path = os.path.join(output_dir, f"{base}{ext.lower()}")
    cv.imwrite(out_path, resized)
    processed += 1

print(f"Saved {processed} resized images to {output_dir}. Skipped {skipped} files.")