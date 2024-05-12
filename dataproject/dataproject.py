import pandas as pd
import pandasdmx as pdmx
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
import geopandas as gpd
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from IPython.display import HTML

def fetching_data_emplrate():
    """ Import and clean data on employment rates """ 

    # Tell pdmx we want OECD data
    oecd = pdmx.Request("OECD")

    # Set out everything about the request in the format specified by the OECD API
    data_emplrate = oecd.data(
        resource_id="STLABOUR",
        key="AUS+AUT+BEL+CAN+CHL+COL+CRI+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LVA+LTU+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA.LREM64FE+LREM64MA+LREM64TT.STSA.A/all?startTime=2008&endTime=2022",
    ).to_pandas()

    emplrate = pd.DataFrame(data_emplrate).reset_index()

    # Drop measure and frequency
    emplrate.drop(['MEASURE', 'FREQUENCY'], axis=1, inplace=True) 

    # Rename 
    emplrate.rename(columns = {'TIME_PERIOD':'YEAR', 'value':'EMPLRATE'}, inplace=True)
    emplrate['SUBJECT'].replace({'LREM64FE': 'Female', 'LREM64MA': 'Male', 'LREM64TT': 'All'}, inplace=True)

    return emplrate

def fetching_data_hours():
    """ Import and clean data on average hours worked per person employed """ 
    
    # Tell pdmx we want OECD data
    oecd = pdmx.Request("OECD")
    
    # Set out everything about the request in the format specified by the OECD API
    data_hours = oecd.data(
        resource_id="PDB_LV",
        key="AUS+AUT+BEL+CAN+CHL+COL+CRI+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LVA+LTU+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA.T_HRSAV.PEHRS/all?startTime=2008&endTime=2022",
    ).to_pandas()

    hours = pd.DataFrame(data_hours).reset_index()

    # Drop subject and measure
    hours.drop(['SUBJECT', 'MEASURE'], axis=1, inplace=True) 

    # Rename 
    hours.rename(columns = {'TIME_PERIOD':'YEAR', 'value':'AVHRS'}, inplace=True)

    return hours

def format_float(value):
    """ Set format for decimals """ 

    return "{:.2f}".format(value)

def table(emplrate, hours):
    """ Create a table of descriptive statistics """ 

    def descriptive_stats(country, gender):
        pd.options.display.float_format = format_float
    
        # Filter data for the selected country and gender
        country_gender_data_empl = emplrate[(emplrate['LOCATION'] == country) & (emplrate['SUBJECT'] == gender)]
        country_data_hours = hours[hours['LOCATION'] == country]

        # Employment Rate statistics
        mean_emplrate = country_gender_data_empl['EMPLRATE'].mean()
        max_emplrate = country_gender_data_empl['EMPLRATE'].max()
        min_emplrate = country_gender_data_empl['EMPLRATE'].min()
        max_year_empl = country_gender_data_empl[country_gender_data_empl['EMPLRATE'] == max_emplrate]['YEAR'].iloc[0]
        min_year_empl = country_gender_data_empl[country_gender_data_empl['EMPLRATE'] == min_emplrate]['YEAR'].iloc[0]

        # Hours Worked statistics
        mean_hours = country_data_hours['AVHRS'].mean()
        max_hours = country_data_hours['AVHRS'].max()
        min_hours = country_data_hours['AVHRS'].min()
        max_year_hours = country_data_hours[country_data_hours['AVHRS'] == max_hours]['YEAR'].iloc[0]
        min_year_hours = country_data_hours[country_data_hours['AVHRS'] == min_hours]['YEAR'].iloc[0]

        # Prepare data for display
        stats_emplrate = pd.DataFrame({
            'Statistic': [
               'Mean Employment Rate', 'Max Employment Rate', 'Min Employment Rate'
            ],
            'Value': [
                mean_emplrate, max_emplrate, min_emplrate
            ],
            'Year': [
                '', max_year_empl, min_year_empl
            ]
        })

        stats_hours = pd.DataFrame({
            'Statistic': [
                'Mean Employment Rate', 'Max Employment Rate', 'Min Employment Rate'
            ],
            'Value': [
                mean_emplrate, max_emplrate, min_emplrate
            ],
            'Year': [
                '', max_year_empl, min_year_empl
            ]
        })

        # Display the DataFrames side by side
        html = (
            stats_emplrate.to_html(index=False) +
            "<br>" +
            stats_hours.to_html(index=False)
        )
        display(HTML(html))

    # Dropdown widget for country selection
    countries = emplrate['LOCATION'].unique()
    country_dropdown = widgets.Dropdown(options=countries, description='Country:')

    # Dropdown for gender selection
    gender_dropdown = widgets.Dropdown(options=['All', 'Male', 'Female'], value='All', description='Gender:')

    return widgets.interactive(descriptive_stats, country=country_dropdown, gender=gender_dropdown)


