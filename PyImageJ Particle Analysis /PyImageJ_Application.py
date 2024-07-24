'''
PyImageJ Functions to Create Particle CSV file data 
'''
from Macro_class import MacroFunctions
import cv2 
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

class PyImageJAPI:
    def __init__(self, image_path):
        self.image_path = image_path

    def get_scale(MacroFunctions): 
        '''function to open OpenCV GUI to allow user to set scale values for ImageJ'''

        # read image into opencv 
        image = cv2.imread(MacroFunctions.image_path)

        # open OpenCV GUI to allow user to select area 
        r = cv2.selectROI("Select the area", image, showCrosshair=True, fromCenter=False)

        # close GUI window
        cv2.destroyWindow("Select the area")

        # get region of interest dimensions(ROI)
        x, y, w, h = r

        # measure length in pixels
        scale_in_pixels = w

        #print width in pixels
        print(f"Width: {scale_in_pixels} pixels")

        return  scale_in_pixels
    
    def get_threshold(MacroFunctions):
        '''function to open interactive Threshold GUI for user to set image Threshold, as user for threshold value'''

        # read image into opencv in grayscale
        image = cv2.imread(MacroFunctions.image_path, cv2.IMREAD_GRAYSCALE)

        # create plot for threshold and to display image
        fig, ax = plt.subplots()
        plt.subplots_adjust(left=0.25, bottom=0.25)
        image_display = ax.imshow(image, cmap='binary')
        ax.set_title("Threshold")

        #create slider
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
            ret, thresh1 = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
            image_display.set_data(thresh1)
            ax.set_title(f"Interactive Threshold - Value: {threshold_value}")

        slider.on_changed(update)
        plt.show()

        threshold = int(input('Please Type your Threshold Value:'))

        return threshold

    def run_macros(MacroFunctions):
        '''function to run macro functions on an image based on user inputs'''

        # open image
        MacroFunctions.open_image()






    
    






