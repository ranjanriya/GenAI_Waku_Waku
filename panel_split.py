from PIL import Image, ImageFilter
import numpy as np
import os
from scipy.signal import find_peaks

def detect_panel_boundaries(image_path, threshold_rel=0.3, min_panel_height=150):
    """
    Detects panel boundaries in a comic book page image.
    :param image_path: Path to the input image.
    :param threshold_rel: Relative threshold for peak detection.
    :param min_panel_height: Minimum height of panels to be detected.
    :return: List of y-coordinates where panels are detected.
    """
    image = Image.open(image_path).convert("L")  # Convert to grayscale
    edges = image.filter(ImageFilter.FIND_EDGES)  # Detect edges
    edge_array = np.array(edges)
    
    # Compute the sum of edge intensity along horizontal lines
    horizontal_intensity = np.sum(edge_array, axis=1)
    
    # Normalize intensity and apply relative thresholding
    threshold = threshold_rel * np.max(horizontal_intensity)
    peaks, _ = find_peaks(horizontal_intensity, height=threshold, distance=min_panel_height)
    
    return peaks.tolist()


def filter_panel(panel, white_threshold=0.9, dark_threshold=0.8):
    """
    Check if a panel is mostly white or dark.
    :param panel: The panel image.
    :param white_threshold: Threshold for white pixel ratio.
    :param dark_threshold: Threshold for dark pixel ratio.
    :return: True if the panel is mostly white or dark, False otherwise.
    """
    gray_panel = panel.convert("L")
    panel_array = np.array(gray_panel)
    
    # Compute white pixel ratio

    white_ratio = np.sum(panel_array > 240) / panel_array.size

    #compute dark pixel ratio
    dark_ratio = np.sum(panel_array < 100) / panel_array.size
    
    return white_ratio > white_threshold or dark_ratio > dark_threshold



def split_panels(image_path, output_folder, output_prefix="panel", min_panel_height=150):
    """
    Splits a comic book page image into panels based on detected boundaries.
    :param image_path: Path to the input image.
    :param output_folder: Folder to save the split panels.
    :param output_prefix: Prefix for the output panel filenames.
    :param min_panel_height: Minimum height of panels to be detected.
    :return: List of paths to the saved panel images.
    """
    image = Image.open(image_path)
    boundaries = detect_panel_boundaries(image_path, min_panel_height=min_panel_height)
    
    panels = []
    y_start = 0
    
    for y_end in boundaries + [image.height]:
        if y_end - y_start >= min_panel_height:  # Ensure minimum panel size
            panel = image.crop((0, y_start, image.width, y_end))
            if not filter_panel(panel):  # Filter out white or mostly text panels
                panels.append(panel)
            y_start = y_end
    
    os.makedirs(output_folder, exist_ok=True)
    panel_paths = []
    for idx, panel in enumerate(panels):
        panel_path = os.path.join(output_folder, f"{output_prefix}_{idx+1}.jpg")
        panel.save(panel_path)
        panel_paths.append(panel_path)
    
    return panel_paths

def process_folder(input_folder, output_folder, min_panel_height=150):
    """
    Processes all images in the input folder and splits them into panels.
    :param input_folder: Folder containing the input images.
    :param output_folder: Folder to save the split panels.
    :param min_panel_height: Minimum height of panels to be detected.
    """
    os.makedirs(output_folder, exist_ok=True)
    all_images = [f for f in os.listdir(input_folder) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
    
    for image_name in all_images:
        image_path = os.path.join(input_folder, image_name)
        image_output_folder = os.path.join(output_folder, os.path.splitext(image_name)[0])
        split_panels(image_path, image_output_folder, min_panel_height=min_panel_height)



input_folder = "your_input_folder"  # Replace with your input folder path
output_folder = "your_output_folder"  # Replace with your output folder path
process_folder(input_folder, output_folder)
