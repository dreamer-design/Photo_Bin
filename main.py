import cv2 as cv
import os
import re
import numpy as np

# Data/IO
ROOT_DIR = "./images_rembg"  # root of binned images
VALID_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp")

# Sorting
SORT_SUBJECTS = True
SORT_WITHIN_SUBJECT = True

# Display options
DISPLAY_SUBJECT_INDEX = 0           # which subject to visualize
SHOW_WINDOWS = True                 # set False for headless mode

def load_files():
    # Root of binned images: images_binned/<subject>/<files>
    root_dir = ROOT_DIR
    valid_exts = VALID_EXTS
    number_suffix_re = re.compile(r".*\((\d+)\)$") # Helper for sort trail (12)

    def natural_key(filename_base: str):
        m = number_suffix_re.match(filename_base)
        return int(m.group(1)) if m else 0

    if not os.path.isdir(root_dir):
        raise FileNotFoundError(f"'{root_dir}' not found. Run the binning step first.")

    # Collect subjects (subdirectories)
    subjects = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
    if SORT_SUBJECTS:
        subjects.sort()

    # 2D list of image paths per subject
    paths_2d = []
    for subject in subjects:
        subject_dir = os.path.join(root_dir, subject)
        files = [f for f in os.listdir(subject_dir) if os.path.splitext(f)[1].lower() in valid_exts]
        # Sort within subject by numeric suffix if present
        if SORT_WITHIN_SUBJECT:
            files.sort(key=lambda f: natural_key(os.path.splitext(os.path.basename(f))[0]))
        subject_paths = [os.path.join(subject_dir, f) for f in files]
        if subject_paths:
            paths_2d.append(subject_paths)

    # Load images into a 2D list parallel to paths_2d
    images_2d = []
    for subject_paths in paths_2d:
        subject_images = []
        for p in subject_paths:
            img = cv.imread(p)
            if img is None:
                continue
            subject_images.append(img)
        if subject_images:
            images_2d.append(subject_images)
    
    return images_2d

# img is an ndarray
def quick_fill(img):
    # For each pixel in img that is not 0, set it to 255
    # print(img.shape)
    mask = (img != 0).any(axis=2)
    img[mask] = [255, 255, 255]
    return img

def check_fully_enclosed(filled):
    height = filled.shape[0]  # rows = 683
    width = filled.shape[1]   # cols = 1024

    print(height, width)

    # Vectorized boundary checks across all channels
    top_has_nonzero = np.any(filled[0, :, :] != 0)
    bottom_has_nonzero = np.any(filled[height - 1, :, :] != 0)
    left_has_nonzero = np.any(filled[:, 0, :] != 0)
    right_has_nonzero = np.any(filled[:, width - 1, :] != 0)

    return not (top_has_nonzero or bottom_has_nonzero or left_has_nonzero or right_has_nonzero)

def main():    
    # Load overrides from config.json if present
    images_2d = load_files()

    # clamp index within range
    subject_index = max(0, min(DISPLAY_SUBJECT_INDEX, len(images_2d) - 1))
     # retrieve list of subject images and sets 
    current_subject_images = images_2d[subject_index] if images_2d and images_2d[subject_index] else []
   # set initial image
    current_idx = 0
    current_img = current_subject_images[current_idx] if current_subject_images else None

    print(f"Loaded {sum(len(row) for row in images_2d)} images across {len(images_2d)} subjects.")
    print(len(images_2d[0]))

    # Run Once
    qf = quick_fill(current_img) # alt process image
    cv.imshow("Filled", qf )

    cv.moveWindow("Filled", 700, 0)

    while True:
        key = cv.waitKey(30) & 0xFF
        if key == 32:  # space -> next image in subject
            if current_subject_images:
                current_idx = (current_idx + 1) % len(current_subject_images)
                current_img = current_subject_images[current_idx]
                qf = quick_fill(current_img)
                cv.imshow("Filled", qf )
            continue        
        if key in (ord('c'), ord('C')):  #  check
            print("Fully enclosed: ", check_fully_enclosed(qf) )
            continue        
        if key in (ord('o'), ord('O')):  # place holder for next thing i need
            
            continue
        if key in (27, ord('q')):  # ESC or q to quit
            break

    cv.destroyAllWindows()

if __name__ == "__main__":
    main()