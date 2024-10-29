"""
-------------------------------------------------
Program: column_utils
Author: Daniel Lawson
Date: August 26, 2024
-------------------------------------------------

Description:
This module provides utility functions for handling DataFrame columns.
It includes methods for extracting column names based on patterns, indexing
series, and retrieving column names based on user input.

Functions:
- get_column_names: Extract column names matching a given pattern.
- index_series: Index a series from the DataFrame based on a guessed column name.
- index_column_name: Retrieve the column name based on a guessed name.
"""


def get_column_names(df, guess_name):
    """
    Extract column names that match the guess_name pattern.

    Args:
        df (pandas.DataFrame): The DataFrame to search in.
        guess_name (str): The substring to filter column names.

    Returns:
        numpy.ndarray: An array of matching column names.
    """
    filtered_df = df.filter( like= guess_name)
    return filtered_df.columns.values



def index_series(df, guess_name):
    """
    Index a series from the DataFrame based on a guessed column names.

    Args:
        df (pandas.DataFrame): The DataFrame to index from.
        guess_name (str): The substring to filter column names.

    Returns:
        pandas.Series: The indexed series corresponding to the selected column.
    """

    names = get_column_names( df, guess_name )

    if len(names) == 1:
        # If there is only one matching column, use it
        x_data = df[names[0]]
    else:
        #if there are multiple matching columns
        print( "The following column names were found: " )
        for idx, name in enumerate( names ):
            print(f"{idx}: {name}")
        # Prompt user for input
        user_index = int( input(prompt="Select the index of the column wanted") )
        #Ensure the user_index is valid
        if 0 <= user_index <= len(names):
            x_data = df[names[user_index]]
        else:
            print( "Invalid index Selection." )
    return x_data



def index_column_name(df, guess_name):
    """
    Index and return the column name from the DataFrame based on a guessed name.

    Args:
        df (pandas.DataFrame): The DataFrame to index from.
        guess_name (str): The substring to filter column names.

    Returns:
        str: The name of the indexed column, or None if selection is invalid.
     """
    names = get_column_names( df, guess_name )

    if len(names) == 1:
        # If there is only one matching column, use it
        column_index = df.columns.tolist().index( names[0] ) 
        column_name = df.columns.values[ column_index ]
        
    else:
        #if there are multiple matching columns
        print( "The following column names were found: " )
        for idx, name in enumerate( names ):
            print(f"{idx}: {name}")
        # Prompt user for input
        user_index = int( input(prompt="Select the index of the column wanted: " ) )
        # Ensure the user_index is valid
        if 0 <= user_index <= len(names):
            column_index = df.columns.tolist().index( names[0] ) 
            column_name = df.columns.values[ column_index ]
        else:
            print( "Invalid index Selection." )
    return column_name

'''-----------------------------------------------------------------------'''