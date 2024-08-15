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