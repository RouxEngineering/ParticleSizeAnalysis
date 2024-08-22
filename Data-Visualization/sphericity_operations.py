'''                                                                       '''
'''Program sphereicity_operations                                         '''
'''                                                                       '''
'''This file contains a function to compute sphericity and one to
add it to the dataframe.                                                  '''


# Import statements
import pandas as pd       # Required for dataframe
import numpy as np        # Required for math operations

# 1. Compute Sphericity for all particles in Dataframe 
def compute_sphericity( df , area_column_name="Area", perim_column_name="Perim."):

    # Convert Pandas Series to Numpy Array
    Area = np.array(  df[area_column_name] )    # Area
    Perim = np.array( df[perim_column_name] ) # real  Perimeter column vector
    
    # Compute the perimeter of an equivalent circle
    eff_Perim = 2*np.sqrt(np.pi*Area) 

    # Compute a Sphericity (ratio)
    sphericity = np.divide( eff_Perim, Perim )       

    return sphericity

# 2. Add sphereicity to the dataframe
def add_sphericity( df , area_column_name, perim_column_name ):
    sphericity_ratio = compute_sphericity( df, area_column_name, perim_column_name)
    df["Sphericity"] = sphericity_ratio
    return df



# Add all appropriate columns related to sphericity metrics to dataframe 
def build_sphericity_metrics_dataframe( input_dataframe, area_col_name, perimeter_col_name, target_col_name, suf):
    from frequency_operations import add_cumulative_frequency, add_cumulative_percentage
    modified_input_dataframe = add_sphericity(
        df = input_dataframe,
        area_column_name = area_col_name,
        perim_column_name= perimeter_col_name)
    new_df = add_cumulative_frequency(
         DataFrame= modified_input_dataframe,
         target_column_name= target_col_name,
         suffix= suf
         )
    new_df = add_cumulative_percentage(
        DataFrame= new_df,
        target_column_name= target_col_name,
        column_suffix= suf
        )
    return new_df

## !!!
# Determine whether it makes sense to create a new dataframe in the add_sphericity column or just in the frequency operation functions!!
