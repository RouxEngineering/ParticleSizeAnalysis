import cv2

# Read image
image = cv2.imread("/Users/sarah/Documents/areospace research/material recycling project/PyImageJ-Particle-Analysis/Particle Images/Ti64_Lot232-EZ2316_1Use_10X_Scale.png")

# Display image and select ROI
r = cv2.selectROI("Select the area", image, showCrosshair=True, fromCenter=False)

# Close the window after ROI selection
cv2.destroyWindow("Select the area")

# Check if ROI was selected
if r != (0, 0, 0, 0):
    # Get ROI coordinates and dimensions
    x, y, w, h = r

    # Measure length in pixels
    width_in_pixels = w
    height_in_pixels = h

    print(f"Width: {width_in_pixels} pixels")
    print(f"Height: {height_in_pixels} pixels")

    # Optionally, display the selected ROI
    roi = image[y:y+h, x:x+w]

    # Display the ROI using OpenCV
    cv2.imshow("ROI", roi)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No ROI selected.")
