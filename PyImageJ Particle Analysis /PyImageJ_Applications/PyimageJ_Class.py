'''
PyImageJ Functions to Create Particle CSV file data 
'''
from Macro_class import MacroFunctions
import cv2 
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import os
import pandas as pd

class PyImageJApp:
    def __init__(self):
        self.macro_functions = None

    def get_scale(self): 
        '''function to open OpenCV GUI to allow user to set scale values for ImageJ'''

        # read image into opencv 
        image = cv2.imread(self.macro_functions.image_path)

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

        scale_in_pixels= int(input('Please type the pixel width value:'))

        return  scale_in_pixels
    
    def get_threshold(self):
        '''function to open interactive Threshold GUI for user to set image Threshold, as user for threshold value'''

        # read image into opencv in grayscale
        image = cv2.imread(self.macro_functions.image_path)

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

    def prompt_user(self):
        '''function to prompt user for the preprocessing steps they would like to do
        
        returns list of operations that user wants to do
        ''' 
        # initialize dictionary of operation choices for user to select from 
        operation_dict = {
            1:'change image type', 
            2:'set threshold',
            3: 'convert to binary mask', 
            4: 'set scale', 
            5:'analyze particles',
            6:'save'

        }

        selected_operations = []

        for key, operation in operation_dict.items():
            choice = input(f"Do you want to {operation}? (yes/no): ").strip().lower()
            if choice == 'yes':
                selected_operations.append(key)

        return selected_operations
    
    def initialize_threshold_scale(self, operations):
        '''function to initalize threshold and scale values for one image'''

        if 2 in operations: 
            self.macro_functions.threshold_min = int(self.get_threshold())
            self.macro_functions.threshold_max = 225 

        if 4 in operations: 
            self.macro_functions.pixels = int(self.get_scale())
            self.macro_functions.scale = float(input('Input the known scale value:')) 
            self.macro_functions.unit = input('Please enter the unit for the scale: ')

        return operations

    def analyze_particles_parameters(self, operations):
        '''prompt user for parameters circularity min and max and size min and max'''
        if 5 in operations:
            self.macro_functions.particle_size_min = float(input("Please enter the min particle size value(Pixels^2):"))
            max_particle_size_input = input("Please enter the max particle size value (Default value is Infinity): ")

            # If no input is provided, use the default value (Infinity)
            if max_particle_size_input == "":
                self.macro_functions.particle_size_max = 'Infinity'
            else:
                self.macro_functions.particle_size_max = float(max_particle_size_input)
            self.macro_functions.circularity_min = float(input("Please enter circularity min value:"))
            self.macro_functions.circularity_max = float(input("Please enter circularity max value(limit:1.00)"))

    def running_macros(self, operations):
        '''function to create macros based on a list of returned operations'''

        # initialize operation commands to open image and iteratively add onto preprocessing and analysis 
        macro_cmd = [self.macro_functions.open_image()]

        for operation in operations: 
            if operation == 1:
                macro_cmd.append(self.macro_functions.set_8bit())

            elif operation == 2:
                macro_cmd.append(self.macro_functions.set_threshold())

            elif operation == 3: 
                macro_cmd.append(self.macro_functions.binary_mask())

            elif operation == 4:
                macro_cmd.append(self.macro_functions.set_scale())

            elif operation == 5:
                macro_cmd.append(self.macro_functions.set_measurements())
                macro_cmd.append(self.macro_functions.analyze_particles())
                macro_cmd.append(self.macro_functions.save_type('Results', self.macro_functions.results_path))
                macro_cmd.append(self.macro_functions.save_type('png',self.macro_functions.output_path))

        # join script
        macro_script = "\n".join(macro_cmd)
        return macro_script
    
    def label_particles(self, operations): 
        '''create function to label particles on each image based on the x,y coordinates and update image'''

        img = cv2.imread(self.macro_functions.output_path)

        #create pandas df and iterativly label each particle 
        particle_analysis_df = pd.read_csv(self.macro_functions.results_path)

        # create list of tuples 
        coordinates = particle_analysis_df.filter(['X','Y'], axis=1)

        # convert to list of tuples
        if 4 in operations:
            tuples_list = [(int((row['X']*self.macro_functions.pixels)/self.macro_functions.scale), int((row['Y']*self.macro_functions.pixels)/self.macro_functions.scale)) for index, row in coordinates.iterrows()]
        else:
            tuples_list = [(int(row['X']), int(row['Y'])) for index, row in coordinates.iterrows()]



        # centroid parameters
        radius = 10
        color = (0, 0, 255) 
        thickness = -1

        for coordinate in tuples_list: 
            cv2.circle(img, coordinate, radius, color, thickness)

        cv2.imwrite(self.macro_functions.output_path, img)
        





        







        

            






        









    
    






