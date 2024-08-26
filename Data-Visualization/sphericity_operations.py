"""
-------------------------------------------------
Program: sphericity_operations
Author: Daniel Lawson
Date: August 13, 2024
-------------------------------------------------

Description:
This module contains functions for computing sphericity and adding it to a DataFrame. The functions include:
1. `compute_sphericity`: Calculates the sphericity of particles based on area and perimeter.
2. `add_sphericity`: Adds the computed sphericity to the DataFrame.
3. `build_sphericity_metrics_dataframe`: Builds a DataFrame with sphericity metrics and cumulative statistics.

"""

# Import statements
import pandas as pd       # Required for dataframe
import numpy as np        # Required for math operations


def compute_sphericity( df , area_column_name="Area", perim_column_name="Perim."):
    """
    Compute the sphericity for all particles in the DataFrame.

    Sphericity is computed as the ratio of the perimeter of an equivalent circle to the actual perimeter of the particle.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        area_column_name (str): The name of the column containing area values.
        perim_column_name (str): The name of the column containing perimeter values.

    Returns:
        numpy.ndarray: Array of sphericity ratios computed for each particle.

    Raises:
        KeyError: If the specified area or perimeter columns do not exist in the DataFrame.
    """
    # Convert Pandas Series to Numpy Array
    Area = np.array(  df[area_column_name] )    # Area
    Perim = np.array( df[perim_column_name] )   # real Perimeter column vector
    
    # Compute the perimeter of an equivalent circle
    eff_Perim = 2*np.sqrt(np.pi*Area) 

    # Compute the Sphericity ratio
    sphericity = np.divide( eff_Perim, Perim )       

    return sphericity



def add_sphericity( df , area_column_name, perim_column_name ):
    """
    Add sphericity to the DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame to update.
        area_column_name (str): The name of the column containing area values.
        perim_column_name (str): The name of the column containing perimeter values.

    Returns:
        pandas.DataFrame: Updated DataFrame with an additional 'Sphericity' column.
    """
    sphericity_ratio = compute_sphericity( df, area_column_name, perim_column_name)
    df["Sphericity"] = sphericity_ratio
    return df


 
def build_sphericity_metrics_dataframe( input_dataframe, area_col_name, perimeter_col_name, target_col_name, suf):
    """
    Build a DataFrame with sphericity metrics and cumulative statistics.

    This function adds sphericity metrics to the input DataFrame, then calculates cumulative frequency and percentage.

    Args:
        input_dataframe (pandas.DataFrame): The DataFrame to process.
        area_col_name (str): The name of the column containing area values.
        perimeter_col_name (str): The name of the column containing perimeter values.
        target_col_name (str): The name of the column to compute cumulative frequency and percentage for.
        suf (str): Suffix to append to cumulative frequency and percentage column names.

    Returns:
        pandas.DataFrame: Updated DataFrame with sphericity metrics, cumulative frequency, and percentage.
    """
    from frequency_operations import add_cumulative_frequency, add_cumulative_percentage

    # Add sphericity to the DataFrame
    modified_input_dataframe = add_sphericity(
        df = input_dataframe,
        area_column_name = area_col_name,
        perim_column_name= perimeter_col_name)
    
    # Add cumulative frequency column
    new_df = add_cumulative_frequency(
         DataFrame= modified_input_dataframe,
         target_column_name= target_col_name,
         suffix= suf
         )
    
    # Add cumulative percentage column
    new_df = add_cumulative_percentage(
        DataFrame= new_df,
        target_column_name= target_col_name,
        column_suffix= suf
        )
    return new_df

'''-----------------------------------------------------------------------'''
## !!!
# Determine whether it makes sense to create a new dataframe in the add_sphericity column or just in the frequency operation functions!!
 