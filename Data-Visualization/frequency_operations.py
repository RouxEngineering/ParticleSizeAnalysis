'''                                                                       '''
'''Program frequency_operations                                           '''
'''                                                                       '''
''' There a four functions in this file:
1. Calculate cumulative frequency for a given column
- This file used the method of finding the frequency
    of each (diameter) outcome in the input pandas dataframe.
2.  Add the cumulative frequency to dataframe 
3. Compute cumulative percentage for each particle, 
    Accounting for repeats
4. Add cumulative percentage to dataframe                                 '''


# Note: suffix will denote the target column that all
#  subsequent functions are based off of 


# Import statements
import pandas as pd       # Required for dataframes
import numpy as np        # Required for numpy arrays

# 1. Calculate cumulative frequency for a given 
# column (target_column)
def compute_cumulative_freqency( DataFrame, target_column_name ):
    df = DataFrame.copy() # Create a new Dataframe to avoid modifying input 
    
    try:
        df[str(target_column_name)]
    except KeyError:                                    # handle KeyError
        print(f'''A KeyError has occured: {KeyError}. 
Target column, {target_column_name}, DOESN'T exist.\n''')
    else:                                               # No error, code block
        print('''Target column exist.\n''')

    # Sort the input dataframe passed into the function asending order ( modify in place)
    df.sort_values( by=str(target_column_name), inplace=True) 

    # Create a list of sorted values 
    column_content_list = list( df[target_column_name] )

    # Debugging:
    print( df[target_column_name] )
    # print("\nSorted list, \n",column_content_list)
    
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

    # # Debugging: Display keys and freq lists
    # print("\nUnique keys list: \n",keys)
    # print("\nFrequecy of the outcomes (handling repeats):\n",
    #     freq )
    # print("Length of freq list:\n", len(freq) )

    # Count total particles
    total_elements = len( column_content_list )
    print("\ntotal_particles: ", total_elements)

    # Add particle number col, [)
    df["Particle_number"]= np.arange(1, total_elements+1)      

    # Calculate Cumulative Frequency based of the Frequency 
    cumulative_frequency = []
    
    for j in range( total_elements ):
        if len(cumulative_frequency) > 0:       # if list at least one element
            cumulative_frequency.append(
                freq[j] + cumulative_frequency[j - 1])
        else:                            # else the list must be empty 
            cumulative_frequency.append(freq[j])
    
    return df, cumulative_frequency, total_elements  # Return the modified DataFrame



#2. Add the cumulative frequency to dataframe 
def add_cumulative_frequency( DataFrame, target_column_name, suffix ):
    # Add the cumulative frequency column to dataframe
    df, cum_freq, total_elements = compute_cumulative_freqency( DataFrame, target_column_name )

    if df is not None:  # Ensure the dataframe is value 
        df[f"cumulative frequency {suffix}"] = cum_freq

    return df




# 3. Compute cumulative percentage for each particle, 
#       Accounting for repeats
def compute_cumulative_percentage( DataFrame, target_column_name):
    df = DataFrame
    # Grab cumulative frequency (array) and total particle (int)
    df, cumulative_freq, total_particles = compute_cumulative_freqency( df, 
                                                            target_column_name)
    cumulative_percentage = (np.array(cumulative_freq)/total_particles)*100
    
    # print("New cumulative percentage particle:\n",
    #     cumulative_percentage )
    
    return cumulative_percentage



# 4. Add cumulative percentage to dataframe
def add_cumulative_percentage(DataFrame, target_column_name, column_suffix ): 
    df =DataFrame
    # Add cumulative percentage array to input dataframe
    cum_per = compute_cumulative_percentage( df, target_column_name )
    df[f"cumulative_%_particle {column_suffix}"] = cum_per  

    return df

