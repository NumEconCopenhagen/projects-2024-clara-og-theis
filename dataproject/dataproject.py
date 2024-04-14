import pandasdmx as pdmx
import pandas as pd

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

    return hours


