"""
Program: calculations.py  
Author: Daniel Lawson  
Date: December 6, 2024  
Last Updated: December 9, 2024  

Description:  
    This module provides tools for analyzing particle datasets, including frequency, cumulative frequency, diameter-based metrics,  
    and area percentage distributions. The functionality is particularly useful for particle distribution analysis, offering insights  
    into size distributions, cumulative characteristics, and area-based metrics.  

Key Features:  
    - **Frequency and Cumulative Frequency Metrics:** Calculate and append the frequency of unique values and cumulative frequency (%)  
    for a specified particle parameter (e.g., diameter, circularity, aspect ratio).  
    - **Diameter Metrics:** Compute effective particle diameters assuming circular equivalence based on area, and calculate related  
    cumulative statistics.  
    - **Area Percentage Distributions:** Uses physical particle parameter (e.g., diameter, circularity) and calculate per-bin and  
    cumulative area percentage distributions.  
    - **FlowCam and PyImageJ Support:** Includes specific support for datasets from FlowCam and PyImageJ's Analyze Particles.  

Functions:  
    - `add_frequency_stats_to_dataframe`: Appends frequency-related metrics (particle count, frequency, cumulative frequency)  
    to a DataFrame.  
    - `build_diameter_metrics_dataframe`: Computes effective diameter metrics and cumulative statistics based on dataset type.  
    - `compute_bin_and_cumulative_area_percentages`: Bins a physical particle parameter and calculates per-bin and cumulative  
    area percentage distributions, providing detailed area-based insights into particle datasets.  

Dependencies:  
- pandas  
- numpy  
- logging  
- Data Processing, Regression, Visualizations.Visualizations.utils.column_utils  
"""

# Import statements
import pandas as pd       # For manipulating and analyzing data in tabular form
import numpy as np        # For numerical operations and array manipulations
import logging
from utils.column_utils import index_column_name  #  For dynamic column name indexing in DataFrames.  

# Configure logging (set level, output format)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_frequency_stats_to_dataframe(DataFrame, target_column_name):
    """
    Calculate the frequency and cumulative frequency of values in a specified column, 
    and append these statistics as new columns to the DataFrame.

    This function sorts the DataFrame by the target column, computes the frequency of each 
    unique value, and calculates the cumulative frequency as a percentage of the total. 
    It then appends these calculated metrics to the DataFrame along with a "Particle_number" 
    column, where the particle number is assigned based on the sorted order of the target column.

    Args:
        DataFrame (pandas.DataFrame): The DataFrame containing the data to analyze.
        target_column_name (str): The name of the column for which frequency metrics are calculated.

    Returns:
        pandas.DataFrame: A new DataFrame with added columns: 
            "Particle_number", "Frequency", and "Cumulative Frequency (%)".
        int: The total number of rows (particles) in the DataFrame.
    
    Raises:
        KeyError: If the target column does not exist in the DataFrame.
    
    Example:
        df, total_particles = add_frequency_stats_to_dataframe(df, 'diameter')
    """
    # Check if the target column exists in the DataFrame
    if target_column_name not in DataFrame.columns:
        raise KeyError(
            f"""Target column '{target_column_name}' does not exist in the DataFrame. 
            Cannot compute frequency or cumulative frequency columns. 
            Available Columns: {DataFrame.columns}"""
        )

    # Sort the DataFrame by the target column for consistent particle number assignment
    df = DataFrame.sort_values(by=target_column_name).copy()

    # Compute the frequency of each unique value in the target column
    frequencies = df[target_column_name].value_counts().sort_index()

    # Map the raw frequency to the corresponding rows in the DataFrame
    df["Frequency"] = df[target_column_name].map(frequencies)

    # Compute cumulative frequency as a percentage of the total number of rows
    cumulative_frequency = frequencies.cumsum() / df.shape[0] * 100
    df["Cumulative Frequency"] = df[target_column_name].map(cumulative_frequency)

    # Assign a particle number based on the sorted order of the target column
    df["Particle_number"] = np.arange(1, len(df) + 1)

    # Return the updated DataFrame and the total number of particles (rows)
    return df, len(df)



