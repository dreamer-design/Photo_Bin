# def check_continuous(outline_mask):
#     # Determine if the outline forms at least one enclosed region; also return interior mask
#     if outline_mask is None or outline_mask.size == 0:
#         return False, None
#     # Ensure binary 0/255 uint8
#     outline = (outline_mask > 0).astype("uint8") * 255
#     h, w = outline.shape[:2]
#     # Prepare background where outline acts as a barrier
#     background = np.where(outline > 0, 0, 255).astype("uint8")
#     # Flood fill from the border; use mask with 2-pixel padding as required by OpenCV
#     flood_mask = np.zeros((h + 2, w + 2), dtype="uint8")
#     cv.floodFill(background, flood_mask, (0, 0), 128)
#     # Pixels that remain 255 are enclosed (not reachable from the border)
#     interior_mask = (background == 255).astype("uint8") * 255
#     enclosed_exists = np.any(interior_mask == 255)
#     return bool(enclosed_exists), interior_mask

# def check_single_enclosed(filled_mask, min_area: int = MIN_COMPONENT_AREA):
#     # True if there is exactly one connected component in the filled mask
#     if filled_mask is None or filled_mask.size == 0:
#         return False
#     _, binary = cv.threshold(filled_mask, 127, 255, cv.THRESH_BINARY)
#     num_labels, labels = cv.connectedComponents(binary)
#     if num_labels <= 1: 
#         return False
#     # Count components with area >= min_area
#     counts = []
#     for label in range(1, num_labels):
#         area = int(np.sum(labels == label))
#         if area >= min_area:
#             counts.append(area)
#     return len(counts) == 1


# # Update parameters
# CANNY_LOW = int(low)
# CANNY_HIGH = int(high)
# GAUSSIAN_BLUR_KERNEL = (int(blur_k), int(blur_k))
# MORPH_KERNEL_SIZE = (int(morph_k), int(morph_k))
# MORPH_CLOSING_ITERATIONS = int(morph_iters)    