'''
PyImageJ Application
'''
import imagej
from imagej import Mode
from Macro_Class import MacroFunctions
from PyimageJ_Class import PyImageJApp
import os
from os import listdir


def read_imagefiles(image_directory):
    '''function to iteratively get the paths for every image in the the particle image path retuns list of image paths to be opened
    args:
    image_directory = folder path for images
    
    return:
    list_of_imagepaths = list of image paths for each image in folder'''
    
    list_of_imagepaths = []

    # iterate over image_directory
    for image in os.listdir(image_directory):
        list_of_imagepaths.append(image)

    return list_of_imagepaths


def main():

    # initalize image
    ij = imagej.init('net.imagej:imagej+net.imagej:imagej-legacy', mode=Mode.HEADLESS)

    # initialize application
    app = PyImageJApp()

    # prompt users for directories 
    image_directory = str(input("Please enter the image directory path:"))+'/'
    results_directory = str(input("Please enter your results directory path:"))+'/'
    output_directory = str(input("Please enter your output directory path:"))+'/'

    list_of_imagepaths = read_imagefiles(image_directory)

    if list_of_imagepaths:
        
        # initialize threshold and scale using first image 
            first_image_path = list_of_imagepaths[0]
            absolute_image_path = image_directory + first_image_path 
            absolute_results_path = os.path.splitext(results_directory + first_image_path )[0]+'_results.csv'
            absolute_output_path = os.path.splitext(output_directory + first_image_path )[0]+'_processedimage.png'

            app.macro_functions = MacroFunctions(
            image_path=absolute_image_path,
            results_path=absolute_results_path,
            output_path=absolute_output_path,
            )
            # prompt user for operation inputs 
            operations = app.prompt_user()

            # set scale and threshold if requested
            app.initialize_threshold_scale(operations)
            app.analyze_particles_parameters(operations)
            
            # apply macro to every single image in folder
            for image_path in list_of_imagepaths:
                absolute_image_path = os.path.join(image_directory, image_path)
                absolute_results_path = os.path.splitext(os.path.join(results_directory, image_path))[0] + '_results.csv'
                absolute_output_path = os.path.splitext(os.path.join(output_directory, image_path))[0] + '_processedimage.png'

                app.macro_functions = MacroFunctions(
                    image_path=absolute_image_path,
                    results_path=absolute_results_path,
                    output_path=absolute_output_path,
                    threshold_min=app.macro_functions.threshold_min,
                    threshold_max=app.macro_functions.threshold_max,
                    scale=app.macro_functions.scale,
                    unit=app.macro_functions.unit,
                    pixels=app.macro_functions.pixels,
                    particle_size_min=app.macro_functions.particle_size_min,
                    circularity_min=app.macro_functions.circularity_min
                )

                macro = app.running_macros(operations)
                ij.py.run_macro(macro)

                # label particles and update png
                app.label_particles(operations)


if __name__ == '__main__':
    main()



