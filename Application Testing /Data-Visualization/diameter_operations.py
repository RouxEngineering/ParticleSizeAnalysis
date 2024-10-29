"""
-------------------------------------------------
Program: diameter_operations
Author: Daniel Lawson
Date: August 13, 2024
-------------------------------------------------

Description:
This module contains functions for computing effective diameter and related metrics for a given DataFrame. The functions include:
1. `compute_eff_diameter`: Calculates the effective diameter based on the area column.
2. `add_eff_diameter`: Adds columns for effective diameter and radius to the DataFrame.
3. `build_diameter_metrics_dataframe`: Builds a DataFrame with diameter metrics, including cumulative frequency and percentage.
"""

# Import statements
import pandas as pd       # Required for dataframe
import numpy as np        # Required for math operations and contants

def compute_eff_diameter(df, area_column_name="Area"):
    """
    Compute the effective diameter based on the area column.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        area_column_name (str): The name of the column containing area values.

    Returns:
        numpy.ndarray: Array of effective diameters computed from the area values.

    Raises:
        KeyError: If the specified area column does not exist in the DataFrame.
    """

    data = df
    
    try:
        # Comute effective radius using the formula r = (A/π) ^ 0.5
        effective_radius = (np.array( data[area_column_name] )/np.pi)**0.5
    except KeyError:
        print(f'''A KeyError has occured: {KeyError}. The input dataframe has not column called {area_column_name}.\n''')
        return None
    else:
        # Compute the effective diameter as twice the effective radius 
        effective_diameter = effective_radius*2             
        return effective_diameter
    
    

def add_eff_diameter( input_dataframe, area_column_name, perimeter_column_name, unit="pixels"):
    """
    Add effective diameter and radius columns to the DataFrame.

    Args:
        input_dataframe (pandas.DataFrame): The DataFrame to update.
        area_column_name (str): The name of the column containing area values.
        perimeter_column_name (str): The name of the column containing perimeter values.
        unit (str): Unit of measurement for the columns (default is "pixels").

    Returns:
        pandas.DataFrame: Updated DataFrame with columns for area, perimeter, effective diameter, and effective radius.
    
    Raises:
        KeyError: If the File_key column is expected but not present in the DataFrame.
    """
    diameter_array = compute_eff_diameter( input_dataframe, area_column_name )
    data = input_dataframe

    # Create a new dataframe with additional diameter metric
    output_dataframe = pd.DataFrame(
        { 
            f"Area_{unit}^2": data[ area_column_name ],            # extract Area
            f"Perim_{unit}": data[perimeter_column_name],          # extract Perimeter
            f"eff_diameter_{unit}": diameter_array,                # Effective  diameter  
            f"eff_radius_{unit}": diameter_array/2,                # Effective  radius
        }) 
    
    try:
        # Attempt to key the File_key column if present 
        output_dataframe["File_key"] = data["File_key"]
    
    except KeyError:         
        print(f'''A KeyError has occured: {KeyError}. The input dataframe consist of one file.\n''')
    
    else:                                          
        print('''Multiple files are in this input dataframe, File_key column ADDED.''')
        
    return output_dataframe



def build_diameter_metrics_dataframe( input_dataframe, area_col_name, perimeter_col_name, target_col_name, unit, suf, FlowCam = True):
    """
    Build a DataFrame with diameter metrics including cumulative frequency and percentage.

    Args:
        input_dataframe (pandas.DataFrame): The DataFrame to process.
        area_col_name (str): The name of the area column.
        perimeter_col_name (str): The name of the perimeter column.
        target_col_name (str): The name of the column to compute cumulative frequency and percentage for.
        unit (str): Unit of measurement for the columns.
        suf (str): Suffix to append to cumulative frequency and percentage column names.
        FlowCam (bool): Flag indicating whether the DataFrame is FlowCam or not (default is True).

    Returns:
        pandas.DataFrame: Updated DataFrame with diameter metrics and cumulative statistics.
    """
    from frequency_operations import add_cumulative_frequency, add_cumulative_percentage

    if not FlowCam: # if dataframe is not flowcam, add effective diameter column (modify in place)
        input_dataframe = add_eff_diameter( 
                                            input_dataframe=input_dataframe, 
                                            area_column_name=area_col_name, 
                                            perimeter_column_name=perimeter_col_name,
                                            unit= unit
                                            )
        
    # Add cumulative frequency column ( copy )
    new_df = add_cumulative_frequency(
                    DataFrame= input_dataframe,
                    target_column_name= target_col_name,
                    suffix = suf
                    )
    
    # Add cumulative percentage column
    new_df = add_cumulative_percentage( 
        DataFrame= new_df, 
        target_column_name= target_col_name,
        column_suffix= suf,
    )
    return new_df

'''-----------------------------------------------------------------------'''