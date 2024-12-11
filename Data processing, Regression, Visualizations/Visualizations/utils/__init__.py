"""
`utils` Package

The `utils` package provides tools to process and analyze and plot pandas dataframes, 
with a focus on manipulating specific columns to extract meaningful metrics 
like diameter and frequency or retrieve column metadata. This package is 
designed to support operations that streamline data preparation and 
analysis, particularly for applications where particle diameter and 
distributions metrics are needed.

Modules dedicated to visualizing the data metrics produced by the operations in
this package. This includes tools to create frequency distribution plots, 
physical particle parameter plots, and other data visualizations for 
effective data analysis and presentation.

Modules:
--------
- `calculations.py`:
    - `add_frequency_stats_to_dataframe`:
        Function to compute frequency and cumulative frequency data, which 
        are useful for statistical analysis of data distributions within a dataframe.

    - `build_diameter_metrics_dataframe`:
        Function in this module add and calculate diameter-related metrics in a pandas dataframe. 
        These metrics are stored in a new columns, enabling further analysis of particle sizes.
    - `compute_bin_and_cumulative_area_percentages`: 
        Function that uses physical particle parameter (e.g., diameter, circularity) to calculate per-bin and  
        cumulative area percentage distributions.  
        
- `column_utils.py`:
    Provides utility functions to extract column names and indices from existing dataframe columns. 
    These functions help streamline the retrieval and organization of column metadata.

"""
