# %% [markdown]
# # This file will Visualize FlowCam Exported Data 

# %%
# Import Libraries, packages, and modules
import os
import pandas as pd
import plotly.express as px
from frequency_operations import *
from sphericity_operations import add_sphericity

# %%
# create filepath and verify file exist
flowcam_filepath = "/Users/Daniel/Desktop/Full_Results_of_R02_2024_07_16.csv"

if os.path.isfile(flowcam_filepath): 
    print("FlowCam file path is a file:")
    print( flowcam_filepath.split("/")[-1] )    # Use string method to show output file

else:
    print("Error please provide a valid file path.")

# %% [markdown]
# ## Create a pandas dataframe

# File not encoded with UFT-8

# Try to open file with decoding method "ISO-8859-1" (latin1)
method = "latin1"   
try: 
    df = pd.read_csv( flowcam_filepath, encoding= method )
except UnicodeDecodeError:
    print( "The file could not be decoded with {method} encoding. Try another encoding.".format(method) )

print( f"This dataframe has a shape of {df.shape}.\n" )

# %% [markdown]
# Information about the dataframe

# Check data types
df.dtypes

# Create a list of all column names in relavent dataframe
column_names = df.columns.tolist()
print(column_names)


# %% [markdown]
# #### Find index of relavent columns

# %%

# Grab index & name for a specific columns

# Area 
area_filled_index = column_names.index("Area (Filled) (µm²)")
area_column_name = column_names[ area_filled_index ]
print( "area column: ", area_column_name )

# Perimeter
perimeter_index = column_names.index("Perimeter (µm)")
perimeter_column_name = column_names[ perimeter_index ]
print( "perimeter column: ", perimeter_column_name )

# Diameter
diameter_abd_index = column_names.index("Diameter (ABD) (µm)")
diameter_abd_column_name = column_names[ diameter_abd_index ]
print(  "effective diameter column: ", diameter_abd_column_name )

# %% [markdown]
# ### Effecive Diameter

# %% [markdown]
# #### Determine cumulative frequency for Eff. Diameter 

# %%

diameter_data = add_cumulative_frequency(
    DataFrame= df,
    target_column_name= diameter_abd_column_name,
    suffix="dia"
)
print("\nAdded Diamter-cumulative frequency column\n")

print("new dataframe has shape: ", diameter_data.shape )

# %% [markdown]
# #### Determine cumulative percentage for Effective Diameter


# %%

diameter_data = add_cumulative_percentage(
    DataFrame= diameter_data,
    target_column_name= diameter_abd_column_name,
    column_suffix=""
)
print("\nAdded Diamter-cumulative percentage column\n")

diameter_data.head()


# %% [markdown]
# ### Sphericity

# %% [markdown]
# #### Add sphericity column
# import from the correct files!

# from sphericity_operations import build_sphericity_metrics_dataframe

def build_sphericity_metrics_dataframe( Dataframe, area_col_name, perimeter_col_name, target_col_name, suf):
    from frequency_operations import add_cumulative_frequency, add_cumulative_percentage
    Dataframe = add_sphericity(
        df = Dataframe,
        area_column_name = area_col_name,
        perim_column_name= perimeter_col_name)
    new_df = add_cumulative_frequency(
         DataFrame= df,
         target_column_name= target_col_name,
         suffix= suf
         )
    new_df = add_cumulative_percentage(
        DataFrame= new_df,
        target_column_name= target_col_name,
        column_suffix= suf
        )
    return new_df

new_sphericity_dataframe = build_sphericity_metrics_dataframe( 
    Dataframe=df, 
    area_col_name= area_column_name,
    perimeter_col_name= perimeter_column_name,
    target_col_name= "Sphericity",
    suf = "sph")

new_sphericity_dataframe.head()

print("\nAdded Sphericity column\n")
print("\nAdded sphericity-cumulative frequency column\n")
print("\nAdded sphericity-cumulative percentage column\n")

# %% [markdown]
# ## Plots

