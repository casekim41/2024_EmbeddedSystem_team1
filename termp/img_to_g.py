import argparse
import numpy as np
from PIL import Image
import cv2
from scipy.spatial import distance

def optimize_contour_order(contours):
    """Reorder contours to minimize pen movement using nearest-neighbor traversal."""
    reordered_contours = []
    current_position = (0, 0)  # Start at the origin
    remaining_contours = contours.copy()

    while remaining_contours:
        # Find the nearest contour
        nearest_contour_idx = min(
            range(len(remaining_contours)),
            key=lambda i: distance.euclidean(current_position, remaining_contours[i][0][0])
        )
        nearest_contour = remaining_contours.pop(nearest_contour_idx)
        reordered_contours.append(nearest_contour)

        # Update current position to the end of the selected contour
        current_position = nearest_contour[-1][0]

    return reordered_contours

def convert_to_gcode(image, output_file, scale=1.0):
    """Converts the edge image directly to G-code, following optimized contour order."""
    height, width = image.shape
    print(f"Image dimensions: {width}x{height}")

    # Find contours in the binary edge image
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Optimize contour traversal order
    contours = optimize_contour_order(contours)

    with open(output_file, 'w') as f:
        f.write("G21 ; Set units to millimeters\n")
        f.write("G90 ; Absolute positioning\n")
        f.write("M3 S255 ; Pen down\n")

        for contour in contours:
            # Move to the starting point of the contour
            start_x, start_y = contour[0][0]
            scaled_start_x = start_x * scale
            scaled_start_y = start_y * scale
            f.write(f"G0 X{scaled_start_x:.3f} Y{scaled_start_y:.3f}\n")  # Move pen without drawing

            # Follow the contour points
            f.write("G1 ; Start drawing\n")
            for point in contour:
                x, y = point[0]
                scaled_x = x * scale
                scaled_y = y * scale
                f.write(f"G1 X{scaled_x:.3f} Y{scaled_y:.3f}\n")

        f.write("M3 S0 ; Pen up\n")
        f.write("G0 X0 Y0 ; Return to origin\n")

    print(f"G-code saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Convert edge image to G-code.")
    parser.add_argument("input_image", help="Path to the edge image (input)")
    parser.add_argument("output_gcode", help="Path to the G-code file (output)")
    parser.add_argument("--scale", type=float, default=1.0, help="Scale for the G-code coordinates")
    args = parser.parse_args()

    # Open the input image
    image = Image.open(args.input_image).convert('L')  # Convert to grayscale
    image_array = np.array(image)

    # Threshold the image to binary (edge detection produces binary images)
    _, binary_image = cv2.threshold(image_array, 127, 255, cv2.THRESH_BINARY)

    # Convert the edge image directly to G-code
    convert_to_gcode(binary_image, args.output_gcode, scale=args.scale)

if __name__ == "__main__":
    main()

