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
def compute_cumulative_freqency( df, target_column ):
    try:
        df[str(target_column)]
    except KeyError:                                    # handle KeyError
        print(f'''KeyError value error. 
target column, {target_column}, DOESN'T exist.\n''')
    else:                                               # No error, code block
        print('''Target column exist.\n''')

    # Sort the input dataframe passed into the function asending order 
    df.sort_values( by=str(target_column), inplace=True) 

    # Create a list of sorted values 
    column_content_list = list( df[target_column] )

    # Debugging:
    print( df[target_column] )
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
    
    return cumulative_frequency, total_elements  # output a tuple 



#2. Add the cumulative frequency to dataframe 
def add_cumulative_frequency(df, target_column, suffix ):
    # Add the cumulative frequency column to dataframe
    cum_freq, total_elements = compute_cumulative_freqency( df, target_column )
    df[f"cumulative_frequency_{suffix}"] = cum_freq

    return df




# 3. Compute cumulative percentage for each particle, 
#       Accounting for repeats
def compute_cumulative_percentage(df, target_column):

    # Grab cumulative frequency (array) and total particle (int)
    cumulative_freq, total_particles = compute_cumulative_freqency(df, 
                                                            target_column)
    cumulative_percentage = (np.array(cumulative_freq)/total_particles)*100
    
    # print("New cumulative percentage particle:\n",
    #     cumulative_percentage )
    
    return cumulative_percentage



# 4. Add cumulative percentage to dataframe
def add_cumulative_percentage(df, target_column, column_suffix ): 

    # Add cumulative percentage array to input dataframe
    cum_per = compute_cumulative_percentage( df, target_column )
    df[f"cumulative_%_particle_{column_suffix}"] = cum_per  

    return df

