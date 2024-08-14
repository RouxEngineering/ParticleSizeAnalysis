'''                                                                       '''
'''Program diameter_operations                                            '''
'''                                                                       '''
'''This file has a function that calculates the effective diameter and 
outputs a numpy array.
The next funtion returns a pandas dataframe that contains:
Area, Perim,effective radius, effective diameter                          '''


# Import statements
import pandas as pd       # Required for dataframe
import numpy as np        # Required for math operations, contants

def compute_eff_diameter(df):

    data = df

    # Compute Radius, r = (A/PI) ^ 0.5
    effective_radius = (np.array(data["Area"])/np.pi)**0.5
    effective_diameter = effective_radius*2             # Compute Radius,
    return effective_diameter

def add_eff_diameter( df, unit="pixels"):

    diameter_array = compute_eff_diameter( df )
    data = df

    # Create a new dataframe
    output_dataframe = pd.DataFrame(
        { 
        f"Area_{unit}": data["Area"],                   # extract Area
        f"Perim_{unit}": data["Perim."],                # extract Perimeter
        f"eff_diameter_{unit}": diameter_array,         # add eff diameter  
        f"eff_radius_{unit}": diameter_array/2,         # add eff radius
        }) 
    
    # Attempt to key the File_key from the input dataframe
    try:
        output_dataframe["File_key"] = data["File_key"]
    
    except KeyError:                                    # handle KeyError
        print(f'''A KeyError has occured: {KeyError}. 
The input dataframe consist of one file.\n''')
    
    else:                                               # No error, code block
        print('''Multiple files are in this input dataframe,
File_key column ADDED.''')
        
    return output_dataframe
        
