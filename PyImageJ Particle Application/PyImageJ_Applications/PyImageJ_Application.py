'''
PyImageJ Application
'''
import imagej
from imagej import Mode
from PyimageJ_Class import PyImageJApp
from Macro_class import MacroFunctions
import os
import glob
import pandas as pd
from PIL import Image
from tkinter import filedialog 


def read_imagefiles(image_directory):
    '''function to iteratively get the paths for every image in the particle image path returns list of image paths to be opened and convert them to png if not already png files
    args:
    image_directory = folder path for images
    
    return:
    list_of_imagepaths = list of image paths for each image in folder'''

    list_of_imagepaths = []

    for filename in os.listdir(image_directory):
        list_of_imagepaths.append(filename)
    
    list_of_imagepaths.sort()

    return list_of_imagepaths

def concat_csvfiles(results_directory):
    '''function that asks user to select a directory and concat the csv files in a directory into one csv'''
    csv_name = input('Input concatenated CSV file name:')
    path = results_directory

    # Get all CSV files in the directory
    files = glob.glob(os.path.join(path, "*.csv"))

    # Initialize an empty list to hold the dataframes
    flist = []

    # Loop through the files and read them into dataframes
    for filename in files:
        df = pd.read_csv(filename, index_col=False)
        flist.append(df)

    # Concatenate all dataframes into one
    df_out = pd.concat(flist, axis=0, ignore_index=True)

    # Save the concatenated dataframe to a new CSV file
    df_out.to_csv(os.path.join(path, f'{csv_name}.csv'), index=False)

def run_app(scale_directory, image_directory, app, list_of_imagepaths, results_directory, output_directory, ij):
    '''function to run application based on user directory inputs'''
    if list_of_imagepaths:
        
        # initialize threshold and scale using scale png
        if scale_directory:
            absolute_image_path = os.path.join(image_directory, scale_directory)
            absolute_results_path = os.path.splitext(os.path.join(results_directory, scale_directory))[0] + '_results.csv'
            absolute_output_path = os.path.splitext(os.path.join(output_directory, scale_directory))[0] + '_processedimage.png'

            app.macro_functions = MacroFunctions(
                image_path=absolute_image_path,
                results_path=absolute_results_path,
                output_path=absolute_output_path,
            )
        # prompt user for operation inputs 
        operations = app.prompt_user()

        # set scale and threshold if requested
        app.initialize_threshold_scale(operations, image_directory)
        app.analyze_particles_parameters(operations)
        
        # apply macro to every single image in folder
        for image_path in list_of_imagepaths:
            if os.path.basename(image_path).lower() == 'scale.png' or not image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tif')):
                continue
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

def prompt_user():
    '''prompt user for inputs for running PyImageJ Application'''

    ij = imagej.init('net.imagej:imagej+net.imagej:imagej-legacy', mode=Mode.HEADLESS)

    # initialize application
    app = PyImageJApp()

    # prompt users for directories 
    print("Please select the image folder:")
    image_directory = filedialog.askdirectory()
    print("Please select results folder to save csv files")
    results_directory = filedialog.askdirectory() 
    print("Please select the processed images folder")
    output_directory = filedialog.askdirectory() 
    print("Please select the image you will use as the scale")
    scale_directory = filedialog.askopenfilename()

    list_of_imagepaths = read_imagefiles(image_directory)

    run_app(scale_directory, image_directory, app, list_of_imagepaths, results_directory, output_directory, ij)
    


def concatenate_csv_files(input_folder):
    '''function to concatenate all csv files in one folder into one csv '''

    combined_df = pd.concat(
        [pd.read_csv(os.path.join(input_folder, f)) for f in os.listdir(input_folder) if f.endswith('.csv')],
        ignore_index=True
    )

    output_file_path = os.path.join(input_folder, 'concatenated_output.csv')

    combined_df.to_csv(output_file_path, index=False)

def main():
      
    prompt_user()

    confirmation = input('Do you want to concatenate the CSV files in this folder? (yes/no): ')
    if confirmation.lower() == 'yes':
        print('Please select the folder where you would like to concatenate the csv files')
        csv_folder = filedialog.askdirectory() 
        concatenate_csv_files(input_folder=csv_folder)
    else:
        print("Concatenation process was cancelled.")


if __name__ == '__main__':
    main()