# %%
print( "columns in daimeter dataframe:\n", diameter_data.columns[-10:] )
print("columns in sphericity datafram:\n", new_sphericity_dataframe.columns[-10:])

# %% [markdown]
# ### Relational plots
# * To add text would require plotly.go

# %%
# Figure 1: Count (percentage) vs Effective Diameter

# Scatter plot 
fig1 = px.scatter(
    diameter_data,
    # Create trace 1
    x = diameter_abd_column_name,
    y = diameter_data.columns[-1], 
    # Customize figure    
    height=400,
    width=600,
    hover_name= "Particle_number",
    title="Cumulative Percentage (particle) vs. Effective Diameter (µm)",
    color = diameter_data.columns[0],
    labels={
        diameter_data.columns[-1]: "Cumulative Percentage (%)",
        diameter_abd_column_name: "Effective Diameter (µm)",
        diameter_data.columns[0]: "Powder:",
            }
                )

# Add a line plot: trace 2
fig1.add_scatter(
                 x= diameter_data[ diameter_abd_column_name ],
                 y =diameter_data[ diameter_data.columns[-1] ] ,
                 mode='lines',
                 showlegend=True,
                 )


# Customize Legend 
# Apply updates to each trace (method)
newnames = { fig1.data[0].name:"Virgin Ti-6Al-4V Run #2",
            fig1.data[1].name: "Line Plot - Virgin Ti-6Al-4V Run #2"} # keep the second trace the same 
# print("Before updating Figure 1 trace(s):\n", fig1.data) # debugging
fig1.for_each_trace( 
    lambda trace: # lambda arguments: expression
        trace.update( 
            # trace properties 
            name = newnames[trace.name], # acess the value stored in current trace key
            legendgroup = newnames[trace.name], 
                    )) 

print("Trace name: ", fig1.data[0].name )
print("Legend group: ", fig1.data[0].legendgroup )
print("Hover template: ", fig1.data[0].hovertemplate ) # keep the same for now
# print("\nAfter updating Figure 1 trace(s):\n", fig1.data) # Debugging

# Change Figure layout
fig1.update_layout(
    # figure color
    {'plot_bgcolor': 'white',   # inside axes
    'paper_bgcolor': 'white',   # outside axes 
    'font_family': 'Calibre',
    },  
    # Axes
    xaxis = dict(ticks = "outside", 
                 tickcolor="black",
                 showgrid=False,
                 zeroline=False,
                 # axes lines
                 showline=True, linecolor="black",linewidth=1,
                 #ticks
                 range = [0, 300],
                 dtick = 10),
    yaxis = dict(ticks = "outside", 
                tickcolor="black",
                showgrid=False,
                zeroline=False,
                showline=True, linecolor="black",linewidth=1,
                # ticks
                range= [0,100],),
    legend=dict( # update legend orienntation & position
        orientation="v", 
        x=1,
        y=0,
        yanchor="bottom",
        xanchor="right",
    ),
    )

fig1.show()


# %%
# print( sph_data.columns[9] )

# %%
# Figure 2: Count (percentage) vs Sphericity

# Scatter plot
fig2 = px.scatter(
    new_sphericity_dataframe,
    x = "Sphericity",
    y = new_sphericity_dataframe.columns[-1],
    # customize figure
    height=400,
    width=600,
    hover_name= "Particle_number",
    title="Cumulative Percentage (particle) vs. Sphericity (unitless)", 
    color= new_sphericity_dataframe[ new_sphericity_dataframe.columns[0] ],
    labels = {
        new_sphericity_dataframe.columns[-1]: "Cumulative Percentage (%)",
        new_sphericity_dataframe.columns[-4]: "Sphericity (unitless)",
        "Name": "Powder",
        }
                )

# Add line plot
fig2.add_scatter(
                x= new_sphericity_dataframe[ "Sphericity" ],
                 y =new_sphericity_dataframe[ new_sphericity_dataframe.columns[-1] ] ,
                 mode='lines',
                 showlegend=True,
)

