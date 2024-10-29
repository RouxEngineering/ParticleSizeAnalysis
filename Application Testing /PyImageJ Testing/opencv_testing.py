import cv2

# read file image
image = cv2.imread("/Users/sarah/Documents/areospace research/material recycling project/PyImageJ-Particle-Analysis/Particle Images/Ti64_Lot232-EZ2316_1Use_10X_Scale.png")

#  open gui and allow user to select area
r = cv2.selectROI("Select the area", image, showCrosshair=True, fromCenter=False)

# close window 
cv2.destroyWindow("Select the area")

# cheeck for region of interest selection
if r != (0, 0, 0, 0):
    # get roi dimesion
    x, y, w, h = r

    # measure length in pixels
    width_in_pixels = w
    height_in_pixels = h

    print(f"Width: {width_in_pixels} pixels")


else:
    print("No ROI selected.")
