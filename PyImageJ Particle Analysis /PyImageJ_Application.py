'''
PyImageJ Application
'''
import imagej
from imagej import Mode
from Macro_Class import MacroFunctions
from PyimageJ_Class import PyImageJApp



def main():

    # initalize imagej
    ij = imagej.init('net.imagej:imagej+net.imagej:imagej-legacy', mode=Mode.HEADLESS)

    
    macro_funcs = MacroFunctions(
    image_path='/Users/sarah/Documents/areospace research/material recycling project/PyImageJ-Particle-Analysis/Particle Images/Ti64_Lot232-EZ2316_1Use_10X_Scale.png',
    results_path='/Users/sarah/Documents/areospace research/material recycling project/PyImageJ-Particle-Analysis/Processed Results/results_summary.csv',
    output_path='/Users/sarah/Documents/areospace research/material recycling project/PyImageJ-Particle-Analysis/Processed Images/processed_img.png',
    )

    app = PyImageJApp(macro_funcs)
    macro = app.running_macros()
    
    ij.py.run_macro(macro)





main()



