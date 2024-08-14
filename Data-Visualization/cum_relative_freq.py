'''                                                    '''
'''Program cum_relative_frequency                      '''
'''                                                    '''
'''This program comuptes the cumulative percentage
    for a given Independent Variable for a pandas 
    dataframe object.                                  '''

# Import statements
import pandas as pd       # Required for dataframe
import os                 # Required for path confimation
import math               # Required for PI
import numpy as np

def cum_relative_freq(input_dataframe):

    data = input_dataframe
   
    # Create a new dataframe, Raidus & Area Column
    output_dataframe = pd.DataFrame(
        { 
        "Area": data["Area"],
        # A = PI * r^2; r = (A/PI) ^2 (this is great but I think the formula for r should be r = sqrt(A/PI). The sqrt is already from the math library)
        "eff_radius": (data["Area"]/math.pi)**0.5
        }) 
    
    #Create Diameter Column
    output_dataframe["eff_diameter_microns"]=\
        output_dataframe["eff_radius"] * 2
       
    # Attempt to key the File_key from the input df
    try:
        output_dataframe["File_key"] = data["File_key"]
    # handle KeyError
    except KeyError:
        print('''KeyError value error excepted.
The input dataframe consist of one file.''')
    # Execue code when there is no error
    else:
        print('''Multiple files are in this input dataframe,
File_key column ADDED.''')
        
        
    # Sort the data: ascending order, effective diameter
    output_dataframe = output_dataframe.sort_values(
        by="eff_diameter_microns")

    # Create a list of sorted values 
    eff_diameter_ls = list(
        output_dataframe["eff_diameter_microns"]
        )
    # Debugging:
    # print("Sorted list, \n", eff_diameter_ls)
    
    # Calaculate Frequency of each event outcome 
    keys = list()
    freq = list()

    for i in range( len(eff_diameter_ls) ):
        if eff_diameter_ls[i] in keys:
            index = keys.index(eff_diameter_ls[i])
            freq[index] += 1
            freq += [0]
        else: 
            keys.append(eff_diameter_ls[i])
            freq += [1]

    # Debugging: Display keys and freq lists
    # print("\nUnique keys list: ", keys)
    # print("\nFrequecy of the outcomes (handling repeats): ",
    #     freq )
    # print("Length of freq list: ", len(freq) )

    # Count total particles
    total_particles = len(eff_diameter_ls)
    print("\ntotal_particles: ", total_particles)

    # Calculate Cumulative Frequency based of the Frequency 
    cum_freq2 = []

    for j in range( total_particles ):
        # if the list has one element in
        if len(cum_freq2) > 0: 
            cum_freq2.append(freq[j] + cum_freq2[j - 1] )
        # else the list must be empty 
        else: 
            cum_freq2.append(freq[j])


    # # Original cumulative relative frequency
    # cum_freq1 = np.arange(1, total_particles +1)
    # print("cum_freq1: ", cum_freq1)
    # cumulative_relative_freq1 = (cum_freq1/total_particles)*100 
    # print("\nOriginal cumulative percentage particle: ",
    #       cumulative_relative_freq1 )

    # Compute cumulative percentage for each particle,
    #   Accounting for repeats
    # print("\ncum_freq2: ", cum_freq2)
    cum_rel_freq2 = (np.array(cum_freq2)/total_particles)*100
    print("New cumulative percentage particle:\n",
        cum_rel_freq2 )
    
    # Add calculated lists to output dataframe
    output_dataframe["cumulative_frequency"] = cum_freq2
    output_dataframe["cumulative_percentage"] = cum_rel_freq2

    # Particle Number Column, sorted by size (ascending)
    output_dataframe["Particle_number"]= np.arange(1, 
                                    total_particles + 1)
    return output_dataframe
        
