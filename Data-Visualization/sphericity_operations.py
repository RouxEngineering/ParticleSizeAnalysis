'''                                                                       '''
'''Program sphereicity_operations                                         '''
'''                                                                       '''
'''This file contains a function to compute sphericity and one to
add it to the dataframe.                                                  '''


# Import statements
import pandas as pd       # Required for dataframe
import os                 # Required for path confimation
import math               # Required for PI
import numpy as np

# 1. Compute Sphericity for all particles in Dataframe 
def compute_sphericity( df ):

    # Convert Pandas Series to Numpy Array
    Area = np.array( df.filter(like="Area") )      # Area
    Perim = np.array( df.filter(like= "Perim") )  # real Perimeter

    # Compute the perimeter of an equivalent circle
    eff_Perim = 2*np.sqrt(np.pi*Area) 
    
    # Compute a Sphericity (ratio)
    sphericity = eff_Perim/Perim                

    return sphericity

# 2. Add sphereicity to the dataframe
def add_sphericity( df ):
    sphericity_ratio = compute_sphericity( df)
    df["Sphericity"] = sphericity_ratio
    return df