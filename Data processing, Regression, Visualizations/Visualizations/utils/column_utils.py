"""
Program: column_utils.py  
Author: Daniel Lawson  
Date: August 26, 2024  
Last Updated: December 6, 2024  

Description:  
Module for Dynamic DataFrame Column Operations  

This module provides utility functions for dynamically working with DataFrame columns, 
including filtering, indexing, and retrieving column names based on user-specified patterns. 
It is designed to simplify operations on datasets with variable or inconsistent column naming.  

Key Features:  
- Filter column names in a DataFrame using a substring match.  
- Index a DataFrame column based on a guessed name and return the corresponding Series.  
- Retrieve the name of a DataFrame column using partial name matching, with user selection for 
  multiple matches.  

Functions:  
    `get_column_names`: Extracts column names containing a specified substring.  
    `index_series`: Retrieves a Series from the DataFrame based on a guessed column name.  
    `index_column_name`: Retrieves a column name from the DataFrame using a guessed substring.  

Dependencies:  
    - pandas: For DataFrame manipulation.  
    - numpy: For handling array outputs.  
"""



def get_column_names(df, guess_name):
    """
    Extract column names from the DataFrame that contain the specified substring.

    Args:
        df (pandas.DataFrame): The DataFrame to search for matching column names.
        guess_name (str): The substring used to filter column names.

    Returns:
        numpy.ndarray: An array of column names that match the provided substring.

    Example:
        columns = get_column_names(df, "diameter")
        print(columns)  # Output: ['Particle Diameter', 'Diameter µm']
    """
    # Filter the DataFrame's column names using the provided substring
    filtered_df = df.filter(like=guess_name)
    return filtered_df.columns.values



def index_series(df, guess_name):
    """
    Retrieve a Series from the DataFrame based on a guessed column name.

    This function first searches for columns containing the guessed substring. If a 
    single match is found, it selects the corresponding Series. If multiple matches 
    are found, it prompts the user to select the desired column index.

    Args:
        df (pandas.DataFrame): The DataFrame to retrieve the Series from.
        guess_name (str): The substring used to filter column names.

    Returns:
        pandas.Series: The Series corresponding to the selected column.
        None: If no match is found or an invalid index is selected.

    Example:
        series = index_series(df, "diameter")
        print(series.head())
    """
    # Retrieve column names that match the guessed name
    names = get_column_names(df, guess_name)

    if len(names) == 1:
        # If only one match is found, return the corresponding Series
        print(f"Selected column: {names[0]}")
        return df[names[0]]
    elif len(names) > 1:
        # Multiple matches found; prompt user to select an index
        print("The following column names were found:")
        for idx, name in enumerate(names):
            print(f"{idx}: {name}", flush=True)

        try:
            user_index = int(input("Select the index of the desired column: "))
            # Validate user input
            if 0 <= user_index < len(names):
                return df[names[user_index]]
            else:
                print("Invalid index selection.")
        except ValueError:
            print("Invalid input. Please enter a numeric index.")
    else:
        # No matching columns found
        print(f"No matches found for '{guess_name}' in DataFrame.")
    return None



def index_column_name(df, guess_name):
    """
    Retrieve the name of a column from the DataFrame based on a guessed substring.

    This function searches for columns containing the guessed substring. If a single 
    match is found, it returns the column name. If multiple matches are found, the 
    user is prompted to select the desired column index.

    Args:
        df (pandas.DataFrame): The DataFrame to search for column names.
        guess_name (str): The substring used to filter column names.

    Returns:
        str: The name of the selected column.
        None: If no match is found or an invalid index is selected.

    Example:
        column_name = index_column_name(df, "diameter")
        print(column_name)  # Output: "Effective Diameter (µm)"
    """
    # Retrieve column names matching the guessed substring
    names = get_column_names(df, guess_name)

    if len(names) == 1:
        # Single match found; return the column name
        return names[0]
    elif len(names) > 1:
        # Multiple matches found; prompt user to select an index
        print(f"Multiple columns matched the guess '{guess_name}':")
        for idx, name in enumerate(names):
            print(f"\t{idx}: {name}")

        try:
            user_index = int(input("Select the index of the desired column: "))
            # Validate user input
            if 0 <= user_index < len(names):
                return names[user_index]
            else:
                print("Invalid index selection. No column returned.")
        except ValueError:
            print("Invalid input. Please enter a numeric index.")
    else:
        # No matching columns found
        print(f"No matches found for '{guess_name}' in DataFrame.")
    return None
