'''                                                    '''
'''Program plot_cumulative_percent                     '''
'''                                                    '''
'''This program uses Matplotlib.pyplot to graph the
 cumulative percentage for a given Independent Variable 
 from a pandas dataframe. 
 
 Note: The dataframe should be an output csv file 
 from PyImageJ: Analyze Particles function.            '''

import matplotlib.pyplot as plt
import pandas as pd

# Define a list of colors
pal = ["#45616F","#A74C5C","#CB7165","#3A3B46","#208E62"]

def plot_cumulative_percentage(
        x1, y1, 
        xTitle1= "None", yTitle1 = "None",
        x2=None, y2=None,
        xTitle2 ="None", yTitle2 = "None"
        ):
    
    # Define Figure and Properties:
    fig = plt.figure(figsize=(6,5))
    width = 0.6
    height = 0.5
    ax_bottom_left_ypos = 0.4
    ax_bottom_left_xpos = 0.15

    # Create axes and data
    if x2 is None and y2 is None: # do comparisoon
        print("1 Figure, 1 axes")
        print(type(x2), type(y2))
        # Add Figure axes
        ax = plt.axes([ax_bottom_left_xpos,  
                       ax_bottom_left_ypos,
                       width, 
                       height])
        # Add data to axes 
        ax.plot( x1, y1, pal[0], marker="o")
        # Set axes names 
        ax.set_xlabel(xTitle1)
        ax.set_ylabel(yTitle1)
        # Display plot
        plt.show()

    elif x2.all() and y2.all():
        print("1 Figure, 2 axes")
        
        # Add first axes
        ax1 = plt.axes([ax_bottom_left_xpos, 
                        ax_bottom_left_ypos,
                        width, 
                        height])
        # Add data to fist axes
        ax1.plot( x1, y1, pal[0])
        # Set first axes names
        ax1.set_xlabel(xTitle1)
        ax1.set_ylabel(yTitle1)

        # Add second axes    
        ax2 = plt.axes([ax_bottom_left_xpos + 0.7, 
                        ax_bottom_left_ypos,
                        width, 
                        height])
        # Add data to second axes
        ax2.plot( x2, y2, pal[1])
        # Ser second axes names
        ax2.set_xlabel(xTitle2)
        ax1.set_ylabel(yTitle2)
        # fig.
        fig.suptitle("Cumulative Percentage Plots",
                      ha= "left", fontsize=16)
        # Display plot
        plt.show()
    
    return fig