def build_diameter_metrics_dataframe(
    df, 
    target_column: str = "Effective Diameter (µm)", 
    area_col: str = None
):
    """
    Build a DataFrame with diameter-related metrics, including cumulative frequency and percentage.

    This function computes the effective diameter for particles based on the provided `area_col` (PyImageJ datasets) 
    or uses an existing `target_column` in the DataFrame if no `area_col` is specified (FlowCam datasets). 
    Frequency-related metrics are added to the DataFrame in both cases.

    Args:
        df (pandas.DataFrame): The input DataFrame containing particle data to process.
        target_column (str): The column name for effective diameter or the target for frequency calculations.
                             Defaults to "Effective Diameter (µm)".
        area_col (str, optional): The name of the column containing particle area. If provided, the effective diameter
                                  is computed using this column. If None, it is assumed the `target_column` already exists
                                  and corresponds to FlowCam data.

    Returns:
        pandas.DataFrame: Updated DataFrame with computed or existing diameter column and frequency metrics.
        str: The name of the diameter column used for metrics.

    Raises:
        KeyError: If the required `area_col` is not present in the DataFrame when specified.

    Notes:
        - If `area_col` is provided, the dataset is assumed to originate from PyImageJ's Analyze Particles CSV.
          Effective diameter is calculated using the formula for the diameter of a circle with the same area:
          `diameter = sqrt((4 * area) / π)`.
        - If `area_col` is not provided, the dataset is assumed to be from FlowCam's exported data, which already 
          contains the target diameter column.
        - Frequency-related columns include cumulative frequency and percentage for the diameter values.
    """
    if area_col:
        # Validate the presence of the specified area column
        if area_col not in df.columns:
            raise KeyError(f"Area column '{area_col}' not found in the DataFrame.")

        # Compute the effective diameter
        logging.info(f"Computing effective diameter and storing in '{target_column}'.")
        df[target_column] = np.sqrt((4 * df[area_col]) / np.pi)
        logging.info(f"Computed diameter stats: min={df[target_column].min()}, max={df[target_column].max()}")

    # Add frequency-related columns
    logging.info(f"Adding frequency-related columns for '{target_column}'.")
    df, _ = add_frequency_stats_to_dataframe(df, target_column)
    logging.info(f"Frequency columns added successfully.")

    return df, target_column




def compute_bin_and_cumulative_area_percentages(
        df, 
        target_column,
        area_column: str  = None,
        bin_width: float = 5
) -> tuple[str, np.ndarray, list, list]:
    """
    Calculate the per-bin and cumulative area percentage distribution for a dataset, based on a specified 
    physical particle parameter (e.g., diameter, circularity). 

    This function bins the values from the target column (physical parameter) and calculates the corresponding 
    area percentages for each bin, as well as the cumulative area percentage distribution.

    Parameters:
        df (pd.DataFrame): The input dataframe containing particle data, including the target column and area column.
        target_column (str): The name of the column representing the physical parameter to bin (e.g., 'diameter', 'circularity').
        area_column (str, optional): The name of the column representing the area of the particles. If None, it defaults to the column name 'Area'.
        bin_width (float, optional): The width of each bin for the target column. Default is 5.

    Returns:
        tuple:
            - str: The column name representing particle areas.
            - np.ndarray: The array of bin edges (i.e., the boundaries for each bin).
            - list: The list of per-bin area percentages.
            - list: The list of cumulative area percentages for all bins.

    Example:
        >>> import pandas as pd
        >>> data = {
        >>>     "diameter": [1.2, 2.5, 3.8, 4.0, 5.5],
        >>>     "area": [10, 15, 20, 5, 10]
        >>> }
        >>> df = pd.DataFrame(data)
        >>> bin_percentages, cumulative_percentages, area_column, bins = compute_bin_and_cumulative_area_percentages(
        >>>     df, target_column="diameter", area_column="area", bin_width=1.0
        >>> )
        >>> print("Per-bin area percentages:", bin_percentages)
        >>> print("Cumulative area percentages:", cumulative_percentages)
    """

    # If no area_column is provided, attempt to find a column named 'Area'
    if area_column is None:
        logging.info("No area column specified. Defaulting to 'Area'.")
        area_column = index_column_name(df, "Area")
    
    logging.info(f"Using '{area_column}' as the area column.")

    # Convert the target column and area column to numeric, coercing errors to NaN
    df[target_column] = pd.to_numeric(df[target_column], errors='coerce')
    df[area_column] = pd.to_numeric(df[area_column], errors='coerce')

    # Replace NaN values with 0 in both columns
    df[target_column].fillna(0, inplace=True)
    df[area_column].fillna(0, inplace=True)

    # Calculate the bin edges based on the specified bin width
    bins = np.arange(df[target_column].min(), df[target_column].max() + bin_width, bin_width)

    # Initialize a list to store the total area in each bin
    bin_areas = []

    # Loop through each bin to calculate the total area for particles within that bin
    for i in range(len(bins) - 1):
        # Get the particles that fall within the current bin range
        in_bin = (df[target_column] >= bins[i]) & (df[target_column] < bins[i + 1])
        particles_in_bin = df[in_bin]

        # Sum the areas of the particles within this bin
        total_area_in_bin = particles_in_bin[area_column].sum()

        # Append the total area for this bin to the list
        bin_areas.append(total_area_in_bin)

    # Calculate the area percentage for each bin
    total_area = df[area_column].sum()
    bin_area_percentages = [
        (area / total_area) * 100 if total_area > 0 else 0 for area in bin_areas
    ]

    # Calculate the cumulative area percentage distribution
    cumulative_area_percentages = np.cumsum(bin_area_percentages)

    # Return the area column, bin edges, per-bin area percentages, and cumulative area percentages
    return (area_column, bins, bin_area_percentages, cumulative_area_percentages)