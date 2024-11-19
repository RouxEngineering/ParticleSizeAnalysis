import os
import glob
import pandas as pd
from tkinter import filedialog
from PyimageJ_Class import PyImageJApp
from Macro_class import MacroFunctions
import imagej
from imagej import Mode


class PyImageJApplication:
    def __init__(self):
        """initalizing PyimageJ application"""
        self.ij = imagej.init('net.imagej:imagej+net.imagej:imagej-legacy', mode=Mode.HEADLESS)
        self.app = PyImageJApp()

    @staticmethod
    def read_imagefiles(image_directory):
        """get image paths of all images from a folder
        arg: 
        image_directory (str): folder path containing imagees

        return:
        list: list of image file paths
        """
        return sorted([filename for filename in os.listdir(image_directory)])

    @staticmethod
    def concatenate_csv_files(input_folder, output_filename='concatenated_file.csv'):
        """concatenate csv files into one csv

        Args:
            input_folder (str):directory of folders with .csv files
            output_filename (str): name of concatenated file 
        """
        combined_df = pd.concat(
            [pd.read_csv(os.path.join(input_folder, f)) for f in os.listdir(input_folder) if f.endswith('.csv')],
            ignore_index=True
        )
        output_file_path = os.path.join(input_folder, output_filename)
        combined_df.to_csv(output_file_path, index=False)

    def run_app(self, scale_directory, image_directory, list_of_imagepaths, results_directory, output_directory):
        """run image processing application."""
        if list_of_imagepaths:
            # Initialize threshold and scale using scale image
            if scale_directory:
                absolute_image_path = os.path.join(image_directory, scale_directory)
                absolute_results_path = os.path.splitext(os.path.join(results_directory, scale_directory))[0] + '_results.csv'
                absolute_output_path = os.path.splitext(os.path.join(output_directory, scale_directory))[0] + '_processedimage.png'

                self.app.macro_functions = MacroFunctions(
                    image_path=absolute_image_path,
                    results_path=absolute_results_path,
                    output_path=absolute_output_path,
                )

            # Prompt user for operations
            operations = self.app.prompt_user()

            # Set scale and threshold if requested
            self.app.initialize_threshold_scale(operations, image_directory)
            self.app.analyze_particles_parameters(operations)

            # Apply macro to every single image in the folder
            for image_path in list_of_imagepaths:
                if os.path.basename(image_path).lower() == 'scale.png' or not image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tif')):
                    continue

                absolute_image_path = os.path.join(image_directory, image_path)
                absolute_results_path = os.path.splitext(os.path.join(results_directory, image_path))[0] + '_results.csv'
                absolute_output_path = os.path.splitext(os.path.join(output_directory, image_path))[0] + '_processedimage.png'

                self.app.macro_functions = MacroFunctions(
                    image_path=absolute_image_path,
                    results_path=absolute_results_path,
                    output_path=absolute_output_path,
                    threshold_min=self.app.macro_functions.threshold_min,
                    threshold_max=self.app.macro_functions.threshold_max,
                    scale=self.app.macro_functions.scale,
                    unit=self.app.macro_functions.unit,
                    pixels=self.app.macro_functions.pixels,
                    particle_size_min=self.app.macro_functions.particle_size_min,
                    circularity_min=self.app.macro_functions.circularity_min
                )

                macro = self.app.running_macros(operations)
                self.ij.py.run_macro(macro)

                # Label particles and update PNG
                self.app.label_particles(operations)

    @staticmethod
    def create_output_folders(image_directory):
        """create folders to put results and processed images into

        Args:
            image_directory (str): path to folder with images

        Returns:
            tuple: path to the results folder and processed images folder
        """
        results_folder = os.path.join(image_directory, "results")
        processed_images_folder = os.path.join(image_directory, "processed_images")

        os.makedirs(results_folder, exist_ok=True)
        os.makedirs(processed_images_folder, exist_ok=True)

        return results_folder, processed_images_folder

    def run_with_auto_folders(self):
        """run application with folders created"""
        print("Please select the folder containing images:")
        image_directory = filedialog.askdirectory()

        # create output folders
        results_folder, processed_images_folder = self.create_output_folders(image_directory)

        # Select the scale image
        print("Please select the image you will use as the scale:")
        scale_directory = filedialog.askopenfilename()

        list_of_imagepaths = self.read_imagefiles(image_directory)
        self.run_app(scale_directory, image_directory, list_of_imagepaths, results_folder, processed_images_folder)

        confirmation = input("do you want to concatenate all CSV files in the results folder? (yes/no): ").strip().lower()
        if confirmation == "yes":
            self.concatenate_csv_files(results_folder)
        else:
            print("CSV concatenation terminated.")

    def main(self):
        """run application"""
        self.run_with_auto_folders()


if __name__ == '__main__':
    app = PyImageJApplication()
    app.main()