# Update Legend
for idx, name in enumerate([ "Virgin Ti-6Al-4V Run #2", "Line Plot - Virgin Ti-6Al-4V Run #2" ]):
    fig2.data[idx].name = name
    fig2.data[idx].legendgroup = name
    # fig2.data[idx].hovertemplate = name

# Figure 2 layout
fig2.update_layout(
    # Transparent background
    {'plot_bgcolor': 'white',   
    'paper_bgcolor': 'white',
    'font_family': 'Calibre',
    }, 
    xaxis = dict(ticks = "outside", 
                 tickcolor="black",
                 showgrid=False,
                 zeroline=False,
                 # axes lines
                 showline=True, linecolor="black",linewidth=1,
                 #range
                 range=[0, 1.0],),
    yaxis = dict(ticks = "outside", 
                tickcolor="black",
                showgrid=False,
                zeroline=False,
                showline=True, linecolor="black",linewidth=1,
                # range
                range= [0, 100],),
    legend=dict( # update legend orienntation & position
        orientation="v", 
        x=0,
        y=1,
        yanchor="top",
        xanchor="left",
    ),
)

fig2.show()


# %% [markdown]
# ### Distributional Plots

# %% [markdown]
# #### Histograms

# %%
# Figure 3: Histogram of effective diameter
fig3 = px.histogram(
    diameter_data, 
    x= diameter_abd_column_name,
    nbins = 40,
    # customize figure
    height=400,
    width=600,
    text_auto=True, # marginal="rug",
    title="Histogram of Virgin Ti-6Al-4V Powder Effective Diameter (µm)",
    color = diameter_data[ diameter_data.columns[0] ],
    labels ={
        diameter_abd_column_name: "Effective Diameter (µm)",
    },
)

# Update traces
fig3.update_traces(
    marker_line_width=0.1,
    marker_line_color="black",
    name = "Virgin Ti-6Al-4V Run #2"
    )

# update Layout
fig3.update_layout(
    {'plot_bgcolor': 'white',   
    'paper_bgcolor': 'white',
    'font_family': 'Calibre',},
    xaxis=dict(
        # zeroline=True,
        showline=True, linecolor="black",linewidth=1,
        # ticks
        dtick = 10,
        range = [0, 280],
            ),
    yaxis=dict(
        showline=True, linecolor="black",linewidth=1,
    ),
    legend=dict( # update legend orienntation & position
        orientation="v", 
        x=1,
        y=1,
        yanchor="top",
        xanchor="right",
    ),
)


fig3.show()

# %%

# Figure 4: Histogram of Sphericity
fig4 = px.histogram(
    new_sphericity_dataframe, 
    x= "Sphericity",
    nbins = 38,
     # customize figure
    height=400,
    width=600,
    text_auto=True, # marginal="rug",
    title="Histogram of Virgin Ti-6Al-4V Sphericity (unitless)",
    color = new_sphericity_dataframe[ new_sphericity_dataframe.columns[0] ],
    labels ={
        "Sphericity": "Sphericity (unitless)",
        "Name": "Powder",
    },
)

# Update traces
fig4.update_traces(
    marker_line_width=0.1,
    marker_line_color="black",
    name = "Virgin Ti-6Al-4V Run #2"
    )

# update Layout
fig4.update_layout(
    {'plot_bgcolor': 'white',   
    'paper_bgcolor': 'white',
    'font_family': 'Calibre',},
    xaxis=dict(
        showline=True, linecolor="black",linewidth=1,
        # ticks
        dtick = 1/10,
        range = [0, 0.9],
            ),
    yaxis=dict(
        showline=True, linecolor="black",linewidth=1,
    ),
    legend=dict( # update legend orienntation & position
        orientation="v", 
        x=0, # gird area
        y=1,
        yanchor="top",  # top, left corner location
        xanchor="left",
    ),
    
)


fig4.show()
# %%
# Expect most virgin particles to have sizes >= 40, <= 100 microns
# Expect  resuse powders to be larger in size, and less sattelite particles (actually good): >= 45 , <= 150


