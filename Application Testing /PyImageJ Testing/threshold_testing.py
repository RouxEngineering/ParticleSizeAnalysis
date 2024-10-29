import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# initialize path to image
path = '/Users/sarah/Documents/areospace research/material recycling project/PyImageJ-Particle-Analysis/Particle Images/Ti64_Lot232-EZ2316_1Use_10X_Scale.png'
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # read image in grayscale 

# create plot for threshold and display image
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
image_display = ax.imshow(img, cmap='binary')
ax.set_title("Interactive Threshold")

# create slider 
slider_axes = fig.add_axes([0.25, 0.1, 0.65, 0.03])
slider = Slider(slider_axes,
    label='Threshold Value', 
    valmin = 1,
    valmax=255, 
    orientation='horizontal', 
    valstep=1
)


# create function to update based on threshold value 
def update(val):
    threshold_value = slider.val
    ret, thresh1 = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY)
    image_display.set_data(thresh1)
    ax.set_title(f"Interactive Threshold - Value: {threshold_value}")


slider.on_changed(update)

plt.show()