def worldmapemp(emplrate):
    """ Create a world map of employment rates """ 

    # Import world map data
    worldmap = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    def create_map_emplrate(gender):
        # Looking at employment rates in 2022
        emplrate_map = emplrate[(emplrate['SUBJECT'] == gender) & (emplrate['YEAR'] == '2022')]

        # Merge employment rate data and world map data
        mapdata_emplrate = pd.merge(worldmap, emplrate_map, how="left", left_on='iso_a3', right_on='LOCATION')

        # Plot the map
        fig, ax = plt.subplots(1, 1, figsize=(20, 16))
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="2%", pad="0.5%")
        mapdata_emplrate.plot(column="EMPLRATE", ax=ax, cax=cax, cmap='OrRd', legend=True, legend_kwds={"label": f"Employment rate in 2022 for {gender} (%)"}, missing_kwds={'color':'lightgrey'}, vmin=45, vmax=85)
        ax.set_title(f'Employment rate for OECD countries in 2022', size=20)
        plt.show()

    # Dropdown menu 
    gender_dropdown = widgets.Dropdown(options=['All', 'Male', 'Female'], value='All', description='Gender:')
    
    return widgets.interactive(create_map_emplrate, gender=gender_dropdown)

def worldmaphours(hours):
    """ Create a world map of average hours worked per person employed """ 

    # Import world map data
    worldmap = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Looking at working hours in 2022
    hours_map = hours[hours['YEAR'] == '2022']

    # Merge employment rate data and world map data
    mapdata_hours = pd.merge(worldmap, hours_map, how="left", left_on='iso_a3', right_on='LOCATION')

    # Plot the map
    fig, ax = plt.subplots(1, 1, figsize=(20, 16))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2%", pad="0.5%")
    mapdata_hours.plot(column="AVHRS", ax=ax, cax=cax, cmap='OrRd', legend=True, legend_kwds={"label": f"Average working hours per person employed (hours per year)"}, missing_kwds={'color':'lightgrey'}, vmin=1400, vmax=2000)
    ax.set_title(f'Average working hours per person employed in OECD countries in 2022', size=20)
    plt.show()

def index(data_merged):
    """ Create an index for average hours worked per person employed """ 

    # Create the baseline and add it as a column to the dataset
    baseline_avhrs_2008 = data_merged[data_merged['YEAR'] == '2008'].groupby('LOCATION')['AVHRS'].first()
    data_merged['baseline_avhrs'] = data_merged['LOCATION'].map(baseline_avhrs_2008)

    # Compute the index
    data_merged['AVHRS_index'] = (data_merged['AVHRS'] / data_merged['baseline_avhrs'])*100

def plotacrosstime(data_merged):
    """ Plot the index across time """ 

    def time_plot(**kwargs):
        selected_locations = [location for location, value in kwargs.items() if value]
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(1, 1, 1)
        for location in selected_locations:
            ax.plot(data_merged[(data_merged['LOCATION'] == location) & (data_merged['SUBJECT'] == 'All')]['YEAR'], 
                    data_merged[(data_merged['LOCATION'] == location) & (data_merged['SUBJECT'] == 'All')]['AVHRS_index'], 
                    label=location)
        ax.set_xlabel('Year')
        ax.set_ylabel('Indexed average hours worked per person employed (2008 = 100)')
        ax.set_title('Indexed average hours worked per person employed across time')
        ax.legend()
        plt.show()

    # Create checkboxes for selecting LOCATION
    locations_checkbox = {location: widgets.Checkbox(value=(location == 'DNK' or i < 3), description=location) for i, location in enumerate(data_merged['LOCATION'].unique())}

    return widgets.interactive(time_plot, **locations_checkbox)

def scatterplot(data_merged):
    """ Creates a scatter plot of employment rates against working hours """

    # Create the figure
    plt.figure(figsize=(10, 6))
    plt.scatter(x=data_merged[(data_merged['SUBJECT'] == 'All') & (data_merged['YEAR'] == '2022')]['AVHRS'], 
                y=data_merged[(data_merged['SUBJECT'] == 'All') & (data_merged['YEAR'] == '2022')]['EMPLRATE'])

    plt.xlabel('Average hours worked per person employed (hours per year)')
    plt.ylabel('Employment rate (%)')
    plt.title('Scatter plot of employment rate against average working hours across OECD countries in 2022')

    # Annotate points with country names
    for index, row in data_merged[(data_merged['SUBJECT'] == 'All') & (data_merged['YEAR'] == '2022')].iterrows():
        plt.annotate(row['LOCATION'], (row['AVHRS'], row['EMPLRATE']))

    plt.show()

def barchart(data_merged):
    """ Creates a bar chart of employment rates for males and females, respectively """

    def update_plot(gender):
        plt.figure(figsize=(10, 6))
        
        # Filter data for the selected gender and year
        filtered_data = data_merged[(data_merged['YEAR'] == '2022') & (data_merged['SUBJECT'] == gender)]

        # Sort the data in descending order of employment rate
        sorted_data = filtered_data.sort_values(by='EMPLRATE', ascending=False)

        # Plotting the data
        plt.bar(sorted_data['LOCATION'], sorted_data['EMPLRATE'], color='skyblue')
        plt.bar(sorted_data[sorted_data['LOCATION'] == 'DNK']['LOCATION'], sorted_data[sorted_data['LOCATION'] == 'DNK']['EMPLRATE'], color='blue')
        
        plt.xlabel('Country')
        plt.ylabel('Employment Rate (%)')
        plt.title(f'{gender} Employment Rates in OECD Countries in 2022')
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
        plt.show()

    # Create dropdown menu for selecting gender
    gender_dropdown = widgets.Dropdown(options=['Male', 'Female'], value='Female', description='Gender:')

    return widgets.interactive(update_plot, gender=gender_dropdown)