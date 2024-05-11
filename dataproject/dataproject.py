import pandas as pd
import pandasdmx as pdmx
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
import geopandas as gpd
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from IPython.display import HTML

def fetching_data_emplrate():
    """ Import data on employment rates """ 

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
    """ Import data on average hours worked per person employed """ 
    
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
    return "{:.2f}".format(value)

def table(emplrate, hours):
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