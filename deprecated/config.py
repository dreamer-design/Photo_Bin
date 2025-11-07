import os
import json

# =====================
# Configuration
# =====================
# Data/IO
ROOT_DIR = "./images_rembg"  # root of binned images
VALID_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp")

# Sorting
SORT_SUBJECTS = True
SORT_WITHIN_SUBJECT = True

# Processing parameters
GAUSSIAN_BLUR_KERNEL = (5, 5)       # must be odd numbers
CANNY_LOW = 0
CANNY_HIGH = 76
MORPH_KERNEL_SIZE = (3, 3)
MORPH_CLOSING_ITERATIONS = 2
MIN_COMPONENT_AREA = 700            # for single enclosed check

# Display options
DISPLAY_SUBJECT_INDEX = 0           # which subject to visualize
SHOW_WINDOWS = True                 # set False for headless mode

# Load config.json if present to override defaults
def Load_config():
    global ROOT_DIR, GAUSSIAN_BLUR_KERNEL, CANNY_LOW, CANNY_HIGH, MORPH_KERNEL_SIZE, MORPH_CLOSING_ITERATIONS, MIN_COMPONENT_AREA, DISPLAY_SUBJECT_INDEX, SHOW_WINDOWS
    CONFIG_PATH = "config.json"
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                _cfg = json.load(f)
            ROOT_DIR = _cfg.get("ROOT_DIR", ROOT_DIR)
            if "GAUSSIAN_BLUR_KERNEL" in _cfg:
                k = _cfg.get("GAUSSIAN_BLUR_KERNEL", GAUSSIAN_BLUR_KERNEL)
                GAUSSIAN_BLUR_KERNEL = (int(k[0]), int(k[1])) if isinstance(k, (list, tuple)) and len(k) == 2 else GAUSSIAN_BLUR_KERNEL
            CANNY_LOW = int(_cfg.get("CANNY_LOW", CANNY_LOW))
            CANNY_HIGH = int(_cfg.get("CANNY_HIGH", CANNY_HIGH))
            if "MORPH_KERNEL_SIZE" in _cfg:
                mk = _cfg.get("MORPH_KERNEL_SIZE", MORPH_KERNEL_SIZE)
                MORPH_KERNEL_SIZE = (int(mk[0]), int(mk[1])) if isinstance(mk, (list, tuple)) and len(mk) == 2 else MORPH_KERNEL_SIZE
            MORPH_CLOSING_ITERATIONS = int(_cfg.get("MORPH_CLOSING_ITERATIONS", MORPH_CLOSING_ITERATIONS))
        except Exception:
            pass

def save_config(config_path: str, img_shape, min_area_pct: int):
    h, w = img_shape[:2]
    data = {
        "ROOT_DIR": ROOT_DIR,
        "GAUSSIAN_BLUR_KERNEL": list(GAUSSIAN_BLUR_KERNEL),
        "CANNY_LOW": int(CANNY_LOW),
        "CANNY_HIGH": int(CANNY_HIGH),
        "MORPH_KERNEL_SIZE": list(MORPH_KERNEL_SIZE),
        "MORPH_CLOSING_ITERATIONS": int(MORPH_CLOSING_ITERATIONS),
    }
    with open(config_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved parameters to {config_path}")