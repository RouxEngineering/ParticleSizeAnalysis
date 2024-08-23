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

def compute_eff_diameter(df, area_column_name="Area"):

    data = df
    
    # Compute Radius, r = (A/PI) ^ 0.5
    try:
        effective_radius = (np.array( data[area_column_name] )/np.pi)**0.5
    except KeyError:
        print(f'''A KeyError has occured: {KeyError}. 
The input dataframe has not column called {area_column_name}.\n''')
    else:
        effective_diameter = effective_radius*2             # Compute Radius,
        # print("eff diameter \n", effective_diameter, "\n", effective_diameter.shape )
        # print("eff radius \n", effective_diameter/2, "\b", (effective_diameter/2).shape)
        # print(" Target area column: ", data[area_column])
        return effective_diameter
    
    

def add_eff_diameter( df, area_column_name, perimeter_column_name, unit="pixels"):

    diameter_array = compute_eff_diameter( df, area_column_name )
    data = df

    # Create a new dataframe
    output_dataframe = pd.DataFrame(
        { 
        f"Area_{unit}^2": data[ area_column_name ],            # extract Area
        f"Perim_{unit}": df[perimeter_column_name],          # extract Perimeter
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



# Add all appropriate columns related to diameter metrics to dataframe 
def build_diameter_metrics_dataframe( input_dataframe, area_col_name, perimeter_col_name, target_col_name, unit, suf, FlowCam = True):
    from frequency_operations import add_cumulative_frequency, add_cumulative_percentage
    if not FlowCam: # if dataframe is not flowcam (default to true), add effective diameter column (modify in place)
        input_dataframe = add_eff_diameter( 
                                            df=input_dataframe, 
                                            area_column_name=area_col_name, 
                                            perimeter_column_name=perimeter_col_name,
                                            unit= unit
                                            )
    # Add dataframe cumulative frequency column ( copy )
    new_df = add_cumulative_frequency(
                    DataFrame= input_dataframe,
                    target_column_name= target_col_name,
                    suffix = suf
                    )
    
    new_df = add_cumulative_percentage( 
        DataFrame= new_df, # target database
        target_column_name= target_col_name,
        column_suffix= suf,
    )
    return new_df