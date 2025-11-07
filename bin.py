import cv2 as cv
import os
import re
import shutil

# Directories
input_dir = "./images_resized"
output_root = "./images_binned"
os.makedirs(output_root, exist_ok=True)

# Supported extensions (case-insensitive)
valid_exts = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp")

# Regex to capture subject before trailing numeric parentheses, e.g., "subject name (12)"
subject_pattern = re.compile(r"^(?P<subject>.*?)[\s_]*\(\d+\)$")

processed = 0
skipped = 0

for fname in sorted(os.listdir(input_dir)):
    in_path = os.path.join(input_dir, fname)
    if not os.path.isfile(in_path):
        continue

    name, ext = os.path.splitext(fname)
    if ext.lower() not in valid_exts:
        skipped += 1
        continue

    match = subject_pattern.match(name)
    if match:
        subject = match.group("subject").strip()
    else:
        # If no numeric suffix, use the full base name as the subject
        subject = name.strip()

    # Normalize empty subject just in case
    if not subject:
        subject = "unknown_subject"

    out_dir = os.path.join(output_root, subject)
    os.makedirs(out_dir, exist_ok=True)

    out_path = os.path.join(out_dir, fname)
    shutil.copy2(in_path, out_path)
    processed += 1

print(f"Binned {processed} images into '{output_root}'. Skipped {skipped} files.")
