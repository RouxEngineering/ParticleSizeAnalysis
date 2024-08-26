"""
-------------------------------------------------
Program: frequency_operations
Author: Daniel Lawson
Date: August 13, 2024
-------------------------------------------------

Description:
This module contains functions for computing cumulative frequency and cumulative percentage 
based on a given column in a pandas DataFrame. The functions include:
1. `compute_cumulative_frequency`: Calculates cumulative frequency for a given column.
2. `add_cumulative_frequency`: Adds the cumulative frequency to the DataFrame.
3. `compute_cumulative_percentage`: Computes cumulative percentage for each particle.
4. `add_cumulative_percentage`: Adds cumulative percentage to the DataFrame.
"""

# Import statements
import pandas as pd       # Required for dataframes
import numpy as np        # Required for numpy arrays



def compute_cumulative_freqency( DataFrame, target_column_name ):
    """
    Calculate cumulative frequency for a given column.

    Args:
        DataFrame (pandas.DataFrame): The DataFrame containing the data.
        target_column_name (str): The name of the column to compute 
        frequency for.

    Returns:
        pandas.DataFrame: DataFrame with an added "Particle_number" column.
        list: Cumulative frequency of each unique value in the target column.
        int: Total number of particles (rows) in the DataFrame.
    
    Raises:
        KeyError: If the target column does not exist in the DataFrame.
    """
    df = DataFrame.copy() # Create a new Dataframe to avoid modifying input 
    
    try:
        df[str(target_column_name)]
    except KeyError:                               
        print(f'''A KeyError has occured: {KeyError}. 
Target column, {target_column_name}, DOESN'T exist.\n''')
    else:                                              
        print('''Target column exist.\n''')

    # Sort the input dataframe in ascending order
    df.sort_values( by=str(target_column_name), inplace=True) 

    # Create a list of sorted values 
    column_content_list = list( df[target_column_name] )
    
    # Calaculate Frequency of each event outcome 
    keys = list()
    freq = list()

    for i in range( len(column_content_list) ):
        if column_content_list[i] in keys:
            index = keys.index(column_content_list[i])
            freq[index] += 1
            freq += [0]
        else: 
            keys.append(column_content_list[i])
            freq += [1]

    # Count total particles
    total_elements = len( column_content_list )
    print("\ntotal_particles: ", total_elements)

    # Add particle number column
    df["Particle_number"]= np.arange(1, total_elements+1)      

    # Calculate Cumulative Frequency based upon number of times an outcome is observed 
    cumulative_frequency = []
    for j in range( total_elements ):
        if len(cumulative_frequency) > 0: # if list at least one element
            cumulative_frequency.append( freq[j] + cumulative_frequency[j - 1] )
        else: # else the list must be empty 
            cumulative_frequency.append(freq[j])
    
    return df, cumulative_frequency, total_elements 



def add_cumulative_frequency( DataFrame, target_column_name, suffix ):
    """
    Add the cumulative frequency to the DataFrame.

    Args:
        DataFrame (pandas.DataFrame): The DataFrame to update.
        target_column_name (str): The name of the column to compute frequency for.
        suffix (str): Suffix to append to the cumulative frequency column name.

    Returns:
        pandas.DataFrame: Updated DataFrame with the cumulative frequency column added.
    """
    df, cum_freq, total_elements = compute_cumulative_freqency( DataFrame, 
                                                               target_column_name )

    if df is not None:  # Ensure the dataframe has content 
        df[f"cumulative frequency {suffix}"] = cum_freq

    return df



def compute_cumulative_percentage( DataFrame, target_column_name):
    df = DataFrame
    """
    Compute cumulative percentage for each particle, accounting for repeats.

    Args:
        DataFrame (pandas.DataFrame): The DataFrame containing the data.
        target_column_name (str): The name of the column to compute percentage for.

    Returns:
        numpy.ndarray: Array of cumulative percentages for each particle.
    """
    df, cumulative_freq, total_particles = compute_cumulative_freqency( df, target_column_name)
    cumulative_percentage = (np.array(cumulative_freq)/total_particles)*100

    return cumulative_percentage




def add_cumulative_percentage(DataFrame, target_column_name, column_suffix ): 
    """
    Add cumulative percentage to the DataFrame.

    Args:
        DataFrame (pandas.DataFrame): The DataFrame to update.
        target_column_name (str): The name of the column to compute percentage for.
        column_suffix (str): Suffix to append to the cumulative percentage column name.

    Returns:
        pandas.DataFrame: Updated DataFrame with the cumulative percentage column added.
    """
    df =DataFrame
    cum_per = compute_cumulative_percentage( df, target_column_name )
    df[f"cumulative_%_particle {column_suffix}"] = cum_per  

    return df

'''-----------------------------------------------------------------------'''
