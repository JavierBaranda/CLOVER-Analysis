# -*- coding: utf-8 -*-
"""
===============================================================================
                 SUSTAINABLE MINI-GRID ANALYSIS FOR NYABIHEKE
===============================================================================
                            Most recent update:
                               28 August 2019
===============================================================================
Made by:
    
    Javier Baranda Alonso
    MSc in Sustainable Energy Futures 2018-2019
    javier.baranda-alonso18@imperial.ac.uk
===============================================================================
"""

# Import the Python packages utilised
import numpy as np
import pandas as pd
import math
import datetime
from itertools import cycle, islice
import matplotlib
import matplotlib.pyplot as plt
import os
import time
import collections
import seaborn as sns


# Import CLOVER scripts, available for dowload at: https://github.com/phil-sandwell/CLOVER
import sys
sys.path.insert(0, self.CLOVER_filepath+'/CLOVER-master/Scripts/Generation scripts/')
from Solar import Solar
from Diesel import Diesel
import sys
sys.path.insert(0, self.CLOVER_filepath + '/CLOVER-master/Scripts/Load scripts/')
from Load import Load
import sys
sys.path.insert(0, self.CLOVER_filepath + '/CLOVER-master/Scripts/Impact scripts/')
from Finance import Finance
import sys
sys.path.insert(0, self.CLOVER_filepath + '/CLOVER-master/Scripts/Impact scripts/')
sys.path.insert(0, self.CLOVER_filepath + '/CLOVER-master/Scripts/Conversion scripts')
from Conversion import Conversion
sys.path.insert(0, self.CLOVER_filepath + '/CLOVER-master/Scripts/Simulation scripts')
from Energy_System import Energy_System
sys.path.insert(0, self.CLOVER_filepath + '/CLOVER-master/Scripts/Optimisation scripts')
from Optimisation import Optimisation


class Analysis():
    def __init__(self):
        self.location = 'Refugee_Camp'
        self.CLOVER_filepath = '*****Introduce here your CLOVER folder location*****/CLOVER-master/'
        self.location_filepath = self.CLOVER_filepath + '/Locations/' + self.location
    
# =============================================================================
#                          SCRIPT DESCRIPTION
# =============================================================================
#
#    The following script is divided in a number of functions that use the
#    simulation and optimisation features available in CLOVER to model 
#    mini-grid systems. 
#
#    These functions obtain, manipulate and present specific outputs of 
#    this analysis in a graphic manner, saving the corresponding data in
#    different .csv files.
#
#    While this script performs different analyses and presents the results in
#    an automated manner, it is tailored to the purposes of the case study for
#    Nyabiheke and further modifications are required for its use in a different
#    location or for a different analysis.
#
#    For its use, first download CLOVER from: https://github.com/phil-sandwell/CLOVER
#    and follow the set up guide there included 
#   
#
# =============================================================================
#                           Simulation functions
# =============================================================================                          
#
#           * get_solaroutput (init_year)
#               Collect and save 15 years of solar irradiation from renewables.ninja 
#               for the selected location           
#
#           * get_loaddata (Loadtype)
#               Obtain data about the number of devices in use, hourly load by 
#               device and total load of the system on an hourly basis
# 
#           * simulate_system (PV_kWp, storage_kWh, Systype, Loadtype)
#               Perform a simulation with the chosen system inputs and saves outputs
#
#           * optimise_system (Systype, Loadtype, max_blackouts, Stepsize)
#               Perform an optimisation of the type of system/scenario selected and saves outputs           
# 
# =============================================================================

# Define the colour palet that will be used for all figures:
mypalet=['lightseagreen','darkcyan','lightsalmon','palevioletred','steelblue','cornflowerblue','orchid','yellowgreen','gold','burlywood']

def get_solaroutput (init_year):

    """        
    Collect and save 15 years of solar irradiation from renewables.ninja (https://www.renewables.ninja/)

    Input: Initial year 
    
    Output: .csv file with the hourly solar irradiation data of 15 years from the Initial year
    
    """
    # Indicate final year and period desired
    final_year = init_year + 14
    
    for i in range(init_year, final_year+1):
        
        #Save solar output from renewables.ninja for each year
        Solar().save_solar_output(i)
        
        print ('Solar output from year', i, 'saved.')
                
        # Delay 10 seconds to avoid block by renewables.ninja
        time.sleep(10)

    
    # Combine all single year solar outputs into a single file    
    Solar().total_solar_output(init_year)
    
    print ('Total solar output combined and saved.')
    
def get_loaddata (Loadtype):
    """
    Obtain data about the number of devices in use, hourly load by 
    device and total load of the system on an hourly basis

    Input: Load profile for the selected scenario, between 'InstitutionalBase', 'InstitutionalAdv', 'Mix1', 'Mix2'
    
    Output: Obtain number of devices, device load and total load hourly data
    
    """
    # Read the Devices.csv file containing devices information of the selected load scenario     
    filepath = self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Load/Devices.csv'    
    df_devices = pd.read_csv(filepath)    
    length = len(df_devices.index) 

    # Modify the number of devices existent according to the load scenario in Devices.csv    
    
    if Loadtype == 'Mix1' : # Corresponding to Scenario 1
        
        # Disable all loads                         
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider initial public and private loads        
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'
               
        # Consider initial private loads        
        for n in range(0, length) :           
                
            #Restore initial number of restaurants and salons
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,3] = 0
                df_devices.iat[n,4] = 0
                
            if df_devices.iat[n,7] == 'Commercial':

                df_devices.iat[n,5]= 0
                df_devices.iat[n,6]= 0
                
    elif Loadtype == 'Mix2' : # Corresponding to Scenario 2A
        
        # Disable all loads                        
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider initial loads       
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'
                      
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'
                   
        # Consider additional private loads              
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,1] = 'Y'           
            
            # Restore initial number of private loads
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,3] = 0
                df_devices.iat[n,4] = 0
                
            #Add an extra restaurant and salon
            if df_devices.iat[n,0] == 'Restaurant1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Salon1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Restaurant2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,0] == 'Salon2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,8] == 'Additional': #Add 2 bars and 2 popcorn shops
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'WeldingShop':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
            if df_devices.iat[n,7] == 'Commercial':

                df_devices.iat[n,5]= 0
                df_devices.iat[n,6]= 0
                

    elif Loadtype == 'Mix1Adv' : # Corresponding to Scenario 3
        
        # Disable all loads                         
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider Mix1 loads and advanced public loads, substitute HealthCentre for Hospital        
        for n in range(0, length):
            
            if df_devices.iat[n,8] == 'Advanced':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,0] == 'HealthCentre':
                df_devices.iat[n,1] = 'N'
                
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'     
                
            #Restore initial number of restaurants and salons
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,3] = 0
                df_devices.iat[n,4] = 0
                
            if df_devices.iat[n,7] == 'Commercial':

                df_devices.iat[n,5]= 0
                df_devices.iat[n,6]= 0


    elif Loadtype == 'Mix2Adv' : # Corresponding to Scenario 4
        
        # Disable all loads      
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider Mix1 loads, additional private loads and advanced public loads, substitute HealthCentre for Hospital       
        for n in range(0, length):
            
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,8] == 'Advanced':
                df_devices.iat[n,1] = 'Y'    
                
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,0] == 'HealthCentre':
                df_devices.iat[n,1] = 'N'


        # Consider additional private loads               
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,1] = 'Y'
            
            # Restore initial number of private loads
            if df_devices.iat[n,7] == 'Private':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                

            #Add an extra restaurant and salon
            if df_devices.iat[n,0] == 'Restaurant1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Salon1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Restaurant2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,0] == 'Salon2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,8] == 'Additional': #2 bars and 2 popcorn shops
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'WeldingShop':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
        # Consider doubled private loads of Scenario 2B
        for n in range(0, length) : 
            
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] *= 2.0
                df_devices.iat[n,4] *= 2.0

                df_devices.iat[n,5]= 0
                df_devices.iat[n,6]= 0
                
    elif Loadtype == 'Mix2B' : # Corresponding to Scenario 2B
        
        # Disable all loads                       
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider initial loads       
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'             
        
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'
                   
        # Consider additional private loads              
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,1] = 'Y'
            
            # Restore initial number of private loads
            if df_devices.iat[n,7] == 'Private':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                

            #Add an extra restaurant and salon
            if df_devices.iat[n,0] == 'Restaurant1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Salon1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Restaurant2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,0] == 'Salon2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,8] == 'Additional': #2 bars and 2 popcorn shops
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'WeldingShop':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
        # Duplicate the number of private loads in comparison with Scenario 2A        
        for n in range(0, length) : 
            
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] *= 2.0
                df_devices.iat[n,4] *= 2.0

                df_devices.iat[n,5]= 0
                df_devices.iat[n,6]= 0
                
    elif Loadtype == 'Mix1to2B' : # Corresponding to Approach A and Approach B
        
        # Disable all loads                         
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider initial loads        
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'
                   
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'
                   
        # Consider additional private loads               
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,1] = 'Y'
            

            # Restore initial number of private loads
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
            
            # No additional private loads initially
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,3] = 0.0                  

            #Add extra restaurant and salon
            if df_devices.iat[n,0] == 'Restaurant1':
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Salon1':
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Restaurant2':
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,0] == 'Salon2':
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,8] == 'Additional': #2 bars and 2 popcorn shops
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'WeldingShop':
                df_devices.iat[n,4] = 0.0003125
                
        
        for n in range(0, length) : 
            
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,4] *= 2.0
                df_devices.iat[n,4] += 0.0003125
                df_devices.iat[n,5]= 0.04
                df_devices.iat[n,6]= 0.5
        
    # Substitute new values in Scenario  Inputs.csv file for simulation
    df_devices.to_csv(filepath, index=None)
         
    # get the number of each device in the community on a given day
    Load().number_of_devices_daily()
    
    # get the daily utilisation profile (365x24 matrix) for each device
    Load().get_device_daily_profile()
    
    # generate the number of devices in use for each hour
    Load().devices_in_use_hourly()
    
    # Initialize values for cumulative public, private and household load
    total_load_public = list(np.zeros(131400))
    total_load_commercial = list(np.zeros(131400))    
    total_load_household = list(np.zeros(131400))    
    
    # get the load of each device, using the load obtained from the smart meter data:
    for n in range(0, length):
        
        # For each device considered in the corresponding scenario
        if df_devices.iat[n,1] == 'Y':
            
            # Name of device
            txt=df_devices.iat[n,0]
            
            # Number of devices
            filepath = self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Load/Devices in use/{}_in_use.csv'.format(txt)       
            Number_of_devices=pd.read_csv(filepath)       
           
            # For existent private loads
            if df_devices.iat[n,8] == 'Existent':
      
               # Read the hourly energy consumption data from the smart meter
               txt=df_devices.iat[n,0]   
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Hourly energy consumption data/{}_data.csv".format(txt)
               df1 = pd.read_csv(filepath)

               hourly_mean=pd.DataFrame(columns=['Hour','Power'], index=None)
               hourly_mean_x=pd.DataFrame(columns=['Hour','Power'], index=None)
               
               # Obtain the average load for every hour of the day (0,23)
               for i in range(0, 24):
    
                  df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[0]                 
                  dflocal = pd.DataFrame({"Hour":[i], 
                    "Power":[df_i]})       
                  
                  hourly_mean=pd.concat([hourly_mean, dflocal])
                  
                  # This part is used to calculate the total cumulative load                 
                  df_x = df_i                 
                  dflocal_x = pd.DataFrame({"Hour":[i], 
                    "Power":[df_x]})
                  
                  hourly_mean_x=pd.concat([hourly_mean_x, dflocal_x]) 
                  
            # For existent public loads (smart meter, get the hourly load)           
            elif df_devices.iat[n,8] == 'Base':
                               
               # Read the hourly energy consumption data from the smart meter    
               txt=df_devices.iat[n,0]
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Hourly energy consumption data/{}_data.csv".format(txt)
               df1 = pd.read_csv(filepath)

               hourly_mean=pd.DataFrame(columns=['Hour','Power'], index=None)
               hourly_mean_x=pd.DataFrame(columns=['Hour','Power'], index=None)
 
               # Obtain the average load for every hour of the day (0,23)          
               for i in range(0, 24):
    
                  df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[0]    
                  dflocal = pd.DataFrame({"Hour":[i], 
                    "Power":[df_i]})       
                  
                  hourly_mean=pd.concat([hourly_mean, dflocal])
                  
                  # This part is used to calculate the total cumulative load                 
                  df_x = df_i
                  dflocal_x = pd.DataFrame({"Hour":[i], 
                    "Power":[df_x]})                 
                  hourly_mean_x=pd.concat([hourly_mean_x, dflocal_x]) 
                  
            # If hospital is selected, calculate its load (same style than smart meter)                  
            elif df_devices.iat[n,0] == 'Hospital':

               # Read the hourly energy consumption data from the smart meter    
               txt=df_devices.iat[n,0]   
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Hourly energy consumption data/{}_data.csv".format(txt)
               df1 = pd.read_csv(filepath)

               hourly_mean=pd.DataFrame(columns=['Hour','Power'], index=None)
               hourly_mean_x=pd.DataFrame(columns=['Hour','Power'], index=None)

               # Obtain the average load for every hour of the day (0,23)               
               for i in range(0, 24):
    
                  df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[0]
                  
                  dflocal = pd.DataFrame({"Hour":[i], 
                    "Power":[df_i]})
        
                  hourly_mean=pd.concat([hourly_mean, dflocal])
                  
                  # This part is used to calculate the total cumulative load                 
                  df_x = df_i
                  dflocal_x = pd.DataFrame({"Hour":[i], 
                    "Power":[df_x]})                 
                  hourly_mean_x=pd.concat([hourly_mean_x, dflocal_x]) 
            
            # For produtive devices with non smart meter data, calculate the hourly load            
            elif df_devices.iat[n,8] == 'Additional':
            
               # Read the hourly energy consumption data from the smart meter    
               txt=df_devices.iat[n,0] 
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Hourly energy consumption data/{}_data.csv".format(txt)
               df1 = pd.read_csv(filepath)

               hourly_mean=pd.DataFrame(columns=['Hour','Power'], index=None)
               hourly_mean_x=pd.DataFrame(columns=['Hour','Power'], index=None)

               # Obtain the average load for every hour of the day (0,23)
               for i in range(0, 24):
    
                  df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]
                  dflocal = pd.DataFrame({"Hour":[i], 
                    "Power":[df_i]})
        
                  hourly_mean=pd.concat([hourly_mean, dflocal])
                  
                  # This part is used to calculate the total cumulative load                 
                  df_x = df_i
                  dflocal_x = pd.DataFrame({"Hour":[i], 
                    "Power":[df_x]})                 
                  hourly_mean_x=pd.concat([hourly_mean_x, dflocal_x])
               
            # For public devices with non smart meter data, calculate the hourly load                   
            elif df_devices.iat[n,8] == 'Advanced':
                
               # Read the hourly energy consumption data from the smart meter    
               txt=df_devices.iat[n,0]    
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Hourly energy consumption data/{}_data.csv".format(txt)
               df1 = pd.read_csv(filepath)

               hourly_mean=pd.DataFrame(columns=['Hour','Power'], index=None)
               hourly_mean_x=pd.DataFrame(columns=['Hour','Power'], index=None)

               # Obtain the average load for every hour of the day (0,23)
               for i in range(0, 24):
    
                  df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]
    
                  dflocal = pd.DataFrame({"Hour":[i], 
                    "Power":[df_i]})
        
                  hourly_mean=pd.concat([hourly_mean, dflocal])

                  # This part is used to calculate the total cumulative load                                          
                  df_x = df_i 
                  dflocal_x = pd.DataFrame({"Hour":[i], 
                    "Power":[df_x]})                
                  hourly_mean_x=pd.concat([hourly_mean_x, dflocal_x]) 
                  
               #CurrentLoad = np.add(public_hourly_mean['Power'], hourly_mean_x['Power'])
               #public_hourly_mean['Power'] = CurrentLoad
               
                  
            # Take device load file and repeat the total hourly load obtained until filled and save it
            filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/total_load.csv"  
            df_load = pd.read_csv(filepath)
    
            length = len(df_load.index)
            num=int(length/len(hourly_mean))
            df_singledevice_load = pd.concat([hourly_mean]*num, ignore_index=True) 
            intro=pd.DataFrame({"Hour":['NaN'], "Power":[1]})   
            singledevice_load = pd.concat([intro, df_singledevice_load], ignore_index=True)

            # Save the new device load file
            filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device Load/{}_load.csv".format(txt)
            singledevice_load.to_csv(filepath, index=None, header =None)
            
            # Calculate the total load corresponding to the number of devices existent
            totaldevice_load=Number_of_devices
            totaldevice_load['0']=np.multiply(df_singledevice_load['Power'],Number_of_devices['0'])

            # Add the total load from those devices to the total public or private cumulative load            
            if df_devices.iat[n,7] == 'Public':
                
               CurrentLoad = np.add(total_load_public, totaldevice_load['0'])
               total_load_public = CurrentLoad
                              
            if df_devices.iat[n,7] == 'Commercial':
                
               CurrentLoad = np.add(total_load_commercial, totaldevice_load['0'])
               total_load_commercial = CurrentLoad
               
    # Open previously generated total_load.csv file created by CLOVER         
    filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/total_load.csv"  
    df_load = pd.read_csv(filepath)
    
    length = len(df_load.index)
    num=int(length/len(hourly_mean))

    # Create the new total_load file to substitute the previously existing one   

    total_load = pd.DataFrame({'Domestic':[],'Commercial':[],'Public':[]})
    
    total_load['Domestic']=total_load_household
    total_load['Commercial']=total_load_commercial   
    total_load['Public']=total_load_public
    
    # Save the new total_load.csv file
    filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device Load/total_load.csv"
    total_load.to_csv(filepath, index=True)    

    print('All loads in use calculated, total load calculated and saved.')

    
    
def simulate_system (PV_kWp, storage_kWh, Systype, Loadtype):
   
    #! Need to complete Loadtype automation with load profiles/devices
    
    """
    Perform a simulation with the chosen system characteristics and saves outputs
    
    
    Input: PV and battery size in KWp (0 if diesel system)
           System type, between 'Diesel', 'Hybrid', or 'PVBatt'
           Load profile for the selected scenario, between 'Mix1', 'Mix2', 'Mix2B', 'Mix1Adv', 'Mix2Adv', 'Mix1to2B'
    
    Output:
        
    [1 rows x 7 columns] DataFrame
    
    	Start year / End year / Initial PV size / Initial storage size / Final PV size / Final storage size / Diesel capacity / System details	

    [Nofhours rows x 18 columns] DataFrame
    
    Load energy (kWh) / Total energy used (kWh) / Unmet energy (kWh) / Blackouts / 
    Renewables energy used (kWh) / Storage energy supplied (kWh) / Grid energy (kWh) / Diesel energy (kWh) /
    Diesel times / Diesel fuel usage (l) / Storage profile (kWh) / Renewables energy supplied (kWh) / Hourly storage (kWh) / Dumped energy (kWh) / Battery health / Households / Kerosene lamps / Kerosene mitigation


    """
    
    # Read the Devices.csv file containing devices information of the selected load scenario     
    filepath = self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Load/Devices.csv'    
    df_devices = pd.read_csv(filepath)    
    length = len(df_devices.index) 

    # Modify the number of devices existent according to the load scenario in Devices.csv    
    
    if Loadtype == 'Mix1' : # Corresponding to Scenario 1
        
        # Disable all loads                         
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider initial public and private loads        
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'
               
        # Consider initial private loads        
        for n in range(0, length) :           
                
            #Restore initial number of restaurants and salons
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,3] = 0
                df_devices.iat[n,4] = 0
                
            if df_devices.iat[n,7] == 'Commercial':

                df_devices.iat[n,5]= 0
                df_devices.iat[n,6]= 0
                
    elif Loadtype == 'Mix2' : # Corresponding to Scenario 2A
        
        # Disable all loads                        
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider initial loads       
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'
                      
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'
                   
        # Consider additional private loads              
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,1] = 'Y'           
            
            # Restore initial number of private loads
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,3] = 0
                df_devices.iat[n,4] = 0
                
            #Add an extra restaurant and salon
            if df_devices.iat[n,0] == 'Restaurant1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Salon1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Restaurant2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,0] == 'Salon2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,8] == 'Additional': #Add 2 bars and 2 popcorn shops
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'WeldingShop':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
            if df_devices.iat[n,7] == 'Commercial':

                df_devices.iat[n,5]= 0
                df_devices.iat[n,6]= 0
                

    elif Loadtype == 'Mix1Adv' : # Corresponding to Scenario 3
        
        # Disable all loads                         
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider Mix1 loads and advanced public loads, substitute HealthCentre for Hospital        
        for n in range(0, length):
            
            if df_devices.iat[n,8] == 'Advanced':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,0] == 'HealthCentre':
                df_devices.iat[n,1] = 'N'
                
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'     
                
            #Restore initial number of restaurants and salons
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,3] = 0
                df_devices.iat[n,4] = 0
                
            if df_devices.iat[n,7] == 'Commercial':

                df_devices.iat[n,5]= 0
                df_devices.iat[n,6]= 0


    elif Loadtype == 'Mix2Adv' : # Corresponding to Scenario 4
        
        # Disable all loads      
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider Mix1 loads, additional private loads and advanced public loads, substitute HealthCentre for Hospital       
        for n in range(0, length):
            
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,8] == 'Advanced':
                df_devices.iat[n,1] = 'Y'    
                
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,0] == 'HealthCentre':
                df_devices.iat[n,1] = 'N'


        # Consider additional private loads               
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,1] = 'Y'
            
            # Restore initial number of private loads
            if df_devices.iat[n,7] == 'Private':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                

            #Add an extra restaurant and salon
            if df_devices.iat[n,0] == 'Restaurant1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Salon1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Restaurant2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,0] == 'Salon2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,8] == 'Additional': #2 bars and 2 popcorn shops
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'WeldingShop':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
        # Consider doubled private loads of Scenario 2B
        for n in range(0, length) : 
            
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] *= 2.0
                df_devices.iat[n,4] *= 2.0

                df_devices.iat[n,5]= 0
                df_devices.iat[n,6]= 0
                
    elif Loadtype == 'Mix2B' : # Corresponding to Scenario 2B
        
        # Disable all loads                       
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider initial loads       
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'             
        
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'
                   
        # Consider additional private loads              
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,1] = 'Y'
            
            # Restore initial number of private loads
            if df_devices.iat[n,7] == 'Private':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                

            #Add an extra restaurant and salon
            if df_devices.iat[n,0] == 'Restaurant1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Salon1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Restaurant2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,0] == 'Salon2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,8] == 'Additional': #2 bars and 2 popcorn shops
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'WeldingShop':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
        # Duplicate the number of private loads in comparison with Scenario 2A        
        for n in range(0, length) : 
            
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] *= 2.0
                df_devices.iat[n,4] *= 2.0

                df_devices.iat[n,5]= 0
                df_devices.iat[n,6]= 0
                
    elif Loadtype == 'Mix1to2B' : # Corresponding to Approach A and Approach B
        
        # Disable all loads                         
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider initial loads        
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'
                   
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'
                   
        # Consider additional private loads               
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,1] = 'Y'
            

            # Restore initial number of private loads
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
            
            # No additional private loads initially
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,3] = 0.0                  

            #Add extra restaurant and salon
            if df_devices.iat[n,0] == 'Restaurant1':
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Salon1':
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Restaurant2':
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,0] == 'Salon2':
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,8] == 'Additional': #2 bars and 2 popcorn shops
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'WeldingShop':
                df_devices.iat[n,4] = 0.0003125
                
        
        for n in range(0, length) : 
            
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,4] *= 2.0
                df_devices.iat[n,4] += 0.0003125
                df_devices.iat[n,5]= 0.04
                df_devices.iat[n,6]= 0.5
                
                
    # Substitute new values in Scenario  Inputs.csv file for simulation
    df_devices.to_csv(filepath, index=None)
        
    # Simulate chosen system in CLOVER on hourly basis for the chosen period
    SysSimulation = Energy_System().simulation(0, 14, PV_kWp, storage_kWh)
        
    # Perform system appraisal (technical, environmental, financial) of simulated system
    AppraisalResults = Optimisation().system_appraisal(SysSimulation)    

                
    # Obtain reliability of system for identifying the saved simulation (0-100)
    filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Scenario/Scenario inputs.csv"    
    df_scenario = pd.read_csv(filepath, header=None)
    Reliability = int((1.0 - float(df_scenario.iat[3,1]))*100.0)  
    
    # Save the outputs from the simulation
    Simulation_Name = 'Sim_PV{}_Storage{}_{}_Re{}_Load{}'.format(PV_kWp, storage_kWh, Systype, Reliability, Loadtype)
    Energy_System().save_simulation(SysSimulation, Simulation_Name)
    
    # Save appraisal results together with optimisation
    Appraisal_Name = 'Sim_PV{}_Storage{}_{}_Re{}_Load{}_Appraisal.csv'.format(PV_kWp, storage_kWh, Systype, Reliability, Loadtype)
    Appraisal_Filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV{}_Storage{}_{}_Re{}_Load{}_Appraisal.csv".format(PV_kWp, storage_kWh, Systype, Reliability, Loadtype) 
    AppraisalResults.to_csv(Appraisal_Filepath)
    
    print('\n Appraisal of simulated system saved as', Appraisal_Name, '\n')
    
def optimise_system (Systype, Loadtype, max_blackouts, Stepsize):  
    
    """
    Perform an optimisation of the type of system/scenario selected and saves outputs
    
    Input: 
           System type, between 'Diesel', 'Hybrid', or 'PVBatt'
           Load profile for the selected scenario, between 'InstitutionalBase', 'InstitutionalAdv', 'Mix1', 'Mix2'
           Maximum fraction of blackouts allowed
           Step size of PV and battery capacity for optimization (in kWp or kWh)

    Output:
        
    [3 rows x 45 columns] DataFrame
    
    	Start year / End year / Initial PV size / Initial storage size / Final PV size / Final storage size / Diesel capacity
        Culative cost ($) / Cumulative system cost ($)
        Cumulative GHGs (kgCO2eq) / Cumulative system GHGs (kgCO2eq)
        Cumulative energy (kWh) / Cumulative discounted energy (kWh)
        LCUE ($/kWh) / Emissions intensity (gCO2/kWh)
        Blackouts / Unmet energy fraction/Renewables fraction
        Total energy (kWh) / Unmet energy (kWh) 
        Renewable energy (kWh) / Storage energy (kWh) / Grid energy (kWh) / Diesel energy (kWh) / Discounted energy (kWh)
        Kerosene displacement / Diesel fuel usage (l)
        Total cost ($) / Total system cost ($) / New equipment cost ($) / New connection cost ($) / O&M cost ($) / Diesel cost ($) / Grid cost ($) / Kerosene cost ($) / Kerosene cost mitigated ($)
        Total GHGs (kgCO2eq) / Total system GHGs (kgCO2eq) / New equipment GHGs (kgCO2eq) / New connection GHGs (kgCO2eq) / O&M GHGs (kgCO2eq) / Diesel GHGs (kgCO2eq) / Grid GHGs (kgCO2eq) / Kerosene GHGs (kgCO2eq) / Kerosene GHGs mitigated (kgCO2eq)
    
    """    
    # Read the Devices.csv file containing devices information of the selected load scenario     
    filepath = self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Load/Devices.csv'    
    df_devices = pd.read_csv(filepath)    
    length = len(df_devices.index) 

    # Modify the number of devices existent according to the load scenario in Devices.csv    
    
    if Loadtype == 'Mix1' : # Corresponding to Scenario 1
        
        # Disable all loads                         
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider initial public and private loads        
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'
               
        # Consider initial private loads        
        for n in range(0, length) :           
                
            #Restore initial number of restaurants and salons
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,3] = 0
                df_devices.iat[n,4] = 0
                
            if df_devices.iat[n,7] == 'Commercial':

                df_devices.iat[n,5]= 0
                df_devices.iat[n,6]= 0
                
    elif Loadtype == 'Mix2' : # Corresponding to Scenario 2A
        
        # Disable all loads                        
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider initial loads       
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'
                      
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'
                   
        # Consider additional private loads              
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,1] = 'Y'           
            
            # Restore initial number of private loads
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,3] = 0
                df_devices.iat[n,4] = 0
                
            #Add an extra restaurant and salon
            if df_devices.iat[n,0] == 'Restaurant1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Salon1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Restaurant2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,0] == 'Salon2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,8] == 'Additional': #Add 2 bars and 2 popcorn shops
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'WeldingShop':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
            if df_devices.iat[n,7] == 'Commercial':

                df_devices.iat[n,5]= 0
                df_devices.iat[n,6]= 0
                

    elif Loadtype == 'Mix1Adv' : # Corresponding to Scenario 3
        
        # Disable all loads                         
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider Mix1 loads and advanced public loads, substitute HealthCentre for Hospital        
        for n in range(0, length):
            
            if df_devices.iat[n,8] == 'Advanced':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,0] == 'HealthCentre':
                df_devices.iat[n,1] = 'N'
                
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'     
                
            #Restore initial number of restaurants and salons
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,3] = 0
                df_devices.iat[n,4] = 0
                
            if df_devices.iat[n,7] == 'Commercial':

                df_devices.iat[n,5]= 0
                df_devices.iat[n,6]= 0


    elif Loadtype == 'Mix2Adv' : # Corresponding to Scenario 4
        
        # Disable all loads      
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider Mix1 loads, additional private loads and advanced public loads, substitute HealthCentre for Hospital       
        for n in range(0, length):
            
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,8] == 'Advanced':
                df_devices.iat[n,1] = 'Y'    
                
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,1] = 'Y'
                
            if df_devices.iat[n,0] == 'HealthCentre':
                df_devices.iat[n,1] = 'N'


        # Consider additional private loads               
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,1] = 'Y'
            
            # Restore initial number of private loads
            if df_devices.iat[n,7] == 'Private':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                

            #Add an extra restaurant and salon
            if df_devices.iat[n,0] == 'Restaurant1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Salon1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Restaurant2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,0] == 'Salon2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,8] == 'Additional': #2 bars and 2 popcorn shops
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'WeldingShop':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
        # Consider doubled private loads of Scenario 2B
        for n in range(0, length) : 
            
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] *= 2.0
                df_devices.iat[n,4] *= 2.0

                df_devices.iat[n,5]= 0
                df_devices.iat[n,6]= 0
                
    elif Loadtype == 'Mix2B' : # Corresponding to Scenario 2B
        
        # Disable all loads                       
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider initial loads       
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'             
        
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'
                   
        # Consider additional private loads              
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,1] = 'Y'
            
            # Restore initial number of private loads
            if df_devices.iat[n,7] == 'Private':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                

            #Add an extra restaurant and salon
            if df_devices.iat[n,0] == 'Restaurant1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Salon1':
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Restaurant2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,0] == 'Salon2':
                df_devices.iat[n,3] = 0.0009375
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,8] == 'Additional': #2 bars and 2 popcorn shops
                df_devices.iat[n,3] = 0.000625
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'WeldingShop':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
                
        # Duplicate the number of private loads in comparison with Scenario 2A        
        for n in range(0, length) : 
            
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] *= 2.0
                df_devices.iat[n,4] *= 2.0

                df_devices.iat[n,5]= 0
                df_devices.iat[n,6]= 0
                
    elif Loadtype == 'Mix1to2B' : # Corresponding to Approach A and Approach B
        
        # Disable all loads                         
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider initial loads        
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'
                   
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Existent':
                df_devices.iat[n,1] = 'Y'
                   
        # Consider additional private loads               
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,1] = 'Y'
            

            # Restore initial number of private loads
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,3] = 0.0003125
                df_devices.iat[n,4] = 0.0003125
            
            # No additional private loads initially
            if df_devices.iat[n,8] == 'Additional':
                df_devices.iat[n,3] = 0.0                  

            #Add extra restaurant and salon
            if df_devices.iat[n,0] == 'Restaurant1':
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Salon1':
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'Restaurant2':
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,0] == 'Salon2':
                df_devices.iat[n,4] = 0.0009375
                
            if df_devices.iat[n,8] == 'Additional': #2 bars and 2 popcorn shops
                df_devices.iat[n,4] = 0.000625
                
            if df_devices.iat[n,0] == 'WeldingShop':
                df_devices.iat[n,4] = 0.0003125
                
        
        for n in range(0, length) : 
            
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,4] *= 2.0
                df_devices.iat[n,4] += 0.0003125
                df_devices.iat[n,5]= 0.04
                df_devices.iat[n,6]= 0.5
         
        
    # Substitute new values in Scenario Inputs Devices.csv file for simulation
    df_devices.to_csv(filepath, index=None)
    
    # Locate and open Optimisation inputs file
    filepathopt = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Optimisation inputs.csv"   
    df_optimisation = pd.read_csv(filepathopt, header=None)
    
    # Set stepsize of optimisation
    df_optimisation.iat [8,1] = Stepsize
    df_optimisation.iat [4,1] = Stepsize
    
    # Set reliability (blackout threshold) for optimisation
    df_optimisation.iat[11,1] = max_blackouts
    
    # Define reliability of system for identifying the saved files
    Reliability = int((1.0 - max_blackouts)*100.0) 
    
    # Find  previous optimization for the closest lower reliability level
    # This is done to reduce the optimisation computing time by starting from a system size closer to the final optimum one

    # For reliabilities (0-100) starting backwards from the desired reliability level:
    for Previous_Reliability in range(Reliability,0,-1):
    
        # Check if optimisation exists
        previousopt_filepath=self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved Optimisations/Opt_{}_Re{}_Load{}.csv'.format(Systype, Previous_Reliability, Loadtype)
        check = os.path.exists(previousopt_filepath) 
    
        if check == True :
           
            # Obtain the PV and storage sizes for that optimization   
            df_previousopt = pd.read_csv(previousopt_filepath, header=None)
            Min_PVsize = df_previousopt.iat[1,3]
            Min_Battsize = df_previousopt.iat[1,4]
    
            # Substitute values in Optimisation inputs:
            df_optimisation.iat [6,1] = Min_Battsize
            df_optimisation.iat [2,1] = Min_PVsize             
            
            break
           
    # Substitute new values in Optimisation inputs.csv file for optimisation
    df_optimisation.to_csv(filepathopt, index=None, header =None)
    
    # Define an initial system with 0 PV, 0 Storage and 13kW of diesel, as installed in Nyabiheke now   
    initial_sys = pd.DataFrame({'Final PV size':0.0,
                                            'Final storage size':0.0,
                                            'Diesel capacity':13,
                                            'Total system cost ($)':0.0,
                                            'Total system GHGs (kgCO2eq)':0.0,
                                            'Discounted energy (kWh)':0.0,
                                            'Cumulative cost ($)':0.0,
                                            'Cumulative system cost ($)':0.0,
                                            'Cumulative GHGs (kgCO2eq)':0.0,
                                            'Cumulative system GHGs (kgCO2eq)':0.0,
                                            'Cumulative energy (kWh)':0.0,
                                            'Cumulative discounted energy (kWh)':0.0,
                                            },index=['System results'])
      
    # Optimise system for the chosen period
    SysOptimisation = Optimisation().multiple_optimisation_step(previous_systems=initial_sys)
    
    # Save the outputs from the optimisation
    Optimisation_Name = 'Opt_{}_Re{}_Load{}'.format(Systype, Reliability, Loadtype)
    Optimisation().save_optimisation(SysOptimisation,Optimisation_Name)
    
# =============================================================================
#                           Analysis functions
# =============================================================================   
#
# Load profiles
# 
#           * public_loadprofile (txt, Loadtype)
#               Obtain and present the average daily load profile of each public facility and total public load profile in the camp           
#
#           * private_loadprofile (txt, Loadtype)
#               Obtain and present the average daily load profile of each private business and the total private load profile of the camp           
# 
#           * total_loadprofile (Loadtype)
#               Obtain and present the average daily load profile of the combined public and private loads of the camp
#
#
# Systems Comparison
#
#           * diesel_sys_performance (max_blackouts, Loadtype)
#               Simulate performance of diesel-powered system for the selected scenario           
# 
#           * diesel_sys_stats (max_blackouts, Loadtype)
#               Present costs, GHGs, diesel consumption of diesel-powered system for the selected scenario        
# 
#           * hybrid_sys_performance (max_blackouts, Loadtype, accuracy)
#               Optimise and simulate the performance of a PV-battery-diesel system for the selected scenario           
# 
#           * hybrid_sys_stats (max_blackouts, Loadtype)
#               Present sys sizes, costs, GHGs, diesel consumption of PV-battery-diesel system for the selected scenario        
# 
#           * PVBatt_sys_performance (max_blackouts, Loadtype, accuracy)
#               Optimise and simulate the performance of a PV-battery system for the selected scenario                      
# 
#           * PVBatt_sys_stats (max_blackouts, Loadtype)
#               Present sys sizes, costs, GHGs of PV-battery system for the selected scenario        
# 
#           * compare_keymetrics (max_blackouts, Loadtype)
#               Compare LCUE, renewables fraction, GHG savings, diesel savings compared to base diesel case         
# 
#           * compare_costs (max_blackouts, Loadtype)
#               Compare breakdown of costs of PVbatt/hybrid systems compared to base diesel case         
#
#           * compare_GHGs (max_blackouts, Loadtype)
#               Compare breakdown of emissions of PVbatt/hybrid systems compared to base diesel case         
#
#
# Sensitivity Analysis
#
#           * LCUE_sensitivity (Loadtype, initial_max_blackout, final_max_blackout, stepsize)
#               Compare LCUE for diesel/hybrid/PVbatt systems for different reliability thresholds           
# 
#           * GHG_sensitivity (Loadtype, initial_max_blackout, final_max_blackout, stepsize)
#               Compare GHG emissions for diesel/hybrid/PVbatt systems for different reliability thresholds           
#
#           * renewables_sensitivity (Loadtype, max_blackouts, initial_renewablesfraction, final_renewablesfraction, stepsize)
#               Compare increase in LCUE for hybrid systems with higher renewables fraction compared to "min LCUE" hybrid system
#
#
# Productive uses of electricity
#
#           * privateimpact_reliability(Loadtype, max_blackouts, Systype)
#               Present reliability drop over time when additional private loads are included in the system         
# 
#           * privateimpact_design(Loadtype, max_blackouts):
#               Present growing load over time from Scenario 1 to Scenario 2B
#               Present compared wasted energy between initial sizing for Scenario 2B and optimized increase
#
#           * tariff_calculation(Systype, max_blackouts)
#              Calculates the tariff for refugee businesses required to recover the additional investment 
#              of Approach A and B scenarios in comparison with optimised PV-Battery System over 15 years
#              Calculates the cost recovered if refugees pay a grid tariff value and the remaining additional costs
#              Calculates the tariff for public users to cover Scenario 1 to 2B complete system (B), and
#              Scenario 1 PV-Battery system plus the remaining additional costs that refugees can't cover
#  
# Scenario comparison
# 
#           * cumulative_capacity(max_blackouts):
#               Present installed PV and storage capacity over lifetime for optimized systes for each scenario
#
#           * cumulative_costs(max_blackouts):
#               Present cumulative costs for optimized systems for each scenario over lifetime
#               Present final LCUE and initial equipment costs for each system for each scenario
#
# =============================================================================   
    

# =============================================================================
#                           Load profiles
#    
#   PRE-REQUISITE: Run get_loaddata(Loadtype) for selected scenario
# =============================================================================   
#

def public_loadprofile (txt, Loadtype):
    """
    
    Obtain and present the average daily load profile of each public facility and total public load profile in the camp
    
    Input: "txt" name of public load to be presented, write "total" to display total loads
           Load profile for the selected scenario, between 'InstitutionalBase', 'InstitutionalAdv', 'Mix1', 'Mix2'
    
    Output: Display on console average hourly load
            Save on /Plots/Plots Public XLoad/ directory a .png graph of the hourly average load     
    
    """    
  
    # Read the load.csv file for the corresponding device selected, or the total public   
    filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/" + txt + "_load.csv"  
    df1 = pd.read_csv(filepath)
    length = len(df1.index)

    # Read the devices.csv file containing hourly load information of the selected facility     
    filepathdevices = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Devices.csv"  
    df_devices = pd.read_csv(filepathdevices)    
    lengthdevices = len(df_devices.index)     
    
    # Create a new column with the hours from 0 to 23 repeatedly
    hours=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    repeated_hours = hours * int(length/len(hours))    
    df1['Hours'] = repeated_hours
    
    # For every load scenario, the load from the existent public facilities is calculated and displayed
    
    # For the existing load in Nyabiheke (Scenario 1)
    if Loadtype == 'Mix1':
        
       # Calculate the average load for each hour (0 to 23)
       hourly_mean = {'1 UNHCR Office':[],
                   '2 Other Offices':[],
                   '5 Water Pump 1':[],
                   '4 Water Pump 2':[],
                   '3 Bank':[],
                   '6 Health Centre':[]}
        
       for i in range(0, 24):
           
           # To calculate the total, first calculate the average load from each facility for each hour
           if txt == 'total':
            
               txt='UNHCR Office'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/UNHCR_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]

               hourly_mean['1 UNHCR Office'].append(df_i)

            
               txt='Other Offices'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/NGOOfficeBlock_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]            
               hourly_mean['2 Other Offices'].append(df_i)
            
            
               txt='Water Pump 1'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/WaterPump1_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]            
               hourly_mean['5 Water Pump 1'].append(df_i)
            
               txt='Water Pump 2'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/WaterPump2_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]            
               hourly_mean['4 Water Pump 2'].append(df_i)
            
               txt='Bank'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/Bank_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]            
               hourly_mean['3 Bank'].append(df_i)            
            
               txt='Health Centre'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/HealthCentre_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]
               hourly_mean['6 Health Centre'].append(df_i)      
            
               txt='total'
    
               # When all hours calculated, plot the resulting graph with the stacked public loads
               if i == 23:
    
                 # Average hourly load profile graph
                 x = hours
                 labels=[]
                 length = len(hourly_mean.keys())
                 allloads = sorted(hourly_mean.items())
                 fig, ax = plt.subplots()
                 Loadsforfigures=[]
                 
                 # Extract the load from each facility from the dictionary created
                 for n in range(0, length):

                    load=allloads[n]
                    namex=load[0]
                    name=namex[2:]
                    labels.append(name)
                    Loadsforfigures.append(load[1])
                 
                 # Create a stacked plot to represent them
                 plt.stackplot(x,Loadsforfigures, colors=['darkcyan','lightseagreen','lightsalmon','lightsteelblue','steelblue','palevioletred'])
                 
                 ax.set(xlabel='Hour of day', ylabel='Load (W)')
                 ax.grid()
                 ax.legend(labels, title=r'$\bf{Public \ loads}$', loc='center right')
                 plt.tight_layout()
                 plt.xticks([0,4,8,12,16,20,23])
                 plt.xlim((0,23))
                 plt.ylim((0,12000))
                 plt.show()
            
                   
           # If not want to represent the total load, only plot the load from the corresponding device
           else:
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]        
               hourly_mean['UNHCR Office'].append(df_i)
            
               # Print average hourly load profile of selected device on console    
               print ("Average hourly " + txt + " load profile = ", hourly_mean)
    
               # Average hourly load profile graph
               x = hours
               y = hourly_mean['UNHCR Office']

               fig, ax = plt.subplots()
               ax.plot(x, y, marker='o', markersize=3)

               ax.set(xlabel='Hour of day', ylabel='Load (W)',
               title="Average hourly " + txt + " load profile")
               ax.grid()
               plt.tight_layout()
               plt.xticks([0,4,8,12,16,20,23])
               plt.xlim((0,23))
               plt.show()
               
    # For Scenario 3, the additional public facilities load profiles are displayed in subplots          
    if Loadtype == 'Mix1Adv':
    
       # Calculate the average load for each hour (0 to 23)
       hourly_mean = {'Hospital':[],'Primary School':[],'Police Station':[],
                      'Vocational Centre':[],'Post Office':[],'Reception Centre':[]}
       
       for i in range(0, 24):
        
           if txt == 'total':
     
               txt='Hospital'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/Hospital_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]
               hourly_mean[txt].append(df_i)

            
               txt='Primary School'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/SchoolPrimary_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]            
               hourly_mean[txt].append(df_i)
            
            
               txt='Police Station'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/StationPolice_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]            
               hourly_mean[txt].append(df_i)
               
               txt='Vocational Centre'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/CentreVocational_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]
               hourly_mean[txt].append(df_i)

            
               txt='Post Office'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/PostOffice_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]            
               hourly_mean[txt].append(df_i)
            
            
               txt='Reception Centre'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/ReceptionCentre_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]            
               hourly_mean[txt].append(df_i)
              
            
               txt='total'
    
               # When all loads calculated, plot the load profiles in subplots
               if i == 23:
    
                 # Average hourly load profile graph
                 x = hours
                 labels=[]
                 length = len(hourly_mean.keys())
                 allloads = list(hourly_mean.items())
                 fig, ((ax1, ax4), (ax2, ax3), (ax5, ax6)) = plt.subplots(3,2, sharex='col', sharey='row')
                 Loadsforfigures=[]
             
                 for n in range(0, length):

                    load=allloads[n]
                    name=load[0]
                    labels.append(name)
                    Loadsforfigures.append(load[1])
                    
                 # Create six subplots to plot the different load profiles added
                    
                 ax1.plot(x, Loadsforfigures[0], color='palevioletred')
                 ax1.set_title(labels[0], fontweight="bold",fontsize=10)
                 ax1.set(xlabel='Hour of day', ylabel='Load (W)')
                 ax1.grid()
                 ax1.set_xlim(0,23)
                 ax1.set_ylim(-100,4000)
                 ax1.set_yticks([0,1000,2000,3000,4000])
                 
                 ax2.plot(x, Loadsforfigures[1], color='yellowgreen')
                 ax2.set_title(labels[1], fontweight="bold", fontsize=10)
                 ax2.set(xlabel='Hour of day', ylabel='Load (W)')
                 ax2.grid() 
                 ax2.set_xlim(0,23)
                 ax2.set_ylim(-20,600)
                 ax2.set_yticks([0,200,400,600])
                 
                 ax3.plot(x, Loadsforfigures[2], color='steelblue')
                 ax3.set_title(labels[2], fontweight="bold",fontsize=10)
                 ax3.grid()
                 ax3.set_xlim(0,23)
                 

                 ax4.plot(x, Loadsforfigures[3], color='orchid')
                 ax4.set_title('\n'+labels[3], fontweight="bold",fontsize=10)
                 ax4.grid()
                 ax4.set_xlim(0,23)
                 
                 ax5.plot(x, Loadsforfigures[4], color='gold')
                 ax5.set_title('\n'+labels[4], fontweight="bold",fontsize=10)
                 ax5.set(xlabel='Hour of day', ylabel='Load (W)')
                 ax5.grid()
                 ax5.set_xlim(0,23)
                 ax5.set_ylim(-20,600)
                 ax5.set_yticks([0,200,400,600])
                 
                 ax6.plot(x, Loadsforfigures[5], color='burlywood')
                 ax6.set_title('\n'+labels[5], fontweight="bold",fontsize=10)
                 ax6.set(xlabel='Hour of day')
                 ax6.grid()
                 ax6.set_xlim(0,23)
                 
                 for ax in fig.get_axes():
                    ax.label_outer()
                 
                 plt.subplots_adjust(left=0.2, bottom=0.01, right=0.8, top=0.99, hspace=0.5)
                 
                 plt.show()
            
           
    # Save graph in corresponding directory, if it does not exist, it creates it
    script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/")
    plot_dir = os.path.join(script_dir, 'Plots/Plots {}Load/Public/'.format(Loadtype))
    plot_name = txt + "_{}_PublicHourlyLoadProfile.png".format(Loadtype)
    
    if not os.path.isdir(plot_dir):
        os.makedirs(plot_dir)
    
    fig.savefig(plot_dir + plot_name, dpi=300, bbox_inches='tight')
    print(' Figure saved as '+plot_name)
    plt.show()
    


def private_loadprofile (txt, Loadtype):
    """
    Obtain and present the average daily load profile of each private business and total private load profile in the camp
    
    Input: "txt" name of private load to be presented, write "total" to display total loads
           Load profile for the selected scenario, between 'InstitutionalBase', 'InstitutionalAdv', 'Mix1', 'Mix2'
        
    
    Output: Display on console average hourly load
            Save on /Plots/Plots Private/ directory a .png graph of the hourly average load
        
    
    """    
    # Read the load.csv file for the corresponding device selected, or the total productive 
    filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/" + txt + "_load.csv"  
    df1 = pd.read_csv(filepath)  
    length = len(df1.index)
   
    # Read the devices.csv file containing hourly load information of the selected facility     
    filepathdevices = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Devices.csv"
    df_devices = pd.read_csv(filepathdevices)    
    lengthdevices = len(df_devices.index)     
    
    # Create a new column with the hours from 0 to 23 repeatedly
    hours=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    repeated_hours = hours * int(length/len(hours))    
    df1['Hours'] = repeated_hours

    # For every load scenario, the load from the existent private devices is calculated and displayed
    
    # For the existing load in Nyabiheke (Scenario 1)    
    if Loadtype == 'Mix1':
    
       # Calculate the average load for each hour (0 to 23)
       hourly_mean = {'Computer Lab':[],
                   'Sewing Cooperative':[],
                   'Restaurant':[],
                   'Restaurant Shop':[],
                   'Salon 2':[],
                   'Salon 1':[],
                   }
        
       # To calculate the total, first calculate the average load from each facility for each hour       
       for i in range(0, 24):
        
           if txt == 'total':
               
               txt='Computer Lab'
               #Get day load data
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/ComputerLab_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]
               hourly_mean[txt].append(df_i)
           
               txt='Salon 1'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/Salon1_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]            
               hourly_mean[txt].append(df_i)
                     
               txt='Salon 2'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/Salon2_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]            
               hourly_mean[txt].append(df_i)
            
               txt='Sewing Cooperative'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/SewingCoop_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]            
               hourly_mean[txt].append(df_i)
            
               txt='Restaurant'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/Restaurant1_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]            
               hourly_mean[txt].append(df_i)            
            
               txt='Restaurant Shop'
               #Get day load data
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/Restaurant2_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i= df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]
               hourly_mean[txt].append(df_i)      
            
               txt='total'
    
               # When all loads calculated, plot the load profiles in subplots    
               if i == 23:
    
                 # Average hourly stacked load profile graph
                 
                 # Extract variables for plotting
                 x = hours
                 labels=[]
                 length = len(hourly_mean.keys())
                 allloads = sorted(hourly_mean.items())
                 fig, ax = plt.subplots()
                 Loadsforfigures=[]
             
                 for n in range(0, length):

                    load=allloads[n]
                    name=load[0]
                    labels.append(name)
                    Loadsforfigures.append(load[1])
     
                 # Create stackplot to represent productive loads
                 plt.stackplot(x,Loadsforfigures, colors=['lightsteelblue','orchid','lightseagreen','darkcyan','lightsalmon','palevioletred'])
                 ax.set(xlabel='Hour of day', ylabel='Load (W)')
                 ax.grid()
                 ax.legend(labels, title=r'$\bf{Private \ loads}$', loc=2, bbox_to_anchor=(1, 0.8, 0, 0))
                 plt.tight_layout()
                 plt.xticks([0,4,8,12,16,20,23])
                 plt.xlim((0,23))
                 plt.ylim((0,1400))
                 plt.show()
            
           # If don't want to represent all stacked, presents a single load profile of the selected device
           else:
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]        
               hourly_mean['Total'].append(df_i)
            
               # Print average hourly load profile of selected device on console    
               print ("Average hourly " + txt + " load profile = ", hourly_mean)
    
               # Average hourly load profile graph
               x = hours
               y = hourly_mean
               fig, ax = plt.subplots()
               ax.plot(x, y, marker='o', markersize=3)
               ax.set(xlabel='Hour of day', ylabel='Load (W)',
               title="Average hourly " + txt + " load profile")
               ax.grid()
               plt.tight_layout()
               plt.xticks([0,4,8,12,16,20,23])
               plt.xlim((0,23))
               plt.ylim((0,1400))
               plt.show()
    
    # For Scenario 2, presents the hourly load profiles of the added productive users           
    if Loadtype == 'Mix2':
    
       # Calculate the average load for each hour (0 to 23)
       hourly_mean = {'Welding Shop':[],'Bar':[],'Popcorn Shop':[]}
                
       for i in range(0, 24):
        
           if txt == 'total':
            
               txt='Popcorn Shop'
               #Get day load data
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/PopcornShop_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]
               hourly_mean[txt].append(df_i)
           
               txt='Welding Shop'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/WeldingShop_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]            
               hourly_mean[txt].append(df_i)
                       
               txt='Bar'
               filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/Bar_load.csv"  
               df1 = pd.read_csv(filepath)
               df1['Hours'] = repeated_hours
               df_i = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[1]            
               hourly_mean[txt].append(df_i)
                          
               txt='total'
       
               # When all hours calculated
               if i == 23:
    
                 # Plot average hourly load profile graph
                 
                 # Extract variables for plotting
                 x = hours
                 labels=[]
                 length = len(hourly_mean.keys())
                 allloads = list(hourly_mean.items())
                 fig, (ax1, ax2, ax3) = plt.subplots(1,3, sharey=True)
                 Loadsforfigures=[]
 
                 # Extract the load from each facility from the dictionary created            
                 for n in range(0, length):

                    load=allloads[n]
                    name=load[0]
                    labels.append(name)
                    Loadsforfigures.append(load[1])
                    
                 # Create a stackplot to represent them 
                 
                 # Welding shop
                 ax1.plot(x, Loadsforfigures[0], color='steelblue')
                 ax1.set_title(labels[0], fontweight="bold")
                 ax1.set(xlabel='Hour of day', ylabel='Load (W)')
                 ax1.grid()
                 ax1.set_ylim(-50,2000)
                 
                 # Bar
                 ax2.plot(x, Loadsforfigures[1], color='palevioletred')
                 ax2.set_title(labels[1], fontweight="bold")
                 ax2.set(xlabel='Hour of day')
                 ax2.grid() 
                 
                 # Popcorn shop
                 ax3.plot(x, Loadsforfigures[2], color='burlywood')
                 ax3.set_title(labels[2], fontweight="bold")
                 ax3.set(xlabel='Hour of day')
                 ax3.grid()
                 
                 plt.tight_layout() 
                 plt.subplots_adjust(left=0.00, bottom=0.2, right=1, top=0.8)
   
                 plt.show()
    
    # Save graph in corresponding directory, if not existent, creates it
    script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/")
    plot_dir = os.path.join(script_dir, 'Plots/Plots {}Load/Private/'.format(Loadtype))
    plot_name = txt + "_{}_PrivateHourlyLoadProfile.png".format(Loadtype)
    
    if not os.path.isdir(plot_dir):
           os.makedirs(plot_dir)
    
    # Save figure
    fig.savefig(plot_dir + plot_name, dpi=300, bbox_inches='tight')
    print(' Figure saved as '+ plot_name)
    plt.show()

def total_loadprofile (Loadtype):
    """
    Obtain and present the average daily total load profile in the camp
    
    Input: Load profile for the selected scenario, between 'InstitutionalBase', 'InstitutionalAdv', 'Mix1', 'Mix2'
        
    
    Output: Display on console average hourly load
            Save on Device Load/Plots_XLoad/ directory a .png graph of the hourly average load
        
    
    """    
    # Read the load .csv file containing total hourly load information of the scenario
    txt='total'
    filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/" + txt + "_load.csv"  
    df1 = pd.read_csv(filepath)   
    length = len(df1.index)
    
    # Create a new column with the hours from 0 to 23 repeatedly
    hours=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    repeated_hours = hours * int(length/len(hours))    
    df1['Hours'] = repeated_hours
    
    # Calculate the  total average public and private load for each hour (0 to 23) 
    
    # For Scenario 1
    if Loadtype == 'Mix1':
        
       hourly_mean = {'Total Public':[],
                   'Total Private':[]
                   }
        
       for i in range(0, 24):
        
            df_i_public = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[3]
            hourly_mean['Total Public'].append(df_i_public)
            
            df_i_private = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[2]
            hourly_mean['Total Private'].append(df_i_private)
    
       # Once all hours are calculated, present average hourly total load profile graph
       x = hours
       labels=[]
       length = len(hourly_mean.keys())
       allloads = sorted(hourly_mean.items(), reverse=True)
       Loadsforfigures=[]
       fig, ax = plt.subplots()
             
       for n in range(0, length):

           load=allloads[n]
           labels.append(load[0])
           Loadsforfigures.append(load[1])
           
       # Represent total public and private loads in a stacked plot
       plt.stackplot(x,Loadsforfigures, colors=['lightseagreen','gold'])        
       ax.set(xlabel='Hour of day', ylabel='Load (W)')
       ax.grid()
       ax.legend(labels, title=r'$\bf{Cumulative \ loads}$', bbox_to_anchor=(1.0, 0.3, 0, 0))
       plt.tight_layout()
       plt.xticks([0,4,8,12,16,20,23])
       plt.xlim((0,23))
       plt.ylim((0,14000))
       plt.show()
       
       # Save figure in corresponding directory, if non existent, creates it
       script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/")
       plot_dir = os.path.join(script_dir, 'Plots/Plots {}Load/Total/'.format(Loadtype))
       plot_name = txt + "_{}_TotalHourlyLoadProfile.png".format(Loadtype)
    
       if not os.path.isdir(plot_dir):
           os.makedirs(plot_dir)
    
       fig.savefig(plot_dir + plot_name, dpi=300)
       print(' Figure saved as '+plot_name)
       plt.show()
        
       #Save the hourly average total load data in a ..csv file   
       df_totalload=pd.DataFrame(hourly_mean, index=None)
       filepath=self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/Plots/Plots {}Load/Total/TotalHourlyProfile.csv".format(Loadtype) 
       df_totalload.to_csv(filepath, index=None)
    
       print( "Data saved as TotalHourlyProfile.csv" )
    
    # For Scenario 2A
    elif Loadtype == 'Mix2':
        
        # Obtain the total load data in Scenario 1    
        loadfilepath=self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/Plots/Plots Mix1Load/Total/TotalHourlyProfile.csv"
        df_ReferenceLoad=pd.read_csv(loadfilepath)
        
        hourly_mean = {'Scenario 1 Public':[],
                   'Scenario 1 Private':[],
                   'Additional Private':[]}
        
        hourly_mean['Scenario 1 Public']=df_ReferenceLoad['Total Public']
        hourly_mean['Scenario 1 Private']=df_ReferenceLoad['Total Private']
        
        #Calculate the additional private load in Mix 2 scenario       
        for i in range(0, 24):
            
            df_i_private = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[2]
            base=df_ReferenceLoad.iat[i,1]
            df_i=df_i_private - base            
            hourly_mean['Additional Private'].append(df_i)
        
        # Average hourly load represented in a stacked plot
        x = hours
        labels=[]
        length = len(hourly_mean.keys())
        allloads = sorted(hourly_mean.items(), reverse=True)
        Loadsforfigures=[]
        fig, ax = plt.subplots()
             
        for n in range(0, length):

           load=allloads[n]
           labels.append(load[0])
           Loadsforfigures.append(load[1])
        
        plt.stackplot(x,Loadsforfigures, colors=['lightseagreen','gold','palevioletred'])        
        ax.set(xlabel='Hour of day', ylabel='Load (W)')
        ax.grid()
        ax.legend(labels, title=r'$\bf{Cumulative \ loads}$', bbox_to_anchor=(1.0, 0.35, 0, 0))
        plt.tight_layout()
        plt.xticks([0,4,8,12,16,20,23])
        plt.xlim((0,23))
        plt.ylim((0,18000))
        plt.show()
        
        # Save the figure in the corresponding directory
        script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/")
        plot_dir = os.path.join(script_dir, 'Plots/Plots {}Load/Total/'.format(Loadtype))
        plot_name = txt + "_{}_TotalHourlyLoadProfile.png".format(Loadtype)
    
        if not os.path.isdir(plot_dir):
           os.makedirs(plot_dir)
    
        fig.savefig(plot_dir + plot_name, dpi=300)
        print(' Figure saved as '+plot_name)
        plt.show()
        
        #Save the hourly average total load data in a file   
        df_totalload=pd.DataFrame(hourly_mean, index=None)
        filepath=self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/Plots/Plots {}Load/Total/TotalHourlyProfile.csv".format(Loadtype)    
        df_totalload.to_csv(filepath, index=None)
    
        print( "Data saved as TotalHourlyProfile.csv" )        
    
    # For Scenario 2B    
    elif Loadtype == 'Mix2B':
        
        # Obtain the load the total load data from Scenario 1     
        loadfilepath=self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/Plots/Plots Mix1Load/Total/TotalHourlyProfile.csv"
        df_ReferenceLoad=pd.read_csv(loadfilepath)
        
        hourly_mean = {'Scenario 1 Public':[],
                   'Scenario 1 Private':[],
                   'Additional Private':[]}
        
        hourly_mean['Scenario 1 Public']=df_ReferenceLoad['Total Public']
        hourly_mean['Scenario 1 Private']=df_ReferenceLoad['Total Private']
        
        #Calculate the additional private load in Scenario 2B      
        for i in range(0, 24):
            
            df_i_private = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[2]
            base=df_ReferenceLoad.iat[i,1]
            df_i=df_i_private - base           
            hourly_mean['Additional Private'].append(df_i)
        
        # Present average hourly total loads in a stacked plot
        x = hours
        labels=[]
        length = len(hourly_mean.keys())
        allloads = sorted(hourly_mean.items(), reverse=True)
        Loadsforfigures=[]
        fig, ax = plt.subplots()
             
        for n in range(0, length):

           load=allloads[n]
           labels.append(load[0])
           Loadsforfigures.append(load[1])
        
        plt.stackplot(x,Loadsforfigures, colors=['lightseagreen','gold','palevioletred'])        
        ax.set(xlabel='Hour of day', ylabel='Load (W)')
        ax.grid()
        ax.legend(labels, title=r'$\bf{Cumulative \ loads}$', bbox_to_anchor=(1.0, 0.35, 0, 0))
        plt.tight_layout()
        plt.xticks([0,4,8,12,16,20,23])
        plt.xlim((0,23))
        plt.ylim((0,25000))
        plt.yticks([0,5000,10000,15000,20000,25000])
        plt.show()
        
        # Save figure in the corresponding directory, creating it
        script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/")
        plot_dir = os.path.join(script_dir, 'Plots/Plots {}Load/Total/'.format(Loadtype))
        plot_name = txt + "_{}_TotalHourlyLoadProfile.png".format(Loadtype)
    
        if not os.path.isdir(plot_dir):
           os.makedirs(plot_dir)
    
        fig.savefig(plot_dir + plot_name,dpi=300)
        print(' Figure saved as '+plot_name)
        plt.show()
        
        #Save the hourly average total load data in a .csv file   
        df_totalload=pd.DataFrame(hourly_mean, index=None)
        filepath=self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/Plots/Plots {}Load/Total/TotalHourlyProfile.csv".format(Loadtype)
    
        df_totalload.to_csv(filepath, index=None)
    
        print( "Data saved as TotalHourlyProfile.csv" )       
    
    # For Scenario 3    
    elif Loadtype == 'Mix1Adv':
        
        # Obtain total load data from Scenario 1       
        loadfilepath=self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/Plots/Plots Mix1Load/Total/TotalHourlyProfile.csv"
        df_ReferenceLoad=pd.read_csv(loadfilepath)
        
        hourly_mean = {'Scenario 1 Public':[],
                   'Scenario 1 Private':[],
                   'Additional Public':[]}
        
        hourly_mean['Scenario 1 Public']=df_ReferenceLoad['Total Public']
        hourly_mean['Scenario 1 Private']=df_ReferenceLoad['Total Private']
        
        #Calculate the additional public load in Scenario 3   
        for i in range(0, 24):
            
            df_i_public = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[3]
            base=df_ReferenceLoad.iat[i,0]
            df_i=df_i_public - base         
            hourly_mean['Additional Public'].append(df_i)
    
        # Present average hourly total loads in a stacked plot
        x = hours
        labels=[]
        length = len(hourly_mean.keys())
        allloads = sorted(hourly_mean.items(), reverse=True)
        Loadsforfigures=[]
        fig, ax = plt.subplots()
             
        for n in range(0, length):

           load=allloads[n]
           labels.append(load[0])
           Loadsforfigures.append(load[1])
        
        plt.stackplot(x,Loadsforfigures, colors=['lightseagreen','gold','steelblue'])        
        ax.set(xlabel='Hour of day', ylabel='Load (W)')
        ax.grid()
        ax.legend(labels, title=r'$\bf{Cumulative \ loads}$', bbox_to_anchor=(1.0, 0.35, 0, 0))
        plt.tight_layout()
        plt.xticks([0,4,8,12,16,20,23])
        plt.xlim((0,23))
        plt.ylim((0,18000))
        plt.show()

        # Save figure in the corresponding directory, creating it    
        script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/")
        plot_dir = os.path.join(script_dir, 'Plots/Plots {}Load/Total/'.format(Loadtype))
        plot_name = txt + "_{}_TotalHourlyLoadProfile.png".format(Loadtype)
    
        if not os.path.isdir(plot_dir):
           os.makedirs(plot_dir)
    
        fig.savefig(plot_dir + plot_name,dpi=300)
        print(' Figure saved as '+plot_name)
        plt.show()
        
        #Save the hourly average total load data in a .csv file   
        df_totalload=pd.DataFrame(hourly_mean, index=None)
        filepath=self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/Plots/Plots {}Load/Total/TotalHourlyProfile.csv".format(Loadtype)
    
        df_totalload.to_csv(filepath, index=None)
    
        print( "Data saved as TotalHourlyProfile.csv" )  
        
    # For Scenario 4    
    elif Loadtype == 'Mix2Adv':
        
        # Obtain total load data from Scenario 1               
        loadfilepath=self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/Plots/Plots Mix1Load/Total/TotalHourlyProfile.csv"
        df_ReferenceLoad=pd.read_csv(loadfilepath)
        
        hourly_mean = {'Scenario 1 Public':[],
                   'Scenario 1 Private':[],
                   'Additional Public':[],                   
                   'Additional Private':[]}
        
        hourly_mean['Scenario 1 Public']=df_ReferenceLoad['Total Public']
        hourly_mean['Scenario 1 Private']=df_ReferenceLoad['Total Private']
        
        #Calculate the additional private  and public load in Scenario 4   
        for i in range(0, 24):
            
            df_i_public = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[3]
            base=df_ReferenceLoad.iat[i,0]
            df_i=df_i_public - base            
            hourly_mean['Additional Public'].append(df_i)
            
            df_i_private = df1.loc[df1['Hours'] == i].mean(axis=0).iloc[2]
            base=df_ReferenceLoad.iat[i,1]
            df_i=df_i_private - base
            
            hourly_mean['Additional Private'].append(df_i)            
        
        # Present average hourly total loads in a stacked plot
        x = hours
        labels=[]
        length = len(hourly_mean.keys())
        allloads = list(hourly_mean.items())
        Loadsforfigures=[]
        fig, ax = plt.subplots()
             
        for n in range(0, length):

           load=allloads[n]
           labels.append(load[0])
           Loadsforfigures.append(load[1])
        
        plt.stackplot(x,Loadsforfigures, colors=['lightseagreen','gold','steelblue','palevioletred'])        
        ax.set(xlabel='Hour of day', ylabel='Load (W)')
        ax.grid()
        ax.legend(labels, title=r'$\bf{Cumulative \ loads}$', fontsize=9, bbox_to_anchor=(1.0, 0.35, 0, 0))
        plt.tight_layout()
        plt.xticks([0,4,8,12,16,20,23])
        plt.xlim((0,23))
        plt.ylim((0,30000))
        plt.show()

        # Save figure in the corresponding directory, creating it        
        script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/")
        plot_dir = os.path.join(script_dir, 'Plots/Plots {}Load/Total/'.format(Loadtype))
        plot_name = txt + "_{}_TotalHourlyLoadProfile.png".format(Loadtype)
    
        if not os.path.isdir(plot_dir):
           os.makedirs(plot_dir)
    
        fig.savefig(plot_dir + plot_name,dpi=300)
        print(' Figure saved as '+plot_name)
        plt.show()
        
        #Save the hourly average total load data in a .csv file   
        df_totalload=pd.DataFrame(hourly_mean, index=None)
        filepath=self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Device load/Plots/Plots {}Load/Total/TotalHourlyProfile.csv".format(Loadtype)
    
        df_totalload.to_csv(filepath, index=None)
    
        print( "Data saved as TotalHourlyProfile.csv" ) 
    
    
    
# =============================================================================
#                           Systems comparison
# =============================================================================   
#
        
def diesel_sys_performance (max_blackouts, Loadtype):
    
    """
    Simulate performance of diesel-powered system for the selected scenario 
    
    Input: max_blackouts  Maximum acceptible blackouts (0.0-1.0)
           Load profile for the selected scenario, between 'InstitutionalBase', 'InstitutionalAdv', 'Mix1', 'Mix2'
        
    Output: File of simulation with hourly performance of system to be analysed with diesel_sys_stats() 
            File of system appraisal (technical, financial, environmental) of selected system
    
    """    
    
    
    # Read the load .csv file containing hourly load information of the selected facility   
    filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Scenario/Scenario inputs.csv"   
    df_scenario = pd.read_csv(filepath, header=None)

    # Define reliability from blackout threshold    
    Reliability= (1.0 - max_blackouts)*100.0
    
    # Performance analysed for diesel system
    Systype = 'Diesel'
    
    # Check if simulation for blackout level exists already, if not, performs simulation
    check = os.path.exists(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV0_Storage0_{}_Re{}_LoadInstitutionalBase.csv".format(Systype, Reliability, Loadtype) ) 
    
    if check == False :
        
        # Read the load .csv file containing hourly load information of the selected facility     
        print('\n Simulation doesn\'t exist, simulation in progress...')
        
        # Set maximum blackout threshold (0.0-1.0)
        if df_scenario.iat[3, 1] != max_blackouts :
            df_scenario.iat[3, 1] = max_blackouts
    
        # Substitute new values in Scenario  Inputs.csv file for simulation
        df_scenario.to_csv(filepath, index=None, header =None)
        
        # Simulate diesel system and saves file as i.e.: Sim_PV0_Storage0_Diesel_Re90_LoadInstitutionalBase.csv        
        Simulation = simulate_system (0,0,Systype,Loadtype)
               
        print('\n Simulation finished, proceed with diesel_sys_stats(max_blackouts, Loadtype) to display results.')
        
    else:
        
        print('\n Simulation already exists, proceed with diesel_sys_stats(max_blackouts, Loadtype) to display results.')
  

def diesel_sys_stats (max_blackouts, Loadtype):
    """
    Present costs, GHGs, diesel consumption of diesel-powered system for the selected scenario 
    
    Input: Simulation file resulting of diesel_sys_performance(max_blackouts,Loadtype)
           Appraisal file resulting of diesel_sys_performance(max_blackouts,Loadtype)
        
    Output: Display LCUE, emissions intensity, Diesel capacity, Diesel fuel usage
            Display breakdown of costs:Total System Cost, Total fuel cost, total O&M cost
            Display breakdown of emissions: ...
            Save on /Plots/Plots Diesel/ directory  the .png graphs  
                
    """ 
    # Performance displayed for diesel system
    Systype = 'Diesel'   
    Reliability= int((1.0 - max_blackouts)*100.0)

    # Specify that there is no PV or storage available    
    PV_kWp=0   
    storage_kWh=0
    
    # Read csv file with diesel system simulation data
    df_dieselsim = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV{}_Storage{}_{}_Re{}_Load{}.csv'.format(PV_kWp, storage_kWh, Systype, Reliability, Loadtype))
    df_dieselapp = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV{}_Storage{}_{}_Re{}_Load{}_Appraisal.csv'.format(PV_kWp, storage_kWh, Systype, Reliability, Loadtype))
    
    # Display LCUE, emissions intensity, Renewables fraction, Total system cost, Cumulative GHGs  
    Appraisal_indexes=[17,14,15,8,10]        
    df_keymetrics=df_dieselapp.iloc[:, Appraisal_indexes]
    
    # Create a directory with the name of the simulation to save the figures 
    script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/")
    plot_dir = os.path.join(script_dir, 'Sim_PV{}_Storage{}_{}_Re{}_Load{}/'.format(PV_kWp, storage_kWh, Systype, Reliability, Loadtype))
    
    if not os.path.isdir(plot_dir):
        os.makedirs(plot_dir)
    
    # Save key metrics obtained in a .csv file)  
    df_keymetrics.to_csv(rself.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV{}_Storage{}_{}_Re{}_Load{}/Key_Metrics.csv'.format(PV_kWp, storage_kWh, Systype, Reliability, Loadtype), index=None)
  
    print('\nKey system metrics saved as Key_Metrics.csv \n'.format(PV_kWp, storage_kWh, Systype, Reliability, Loadtype))
    print(df_keymetrics)
    
    # Display breakdown of costs:Total System Cost, Total equipment cost, total O&M cost, total fuel cost        
    Financial_indexes=[29, 30, 32, 33]        
    df_financialmetrics=df_dieselapp.iloc[:, Financial_indexes]
    
    # Save financial metrics obtained in a .csv file
    df_financialmetrics.to_csv(rself.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV{}_Storage{}_{}_Re{}_Load{}/Financial_Metrics.csv'.format(PV_kWp, storage_kWh, Systype, Reliability, Loadtype), index=None)
    print('Financial metrics saved as Financial_Metrics.csv \n')
    
    # Cost Breakdown Donught     
    labels = ['New equipment cost', 'O&M cost (excluding fuel)', 'Fuel cost']
    sizes = [df_financialmetrics.iat[0,1], df_financialmetrics.iat[0,2], df_financialmetrics.iat[0,3]]
    colors = ['yellowgreen', 'lightsteelblue', 'lightcoral']
    explode = (0.1,0.1,0.1)
    patches, texts, autotexts = plt.pie(sizes, colors=colors, startangle=0, counterclock=True, autopct=lambda p: '{:.1f}%  '.format(p), pctdistance=1.2, explode=explode)
    centre_circle=plt.Circle( (-0.06,-0.05), 0.6, color='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.legend(patches, labels, title=r'$\bf{Cost \ categories}$',loc="lower right", bbox_to_anchor=(0.65, 0, 0.5, 1))
    plt.axis('equal')
    plt.tight_layout()
    plt.title(r'$\bf{Cost \ breakdown \ for \ diesel \ system}$' + '\n \n')
        
    # Name the figure and save it in the corresponding directory
    plot_name = "CostBreakdown_Sim_PV{}_Storage{}_{}_Re{}_Load{}.png".format(PV_kWp, storage_kWh, Systype, Reliability, Loadtype)   
    plt.savefig(plot_dir + plot_name, dpi=300)
    plt.show()

    print('\nFigure saved as ', plot_name)  
         
   # Display breakdown of emissions: Total emissions, Equipment emissions, O&M emissions, fuel emission       
    Environmental_indexes=[37, 39, 41, 42]        
    df_environmentalmetrics=df_dieselapp.iloc[:, Environmental_indexes]
    
    df_environmentalmetrics.to_csv(rself.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV{}_Storage{}_{}_Re{}_Load{}/Environmental_Metrics.csv'.format(PV_kWp, storage_kWh, Systype, Reliability, Loadtype), index=None)
    print('\nEnvironmental metrics saved as Environmental_Metrics.csv \n')
    
    # GHGs Emissions Breakdown Donught  
    labels = ['New equipment emissions', 'O&M emissions (excluding fuel)', 'Fuel emissions']
    sizes = [df_environmentalmetrics.iat[0,1], df_environmentalmetrics.iat[0,2], df_environmentalmetrics.iat[0,3]]
    colors = ['yellowgreen', 'lightsteelblue', 'lightcoral']
    explode = (0.1,0.1,0.1)
    patches, texts, autotexts = plt.pie(sizes, colors=colors, startangle=0, counterclock=True, autopct=lambda p: '{:.1f}%  '.format(p), pctdistance=1.2, explode=explode)
    centre_circle=plt.Circle( (-0.06,-0.01), 0.6, color='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)    
    
    plt.legend(patches, labels, title=r'$\bf{Emission \ categories}$',loc="lower left", bbox_to_anchor=(0.65, 0, 0.5, 1))
    plt.axis('equal')
    plt.tight_layout()
    plt.title(r'$\bf{GHGs \ emissions \ breakdown \ for \ diesel \ system}$' + '\n \n')
        
    # Name the figure and save it in the corresponding directory
    plot_name = "GHGsBreakdown_Sim_PV{}_Storage{}_{}_Re{}_Load{}.png".format(PV_kWp, storage_kWh, Systype, Reliability, Loadtype)
    
    plt.savefig(plot_dir + plot_name, dpi=300)
    plt.show()
        
    print('\nFigure saved as ', plot_name)     

    
def hybrid_sys_performance (max_blackouts, Loadtype, accuracy):
    """
    Simulate performance of diesel-PV-battery system for the selected scenario 
    
    Input: max_blackouts  Maximum acceptible blackouts (0.0-1.0)
           Load profile for the selected scenario, between 'InstitutionalBase', 'InstitutionalAdv', 'Mix1', 'Mix2'
        
    Output: File of optimisation to be analysed with hybrid_sys_stats()        
    
    """  
    # Read the load .csv file containing hourly load information of the selected facility  
    filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Scenario/Scenario inputs.csv"
    df_scenario = pd.read_csv(filepath, header=None)
    
    # Define reliability from blackout threshold
    Reliability= int((1.0 - max_blackouts)*100.0)
    
    # Performance analysed for hybrid system
    Systype = 'Hybrid'
    
    # Check if simulation for blackout level exists already, if not, performs simulation
    check = os.path.exists(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv".format(Systype, Reliability, Loadtype)) 
    
    if check == False :
        
        # Read the load .csv file containing hourly load information of the selected facility     
        print('\n Simulation doesn\'t exist, starting with optimisation...')
    
        # Set maximum blackout threshold (0.0-1.0)
        if df_scenario.iat[3, 1] != max_blackouts :
            df_scenario.iat[3, 1] = max_blackouts
    
        # Substitute new values in Scenario  Inputs.csv file for simulation
        df_scenario.to_csv(filepath, index=None, header =None)
        
        # Simulate diesel system and saves file as i.e.: Sim_PV0_Storage0_Diesel_Re90_LoadInstitutionalBase.csv      
        Optimisation = optimise_system (Systype, Loadtype, max_blackouts, accuracy)
        
        print('\n Optimisation finished, proceed with hybrid_sys_stats(max_blackouts, Loadtype) to display results ...')
        
    else:
        
        print('\n Optimisation already exists, proceed with diesel_sys_stats(max_blackouts, Loadtype) to display results...')
        
    
    
def hybrid_sys_stats (max_blackouts, Loadtype):
    """
    Present costs, GHGs, renewable fraction, diesel consumption of diesel-PV-battery system for the selected scenario 
    
    Input: Optimisation file resulting of hybrid_sys_performance(max_blackouts, Loadtype)
        
    Output: Display LCUE, emissions intensity, Diesel capacity, Diesel fuel usage
             Save them in Key_Metrics.csv file 
            Display breakdown of costs:Total System Cost, Total fuel cost, total O&M cost
             Save them in Financial_Metrics.csv file 
            Display breakdown of emissions: Total, System, Fuel, O&M
             Save them in Environmental_Metrics.csv file 
            Save .png figures on /Saved Optimisations/Optimisation Name*/ directory    
    
    """  
    # Performance displayed for hybrid system
    Systype = 'Hybrid'   
    Reliability= int((1.0 - max_blackouts)*100.0)
    
    # Read csv file with diesel system simulation data
    df_hybridopt = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv'.format(Systype, Reliability, Loadtype))
  
    # Obtain LCUE, emissions intensity, Renewables fraction, Total system cost, Cumulative GHGs   
    Appraisal_indexes=[18,14,15,8,10]        
    df_keymetrics=df_hybridopt.iloc[2, Appraisal_indexes]
    df_keymetrics.iat[0]=df_hybridopt["Renewables fraction"].mean()
    df_keymetrics.iat[2]=df_hybridopt["Emissions intensity (gCO2/kWh)"].mean()
       
    # Create a directory with the name of the simulation to save the figures 
    script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/")
    plot_dir = os.path.join(script_dir, 'Opt_{}_Re{}_Load{}/'.format(Systype, Reliability, Loadtype))
    
    if not os.path.isdir(plot_dir):
        os.makedirs(plot_dir)
    
    df_keymetrics=pd.DataFrame(df_keymetrics)    
    df_keymetrics=df_keymetrics.transpose()
    df_keymetrics.to_csv(rself.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}/Key_Metrics.csv'.format(Systype, Reliability, Loadtype), index=None, header=True)
  
    print('\nKey system metrics saved as Key_Metrics.csv \n')
    print(df_keymetrics)
    
    # Display breakdown of costs:Total System Cost, Total equipment cost, total O&M cost, total fuel cost        
    Financial_indexes=[29, 30, 32, 33]        
    df_financialmetricsperyear=df_hybridopt.iloc[:, Financial_indexes]
    df_financialmetrics= pd.DataFrame(df_financialmetricsperyear.sum())
    df_financialmetrics=df_financialmetrics.transpose()
    
    #  Calculate new PV, storage and diesel installations
    PV_array_size = pd.Series([df_hybridopt.iloc[0,3], df_hybridopt.iloc[1,3]-df_hybridopt.iloc[0,5],df_hybridopt.iloc[2,3]-df_hybridopt.iloc[1,5]])
    storage_size = pd.Series([df_hybridopt.iloc[0,4], df_hybridopt.iloc[1,4]-df_hybridopt.iloc[0,6],df_hybridopt.iloc[2,4]-df_hybridopt.iloc[1,6]])
    
    # Calculate the discounted cost of such installations over the lifetime of the system
    PV_cost_array = Finance().get_PV_cost(PV_array_size,0)
    BOS_cost_array = Finance().get_BOS_cost(PV_array_size,0)
    storage_cost_array = Finance().get_storage_cost(storage_size,0)
    
    # Discount fraction used for installations on years 0,5,10
    discount_fraction = [((1.0 - 0.095)**0),((1.0 - 0.095)**5),((1.0 - 0.095)**10)]
    
    PV_cost = sum(np.multiply(PV_cost_array,discount_fraction))
    storage_cost = sum(np.multiply(storage_cost_array,discount_fraction))
    BOS_cost = sum(np.multiply(BOS_cost_array,discount_fraction))
    
    Other_equip_cost = df_financialmetrics.iat[0,1]-(PV_cost+BOS_cost+storage_cost)
    
    df_equipmentcost=pd.DataFrame()
    df_equipmentcost['PV Cost']=PV_cost
    df_equipmentcost['Storage Cost']=storage_cost
    df_equipmentcost['BOS Cost']=BOS_cost
    df_equipmentcost['Other equipment Cost']= Other_equip_cost
    
    # Save main financial metrics into .csv file
    df_financialmetrics.to_csv(rself.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}/Financial_Metrics.csv'.format(Systype, Reliability, Loadtype), index=None)
    print('Financial metrics saved as Financial_Metrics.csv \n')
    
    # Save breakdown of equipment costs in .csv file
    df_equipmentcost.to_csv(rself.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}/Equipment_costs.csv'.format(Systype, Reliability, Loadtype), index=None)
    print('Equipment costs saved as Financial_Metrics.csv \n')
    
    # Cost Breakdown Donught 
    labels = ['PV Cost', 'Storage Cost', 'BOS Cost', 'Other equipment costs', 'O&M cost (excluding fuel)', 'Fuel cost']
    sizes = [PV_cost, storage_cost, BOS_cost, Other_equip_cost, df_financialmetrics.iat[0,2], df_financialmetrics.iat[0,3]]
    colors = ['gold','yellowgreen','darkcyan','steelblue', 'lightsteelblue', 'lightcoral']
    explode = (0.1,0.1,0.1,0.1,0.1,0.1)
    patches, texts, autotexts = plt.pie(sizes, colors=colors, startangle=0, counterclock=True, autopct='%1.1f%%', pctdistance=1.2, explode=explode)
    centre_circle=plt.Circle( (-0.06,-0.065), 0.6, color='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)    
    
    plt.legend(patches, labels, title=r'$\bf{Cost \ categories}$',loc="lower left", bbox_to_anchor=(0.65, -0.1, 0.5, 1))
    plt.axis('equal')
    plt.tight_layout()
    plt.title(r'$\bf{Cost \ breakdown \ for \ hybrid \ system}$' + '\n \n')
        
    # Name the figure and save it in the corresponding directory
    plot_name = "CostBreakdown_Opt_{}_Re{}_Load{}.png".format(Systype, Reliability, Loadtype)
    plt.savefig(plot_dir + plot_name, dpi=300)
    plt.show()

    print('\nFigure saved as ', plot_name)  
         
    # Obtain breakdown of emissions: Total emissions, Equipment emissions, O&M emissions, fuel emissions     
    Environmental_indexes=[37, 39, 41, 42]        
    df_environmentalmetricsperyear=df_hybridopt.iloc[:, Environmental_indexes]
    df_environmentalmetrics= pd.DataFrame(df_environmentalmetricsperyear.sum())
    df_environmentalmetrics=df_environmentalmetrics.transpose()
    
    # Save environmental metrics in .csv file
    df_environmentalmetrics.to_csv(rself.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}/Environmental_Metrics.csv'.format(Systype, Reliability, Loadtype), index=None)
    print('\nEnvironmental metrics saved as Environmental_Metrics.csv \n')
    
    # GHGs Emissions Breakdown Donught   
    labels = ['New equipment emissions', 'O&M emissions (excluding fuel)', 'Fuel emissions']
    sizes = [df_environmentalmetrics.iat[0,1], df_environmentalmetrics.iat[0,2], df_environmentalmetrics.iat[0,3]]
    colors = ['yellowgreen', 'lightsteelblue', 'lightcoral']
    explode = (0.1,0.1,0.1)
    patches, texts, autotexts = plt.pie(sizes, colors=colors, startangle=0, counterclock=True, autopct='%1.1f%%', pctdistance=1.2, explode=explode)
    centre_circle=plt.Circle( (-0.075,-0.045), 0.6, color='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)    
    
    plt.legend(patches, labels, title=r'$\bf{Emission \ categories}$',loc="lower left", bbox_to_anchor=(0.65, 0, 0.5, 1))
    plt.axis('equal')
    plt.tight_layout()
    plt.title(r'$\bf{GHGs \ emissions \ breakdown \ for \ hybrid \ system}$' + '\n \n')
        
    # Name the figure and save it in the corresponding directory
    plot_name = "GHGsBreakdown_Opt_{}_Re{}_Load{}.png".format(Systype, Reliability, Loadtype)   
    plt.savefig(plot_dir + plot_name, dpi=300)
    plt.show()
    
    print('\nFigure saved as ', plot_name)  
    
    # Obtain the hourly energy performance of the system, divided by technology
       
    # Run simulation of optimization file  
    df_simulation=Energy_System().lifetime_simulation(df_hybridopt)
    
    # Add a column with the hour to simulation file
    hours=pd.Series(data=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])   
    length = len(df_simulation.index)
    num=int(length/len(hours))
    hours_column = pd.concat([hours]*num, ignore_index=True)   
    df_simulation['Hour']=hours_column     
    hourly_variables=pd.DataFrame(columns=[df_simulation.columns])
    hourly_variables['Hour']=hours
    
    # Obtain hourly average of all variables in simulation    
    for column in df_simulation.columns:
            
               hourly_mean=pd.DataFrame()
               
               for i in range(0, 24):
    
                  df_i = df_simulation.loc[df_simulation['Hour'] == i].mean(axis=0).loc[column]   
                  dflocal = pd.DataFrame([df_i])      
                  hourly_mean=pd.concat([hourly_mean, dflocal])
                  
               hourly_variables[column]=list(hourly_mean[0])
           
    hourly_plot=hourly_variables[['Load energy (kWh)','Renewables energy supplied (kWh)','Storage energy supplied (kWh)','Dumped energy (kWh)','Diesel energy (kWh)']]
    
    # Move variables that want to represent to a different variable for plotting           
    for i in range(1, 24):
        
        hourly_plot.iat[i,2]=hourly_variables.iat[i-1,12]-hourly_variables.iat[i,12]
       
    # Average hourly energy use figure
    x = hours
    labels=[]
    length = len(hourly_plot.keys())
    allloads = list(hourly_plot.items())
    Loadsforfigures=[]
    fig, ax = plt.subplots()
    
    # Extract variables for plotting        
    for n in range(0, length):

           load=allloads[n]
           name=str(load[0])
           labels.append(name[2:-9])
           Loadsforfigures.append(load[1])
    
    # Plot hourly load and hourly energy performance    
    ax.plot(x,Loadsforfigures[0]) 
    ax.fill(x,Loadsforfigures[1], color='gold', alpha=0.7)
    ax.fill(x,Loadsforfigures[2], color='yellowgreen', alpha=0.7)
    ax.fill(x,-Loadsforfigures[3], color='lightsteelblue', alpha=0.7)    
    ax.fill_between(x,Loadsforfigures[4],y2=0, color='palevioletred', alpha=0.7)
      
    ax.set(xlabel='Hour of day', ylabel='Energy (kWh)')
    ax.grid()
    ax.legend(labels, loc='upper left', fontsize=8)
    plt.tight_layout()
    plt.xticks([0,4,8,12,16,20,23])
    plt.xlim((0,23))    
    plt.ylim((-5,25))          
    
    # Name the figure and save it in the corresponding directory
    plot_name = "HourlyEnergyProfile_{}_Re{}_Load{}.png".format(Systype, Reliability, Loadtype)    
    plt.savefig(plot_dir + plot_name, dpi=300)
    plt.show()    
    
    print('Figure saved as '+plot_name)
    
    
def PVBatt_sys_performance (max_blackouts, Loadtype, accuracy):
    """
    Simulate performance of diesel-PV-battery system for the selected scenario 
    
    Input: max_blackouts  Maximum acceptible blackouts (0.0-1.0)
           Load profile for the selected scenario, between 'InstitutionalBase', 'InstitutionalAdv', 'Mix1', 'Mix2'
        
    Output: File of optimisation to be analysed with PVbatt_sys_stats()      
    
    """  
    # Read the load .csv file containing hourly load information of the selected facility    
    filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Scenario/Scenario inputs.csv"    
    df_scenario = pd.read_csv(filepath, header=None)
    
    # Define reliability from the blackouts level
    Reliability= int((1.0 - max_blackouts)*100.0)
    
    # Performance studied for the PV-battery system
    Systype = 'PVBatt'
    
    # Check if simulation for blackout level exists already, if not, performs simulation
    check = os.path.exists(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv".format(Systype, Reliability, Loadtype)) 
    
    if check == False :
        
        # Read the load .csv file containing hourly load information of the selected facility     
        print('\n Simulation doesn\'t exist, starting with optimisation...')
    
        # Set maximum blackout threshold (0.0-1.0)
        if df_scenario.iat[3, 1] != max_blackouts :
            df_scenario.iat[3, 1] = max_blackouts
    
        # Substitute new values in Scenario  Inputs.csv file for simulation
        df_scenario.to_csv(filepath, index=None, header =None)
        
        # Simulate diesel system and saves file as i.e.: Sim_PV0_Storage0_Diesel_Re90_LoadInstitutionalBase.csv
        Optimisation = optimise_system (Systype, Loadtype, max_blackouts, accuracy)
        
        print('\n Optimisation finished, proceed with PVBatt_sys_stats(max_blackouts, Loadtype) to display results ...')
        
    else:
        
        print('\n Optimisation already exists, proceed with PVBatt_sys_stats(max_blackouts, Loadtype) to display results...')
    
    
def PVBatt_sys_stats (max_blackouts, Loadtype):
    """
    Present costs, GHGs, renewable fraction of PV-battery system for the selected scenario 
    
    Input: Optimisation file resulting of hybrid_sys_performance(max_blackouts, Loadtype)
        
    Output: Display LCUE, emissions intensity, Diesel capacity, Diesel fuel usage
             Save them in Key_Metrics.csv file 
            Display breakdown of costs:Total System Cost, Total fuel cost, total O&M cost
             Save them in Financial_Metrics.csv file 
            Display breakdown of emissions: Total, System, Fuel, O&M
             Save them in Environmental_Metrics.csv file 
            Save .png figures on /Saved Optimisations/Optimisation Name*/ directory    
     
    """ 
    # Performance displayed for PV-Battery system
    Systype = 'PVBatt'
    Reliability= int((1 - max_blackouts)*100)
    
    # Read csv file with diesel system simulation data
    df_PVBattopt = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv'.format(Systype, Reliability, Loadtype))
  
    # Obtain LCUE, emissions intensity, Renewables fraction, Total system cost, Cumulative GHGs
    Appraisal_indexes=[18,14,15,8,10]        
    df_keymetrics=df_PVBattopt.iloc[2, Appraisal_indexes]
    df_keymetrics.iat[0]=df_PVBattopt["Renewables fraction"].mean()
    df_keymetrics.iat[2]=df_PVBattopt["Emissions intensity (gCO2/kWh)"].mean()
    
    # Create a directory with the name of the simulation to save the figures 
    script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/")
    plot_dir = os.path.join(script_dir, 'Opt_{}_Re{}_Load{}/'.format(Systype, Reliability, Loadtype))
    
    if not os.path.isdir(plot_dir):
        os.makedirs(plot_dir)
    
    # Save key metrics obtained in a .csv file
    df_keymetrics=pd.DataFrame(df_keymetrics)    
    df_keymetrics=df_keymetrics.transpose()
    df_keymetrics.to_csv(rself.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}/Key_Metrics.csv'.format(Systype, Reliability, Loadtype), index=False, header=True)
  
    print('\nKey system metrics saved as Key_Metrics.csv \n')
    print(df_keymetrics)
    
    # Display breakdown of costs:Total System Cost, Total equipment cost, total O&M cost, total fuel cost     
    Financial_indexes=[29, 30, 32, 33]        
    df_financialmetricsperyear=df_PVBattopt.iloc[:, Financial_indexes]
    df_financialmetrics= pd.DataFrame(df_financialmetricsperyear.sum())
    df_financialmetrics=df_financialmetrics.transpose()
    
    # Calculate new PV, storage and diesel installations over lifetime
    PV_array_size = pd.Series([df_PVBattopt.iloc[0,3], df_PVBattopt.iloc[1,3]-df_PVBattopt.iloc[0,5],df_PVBattopt.iloc[2,3]-df_PVBattopt.iloc[1,5]])
    storage_size = pd.Series([df_PVBattopt.iloc[0,4], df_PVBattopt.iloc[1,4]-df_PVBattopt.iloc[0,6],df_PVBattopt.iloc[2,4]-df_PVBattopt.iloc[1,6]])
    
    # Calculate cost of installations over lifetime
    PV_cost_array = Finance().get_PV_cost(PV_array_size,0)
    BOS_cost_array = Finance().get_BOS_cost(PV_array_size,0)
    storage_cost_array = Finance().get_storage_cost(storage_size,0)
    
    # Discount fraction used for discount rate of 9.5%
    discount_fraction = [((1.0 - 0.095)**0),((1.0 - 0.095)**5),((1.0 - 0.095)**10)]
    
    PV_cost = sum(np.multiply(PV_cost_array,discount_fraction))
    storage_cost = sum(np.multiply(storage_cost_array,discount_fraction))
    BOS_cost = sum(np.multiply(BOS_cost_array,discount_fraction))   
    Other_equip_cost = df_financialmetrics.iat[0,1]-(PV_cost+BOS_cost+storage_cost)
    
    df_equipmentcost=pd.DataFrame()
    df_equipmentcost['PV Cost']=PV_cost
    df_equipmentcost['Storage Cost']=storage_cost
    df_equipmentcost['BOS Cost']=BOS_cost
    df_equipmentcost['Other equipment Cost']= Other_equip_cost
 
    # Save financial metrics obtained in .csv file
    df_financialmetrics.to_csv(rself.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}/Financial_Metrics.csv'.format(Systype, Reliability, Loadtype), index=None)
    print('Financial metrics saved as Financial_Metrics.csv \n')
    
    # Save equipment cost breakdown in .csv file
    df_equipmentcost.to_csv(rself.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}/Equipment_costs.csv'.format(Systype, Reliability, Loadtype), index=None)
    print('Equipment costs saved as Financial_Metrics.csv \n')
    
    # Cost Breakdown Donught   
    labels = ['PV Cost', 'Storage Cost', 'BOS Cost', 'Other equipment costs', 'O&M cost']
    sizes = [PV_cost, storage_cost, BOS_cost, Other_equip_cost, df_financialmetrics.iat[0,2]]
    colors = ['gold','yellowgreen','darkcyan','steelblue', 'lightsteelblue']
    explode = (0.1,0.1,0.1,0.1,0.1)
    patches, texts, autotexts = plt.pie(sizes, colors=colors, startangle=180, counterclock=False, autopct='%1.1f%%', pctdistance=1.2, explode=explode)
    centre_circle=plt.Circle( (0.05,0), 0.6, color='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    
    plt.legend(patches, labels, title=r'$\bf{Cost \ categories}$',loc="lower left", bbox_to_anchor=(0.65, -0.05, 0.5, 1))
    plt.axis('equal')
    plt.tight_layout()
    plt.title(r'$\bf{Cost \ breakdown \ for \ PV-battery \ system}$' + '\n \n')
        
    # Name the figure and save it in the corresponding directory
    plot_name = "CostBreakdown_Opt_{}_Re{}_Load{}.png".format(Systype, Reliability, Loadtype)    
    plt.savefig(plot_dir + plot_name, dpi=300)
    plt.show()
    
    print('\nFigure saved as ', plot_name)  
         
    # Obtain breakdown of emissions: Total emissions, Equipment emissions, O&M emissions, fuel emissions        
    Environmental_indexes=[37, 39, 41, 42]        
    df_environmentalmetricsperyear=df_PVBattopt.iloc[:, Environmental_indexes]
    df_environmentalmetrics= pd.DataFrame(df_environmentalmetricsperyear.sum())
    df_environmentalmetrics=df_environmentalmetrics.transpose()
    
    # Save environmental metrics in .csv file
    df_environmentalmetrics.to_csv(rself.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}/Environmental_Metrics.csv'.format(Systype, Reliability, Loadtype), index=None)
    print('\nEnvironmental metrics saved as Environmental_Metrics.csv \n')
    
    # GHGs Emissions Breakdown Donught 
    labels = ['New equipment emissions', 'O&M emissions']
    sizes = [df_environmentalmetrics.iat[0,1], df_environmentalmetrics.iat[0,2]]
    colors = ['yellowgreen', 'lightsteelblue']
    explode = (0.1,0.1)
    patches, texts, autotexts = plt.pie(sizes, colors=colors, startangle=0, counterclock=False, autopct='%1.1f%%', pctdistance=1.2, explode=explode)
    centre_circle=plt.Circle( (-0.07,-0.05), 0.6, color='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    
    plt.legend(patches, labels, title=r'$\bf{Emission \ categories}$',loc="lower left", bbox_to_anchor=(0.65, 0.1, 0.5, 1))
    plt.axis('equal')
    plt.tight_layout()
    plt.title(r'$\bf{GHGs \ emissions \ breakdown \ for \ PV-Battery \ system}$' + '\n \n')
        
    # Name the figure and save it in the corresponding directory
    plot_name = "GHGsBreakdown_Opt_{}_Re{}_Load{}.png".format(Systype, Reliability, Loadtype)  
    plt.savefig(plot_dir + plot_name, dpi=300)
    plt.show()
    
    print('\nFigure saved as ', plot_name)  

    # Obtain the hourly energy performance of the system, divided by technology
       
    # Run simulation of optimization file  
    df_simulation=Energy_System().lifetime_simulation(df_PVBattopt)
    
    # Add a column with the hour to simulation file
    hours=pd.Series(data=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
    length = len(df_simulation.index)
    num=int(length/len(hours))
    hours_column = pd.concat([hours]*num, ignore_index=True)
    df_simulation['Hour']=hours_column  
    hourly_variables=pd.DataFrame(columns=[df_simulation.columns])
    hourly_variables['Hour']=hours    
    
    # Obtain hourly average of all variables in simulation 
    for column in df_simulation.columns:
            
               hourly_mean=pd.DataFrame()
               
               for i in range(0, 24):
    
                  df_i = df_simulation.loc[df_simulation['Hour'] == i].mean(axis=0).loc[column]
                  dflocal = pd.DataFrame([df_i])
                  hourly_mean=pd.concat([hourly_mean, dflocal])
                  
               hourly_variables[column]=list(hourly_mean[0])
                    
    hourly_plot=hourly_variables[['Load energy (kWh)','Renewables energy supplied (kWh)','Dumped energy (kWh)','Storage energy supplied (kWh)']]

    # Move variables that want to represent to a different variable for plotting                     
    for i in range(1, 24):
        
        hourly_plot.iat[i,3]=hourly_variables.iat[i-1,12]-hourly_variables.iat[i,12]
       
    # Extract variables for plotting
    x = hours
    labels=[]
    length = len(hourly_plot.keys())
    allloads = list(hourly_plot.items())
    Loadsforfigures=[]
    fig, ax = plt.subplots()
             
    for n in range(0, length):

           load=allloads[n]
           name=str(load[0])
           labels.append(name[2:-9])
           Loadsforfigures.append(load[1])
           
    # Plot hourly load and hourly energy performance    
    ax.plot(x,Loadsforfigures[0]) 
    ax.fill(x,Loadsforfigures[1], color='gold', alpha=0.7)
    ax.fill(x,-Loadsforfigures[2], color='lightsteelblue', alpha=0.7)
    ax.fill_between(x,Loadsforfigures[3], y2=0, color='yellowgreen', alpha=0.7)       
       
    ax.set(xlabel='Hour of day', ylabel='Energy (kWh)')
    ax.grid()
    ax.legend(labels, loc='upper left', fontsize=8)
    plt.tight_layout()
    plt.xticks([0,4,8,12,16,20,23])
    plt.xlim((0,23)) 
    plt.ylim((-50,70))
    plt.yticks([-50,-40,-20,0,20,40,60,70])            
    
    # Name the figure and save it in the corresponding directory
    plot_name = "HourlyEnergyProfile_{}_Re{}_Load{}.png".format(Systype, Reliability, Loadtype)    
    plt.savefig(plot_dir + plot_name, dpi=300)
    plt.show()    
    
    print('Figure saved as '+plot_name)
    
    #hourly_plot.to_csv(rself.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}/HourlyEnergy.csv'.format(Systype, Reliability, Loadtype), index=None)
    #print('\n Hourly energy performance saved as HourlyEnergy.csv')
    

def compare_keymetrics (max_blackouts, Loadtype):
    """
    Compare LCUE, renewables fraction, GHG savings, diesel savings compared to base diesel case
    
    Input: max_blackouts  Maximum acceptible blackouts (0.0-1.0)
           Load profile for the selected scenario, between 'InstitutionalBase', 'InstitutionalAdv', 'Mix1', 'Mix2'
        
    Output: Display barchart comparing key metrics: LCUE, renewables fraction, GHG savings, diesel savings, total cost savings
            Save on /Plots/Plots Comparison/ directory  .png graphs       
    
    """ 
    # Read the data from Key_Metrics.csv files for diesel, hybrid and PVBatt systems for the reliability level selected
    Reliability= int((1 - max_blackouts)*100)
    
    df_dieselmetrics = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV0_Storage0_Diesel_Re{}_Load{}/Key_Metrics.csv'.format(Reliability, Loadtype))
    df_hybridmetrics = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_Hybrid_Re{}_Load{}/Key_Metrics.csv'.format(Reliability, Loadtype))
    df_PVBattmetrics = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_PVBatt_Re{}_Load{}/Key_Metrics.csv'.format(Reliability, Loadtype))
    

    # Display barchart comparing key metrics: LCUE, Emissions intensity, Total Costs and Total Emissions
    
    # Create color palet for figure    
    my_colors = ['lightcoral', 'lightskyblue', 'yellowgreen']
    
    # First subplot, LCUE
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    ax1.bar(height=[df_dieselmetrics.iat[0,1], df_hybridmetrics.iat[0,1], df_PVBattmetrics.iat[0,1]], x = ["Diesel", "Hybrid", "PV-Batt"], width=0.6, color=my_colors)
    ax1.set_title('LCUE', fontweight="bold",fontsize=10)
    
    # Second subplot, Total System Cost
    ax2.bar(height=[df_dieselmetrics.iat[0,3]/1000, df_hybridmetrics.iat[0,3]/1000, df_PVBattmetrics.iat[0,3]/1000], x = ["Diesel", "Hybrid", "PV-Batt"], width=0.6, color=my_colors)
    ax2.set_title('Total System Cost', fontweight="bold",fontsize=10)
    
    # Third subplot, Emissions Intensity
    ax3.bar(height=[df_dieselmetrics.iat[0,2], df_hybridmetrics.iat[0,2], df_PVBattmetrics.iat[0,2]], x = ["Diesel", "Hybrid", "PV-Batt"], width=0.6, color=my_colors)
    ax3.set_title(r'$\bf{Emissions \ Intensity}$', fontweight="bold",fontsize=10)
    
    # Fourth subplot, Cumulative Emissions
    ax4.bar(height=[df_dieselmetrics.iat[0,4]/1000, df_hybridmetrics.iat[0,4]/1000, df_PVBattmetrics.iat[0,4]/1000], x = ["Diesel", "Hybrid", "PV-Batt"], width=0.6, color=my_colors)
    ax4.set_title('Total Emissions', fontweight="bold",fontsize=10)

    # Set labels for axis
    ax1.set(ylabel='$/kWh')
    ax1.set_yticks([0,0.1,0.2,0.3,0.4,0.5,0.6])
    ax2.set(ylabel='Thousands of $')
    ax2.set_yticks([0,100,200,300,400,500])
    ax3.set(ylabel='gCO2eq/kWh', xlabel='System Type')
    ax3.set_yticks([0,250,500,750,1000,1200])
    ax4.set(xlabel='System Type', ylabel='tCO2eq')
    ax4.set_yticks([0,400,800,1200,1600])
    
    plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, hspace=0.35)
    
    fig.tight_layout() 
    
    # Create a directory to save the figure 
    script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/")
    plot_dir = os.path.join(script_dir, 'Analysis/Comparison_Re{}_Load{}/'.format(Reliability, Loadtype))
    plot_name = 'KeyMetrics_Comparison_Re{}_Load{}.png'.format(Reliability, Loadtype)
    
    if not os.path.isdir(plot_dir):
        os.makedirs(plot_dir)
    
    fig.savefig(plot_dir + plot_name,dpi=300)
    plt.show()
 
    print('Figure saved as ', plot_name)  
    
def compare_costs (max_blackouts, Loadtype):
    """
    Present costs breakdown for PVBatt/hybrid syst compared to base case of diesel-powered system for the selected scenario 
    
    Input: max_blackouts  Maximum acceptible blackouts (0.0-1.0)
           Load profile for the selected scenario, between 'InstitutionalBase', 'InstitutionalAdv', 'Mix1', 'Mix2'
           
    Output: Display barchart of breakdown of costs savings/expenditures of hybrid/PVbatt systems compared to diesel case
            Save on /Plots/Plots Comparison/ directory  .png graphs 
            
    """ 
    # Read the data from Financial_Metrics.csv files for diesel, hybrid and PVBatt systems for the reliability level
    Reliability= int((1 - max_blackouts)*100)
    
    df_dieselcosts = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV0_Storage0_Diesel_Re{}_Load{}/Financial_Metrics.csv'.format(Reliability, Loadtype))
    df_hybridcosts = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_Hybrid_Re{}_Load{}/Financial_Metrics.csv'.format(Reliability, Loadtype))
    df_PVBattcosts = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_PVBatt_Re{}_Load{}/Financial_Metrics.csv'.format(Reliability, Loadtype))
    
    # Calculate the difference of costs between hybrid and PVBatt system vs base diesel case
    df_hybridcosts_comparison= df_hybridcosts - df_dieselcosts
    df_PVBattcosts_comparison= df_PVBattcosts - df_dieselcosts
    
    # Represent barchart with the breakdown of costs of hybrid/PVBatt systems compared to diesel base
    labels = ['Total System\n Costs', 'New Equipment \n Costs', 'O&M Costs \n (excluding fuel)', 'Fuel Costs']
    hybrid_means = df_hybridcosts_comparison.iloc[0]/1000
    PVBatt_means = df_PVBattcosts_comparison.iloc[0]/1000

    x = np.arange(len(labels))  # the label locations
    width = 0.43  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, hybrid_means, width, label='Hybrid System', color='lightskyblue')
    rects2 = ax.bar(x + width/2, PVBatt_means, width, label='PV-Battery System', color='yellowgreen')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Thousands of $')
    ax.set_title(r'$\bf{Cost \ breakdown \ comparison \ by \ system}$'+'\n Values compared to base case with diesel system \n')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.xaxis.set_label_position('bottom')
    ax.legend(loc='lower center')
    ax.set_ylim([-475, 325])
    
    # Attach a text label above each bar in *rects*, displaying its height.
    percentagehybrid= ((df_hybridcosts - df_dieselcosts)/df_dieselcosts)*100.0
    pctcostshybrid=percentagehybrid.iloc[0]

    percentagePVBatt= ((df_PVBattcosts - df_dieselcosts)/df_dieselcosts)*100.0
    pctcostsPVBatt=percentagePVBatt.iloc[0]

    def autolabel(rects):
        
        for rect in rects:   

               height = rect.get_height()                 
                              
               for i in range(0,4):
                   
                   if height == hybrid_means[i]:
                   
                     percentage = pctcostshybrid[i]
                     pctrounded = round(percentage, 0)
                     pct=int(pctrounded)
                                
                     if pct >= 0.0:
                                                
                        ax.annotate('+'+str(pct)+'%',
                          xy=(rect.get_x() + rect.get_width() / 2, height),
                          xytext=(0, 3),  # 3 points vertical offset
                          textcoords="offset points",
                          ha='center', va='bottom', size=8)
                        
                     else:
                         
                        ax.annotate(str(pct)+'%',
                          xy=(rect.get_x() + rect.get_width() / 2, height),
                          xytext=(0, -15),  # 3 points vertical offset
                          textcoords="offset points",
                          ha='center', va='bottom', size=8)

                   elif height == PVBatt_means[i]:
                   
                     percentage = pctcostsPVBatt[i]
                     pctrounded = round(percentage, 0)
                     pct=int(pctrounded)                     
                     
                     if pct >= 0.0:
                                                
                        ax.annotate('+'+str(pct)+'%',
                          xy=(rect.get_x() + rect.get_width() / 2, height),
                          xytext=(0, 3),  # 3 points vertical offset
                          textcoords="offset points",
                          ha='center', va='bottom', size=8)
                        
                     else:
                        ax.annotate(str(pct)+'%',
                          xy=(rect.get_x() + rect.get_width() / 2, height),
                          xytext=(0, -15),  # 3 points vertical offset
                          textcoords="offset points",
                          ha='center', va='bottom', size=8)                        
    
    # Include the labels in the plot           
    autolabel(rects1)
    autolabel(rects2)
 
    fig.tight_layout()

    # Create a directory to save the figure 
    script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/")
    plot_dir = os.path.join(script_dir, 'Analysis/Comparison_Re{}_Load{}/'.format(Reliability, Loadtype))
    plot_name = 'CostBreakdown_Comparison_Re{}_Load{}.png'.format(Reliability, Loadtype)
    
    if not os.path.isdir(plot_dir):
        os.makedirs(plot_dir)
    
    fig.savefig(plot_dir + plot_name,dpi=300)
    plt.show()

    print('Figure saved as ', plot_name)  
    


def compare_GHGs (max_blackouts, Loadtype):
    """
    Present  GHGs breakdown of PVBatt/Hybrid systems vs base case of diesel-powered system for the selected scenario 
    
    Input: max_blackouts  Maximum acceptible blackouts (0.0-1.0)
           Load profile for the selected scenario, between 'InstitutionalBase', 'InstitutionalAdv', 'Mix1', 'Mix2'
           
    Output: Display barchart of breakdown of costs savings/expenditures of hybrid/PVbatt systems compared to diesel case
            Save on /Plots/Plots Comparison/ directory  .png graphs 
            
    """ 
    # Read the data from Environmental_Metrics.csv files for diesel, hybrid and PVBatt systems for that reliability level
    Reliability= int((1 - max_blackouts)*100)
    
    df_dieselGHGs = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV0_Storage0_Diesel_Re{}_Load{}/Environmental_Metrics.csv'.format(Reliability, Loadtype))
    df_hybridGHGs = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_Hybrid_Re{}_Load{}/Environmental_Metrics.csv'.format(Reliability, Loadtype))
    df_PVBattGHGs = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_PVBatt_Re{}_Load{}/Environmental_Metrics.csv'.format(Reliability, Loadtype))
    
    # Calculate the difference of emissions between hybrid and PVBatt system vs base diesel case
    df_hybridGHGs_comparison= df_hybridGHGs - df_dieselGHGs
    df_PVBattGHGs_comparison= df_PVBattGHGs - df_dieselGHGs
    
    # Represent barchart with the breakdown of emissions of hybrid/PVBatt systems compared to diesel base
    labels = ['Total System\n Emissions', 'New Equipment \n Emissions', 'O&M Emissions \n (excluding fuel)', 'Fuel Emissions']
    hybrid_means = df_hybridGHGs_comparison.iloc[0]/1000
    PVBatt_means = df_PVBattGHGs_comparison.iloc[0]/1000

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, hybrid_means, width, label='Hybrid System', color='lightskyblue')
    rects2 = ax.bar(x + width/2, PVBatt_means, width, label='PV-Battery System', color='yellowgreen')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('tonnes of CO2eq')
    ax.set_title(r'$\bf{Emissions \ breakdown \ comparison \ by \ system}$'+'\n Values compared to base case with diesel system \n')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.xaxis.set_label_position('bottom')
    ax.legend(loc='lower center')   
    ax.set_ylim([-1750, 500])
    ax.set_yticks([-1750,-1500,-1250,-1000,-750,-500,-250,0,250, 500])
    
    #Attach a text label above each bar in *rects*, displaying its height.
    percentagehybrid= ((df_hybridGHGs - df_dieselGHGs)/df_dieselGHGs)*100.0
    pctGHGhybrid=percentagehybrid.iloc[0]

    percentagePVBatt= ((df_PVBattGHGs - df_dieselGHGs)/df_dieselGHGs)*100.0
    pctGHGPVBatt=percentagePVBatt.iloc[0]
    
    def autolabel(rects):
        
        for rect in rects:   

               height = rect.get_height()                 
                              
               for i in range(0,4):
                   
                   if height == hybrid_means[i]:
                   
                     percentage = pctGHGhybrid[i]
                     pctrounded = round(percentage, 0)
                     pct=int(pctrounded)
                                          
                     if pct >= 0.0:
                                                
                        ax.annotate('+'+str(pct)+'%',
                          xy=(rect.get_x() + rect.get_width() / 2, height),
                          xytext=(0, 3),  # 3 points vertical offset
                          textcoords="offset points",
                          ha='center', va='bottom', size=8)
                        
                     else:
                        ax.annotate(str(pct)+'%',
                          xy=(rect.get_x() + rect.get_width() / 2, height),
                          xytext=(0, -15),  # 3 points vertical offset
                          textcoords="offset points",
                          ha='center', va='bottom', size=8)

                   elif height == PVBatt_means[i]:
                   
                     percentage = pctGHGPVBatt[i]
                     pctrounded = round(percentage, 0)
                     pct=int(pctrounded)                     
                     
                     if pct >= 0.0:
                                                
                        ax.annotate('+'+str(pct)+'%',
                          xy=(rect.get_x() + rect.get_width() / 2, height),
                          xytext=(0, 3),  # 3 points vertical offset
                          textcoords="offset points",
                          ha='center', va='bottom', size=8)
                        
                     else:
                        ax.annotate(str(pct)+'%',
                          xy=(rect.get_x() + rect.get_width() / 2, height),
                          xytext=(0, -15),  # 3 points vertical offset
                          textcoords="offset points",
                          ha='center', va='bottom', size=8)                        
               
    # Include labels in figure
    autolabel(rects1)
    autolabel(rects2)
 
    fig.tight_layout()

    # Create a directory to save the figure 
    script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/")
    plot_dir = os.path.join(script_dir, 'Analysis/Comparison_Re{}_Load{}/'.format(Reliability, Loadtype))
    plot_name = 'GHGsBreakdown_Comparison_Re{}_Load{}.png'.format(Reliability, Loadtype)
    
    if not os.path.isdir(plot_dir):
        os.makedirs(plot_dir)
    
    fig.savefig(plot_dir + plot_name,dpi=300)
    plt.show()

    print('Figure saved as ', plot_name)  


# =============================================================================
#                           Sensitivity analysis
# =============================================================================   
#
    
def LCUE_sensitivity (Loadtype, initial_max_blackout, final_max_blackout, stepsize, accuracy):
    """
    Compare LCUE for diesel/hybrid/PVbatt systems for different reliability thresholds 
    
    Input: Minimum and maximum reliability thresholds for analysis (0-1), stepsize and load type
        
    Output: Display LCUE of each system vs reliability for "stepsize" resolution in reliability levels
            Save .csv files and .png graphs in Analysis/Sensitivity Analysis directory       
    
    """  
    # Define initial and final reliability levels for sensitivity analysis
    initial_Reliability= int((1.0 - initial_max_blackout)*100.0)
    final_Reliability= int((1.0 - final_max_blackout)*100.0)
    
    # Open optimisation and scenario inputs file
    filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Scenario/Scenario inputs.csv"
                
    # Locate and open Optimisation inputs file
    filepathopt = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Optimisation inputs.csv"
    
    # Create dataframe for LCUE vs Reliability data for diesel, hybrid and PVBatt systems:
    df_LCUEvsRe = pd.DataFrame(columns=['Reliability','LCUE Diesel System', 'LCUE Hybrid System', 'LCUE PV-Batt System'])
    
    # Initialise counter to locate the reliabily results 
    count=0
    
    # For each realiability value in the range specified:
    for blackouts in np.arange(final_max_blackout, initial_max_blackout+0.01, stepsize):
        
        Reliability= int((1 - blackouts)*100)
        
        # Substitute new values in Scenario  Inputs.csv file for simulation
        df_scenario = pd.read_csv(filepath, header=None)
                
        # Substitute new values in Scenario  Inputs.csv file for simulation
        df_scenario.to_csv(filepath, index=None, header =None)
        
        # Substitute new values in Optimisation inputs.csv file for optimisation
        df_optimisation = pd.read_csv(filepathopt, header=None)                   
        df_optimisation.to_csv(filepathopt, index=None, header =None)
        
        # Set maximum blackout threshold (0.0-1.0) in scenario inputs
        if df_scenario.iat[3, 1] != 1.0 - Reliability/100 :
               df_scenario.iat[3, 1] = 1.0 - Reliability/100
               
        # Set reliability (blackout threshold) for optimisation inputs
        df_optimisation.iat[11,1] = 1.0 - Reliability/100
                                                                             
        # For each type of system        
        types = ['diesel','hybrid','PVBatt']        
        for Systype in types:
            
            # Check if simulation for blackout level exists already, if not, performs simulation for diesel, hybrid and/or PVBatt
            if Systype == 'diesel':
                
                check = os.path.exists(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV0_Storage0_{}_Re{}_LoadInstitutionalBase.csv".format(Systype, Reliability, Loadtype) ) 
    
                if check == False :
                
                    print('\n Simulation for {} system with Reliability {}% doesn\'t exist, simulation in progress...'.format(Systype, Reliability))
        
                    # Simulate system for that reliability level and save results              
                    diesel_sys_performance (blackouts, Loadtype)
                    diesel_sys_stats (blackouts, Loadtype)
                    
                else:
                
                   print('\n Simulation for {} system with Reliability {}% found, continuing with the analysis ...'.format(Systype, Reliability))
                
            elif Systype == 'hybrid':
                
                check = os.path.exists(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv".format(Systype, Reliability, Loadtype) ) 
    
                if check == False :
                
                    print('\n Simulation for {} system with Reliability {}% doesn\'t exist, simulation in progress...'.format(Systype, Reliability))
        
                    # Simulate system for that reliability level and save results                                   
                    hybrid_sys_performance (blackouts, Loadtype, accuracy)
                    hybrid_sys_stats (blackouts, Loadtype)
                    
                else:
                
                   print('\n Simulation for {} system with Reliability {}% found, continuing with the analysis ...'.format(Systype, Reliability))
                    
            elif Systype == 'PVBatt':
                
                check = os.path.exists(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv".format(Systype, Reliability, Loadtype) ) 
    
                if check == False :
                
                    print('\n Simulation for {} system with Reliability {}% doesn\'t exist, simulation in progress...'.format(Systype, Reliability))
        
                    # Simulate system for that reliability level and save results                                   
                    PVBatt_sys_performance (blackouts, Loadtype, accuracy)
                    PVBatt_sys_stats (blackouts, Loadtype)
                        
                    print('\n Simulation for {} system with Reliability {}%finished, continuig with the evaluation ...'.format(Systype, Reliability))
        
                else:
                
                   print('\n Simulation for {} system with Reliability {}% found, continuing with the analysis ...'.format(Systype, Reliability))
        
        # Read the optimisation files existent or created
        df_dieselmetrics = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV0_Storage0_Diesel_Re{}_Load{}/Key_Metrics.csv'.format(Reliability, Loadtype))
        df_hybridmetrics = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_Hybrid_Re{}_Load{}/Key_Metrics.csv'.format(Reliability, Loadtype))
        df_PVBattmetrics = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_PVBatt_Re{}_Load{}/Key_Metrics.csv'.format(Reliability, Loadtype))
         
        # Locate the corresponding LCUE values of each system type for each reliability level
        df_LCUEvsRe.loc[count] = [Reliability, df_dieselmetrics.iat[0,1], df_hybridmetrics.iat[0,1],  df_PVBattmetrics.iat[0,1]] 
                             
        print('\nData for Reliability {}% saved.'.format(Reliability))
  
        # Add to the counter to locate results in the corresponding place      
        count +=1
    
    # Save Reliability vs LCUE data on a csv file:
    
    # Create a directory with the name of the data and save it
    script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Analysis/Sensitivity Analysis/")
    plot_dir = os.path.join(script_dir, 'Sensitivity_Re{}to{}_Load{}/'.format(initial_Reliability, final_Reliability, Loadtype))
    
    if not os.path.isdir(plot_dir):
          os.makedirs(plot_dir)
    
    filepath=self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Analysis/Sensitivity Analysis/Sensitivity_Re{}to{}_Load{}/LCUE_sensitivity.csv".format(initial_Reliability, final_Reliability, Loadtype)
    df_LCUEvsRe.to_csv(filepath)
            
    # Plot the graphic of Reliability vs LCUE for diesel, hybrid, PVbatt sys:
    ReliabilityX=df_LCUEvsRe.loc[:,'Reliability']
    ReliabilityX[6]=97
    A=sorted(ReliabilityX)
    WW=(df_LCUEvsRe.loc[:,'LCUE PV-Batt System'])
    B=sorted(WW)
    
    fig, ax = plt.subplots()   
    ax.plot(df_LCUEvsRe.loc[:,'Reliability'], df_LCUEvsRe.loc[:,'LCUE Diesel System'], '-', linewidth=3, color="lightcoral")
    ax.plot(df_LCUEvsRe.loc[:,'Reliability'], df_LCUEvsRe.loc[:,'LCUE Hybrid System'], '-', linewidth=3, color="lightskyblue")
    ax.plot(A, B, '-', linewidth=3, color="yellowgreen")
    plt.xlabel("System reliability (%)", fontsize=15)
    plt.ylabel("LCUE ($/kWh)", fontsize=15)
    ax.grid()
    ax.set_xlim((80,100))
    ax.set_ylim((0,0.7))
    ax.set_xticklabels([80,82.5,85,87.5,90,92.5,95,97.5,100],fontsize=15)
    ax.set_yticklabels([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7],fontsize=15)
    labels=['Diesel System','Hybrid System','PV-Battery System']
    ax.legend(labels,fontsize=15, loc='lower right')    
   
    # Save graph in corresponding Sensitivity Analysis directory
    plot_name = "LCUE_Sensitivity_Re{}to{}_Load{}.png".format(initial_Reliability, final_Reliability, Loadtype)     
    fig.savefig(plot_dir + plot_name,dpi=300,bbox_inches='tight')
    plt.show()    

    print('Figure saved as', plot_name)     
    
def GHG_sensitivity (Loadtype, initial_max_blackout, final_max_blackout, stepsize, accuracy):
    """
    Compare GHGs for diesel/hybrid/PVbatt systems for different reliability thresholds 
    
    Input: Minimum and maximum reliability thresholds for analysis (0-1), stepsize and load type
        
    Output: Display GHGs emissions intensity of each system vs reliability for "stepsize" resolution in reliability levels
            Save .csv files and .png graphs in Analysis/Sensitivity Analysis directory       
    
    """  
    # Define initial and final reliability levels for sensitivity analysis
    initial_Reliability= int((1 - initial_max_blackout)*100.0)
    final_Reliability= int((1 - final_max_blackout)*100.0)
    
    # Open optimisation and scenario inputs file
    filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Scenario/Scenario inputs.csv"
                
    # Locate and open Optimisation inputs file
    filepathopt = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Optimisation inputs.csv"
    
    # Create dataframe for LCUE vs Reliability data for diesel, hybrid and PVBatt systems:
    df_GHGvsRe = pd.DataFrame(columns=['Reliability','GHG Diesel System', 'GHG Hybrid System', 'GHG PV-Batt System'])
    
    # Initialise counter to locate the sensitivity results
    count=0
    
    # For each realiability value in the range specified: 
    for blackouts in np.arange(final_max_blackout, initial_max_blackout+0.01, stepsize):
        
        Reliability= int((1.0 - blackouts)*100.0)
        df_scenario = pd.read_csv(filepath, header=None)               
        df_optimisation = pd.read_csv(filepathopt, header=None)        
        
        # Set maximum blackout threshold (0.0-1.0) in scenario inputs
        if df_scenario.iat[3, 1] != 1.0 - Reliability/100.0 :
               df_scenario.iat[3, 1] = 1.0 - Reliability/100.0
               
        # Substitute new values in Scenario  Inputs.csv file for simulation
        df_scenario.to_csv(filepath, index=None, header =None)
               
        # Set reliability (blackout threshold) for optimisation inputs
        df_optimisation.iat[11,1] = 1.0 - Reliability/100.0
        
        # Substitute new values in Optimisation inputs.csv file for optimisation                  
        df_optimisation.to_csv(filepathopt, index=None, header =None)
                                                                              
        # For each type of system        
        types = ['diesel','hybrid','PVBatt']       
        for Systype in types:
            
            # Check if simulation for blackout level exists already, if not, performs simulation for diesel, hybrid and/or PVBatt

            if Systype == 'diesel':
                
                check = os.path.exists(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV0_Storage0_{}_Re{}_LoadInstitutionalBase.csv".format(Systype, Reliability, Loadtype) ) 
    
                if check == False :
                
                    print('\n Simulation for {} system with Reliability {}% doesn\'t exist, simulation in progress...'.format(Systype, Reliability))
        
                    # Simulate system for that reliability level and save results           
                    diesel_sys_performance (blackouts, Loadtype)
                    diesel_sys_stats (blackouts, Loadtype)
                    
                else:
                
                   print('\n Simulation for {} system with Reliability {}% found, continuing with the analysis ...'.format(Systype, Reliability))
                            
            elif Systype == 'hybrid':
                
                check = os.path.exists(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv".format(Systype, Reliability, Loadtype) ) 
    
                if check == False :
                
                    print('\n Simulation for {} system with Reliability {}% doesn\'t exist, simulation in progress...'.format(Systype, Reliability))
        
                    # Simulate system for that reliability level and save results
                    hybrid_sys_performance (blackouts, Loadtype, accuracy)
                    hybrid_sys_stats (blackouts, Loadtype)
                    
                else:
                
                   print('\n Simulation for {} system with Reliability {}% found, continuing with the analysis ...'.format(Systype, Reliability))
                    
            elif Systype == 'PVBatt':
                
                check = os.path.exists(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv".format(Systype, Reliability, Loadtype) ) 
    
                if check == False :
                
                    print('\n Simulation for {} system with Reliability {}% doesn\'t exist, simulation in progress...'.format(Systype, Reliability))
        
                    # Simulate system for that reliability level and save results                                  
                    PVBatt_sys_performance (blackouts, Loadtype, accuracy)
                    PVBatt_sys_stats (blackouts, Loadtype)
                        
                    print('\n Simulation for {} system with Reliability {}%finished, continuig with the evaluation ...'.format(Systype, Reliability))
        
                else:
                
                   print('\n Simulation for {} system with Reliability {}% found, continuing with the analysis ...'.format(Systype, Reliability))

        # Read the optimisation files existent or created              
        df_dieselmetrics = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV0_Storage0_Diesel_Re{}_Load{}/Key_Metrics.csv'.format(Reliability, Loadtype))
        df_hybridmetrics = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_Hybrid_Re{}_Load{}/Key_Metrics.csv'.format(Reliability, Loadtype))
        df_PVBattmetrics = pd.read_csv(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_PVBatt_Re{}_Load{}/Key_Metrics.csv'.format(Reliability, Loadtype))
 
        # Locate the corresponding emission intensity values of each system type for each reliability level           
        df_GHGvsRe.loc[count] = [Reliability, df_dieselmetrics.iat[0,2], df_hybridmetrics.iat[0,2],  df_PVBattmetrics.iat[0,2]] 
                             
        print('\nData for Reliability {}% saved.'.format(Reliability))

        # Add to the counter to locate results in the corresponding place              
        count +=1
    
    # Save Reliability vs LCUE data on a csv file:
    
    # Create a directory with the name of the data and save it
    script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Analysis/Sensitivity Analysis/")
    plot_dir = os.path.join(script_dir, 'Sensitivity_Re{}to{}_Load{}/'.format(initial_Reliability, final_Reliability, Loadtype))
    
    if not os.path.isdir(plot_dir):
          os.makedirs(plot_dir)
    
    filepath=self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Analysis/Sensitivity Analysis/Sensitivity_Re{}to{}_Load{}/GHG_sensitivity.csv".format(initial_Reliability, final_Reliability, Loadtype)
    df_GHGvsRe.to_csv(filepath)
            
    # Plot the graphic of Reliability vs LCUE for diesel, hybrid, PVbatt sys:
    fig, ax = plt.subplots()    
    ax.plot(df_GHGvsRe.loc[:,'Reliability'], df_GHGvsRe.loc[:,'GHG Diesel System'], '-', linewidth=3, color="lightcoral")
    ax.plot(df_GHGvsRe.loc[:,'Reliability'], df_GHGvsRe.loc[:,'GHG Hybrid System'], '-', linewidth=3, color="lightskyblue")
    ax.plot(df_GHGvsRe.loc[:,'Reliability'], df_GHGvsRe.loc[:,'GHG PV-Batt System'], '-', linewidth=3, color="yellowgreen")
 
    plt.xlabel("System reliability (%)",fontsize=15)
    plt.ylabel("Emissions intensity (gCO2/kWh)",fontsize=15)
    ax.grid()
    ax.set_xlim((80,100))
    ax.set_ylim((0,1200))
    ax.set_xticklabels([80,82.5,85,87.5,90,92.5,95,97.5,100],fontsize=15)
    ax.set_yticklabels([0,200,400,600,800,1000,1200],fontsize=15)
    #ax.legend(['Diesel System','GHG Hybrid System','GHG PV-Batt System'], loc='upper center')    
   
    # Save graph in corresponding Sensitivity Analysis directory
    plot_name = "GHG_Sensitivity_Re{}to{}_Load{}.png".format(initial_Reliability, final_Reliability, Loadtype)
        
    fig.savefig(plot_dir + plot_name,dpi=300,bbox_inches='tight')
    plt.show()    

    print('Figure saved as', plot_name)     
    
    
def renewables_sensitivity (Loadtype, max_blackouts, initial_renewablesfraction, final_renewablesfraction, stepsize): 

    """
    Compare LCUE of optimised hybrid systems of a given reliability level for different renewable fractions
    
    Input: Load profile from selected scenario
           Reliability level to perform sensitivity analysis with
           Initial value of renewables fraction considered
           Final value of renewables fraction considered
           Stepsize for the renewables fraction used in sensitivity analysis
        
    Output: Graphic comparing extra costs (LCUE) of increasing renewables fraction of hybrid system      
    
    """     
    
    # Open optimisation and scenario inputs file
    filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Scenario/Scenario inputs.csv"
                
    # Locate and open Optimisation inputs file
    filepathopt = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Optimisation inputs.csv"
        
    # Create dataframe for LCUE vs Reliability data for diesel, hybrid and PVBatt systems:    
    df_LCUEvsRenewableFraction = pd.DataFrame(columns=['Renewables Fraction','LCUE', 'Total System Cost'])
    additional_cost=pd.Series()
    additional_capex=pd.Series()
    
    # Define reliability level from blackout threshold
    Reliability= int((1 - max_blackouts)*100.0)
    
    # For baseline diesel system        
    Systype='Diesel'
    
    # Locate and open baseline diesel system (renewables fraction=0)    
    filepathsys = self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV0_Storage0_{}_Re{}_Load{}_Appraisal.csv'.format(Systype, Reliability, Loadtype)

    # Read csv file with diesel system simulation data
    df_dieselsys = pd.read_csv(filepathsys)
  
    # Obtain Renewable fraction, LCUE, and Total system cost of the diesel system  
    Appraisal_indexes=[18,14,8,30]        
    df_baselinemetrics=df_dieselsys.iloc[-1, Appraisal_indexes]
       
    # For hybrid system        
    Systype='Hybrid'
    
    # Locate and open min LCUE hybrid system (without renewables fraction constraint)    
    filepathsys = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv".format(Systype, Reliability, Loadtype)

    # Read csv file with hybrid system simulation data
    df_hybridsys = pd.read_csv(filepathsys)
  
    # Obtain Renewable fraction, LCUE, and Total system cost of the reference hybrid system
    Appraisal_indexes=[18,14,8,30]        
    df_referencemetrics=df_hybridsys.iloc[2, Appraisal_indexes]
    df_referencemetrics.iat[0]=df_hybridsys["Renewables fraction"].mean()
    df_referencemetrics.iat[3]=df_hybridsys.iat[0,30]
    
    # Set values of reference minimum LCUE system as first lines of data frame     
    df_LCUEvsRenewableFraction.loc[0] = [df_referencemetrics.iat[0], df_referencemetrics.iat[1], df_referencemetrics.iat[2]] 
    additional_cost.loc[0]=0
    additional_capex.loc[0]=0
    
    # Calculate the total sys savings and additional initial costs of reference hybrid system compared to baseline diesel system
    additional_cost.loc[0]=df_baselinemetrics.iat[2]-df_referencemetrics.iat[2]
    additional_capex.loc[0]=df_referencemetrics["New equipment cost ($)"].sum()-df_baselinemetrics.iat[3]
            
    # Initalise counter to locate sensitivity results (first value assigned to first hybrid system)
    count=1
       
    # For each renewables fraction value in the range specified:   
    for fraction in np.arange(initial_renewablesfraction, final_renewablesfraction+stepsize, stepsize):
    
        # Open scenario inputs and optimisation inputs files
        df_scenario = pd.read_csv(filepath, header=None)
        df_optimisation = pd.read_csv(filepathopt, header=None)                    
        
        # Set maximum blackout threshold (0.0-1.0) in scenario inputs
        if df_scenario.iat[3, 1] != max_blackouts :
               df_scenario.iat[3, 1] = max_blackouts
               
        # Substitute new values in Scenario  Inputs.csv file for simulation
        df_scenario.to_csv(filepath, index=None, header =None)
               
        # Set reliability (blackout threshold) for optimisation inputs
        df_optimisation.iat[11,1] = fraction
        df_optimisation.iat[10,1] = 'Renewables fraction'

        # Substitute new values in Optimisation inputs.csv file for optimisation
        df_optimisation.to_csv(filepathopt, index=None, header =None)                                                                      
            
        # Check if simulation for renewables fraction level exists already, if not, performs simulation for diesel, hybrid and/or PVBatt           
        check = os.path.exists(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/RF{}_Opt_{}_Re{}_Load{}.csv".format(fraction, Systype, Reliability, Loadtype)) 
    
        if check == False :
                
            print('\n Simulation for {} system with Renewables fraction {} doesn\'t exist, simulation in progress...'.format(Systype, fraction))
        
            # If doesn't, simulate system for that reliability level and save results                                   
            hybrid_sys_performance_RF (max_blackouts, Loadtype, fraction)
                               
        else:
                
            print('\n Simulation for {} system with Renewables fraction {} found, continuing with the analysis ...'.format(Systype, fraction))
                    
        # If does, read csv file with hybrid system simulation data
        df_hybridopt = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/RF{}_Opt_{}_Re{}_Load{}.csv'.format(fraction, Systype, Reliability, Loadtype))
  
        # Obtain Renewable fraction, LCUE, and Total system cost of the corresponding hybrid system   
        Appraisal_indexes=[18,14,8,30]        
        df_hybridmetrics=df_hybridopt.iloc[2, Appraisal_indexes]
        df_hybridmetrics.iat[0]=df_hybridopt["Renewables fraction"].mean()
        df_hybridmetrics.iat[3]=df_hybridopt.iat[0,30]
        
        # Obtain total sys savings and additional initial cost compared to baseline diesel system
        additional_cost.loc[count]=df_baselinemetrics.iat[2]-df_hybridmetrics.iat[2]
        additional_capex.loc[count]=df_hybridopt["New equipment cost ($)"].sum()-df_baselinemetrics.iat[3]
        
        # Locate the LCUE, total system cost and renewables fraction in results file
        df_LCUEvsRenewableFraction.loc[count] = [df_hybridmetrics.iat[0], df_hybridmetrics.iat[1], df_hybridmetrics.iat[2]] 
                             
        print('\nData for Renewables fraction {} saved.'.format(fraction))
        
        # Add to the counter to locate results
        count +=1
    
    # Save RenewablesFraction vs LCUE data on a csv file:
    
    # Create a directory with the name of the data and save it
    script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Analysis/Sensitivity Analysis/")
    plot_dir = os.path.join(script_dir, 'Sensitivity_RF{}to{}_Re_{}_Load{}/'.format(initial_renewablesfraction, final_renewablesfraction, Reliability, Loadtype))
    
    if not os.path.isdir(plot_dir):
          os.makedirs(plot_dir)
    
    filepath=self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Analysis/Sensitivity Analysis/Sensitivity_RF{}to{}_Re_{}_Load{}/RenewablesFraction_sensitivity.csv".format(initial_renewablesfraction, final_renewablesfraction, Reliability, Loadtype)
    df_LCUEvsRenewableFraction.to_csv(filepath)
    
    # Restore the Blackouts as optimisation criteria in Optimisation inputs.csv
    filepathopt = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Optimisation inputs.csv"    
    df_optimisation = pd.read_csv(filepathopt, header=None)        
    df_optimisation.iat[10,1] = 'Blackouts'    
    df_optimisation.to_csv(filepathopt, index=None, header =None)       
    
    # Create a polynomic fit for the LCUE variation trend
    xloc = df_LCUEvsRenewableFraction.loc[:,'Renewables Fraction']
    z=np.polyfit(df_LCUEvsRenewableFraction.loc[:,'Renewables Fraction'], (-1.0*(df_LCUEvsRenewableFraction.loc[:,'LCUE']-df_baselinemetrics.iat[1])*100.0/df_baselinemetrics.iat[1]), 6)
    trendpoly = np.poly1d(z) 
    xtrend=np.arange(0.37,1.01,0.01)
    
    # Plot the graphic of Renewable fraction vs increase in LCUE for hybrid system:  
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax.bar(height=additional_cost/1000.0, x=xloc-0.0125, width=0.025, color='yellowgreen',alpha=0.7)
    ax.bar(height=additional_capex/1000.0, x=xloc+0.0125, width=0.025, color='palevioletred',alpha=0.7)
    ax2.plot(xtrend, trendpoly(xtrend), '-', linewidth=3, color="lightskyblue")
    ax.set_xlabel("Renewables fraction (0-1)")
    ax2.set_ylabel("LCUE reduction (-%)")
    ax2.set_ylim([26,38])
    ax.set_ylim([0,250])
    ax.set_xlim([0.33,1.04])
    ax.grid()
    ax.set_ylabel("Cost (Thousands of $)")
    
    # Customize legend
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    custom_lines = [Line2D([0], [0], color='lightskyblue', linewidth=3), 
                Patch(facecolor='yellowgreen', alpha=0.7),
                Patch(facecolor='palevioletred', alpha=0.7)] 
    plt.legend(custom_lines, ['LCUE variation','Total system cost savings','Additional initial new equipment costs'], loc='upper left')
   
    # Save graph in corresponding Sensitivity Analysis directory
    plot_name = "LCUE_Sensitivity_RF{}to{}_Re_{}_Load{}.png".format(initial_renewablesfraction, final_renewablesfraction, Reliability, Loadtype)        
    fig.savefig(plot_dir + plot_name,dpi=300)
    plt.show()    

    print('Figure saved as', plot_name)
    
    
# ------------------------------------------------------------------------------------------------------    
# Alternative hybrid optimisation using renewables fraction as optimisation criteria    
def hybrid_sys_performance_RF (max_blackouts, Loadtype, fraction):
    """
    Simulate performance of diesel-PV-battery system for the selected scenario 
    
    Input: max_blackouts  Maximum acceptible blackouts (0.0-1.0)
           Load profile for the selected scenario, between 'InstitutionalBase', 'InstitutionalAdv', 'Mix1', 'Mix2'
           Renewables fraction used as optimisation criteria
           
    Output: File of optimisation       
    
    """  
    # Read the load .csv file containing hourly load information of the selected facility  
    filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Scenario/Scenario inputs.csv"  
    df_scenario = pd.read_csv(filepath, header=None)   
    Reliability= int((1 - max_blackouts)*100.0)
    
    # Analysis done for hybrid system
    Systype = 'Hybrid'
    
    # Check if simulation for blackout level exists already, if not, performs simulation
    check = os.path.exists(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/RF_{}_Opt_{}_Re{}_Load{}".format(fraction, Systype, Reliability, Loadtype)) 
    
    if check == False :
        
        # Read the load .csv file containing hourly load information of the selected facility     
        print('\n Simulation doesn\'t exist, starting with optimisation...')
    
        # Set maximum blackout threshold (0.0-1.0)
        if df_scenario.iat[3, 1] != max_blackouts :
            df_scenario.iat[3, 1] = max_blackouts
    
        # Substitute new values in Scenario  Inputs.csv file for simulation
        df_scenario.to_csv(filepath, index=None, header =None)
        
        # Simulate diesel system and saves file as i.e.: Sim_PV0_Storage0_Diesel_Re90_LoadInstitutionalBase.csv     
        Optimisation = optimise_system_RF (Systype, Loadtype, max_blackouts, fraction, 10)
        
        print('\n Optimisation for renewables fraction {} finished.'.format(fraction))
        
    else:
        
        print('\n Optimisation for renewables fraction {} already exists.'.format(fraction))
        
    # Restore the Blackouts as optimisation criteria in Optimisation inputs.csv
    filepathopt = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Optimisation inputs.csv"   
    df_optimisation = pd.read_csv(filepathopt, header=None)       
    df_optimisation.iat[10,1] = 'Blackouts'   
    df_optimisation.to_csv(filepathopt, index=None, header =None)    
        
def optimise_system_RF (Systype, Loadtype, max_blackouts, fraction, Stepsize):  
    
    """
    Perform an optimisation of the type of system/scenario selected and saves outputs
    
    Input: 
           System type, between 'Diesel', 'Hybrid', or 'PVBatt'
           Load profile for the selected scenario, between 'InstitutionalBase', 'InstitutionalAdv', 'Mix1', 'Mix2'
           Maximum fraction of blackouts allowed
           Renewables fraction selected for optimisation
           Step size of PV and battery capacity for optimization (in kWp or kWh)

 
    """    
    # Read the Scenario Inputs .csv file containing hourly load information of the selected facility           
    filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Scenario/Scenario inputs.csv" 
    df_scenario = pd.read_csv(filepath, header=None)
     
    if Systype == 'Diesel' :
        
        # Not consider PV or battery storage for optimisation
        if df_scenario.iat[0, 1] != 'N':
            df_scenario.iat[0, 1] = 'N'    
        if df_scenario.iat[1, 1] != 'N':
            df_scenario.iat[1, 1] = 'N'
        
        # Consider only diesel for optimisation
        if df_scenario.iat[2, 1] != 'Y':
            df_scenario.iat[2, 1] = 'Y'    
    
    elif Systype == 'Hybrid' :
        
        # Consider PV and battery storage for optimisation
        if df_scenario.iat[0, 1] != 'Y':
            df_scenario.iat[0, 1] = 'Y'    
        if df_scenario.iat[1, 1] != 'Y':
            df_scenario.iat[1, 1] = 'Y'
        
        # Consider diesel for optimisation
        if df_scenario.iat[2, 1] != 'Y':
            df_scenario.iat[2, 1] = 'Y'  
                      
    elif Systype == 'PVBatt' :
        
        # Consider only PV and battery storage for optimisation
        if df_scenario.iat[0, 1] != 'Y':
            df_scenario.iat[0, 1] = 'Y'    
        if df_scenario.iat[1, 1] != 'Y':
            df_scenario.iat[1, 1] = 'Y'
        
        # Not onsider only diesel for optimisation
        if df_scenario.iat[2, 1] != 'N':
            df_scenario.iat[2, 1] = 'N'  
                       
    # Define diesel backup threshold of system for scenario
    df_scenario.iat[3,1] = max_blackouts
    
    # Substitute new values in Scenario  Inputs.csv file for optimisation
    df_scenario.to_csv(filepath, index=None, header =None)
          
    # Read the load .csv file containing devices information of the selected load scenario             
    filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Load/Devices.csv"    
    df_devices = pd.read_csv(filepath)    
    length = len(df_devices.index)     
    
    # For Scenaio 1 loads          
    if Loadtype == 'Mix1' :
        
        # Disable all loads                       
        for n in range(0,length):
            df_devices.iat[n,1] = 'N'
        
        # Consider existent public base loads       
        for n in range(0, length) :
            
            if df_devices.iat[n,8] == 'Base':
                df_devices.iat[n,1] = 'Y'
               
        # Consider existent private loads       
        for n in range(0, length) :
            
            if df_devices.iat[n,7] == 'Commercial':
                df_devices.iat[n,1] = 'Y'        
        
    # Substitute new values in Scenario  Inputs.csv file for simulation
    df_devices.to_csv(filepath, index=None)    
    
    # Locate and open Optimisation inputs file
    filepathopt = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Optimisation/Optimisation inputs.csv"
    df_optimisation = pd.read_csv(filepathopt, header=None)
    
    # Set stepsize of optimisation
    df_optimisation.iat [8,1] = Stepsize
    df_optimisation.iat [4,1] = Stepsize
    
    # Set renewables fraction as optimisation criteria:
    df_optimisation.iat[10,1] = 'Renewables fraction'
    
    # Set renewables fraction for optimisation
    df_optimisation.iat[11,1] = fraction
    
    # Substitute new values in Optimisation inputs.csv file for optimisation
    df_optimisation.to_csv(filepathopt, index=None, header =None)
   
    # Define an initial system with 0 PV, 0 Storage, and 13kW diesel generator corresponding to the one existing in Nyabiheke
    initial_sys = pd.DataFrame({'Final PV size':0.0,
                                            'Final storage size':0.0,
                                            'Diesel capacity':13,
                                            'Total system cost ($)':0.0,
                                            'Total system GHGs (kgCO2eq)':0.0,
                                            'Discounted energy (kWh)':0.0,
                                            'Cumulative cost ($)':0.0,
                                            'Cumulative system cost ($)':0.0,
                                            'Cumulative GHGs (kgCO2eq)':0.0,
                                            'Cumulative system GHGs (kgCO2eq)':0.0,
                                            'Cumulative energy (kWh)':0.0,
                                            'Cumulative discounted energy (kWh)':0.0,
                                            },index=['System results'])
    
    
    # Optimise system for the chosen period
    SysOptimisation = Optimisation().multiple_optimisation_step(previous_systems=initial_sys)
    
    # Define reliability of system for identifying the saved files
    Reliability = int((1.0 - max_blackouts)*100.0) 
    
    # Save the outputs from the optimisation
    Optimisation_Name = 'RF{}_Opt_{}_Re{}_Load{}'.format(fraction, Systype, Reliability, Loadtype)
    Optimisation().save_optimisation(SysOptimisation,Optimisation_Name)
        

# =============================================================================
#                           Productive uses of electricity
# =============================================================================   
#    

def privateimpact_reliability(Loadtype, max_blackouts, Systype):
    """
    Present reliability drop over time when additional private loads are included in the system 
    
    Input: Minimum reliability threshold (max_blackouts) and Loadtype (Mix1 or Mix1Adv)
        
    Output: Trend line graph showing reliability over lifetime of system
            Save plot on corresponding directory      
    
    """     
    # Read the Scenario Inputs .csv file containing hourly load information of the selected facility            
    filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Scenario/Scenario inputs.csv"   
    df_scenario = pd.read_csv(filepath, header=None)
       
    if Systype == 'Diesel' :
        
        # Not consider PV or battery storage for simulation
        if df_scenario.iat[0, 1] != 'N':
            df_scenario.iat[0, 1] = 'N'    
        if df_scenario.iat[1, 1] != 'N':
            df_scenario.iat[1, 1] = 'N'
        
        # Consider only diesel for simulation
        if df_scenario.iat[2, 1] != 'Y':
            df_scenario.iat[2, 1] = 'Y'    
    
    elif Systype == 'Hybrid' :
        
        # Consider PV and battery storage for simulation
        if df_scenario.iat[0, 1] != 'Y':
            df_scenario.iat[0, 1] = 'Y'    
        if df_scenario.iat[1, 1] != 'Y':
            df_scenario.iat[1, 1] = 'Y'
        
        # Consider diesel for simulation
        if df_scenario.iat[2, 1] != 'Y':
            df_scenario.iat[2, 1] = 'Y'  
                        
    elif Systype == 'PVBatt' :
        
        # Consider only PV and battery storage for simulation
        if df_scenario.iat[0, 1] != 'Y':
            df_scenario.iat[0, 1] = 'Y'    
        if df_scenario.iat[1, 1] != 'Y':
            df_scenario.iat[1, 1] = 'Y'
        
        # Not onsider only diesel for simulation
        if df_scenario.iat[2, 1] != 'N':
            df_scenario.iat[2, 1] = 'N'  
            
    # Define diesel backup threshold of system for scenario
    df_scenario.iat[3,1] = max_blackouts
    
    # Substitute new values in Scenario  Inputs.csv file for optimisation
    df_scenario.to_csv(filepath, index=None, header =None)    
    
    # Define reliability from blackout threshold
    Reliability= int((1.0 - max_blackouts)*100.0)
 
    # Initialise variables of study for each scenario
    monthly_reliability={'Scenario 1 Load':[],
                         'Scenario 2 Load':[],
                         'Scenario 2B Load':[],
                         'Scenario 3 Load':[],
                         'Scenario 4 Load':[]
                         }   
    
    # Create a date range column corresponding to the lifetime of the system (15 years)
    date_rng = pd.date_range(start='1/1/2020', end='1/1/2035', freq='H')
    Date=date_rng[:131400]    
    
    # Create directory to save simulations
    script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Analysis/")
    plot_dir = os.path.join(script_dir, 'Productive Load Impact/{} System {} Re/'.format(Systype, Reliability))  
    if not os.path.isdir(plot_dir):
           os.makedirs(plot_dir)    
    
    # Obtain the load the data for Scenario 1    
    print('\n Obtaining load data for Scenario 1...')

    # Check if simulation for corresponding system exists, if not, performs it
    check = os.path.exists(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/Simulation_{}.csv'.format(Systype, Reliability, 'Mix1'))
    
    if check == False :
                        
            print('\n Simulation not found, getting load data...')    
     
            # Obtain load data for Scenario 1
            get_loaddata('Mix1')
    
            # Read csv file with the optimization for Mix1
            df_hybridopt = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv'.format(Systype, Reliability, Loadtype))
    
            # Run simulation of optimization file    
            df_simulation=Energy_System().lifetime_simulation(df_hybridopt)    
        
            # Save simulation           
            filepath=self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/Simulation_{}.csv'.format(Systype, Reliability, Loadtype)
            df_simulation.to_csv(filepath, index=None)  
            
    else:
            
            print('\n Simulation found, getting reliability data...')           
            
            # Read data from saved simulation
            df_simulation=pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/Simulation_{}.csv'.format(Systype, Reliability, 'Mix1'))
    
    # Include a colum in simulation file with the date and hour
    df_simulation['Date'] = Date
    
    # For every year of lifetime, obtain the monthly average reliability of the system    
    for years in range(2020,2035):
        
        # For every month
        for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:
            
            # Create a mask to filter only data from that month, and obtain the average blackouts
            start_date='01-'+str(month)+'-'+str(years)
            final_date='27-'+str(month)+'-'+str(years)
            mask = (df_simulation['Date'] > start_date) & (df_simulation['Date'] <= final_date)     
            df_month = df_simulation.loc[mask].mean(axis=0).iloc[3]

            # Define average reliability from average blackouts
            df_reliability=(1.0-df_month)*100.0
            monthly_reliability['Scenario 1 Load'].append(df_reliability)
            
    print('\n Monthly reliability data for Scenario 1 calculated.')   
            
    # Obtain the load the data for Scenario 2B
    
    print('\n Obtaining load data for Scenario 2B...')
    
    # Check if simulation for corresponding system exists, if not, performs it
    check = os.path.exists(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/Simulation_{}.csv'.format(Systype, Reliability, 'Mix2B'))
    
    if check == False :
                        
            print('\n Simulation not found, getting load data...')
 
            # Obtain load data for Scenario 2B                                             
            get_loaddata('Mix2B')

            # Read csv file with the optimization for Mix1            
            df_hybridopt = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv'.format(Systype, Reliability, Loadtype))
    
            # Run simulation of optimization file
            df_simulation=Energy_System().lifetime_simulation(df_hybridopt)
    
            # Modify simulation to not to use more than 13kWp of diesel   
            mask = (df_simulation['Diesel energy (kWh)'] > 13.0)   
            extra_diesel=df_simulation['Diesel energy (kWh)'].loc[mask]-13.0   
            previous_diesel_use=df_simulation['Diesel energy (kWh)'].loc[mask]           
            df_simulation['Diesel energy (kWh)'].loc[mask]=13.0   
            df_simulation['Unmet energy (kWh)'].loc[mask]=df_simulation['Unmet energy (kWh)'].loc[mask]+extra_diesel   
            df_simulation['Total energy used (kWh)'].loc[mask]=df_simulation['Total energy used (kWh)'].loc[mask]-extra_diesel               
            diesel_reduction_factor=df_simulation['Diesel energy (kWh)'].loc[mask]/previous_diesel_use   
            df_simulation['Diesel fuel usage (l)'].loc[mask]=df_simulation['Diesel fuel usage (l)'].loc[mask]*diesel_reduction_factor       
            df_simulation['Blackouts'].loc[mask]=1
    
            # Save simulation    
            filepath=self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/Simulation_{}.csv'.format(Systype, Reliability, 'Mix2B')
            df_simulation.to_csv(filepath, index=None)
            
    else:
        
            print('\n Simulation found, getting reliability data...') 

            # Read data from saved simulation            
            df_simulation=pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/Simulation_{}.csv'.format(Systype, Reliability, 'Mix2B'))
      
    # Include a colum in simulation file with the date and hour
    df_simulation['Date'] = Date
        
    # For every year of lifetime, obtain the monthly average reliability of the system    
    for years in range(2020,2035):
        
        # For every month
        for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:

            # Create a mask to filter only data from that month, and obtain the average blackouts
            start_date='01-'+str(month)+'-'+str(years)
            final_date='27-'+str(month)+'-'+str(years)           
            mask = (df_simulation['Date'] > start_date) & (df_simulation['Date'] <= final_date)           
            df_month = df_simulation.loc[mask].mean(axis=0).iloc[3]           
            
            # Define average reliability from average blackouts         
            df_reliability=(1.0-df_month)*100.0           
            monthly_reliability['Scenario 2B Load'].append(df_reliability)
            
    print('\n Monthly reliability data for Scenario 2B calculated.')
    
        
    # Obtain the load the data for Scenario 2A
    
    print('\n Obtaining load data for Scenario 2A...')

    # Check if simulation for corresponding system exists, if not, performs it
    check = os.path.exists(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/Simulation_{}.csv'.format(Systype, Reliability, 'Mix2'))
    
    if check == False :
                        
            print('\n Simulation not found, getting load data...')

            # Obtain load data for Scenario 3                                              
            get_loaddata('Mix2')

            # Read csv file with the optimization for Mix1    
            df_hybridopt = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv'.format(Systype, Reliability, Loadtype))
    
            # Run simulation of optimization file   
            df_simulation=Energy_System().lifetime_simulation(df_hybridopt)
    
            # Modify simulation to not to use more than 13kWp of diesel   
            mask = (df_simulation['Diesel energy (kWh)'] > 13.0)   
            extra_diesel=df_simulation['Diesel energy (kWh)'].loc[mask]-13.0   
            previous_diesel_use=df_simulation['Diesel energy (kWh)'].loc[mask]           
            df_simulation['Diesel energy (kWh)'].loc[mask]=13.0   
            df_simulation['Unmet energy (kWh)'].loc[mask]=df_simulation['Unmet energy (kWh)'].loc[mask]+extra_diesel   
            df_simulation['Total energy used (kWh)'].loc[mask]=df_simulation['Total energy used (kWh)'].loc[mask]-extra_diesel               
            diesel_reduction_factor=df_simulation['Diesel energy (kWh)'].loc[mask]/previous_diesel_use   
            df_simulation['Diesel fuel usage (l)'].loc[mask]=df_simulation['Diesel fuel usage (l)'].loc[mask]*diesel_reduction_factor       
            df_simulation['Blackouts'].loc[mask]=1
    
            # Save simulation   
            filepath=self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/Simulation_{}.csv'.format(Systype, Reliability, 'Mix2')
            df_simulation.to_csv(filepath, index=None)
            
    else:
        
            print('\n Simulation found, getting reliability data...') 

            # Read data from saved simulation            
            df_simulation=pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/Simulation_{}.csv'.format(Systype, Reliability, 'Mix2'))

    
        
    # Include a colum in simulation file with the date and hour       
    df_simulation['Date'] = Date
        
    # For every year of lifetime, obtain the monthly average reliability of the system      
    for years in range(2020,2035):
        
        # For every month
        for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:
 
            # Create a mask to filter only data from that month, and obtain the average blackouts
            start_date='01-'+str(month)+'-'+str(years)
            final_date='27-'+str(month)+'-'+str(years)            
            mask = (df_simulation['Date'] > start_date) & (df_simulation['Date'] <= final_date)            
            df_month = df_simulation.loc[mask].mean(axis=0).iloc[3]            
            
            # Define average reliability from average blackouts            
            df_reliability=(1.0-df_month)*100.0            
            monthly_reliability['Scenario 2 Load'].append(df_reliability)
            
    print('\n Monthly reliability data for Scenario 2 calculated.')
    
    # Obtain the load the data for Scenario 3
    
    print('\n Obtaining load data for Scenario 3...')
    
    # Check if simulation for corresponding system exists, if not, performs it
    check = os.path.exists(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/Simulation_{}.csv'.format(Systype, Reliability, 'Mix1Adv'))
    
    if check == False :
                        
            print('\n Simulation not found, getting load data...')
                                              
            # Obtain load data for Scenario 3 
            get_loaddata('Mix1Adv')

            # Read csv file with the optimization for Mix1    
            df_hybridopt = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv'.format(Systype, Reliability, Loadtype))
    
            # Run simulation of optimization file    
            df_simulation=Energy_System().lifetime_simulation(df_hybridopt)
    
            # Modify simulation to not to use more than 13kWp of diesel   
            mask = (df_simulation['Diesel energy (kWh)'] > 13.0)   
            extra_diesel=df_simulation['Diesel energy (kWh)'].loc[mask]-13.0   
            previous_diesel_use=df_simulation['Diesel energy (kWh)'].loc[mask]           
            df_simulation['Diesel energy (kWh)'].loc[mask]=13.0   
            df_simulation['Unmet energy (kWh)'].loc[mask]=df_simulation['Unmet energy (kWh)'].loc[mask]+extra_diesel   
            df_simulation['Total energy used (kWh)'].loc[mask]=df_simulation['Total energy used (kWh)'].loc[mask]-extra_diesel
            diesel_reduction_factor=df_simulation['Diesel energy (kWh)'].loc[mask]/previous_diesel_use
            df_simulation['Diesel fuel usage (l)'].loc[mask]=df_simulation['Diesel fuel usage (l)'].loc[mask]*diesel_reduction_factor   
            df_simulation['Blackouts'].loc[mask]=1
    
            # Save simulation    
            filepath=self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/Simulation_{}.csv'.format(Systype, Reliability, 'Mix1Adv')
            df_simulation.to_csv(filepath, index=None)
            
    else:
        
            print('\n Simulation found, getting reliability data...') 
            
            # Read data from saved simulation            
            df_simulation=pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/Simulation_{}.csv'.format(Systype, Reliability, 'Mix1Adv'))
                            
    # Include a colum in simulation file with the date and hour         
    df_simulation['Date'] = Date    
        
    # For every year of lifetime, obtain the monthly average reliability of the system     
    for years in range(2020,2035):
        
        # For every month
        for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:

            # Create a mask to filter only data from that month, and obtain the average blackouts
            start_date='01-'+str(month)+'-'+str(years)
            final_date='27-'+str(month)+'-'+str(years)           
            mask = (df_simulation['Date'] > start_date) & (df_simulation['Date'] <= final_date)           
            df_month = df_simulation.loc[mask].mean(axis=0).iloc[3]

            # Define average reliability from average blackouts            
            df_reliability=(1.0-df_month)*100.0            
            monthly_reliability['Scenario 3 Load'].append(df_reliability)
            
    print('\n Monthly reliability data for Scenario 3 calculated.')
        
    # Obtain the load the data for Scenario 4
    
    print('\n Obtaining load data for Scenario 4...')
    
    # Check if simulation for corresponding system exists, if not, performs it
    check = os.path.exists(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/Simulation_{}.csv'.format(Systype, Reliability, 'Mix2Adv'))
    
    if check == False :
                        
            print('\n Simulation not found, getting load data...')
 
            # Obtain load data for Scenario 4                                             
            get_loaddata('Mix2Adv')

            # Read csv file with the optimization for Mix1    
            df_hybridopt = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv'.format(Systype, Reliability, Loadtype))
    
            # Run simulation of optimization file    
            df_simulation=Energy_System().lifetime_simulation(df_hybridopt)
    
            # Modify simulation to not to use more than 13kWp of diesel
            mask = (df_simulation['Diesel energy (kWh)'] > 13.0)   
            extra_diesel=df_simulation['Diesel energy (kWh)'].loc[mask]-13.0   
            previous_diesel_use=df_simulation['Diesel energy (kWh)'].loc[mask]           
            df_simulation['Diesel energy (kWh)'].loc[mask]=13.0   
            df_simulation['Unmet energy (kWh)'].loc[mask]=df_simulation['Unmet energy (kWh)'].loc[mask]+extra_diesel   
            df_simulation['Total energy used (kWh)'].loc[mask]=df_simulation['Total energy used (kWh)'].loc[mask]-extra_diesel           
            diesel_reduction_factor=df_simulation['Diesel energy (kWh)'].loc[mask]/previous_diesel_use
            df_simulation['Diesel fuel usage (l)'].loc[mask]=df_simulation['Diesel fuel usage (l)'].loc[mask]*diesel_reduction_factor    
            df_simulation['Blackouts'].loc[mask]=1
    
            # Save simulation
            filepath=self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/Simulation_{}.csv'.format(Systype, Reliability, 'Mix2Adv')
            df_simulation.to_csv(filepath, index=None)
            
    else:
        
            print('\n Simulation found, getting reliability data...') 
            
            # Read data from saved simulation
            df_simulation=pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/Simulation_{}.csv'.format(Systype, Reliability, 'Mix2Adv'))
    
    # Include a colum in simulation file with the date and hour         
    df_simulation['Date'] = Date    

    # For every year of lifetime, obtain the monthly average reliability of the system            
    for years in range(2020,2035):
        
        # For every month
        for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:
 
            # Create a mask to filter only data from that month, and obtain the average blackouts
            start_date='01-'+str(month)+'-'+str(years)
            final_date='27-'+str(month)+'-'+str(years)           
            mask = (df_simulation['Date'] > start_date) & (df_simulation['Date'] <= final_date)           
            df_month = df_simulation.loc[mask].mean(axis=0).iloc[3]

            # Define average reliability from average blackouts            
            df_reliability=(1.0-df_month)*100.0           
            monthly_reliability['Scenario 4 Load'].append(df_reliability)
            
    print('\n Monthly reliability data for Scenario 4 calculated.')
        
    # Plot reliability over time for all cases
 
    # Define x variable as months of lifetime       
    x=list(range(0,180))
    
    # Extract the data for plotting
    labels=[]
    length = len(monthly_reliability.keys())
    allReliabilities = list(monthly_reliability.items())
    fig, ax = plt.subplots()
    Reliabilityforfigures=[]
             
    for n in range(0, length):

        Re=allReliabilities[n]
        name=Re[0]
        labels.append(name)
        Reliabilityforfigures.append(Re[1])
 
    # Plot the reliability of Scenario 1 system for each load scenario           
    ax.plot(x, Reliabilityforfigures[0], color='lightseagreen',linewidth=3)
    ax.plot(x, Reliabilityforfigures[1], color='yellowgreen',linewidth=3)
    ax.plot(x, Reliabilityforfigures[2], color='palevioletred',linewidth=3)
    ax.plot(x, Reliabilityforfigures[3], color='gold')  
    ax.plot(x, Reliabilityforfigures[4], color='lightsalmon')   
    ax.set_xlabel('Years of lifetime', fontsize=15)
    ax.set_ylabel('Reliability (%)', fontsize=15)#,
    ax.grid()
    ax.legend(labels, bbox_to_anchor=(1, 0.77), fontsize=15)
    ax.set_xticks([0,24,48,72,96,120,144,168]) 
    ax.set_xticklabels([0,2,4,6,8,10,12,14], fontsize=15)
    ax.set_xlim(0,180)
    ax.set_yticklabels([0,20,40,60,80,100], fontsize=15)
    ax.set_ylim(0,105)
    plt.show()     
    
    # Save figure in corresponding directory  
    plot_name = "{}_SystemRe{}_OverLifetime.png".format(Loadtype, Reliability) 
    fig.savefig(plot_dir + plot_name,dpi=300, bbox_inches='tight')
    print(' Figure saved as '+plot_name)
    plt.show()
        
    #Save the monthly total load data in a file     
    df_totalRe=pd.DataFrame(monthly_reliability, index=None)
    filepath=self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/MonthlyReData.csv".format(Systype, Reliability)    
    df_totalRe.to_csv(filepath, index=None)
    
    print( "\n Data saved as MonthlyReData.csv" )
    

def privateimpact_design(Loadtype, max_blackouts):
    """
    Present growing load over time from Scenario 1 to Scenario 2B
    Present compared wasted energy between initial sizing for Scenario 2B and optimized increase
    
    Input: Minimum reliability threshold (max_blackouts) and Loadtype (Mix1to2B)
        
    Output: Present growing load and wasted energy comparing sizing of the system for final load
            vs reasessing and expanding the system every 5 years      
    
    """  
    # Done for a PV-battery system
    Systype = 'PVBatt'
    
    # Read the Scenario Inputs .csv file containing hourly load information of the selected facility     
    filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Scenario/Scenario inputs.csv"
    df_scenario = pd.read_csv(filepath, header=None)
    
    if Systype == 'Diesel' :
        
        # Not consider PV or battery storage for simulation
        if df_scenario.iat[0, 1] != 'N':
            df_scenario.iat[0, 1] = 'N'    
        if df_scenario.iat[1, 1] != 'N':
            df_scenario.iat[1, 1] = 'N'
        
        # Consider only diesel for simulation
        if df_scenario.iat[2, 1] != 'Y':
            df_scenario.iat[2, 1] = 'Y'    
    
    elif Systype == 'Hybrid' :
        
        # Consider PV and battery storage for simulation
        if df_scenario.iat[0, 1] != 'Y':
            df_scenario.iat[0, 1] = 'Y'    
        if df_scenario.iat[1, 1] != 'Y':
            df_scenario.iat[1, 1] = 'Y'
        
        # Consider diesel for simulation
        if df_scenario.iat[2, 1] != 'Y':
            df_scenario.iat[2, 1] = 'Y'  
                        
    elif Systype == 'PVBatt' :
        
        # Consider only PV and battery storage for simulation
        if df_scenario.iat[0, 1] != 'Y':
            df_scenario.iat[0, 1] = 'Y'    
        if df_scenario.iat[1, 1] != 'Y':
            df_scenario.iat[1, 1] = 'Y'
        
        # Not onsider only diesel for simulation
        if df_scenario.iat[2, 1] != 'N':
            df_scenario.iat[2, 1] = 'N'  
            
    # Define diesel backup threshold of system for scenario
    df_scenario.iat[3,1] = max_blackouts
    
    # Substitute new values in Scenario  Inputs.csv file for optimisation
    df_scenario.to_csv(filepath, index=None, header =None)   
 
    # Define reliability from blackout threshold
    Reliability= int((1.0 - max_blackouts)*100.0)
    
    # Initialise the variables used
    monthly_data={'Energy demand':[],
                         'Renewables energy supplied (A)':[],
                         'Storage energy supplied (A)':[],
                         'Wasted energy (A)':[],
                         'Renewables energy supplied (B)':[],
                         'Storage energy supplied (B)':[],
                         'Wasted energy (B)':[]
                         }   
    
    # Create a date range column corresponding to the lifetime of the system  
    date_rng = pd.date_range(start='1/1/2020', end='1/1/2035', freq='H')
    Date=date_rng[:131400]    
  
    # Create directory to save simulations
    script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Analysis/")
    plot_dir = os.path.join(script_dir, 'Productive Load Impact/{} System {} Re/'.format(Systype, Reliability))
    if not os.path.isdir(plot_dir):
           os.makedirs(plot_dir)    

    # Case A: Using static system optimized system for final Scenario 2B load since the beginning

    # Open optimisation file    
    df_opt = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}_{}.csv'.format(Systype, Reliability, Loadtype,'A'))
    
    # Run simulation of optimization file and save it
    df_simulation=Energy_System().lifetime_simulation(df_opt)   
    filepath=self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/Simulation_{}_{}.csv'.format(Systype, Reliability,'Mix1to2B','A')
    df_simulation.to_csv(filepath, index=None)

    # Include a colum in simulation file with the date and hour                     
    df_simulation['Date'] = Date    

    # For every year of lifetime, obtain the monthly average performance of the system                    
    for years in range(2020,2035):
        
        # For every month
        for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:
 
            # Create a mask to filter only data from that month, and obtain the average variables
            start_date='01-'+str(month)+'-'+str(years)
            final_date='27-'+str(month)+'-'+str(years)           
            mask = (df_simulation['Date'] > start_date) & (df_simulation['Date'] <= final_date)
            
            df_demand = df_simulation.loc[mask].mean(axis=0).iloc[0]
            df_renewables = df_simulation.loc[mask].mean(axis=0).iloc[4]
            df_storage = df_simulation.loc[mask].mean(axis=0).iloc[5]
            df_dumped = df_simulation.loc[mask].mean(axis=0).iloc[13]
            
            # Add them to the variables over lifetime
            monthly_data['Energy demand'].append(df_demand)
            monthly_data['Renewables energy supplied (A)'].append(df_renewables)
            monthly_data['Storage energy supplied (A)'].append(df_storage)
            monthly_data['Wasted energy (A)'].append(df_dumped)
            
    print('\n Monthly  data for Scenario A calculated...')
    
    # Case B: Using modular system optimized to adapt to the growing demand every 5 years

    # Consider an increase of load from Scenario 1 to Scenario 2B
    Loadtype='Mix1to2B'
    
    # Open optimisation file
    df_opt = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}_{}.csv'.format(Systype, Reliability, Loadtype, 'B'))
    
    # Run simulation of optimization file and save it
    df_simulation=Energy_System().lifetime_simulation(df_opt)    
    filepath=self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Analysis/Productive Load Impact/{} System {} Re/Simulation_{}_{}.csv'.format(Systype, Reliability,'Mix1to2B','B')
    df_simulation.to_csv(filepath, index=None)
    
    # Include a colum in simulation file with the date and hour                                 
    df_simulation['Date'] = Date
      
     # For every year of lifetime, obtain the monthly average performance of the system                           
    for years in range(2020,2035):
        
        # For every month
        for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:
 
            # Create a mask to filter only data from that month, and obtain the average variables
            start_date='01-'+str(month)+'-'+str(years)
            final_date='27-'+str(month)+'-'+str(years)           
            mask = (df_simulation['Date'] > start_date) & (df_simulation['Date'] <= final_date)
            
            df_demand = df_simulation.loc[mask].mean(axis=0).iloc[0]
            df_renewables = df_simulation.loc[mask].mean(axis=0).iloc[4]
            df_storage = df_simulation.loc[mask].mean(axis=0).iloc[5]
            df_dumped = df_simulation.loc[mask].mean(axis=0).iloc[13]
            
            # Add them to the variables over lifetime
            monthly_data['Renewables energy supplied (B)'].append(df_renewables)
            monthly_data['Storage energy supplied (B)'].append(df_storage)
            monthly_data['Wasted energy (B)'].append(df_dumped)
            
    print('\n Monthly  data for Scenario B calculated...') 
      
    # Plot performance of the system over lifetime for both approaches
    
    # Define x variable as months of lifetime               
    x=list(range(0,180))
 
    # Extract the data for plotting
    labels=[]
    length = len(monthly_data.keys())
    alldata = list(monthly_data.items())
    Dataforfigures=[]
             
    for n in range(0, length):

        Re=alldata[n]
        name=Re[0]
        labels.append(name)
        Dataforfigures.append(Re[1])
        
    # Plot and save design approach A    
    fig, ax1 = plt.subplots()
    ax1.plot(x,Dataforfigures[0], color='darkcyan')        
    ax1.stackplot(x,Dataforfigures[1:4], colors=['gold','yellowgreen','lightsteelblue'])
    plt.subplots_adjust(left=0.01, bottom=0.1, right=0.99, top=0.9, hspace=0.4)
    
    ax1.set_xlabel('Years of lifetime',fontsize=15)
    ax1.set_ylabel('Average Energy (kWh)',fontsize=15)
    ax1.grid()
    ax1.legend(labels, loc='lower right', fontsize=8)
    
    ax1.set_xticks([0,24,48,72,96,120,144,168]) 
    ax1.set_xticklabels([0,2,4,6,8,10,12,14],fontsize=15)
    ax1.set_xlim(0,179) 
    ax1.set_ylim(0,32)
    ax1.set_yticklabels([0,5,10,15,20,25,30],fontsize=15)
    plt.tight_layout()  
        
    plot_name = "{}_SystemRe{}_{}.png".format(Systype, Reliability,'A') 
    fig.savefig(plot_dir + plot_name,dpi=300, bbox_inches='tight')
    print(' Figure saved as '+plot_name)
    plt.show()
    
    
    # Plot and save design approach B
    fig, ax2 = plt.subplots()
    ax2.plot(x,Dataforfigures[0], color='darkcyan')        
    ax2.stackplot(x,Dataforfigures[4:], colors=['gold','yellowgreen','lightsteelblue'])
    plt.subplots_adjust(left=0.01, bottom=0.1, right=0.99, top=0.9, hspace=0.4)
    
    ax2.set_xlabel('Years of lifetime',fontsize=15)
    ax2.set_ylabel('Average Energy (kWh)',fontsize=15)
    ax2.grid()
    ax2.legend(labels=[labels[0],labels[4],labels[5],labels[6]], loc='lower right', fontsize=8)
    
    ax2.set_xticks([0,24,48,72,96,120,144,168]) 
    ax2.set_xticklabels([0,2,4,6,8,10,12,14],fontsize=15)
    ax2.set_yticklabels([0,5,10,15,20,25,30],fontsize=15)
    ax2.set_xlim(0,179)
    ax2.set_ylim(0,32)
    plt.tight_layout()  
        
    plot_name = "{}_SystemRe{}_{}.png".format(Systype, Reliability,'B') 
    fig.savefig(plot_dir + plot_name,dpi=300, bbox_inches='tight')
    print(' Figure saved as '+plot_name)
    plt.show()
    
    # Save lifetime performance data in csv file    
    df_monthlydata=pd.DataFrame(monthly_data)
    file_name='Monthly_energy_data_DesignApproaches.csv'
    df_monthlydata.to_csv(plot_dir+file_name)
    print('\n Data saved as '+file_name)
    
    
def cumulative_capacity(max_blackouts):
    """
    Present installed PV and storage capacity for optimized systes for each scenario over lifetime
    
    Input: Minimum reliability threshold (max_blackouts)
        
    Output: Trend line graph showing PV and battery (dashed) capacity installed over lifetime
            Save plot on corresponding directory      
    
    """       
    # Done for hybrid and PV-battery systems
    types=['PVBatt','Hybrid']
    for Systype in types :
    
       # Read the Scenario Inputs .csv file containing hourly load information of the selected facility     
       filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Scenario/Scenario inputs.csv"   
       df_scenario = pd.read_csv(filepath, header=None)
    
       if Systype == 'Diesel' :
        
           # Not consider PV or battery storage for simulation
           if df_scenario.iat[0, 1] != 'N':
               df_scenario.iat[0, 1] = 'N'    
           if df_scenario.iat[1, 1] != 'N':
               df_scenario.iat[1, 1] = 'N'
        
           # Consider only diesel for simulation
           if df_scenario.iat[2, 1] != 'Y':
               df_scenario.iat[2, 1] = 'Y'    
    
       elif Systype == 'Hybrid' :
        
           # Consider PV and battery storage for simulation
           if df_scenario.iat[0, 1] != 'Y':
            df_scenario.iat[0, 1] = 'Y'    
           if df_scenario.iat[1, 1] != 'Y':
            df_scenario.iat[1, 1] = 'Y'
        
           # Consider diesel for simulation
           if df_scenario.iat[2, 1] != 'Y':
               df_scenario.iat[2, 1] = 'Y'  
                 
       elif Systype == 'PVBatt' :
        
           # Consider only PV and battery storage for simulation
           if df_scenario.iat[0, 1] != 'Y':
               df_scenario.iat[0, 1] = 'Y'    
           if df_scenario.iat[1, 1] != 'Y':
               df_scenario.iat[1, 1] = 'Y'
        
           # Not onsider only diesel for simulation
           if df_scenario.iat[2, 1] != 'N':
               df_scenario.iat[2, 1] = 'N'  
            
       # Define diesel backup threshold of system for scenario
       df_scenario.iat[3,1] = max_blackouts
    
       # Substitute new values in Scenario  Inputs.csv file for optimisation
       df_scenario.to_csv(filepath, index=None, header =None)    
       
       # Define reliability from blackout threshold
       Reliability= int((1.0 - max_blackouts)*100.0)
    
       # Create directory to save simulations
       script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Analysis/")
       plot_dir = os.path.join(script_dir, 'Scenario comparison/{} Re/'.format(Reliability))    
       if not os.path.isdir(plot_dir):
              os.makedirs(plot_dir)   

       # Initalise variables used    
       Capacity_installed={'Scenario 1 PV':[],
                         'Scenario 1 Storage':[],
                         'Scenario 2B PV':[],
                         'Scenario 2B Storage':[],
                         'Scenario 3 PV':[],
                         'Scenario 3 Storage':[],
                         'Scenario 4 PV':[],
                         'Scenario 4 Storage':[]
                         } 
       
       # For every scenario studied
       Scenarios=['Mix1','Mix2B','Mix1Adv','Mix2Adv']        
       for Loadtype in Scenarios :   
       
          if Loadtype=='Mix1':
              column='Scenario 1'
           
          if Loadtype=='Mix2B':
              column='Scenario 2B'
         
          if Loadtype=='Mix1Adv':
              column='Scenario 3'
           
          if Loadtype=='Mix2Adv':
              column='Scenario 4'
        
          #  Open optimisation file corresponding to the system
          df_opt = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv'.format(Systype, Reliability, Loadtype))
     
          # For every iteration period (3x5 years)
          for i in range(0,3) :
        
              # Getting installed and final PV data             
              Initial_PV_capacity=df_opt.iat[i,3]
              Capacity_installed[column+' PV'].append(Initial_PV_capacity)
              Final_PV_capacity=df_opt.iat[i,5]
              Capacity_installed[column+' PV'].append(Final_PV_capacity)
        
              # Getting installed and final storage data  
              Initial_storage_capacity=df_opt.iat[i,4]
              Capacity_installed[column+' Storage'].append(Initial_storage_capacity)
              Final_storage_capacity=df_opt.iat[i,6]
              Capacity_installed[column+' Storage'].append(Final_storage_capacity)  
        
       #Save the size data in a file  
       df_totalSize=pd.DataFrame( Capacity_installed, index=None)
       filepath=self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Analysis/Scenario comparison/{} Re/SystemSizes_{}.csv".format(Reliability,Systype)
       df_totalSize.to_csv(filepath, index=None)
    
       print( "\n Data saved as SystemSizes_{}.csv".format(Systype))
       
       # Allocate results for PV-battery ploting variables
       if Systype=='PVBatt':
    
          labels=[]
          length = len(Capacity_installed.keys())
          allCapacities = list(Capacity_installed.items())  
          Capacityforfigures1=[]
             
          for n in range(0, length):

              Re=allCapacities[n]
              name=Re[0]
              labels.append(name)
              Capacityforfigures1.append(Re[1])

       # Allocate results for hybrid ploting variables              
       if Systype=='Hybrid':
    
          labels=[]
          length = len(Capacity_installed.keys())
          allCapacities = list(Capacity_installed.items())     
          Capacityforfigures2=[]
             
          for n in range(0, length):

              Re=allCapacities[n]
              name=Re[0]
              labels.append(name)
              Capacityforfigures2.append(Re[1])

    # Define x variable as years of lifetime (iteration periods)           
    x=[0,5,5,10,10,15]
     
    # Plot sizes of systems
    
    # For PV battery system, PV in continuous, storage in dashed line
    fig, (ax1,ax2) = plt.subplots(1,2)    
    ax1.plot(x, Capacityforfigures1[0], color='lightseagreen',linewidth=2)
    ax1.plot(x, Capacityforfigures1[1], color='lightseagreen', linestyle='dashed',linewidth=2)
    ax1.plot(x, Capacityforfigures1[2], color='palevioletred')
    ax1.plot(x, Capacityforfigures1[3], color='palevioletred', linestyle='dashed')
    ax1.plot(x, Capacityforfigures1[4], color='gold')  
    ax1.plot(x, Capacityforfigures1[5], color='gold', linestyle='dashed')
    ax1.plot(x, Capacityforfigures1[6], color='lightsalmon') 
    ax1.plot(x, Capacityforfigures1[7], color='lightsalmon', linestyle='dashed')  
    ax1.set(xlabel='Years of lifetime', ylabel='Capacity installed (kW or kWh)')#,
    ax1.grid()    
    ax1.set_xticks([0,2,4,6,8,10,12,14]) 
    ax1.set_xlim(0,15)
    ax1.set_yticks([0,100,200,300,400,500,600,700])
    ax1.set_title('PV-Battery System',fontweight='bold',fontsize=10) 
    
    # For hybrid system, PV in continuous, storage in dashed
    ax2.plot(x, Capacityforfigures2[0], color='lightseagreen',linewidth=2)
    ax2.plot(x, Capacityforfigures2[1], color='lightseagreen', linestyle='dashed',linewidth=2)
    ax2.plot(x, np.multiply(Capacityforfigures2[2],1.02), color='palevioletred')
    ax2.plot(x, np.multiply(Capacityforfigures2[3],1.02), color='palevioletred', linestyle='dashed',linewidth=2)
    ax2.plot(x, Capacityforfigures2[4], color='gold')  
    ax2.plot(x, Capacityforfigures2[5], color='gold', linestyle='dashed')
    ax2.plot(x, Capacityforfigures2[6], color='lightsalmon') 
    ax2.plot(x, Capacityforfigures2[7], color='lightsalmon', linestyle='dashed')  
    ax2.set(xlabel='Years of lifetime')#,
    ax2.grid()    
    ax2.set_xticks([0,2,4,6,8,10,12,14]) 
    ax2.set_xlim(0,15) 
    ax2.set_ylim(-1,80) 
    ax2.set_yticks([0,10,20,30,40,50,60,70,80]) 
    ax2.set_title('Hybrid System',fontweight='bold',fontsize=10)
        
    ax2.legend(labels, bbox_to_anchor=(1, 0.85, 0, 0), fontsize=8)
    plt.subplots_adjust(left=0.01, bottom=0.25, right=0.99, top=0.75, hspace=0.2)    
    plt.show()
                
    # Save figure in the corresponding directory
    plot_name = "Sizes_Re{}_Combined_OverLifetime.png".format(Reliability)
    fig.savefig(plot_dir + plot_name,dpi=300,bbox_inches='tight')
    print(' Figure saved as '+plot_name)
    plt.show()
           
def cumulative_costs(max_blackouts):
    """
    Present cumulative costs for optimized systes for each scenario over lifetime
    
    Input: Minimum reliability threshold (max_blackouts)
        
    Output: Trend line graph showing PV and battery (dashed) capacity installed over lifetime
            Save plot on corresponding directory      
    
    """            
    # Define reliability from blackout threshold  
    Reliability= int((1.0 - max_blackouts)*100.0)

    # Create directory to save simulations
    script_dir = os.path.dirname(self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Analysis/")
    plot_dir = os.path.join(script_dir, 'Scenario comparison/{} Re/'.format(Reliability))
    
    if not os.path.isdir(plot_dir):
           os.makedirs(plot_dir)  
           
    # Initialise variables of study, each system for each scenario       
    cumulative_cost={'Scenario 1 Hybrid':[],
                         'Scenario 1 PV-Battery':[],
                         'Scenario 1 Diesel':[],
                         'Scenario 2B Hybrid':[],
                         'Scenario 2B PV-Battery':[],
                         'Scenario 2B Diesel':[],
                         'Scenario 3 Hybrid':[],
                         'Scenario 3 PV-Battery':[],
                         'Scenario 3 Diesel':[],
                         'Scenario 4 Hybrid':[],
                         'Scenario 4 PV-Battery':[],
                         'Scenario 4 Diesel':[]
                         }   
           
    # Done for all scenarios       
    Scenarios=['Mix1','Mix2B','Mix1Adv','Mix2Adv']
         
    # Done for diesel, hybrid and PV-battery
    Types = ['Hybrid','PVBatt','Diesel']
    
    # Key metrics used for barchart graphic
    df_keymetrics=pd.DataFrame(columns=['LCUE ($/kWh)','Cumulative cost ($)']) 
    
    # For every load Scenario:
    for Loadtype in Scenarios :
        
        # For every system type:
        for Systype in Types:
        
           # Read the Scenario Inputs .csv file containing hourly load information of the selected facility     
           filepath = self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Scenario/Scenario inputs.csv"  
           df_scenario = pd.read_csv(filepath, header=None)    
    
           if Systype == 'Diesel' :
        
               # Not consider PV or battery storage for simulation
               if df_scenario.iat[0, 1] != 'N':
                   df_scenario.iat[0, 1] = 'N'    
               if df_scenario.iat[1, 1] != 'N':
                   df_scenario.iat[1, 1] = 'N'
        
               # Consider only diesel for simulation
               if df_scenario.iat[2, 1] != 'Y':
                   df_scenario.iat[2, 1] = 'Y'    
    
           elif Systype == 'Hybrid' :
        
               # Consider PV and battery storage for simulation
               if df_scenario.iat[0, 1] != 'Y':
                   df_scenario.iat[0, 1] = 'Y'    
               if df_scenario.iat[1, 1] != 'Y':
                   df_scenario.iat[1, 1] = 'Y'
        
               # Consider diesel for simulation
               if df_scenario.iat[2, 1] != 'Y':
                   df_scenario.iat[2, 1] = 'Y'  
                        
           elif Systype == 'PVBatt' :
        
               # Consider only PV and battery storage for simulation
               if df_scenario.iat[0, 1] != 'Y':
                   df_scenario.iat[0, 1] = 'Y'    
               if df_scenario.iat[1, 1] != 'Y':
                   df_scenario.iat[1, 1] = 'Y'
        
               # Not onsider only diesel for simulation
               if df_scenario.iat[2, 1] != 'N':
                   df_scenario.iat[2, 1] = 'N'  
            
           # Define diesel backup threshold of system for scenario
           df_scenario.iat[3,1] = max_blackouts
    
           # Substitute new values in Scenario  Inputs.csv file for optimisation
           df_scenario.to_csv(filepath, index=None, header =None)    
           
           # Check if corresponding optimisation file exists, if not, simulates it
           if Loadtype=='Mix1':
              column='Scenario 1'
           
           if Loadtype=='Mix2B':
              column='Scenario 2B'
        
           if Loadtype=='Mix1Adv':
              column='Scenario 3'
           
           if Loadtype=='Mix2Adv':
              column='Scenario 4'
        
           if Systype == 'Diesel':
        
              check = os.path.exists(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV0_Storage0_{}_Re{}_Load{}_Appraisal.csv'.format(Systype, Reliability, Loadtype)) 
    
              if check == True :              
           
                 # Read csv file with the optimization
                 df_opt = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV0_Storage0_{}_Re{}_Load{}_Appraisal.csv'.format(Systype, Reliability, Loadtype))
            
              elif check == False :
                 
                 # Perform diesel simulation if does not exist previously
                 diesel_sys_performance(max_blackouts, Loadtype)
           
                 # Read csv file with the optimization
                 df_opt = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV0_Storage0_{}_Re{}_Load{}_Appraisal.csv'.format(Systype, Reliability, Loadtype))

              # Create costs dataframe for cumulative cost over lifetime
              df_Costs=pd.DataFrame()               
                
              # Introduce colum with new equipment costs        
              df_Costs['New Eq Costs'] = np.zeros(180)
              df_Costs.iat[0,0]=df_opt.iat[0,30]-13.0*560.0
    
              # Introduce colum with O&M costs            
              df_Costs['O&M Costs'] = np.zeros(180)
              
              # Monthly de-discounted costs over lifetime assuming constant costs
              X= df_opt.iat[0,32]/(0.54474*180.0)
              
              # Assign discount factor to each year over lifetime
              X_0=X*((1.0-0.095)**0.0)
              X_1=X*((1.0-0.095)**1.0)
              X_2=X*((1.0-0.095)**2.0)
              X_3=X*((1.0-0.095)**3.0)
              X_4=X*((1.0-0.095)**4.0)
              X_5=X*((1.0-0.095)**5.0)
              X_6=X*((1.0-0.095)**6.0)
              X_7=X*((1.0-0.095)**7.0)
              X_8=X*((1.0-0.095)**8.0)
              X_9=X*((1.0-0.095)**9.0)
              X_10=X*((1.0-0.095)**10.0)
              X_11=X*((1.0-0.095)**11.0)
              X_12=X*((1.0-0.095)**12.0)
              X_13=X*((1.0-0.095)**13.0)
              X_14=X*((1.0-0.095)**14.0)
 
              # Discount the costs of each year by their corresponding discount factor
              df_Costs.loc[0:11,'O&M Costs'] = X_0
              df_Costs.loc[12:23,'O&M Costs'] = X_1
              df_Costs.loc[24:35,'O&M Costs'] = X_2
              df_Costs.loc[36:47,'O&M Costs'] = X_3
              df_Costs.loc[48:59,'O&M Costs'] = X_4
              df_Costs.loc[60:71,'O&M Costs'] = X_5
              df_Costs.loc[72:83,'O&M Costs'] = X_6
              df_Costs.loc[84:95,'O&M Costs'] = X_7
              df_Costs.loc[96:107,'O&M Costs'] = X_8
              df_Costs.loc[108:119,'O&M Costs'] = X_9
              df_Costs.loc[120:131,'O&M Costs'] = X_10
              df_Costs.loc[132:143,'O&M Costs'] = X_11
              df_Costs.loc[144:155,'O&M Costs'] = X_12
              df_Costs.loc[156:167,'O&M Costs'] = X_13
              df_Costs.loc[168:179,'O&M Costs'] = X_14
    
              # Introduce colum with Diesel costs           
              df_Costs['Diesel Costs'] = np.zeros(180)

              # Monthly de-discounted costs over lifetime assuming constant costs
              X= df_opt.iat[0,33]/(0.54474*180.0)

              # Assign discount factor to each year over lifetime
              X_0=X*((1.0-0.095)**0.0)
              X_1=X*((1.0-0.095)**1.0)
              X_2=X*((1.0-0.095)**2.0)
              X_3=X*((1.0-0.095)**3.0)
              X_4=X*((1.0-0.095)**4.0)
              X_5=X*((1.0-0.095)**5.0)
              X_6=X*((1.0-0.095)**6.0)
              X_7=X*((1.0-0.095)**7.0)
              X_8=X*((1.0-0.095)**8.0)
              X_9=X*((1.0-0.095)**9.0)
              X_10=X*((1.0-0.095)**10.0)
              X_11=X*((1.0-0.095)**11.0)
              X_12=X*((1.0-0.095)**12.0)
              X_13=X*((1.0-0.095)**13.0)
              X_14=X*((1.0-0.095)**14.0)

              # Discount the costs of each year by their corresponding discount factor
              df_Costs.loc[0:11,'Diesel Costs'] = X_0
              df_Costs.loc[12:23,'Diesel Costs'] = X_1
              df_Costs.loc[24:35,'Diesel Costs'] = X_2
              df_Costs.loc[36:47,'Diesel Costs'] = X_3
              df_Costs.loc[48:59,'Diesel Costs'] = X_4
              df_Costs.loc[60:71,'Diesel Costs'] = X_5
              df_Costs.loc[72:83,'Diesel Costs'] = X_6
              df_Costs.loc[84:95,'Diesel Costs'] = X_7
              df_Costs.loc[96:107,'Diesel Costs'] = X_8
              df_Costs.loc[108:119,'Diesel Costs'] = X_9
              df_Costs.loc[120:131,'Diesel Costs'] = X_10
              df_Costs.loc[132:143,'Diesel Costs'] = X_11
              df_Costs.loc[144:155,'Diesel Costs'] = X_12
              df_Costs.loc[156:167,'Diesel Costs'] = X_13
              df_Costs.loc[168:179,'Diesel Costs'] = X_14             
    
        
              # Total monthly costs and cumulative costs   
              df_Costs['Total Costs'] = df_Costs['New Eq Costs']+df_Costs['Diesel Costs']+df_Costs['O&M Costs']
              df_Costs['Cumulative Costs']=np.cumsum(df_Costs['Total Costs'])
        
           elif Systype == 'Hybrid':
               
              # Read csv file with the optimization
              df_opt = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv'.format(Systype, Reliability, Loadtype))  
              
              # Create costs dataframe for cumulative cost over lifetime              
              df_Costs=pd.DataFrame()
        
              # Introduce colum with new equipment costs           
              df_Costs['New Eq Costs'] = np.zeros(180)
              df_Costs.iat[0,0]=df_opt.iat[0,30]
              df_Costs.iat[60,0]=df_opt.iat[1,30]
              df_Costs.iat[120,0]=df_opt.iat[2,30]
    
              # Introduce colum with O&M costs for each of the 3 iteration periods      
              df_Costs['O&M Costs'] = np.zeros(180)
              X_1= df_opt.iat[0,32]/60.0
              X_2=df_opt.iat[1,32]/60.0
              X_3=df_opt.iat[2,32]/60.0
        
              df_Costs.loc[0:59,'O&M Costs'] = X_1
              df_Costs.loc[60:119,'O&M Costs'] = X_2
              df_Costs.loc[120:179,'O&M Costs'] = X_3
    
              # Introduce colum with Diesel costs        
              df_Costs['Diesel Costs'] = np.zeros(180)

              # Monthly de-discounted costs over lifetime for each of the 3 iteration periods
              X_A= df_opt.iat[0,33]/(60.0*0.827)
              X_B=df_opt.iat[1,33]/(60.0*0.502)
              X_C=df_opt.iat[2,33]/(60.0*0.304)
 
              # Discount the costs of each year by their corresponding discount factor             
              X_0=X_A*((1.0-0.095)**0.0)
              X_1=X_A*((1.0-0.095)**1.0)
              X_2=X_A*((1.0-0.095)**2.0)
              X_3=X_A*((1.0-0.095)**3.0)
              X_4=X_A*((1.0-0.095)**4.0)
              X_5=X_B*((1.0-0.095)**5.0)
              X_6=X_B*((1.0-0.095)**6.0)
              X_7=X_B*((1.0-0.095)**7.0)
              X_8=X_B*((1.0-0.095)**8.0)
              X_9=X_B*((1.0-0.095)**9.0)
              X_10=X_C*((1.0-0.095)**10.0)
              X_11=X_C*((1.0-0.095)**11.0)
              X_12=X_C*((1.0-0.095)**12.0)
              X_13=X_C*((1.0-0.095)**13.0)
              X_14=X_C*((1.0-0.095)**14.0)              

              # Discount the costs of each year by their corresponding discount factor
              df_Costs.loc[0:11,'Diesel Costs'] = X_0
              df_Costs.loc[12:23,'Diesel Costs'] = X_1
              df_Costs.loc[24:35,'Diesel Costs'] = X_2
              df_Costs.loc[36:47,'Diesel Costs'] = X_3
              df_Costs.loc[48:59,'Diesel Costs'] = X_4
              df_Costs.loc[60:71,'Diesel Costs'] = X_5
              df_Costs.loc[72:83,'Diesel Costs'] = X_6
              df_Costs.loc[84:95,'Diesel Costs'] = X_7
              df_Costs.loc[96:107,'Diesel Costs'] = X_8
              df_Costs.loc[108:119,'Diesel Costs'] = X_9
              df_Costs.loc[120:131,'Diesel Costs'] = X_10
              df_Costs.loc[132:143,'Diesel Costs'] = X_11
              df_Costs.loc[144:155,'Diesel Costs'] = X_12
              df_Costs.loc[156:167,'Diesel Costs'] = X_13
              df_Costs.loc[168:179,'Diesel Costs'] = X_14      

        
              # Total monthly costs and cumulative costs   
              df_Costs['Total Costs'] = df_Costs['New Eq Costs']+df_Costs['Diesel Costs']+df_Costs['O&M Costs']
              df_Costs['Cumulative Costs']=np.cumsum(df_Costs['Total Costs'])               
               
           else:
        
              # Read csv file with the optimization
              df_opt = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv'.format(Systype, Reliability, Loadtype))  

              # Create costs dataframe for cumulative cost over lifetime                      
              df_Costs=pd.DataFrame()
    
              # Introduce colum with new equipment costs           
              df_Costs['New Eq Costs'] = np.zeros(180)
              df_Costs.iat[0,0]=df_opt.iat[0,30]
              df_Costs.iat[60,0]=df_opt.iat[1,30]
              df_Costs.iat[120,0]=df_opt.iat[2,30]
    
              # Introduce colum with O&M costs for each of the 3 iteration periods            
              df_Costs['O&M Costs'] = np.zeros(180)
              X_1= df_opt.iat[0,32]/60.0
              X_2=df_opt.iat[1,32]/60.0
              X_3=df_opt.iat[2,32]/60.0
       
              df_Costs.loc[0:59,'O&M Costs'] = X_1
              df_Costs.loc[60:119,'O&M Costs'] = X_2
              df_Costs.loc[120:179,'O&M Costs'] = X_3
    
              # Introduce colum with Diesel costs for each of the 3 iteration periods           
              df_Costs['Diesel Costs'] = np.zeros(180)
              X_1=df_opt.iat[0,33]/60.0
              X_2=df_opt.iat[1,33]/60.0
              X_3=df_opt.iat[2,33]/60.0
    
              df_Costs.loc[0:59,'Diesel Costs'] = X_1
              df_Costs.loc[60:119,'Diesel Costs'] = X_2
              df_Costs.loc[120:179,'Diesel Costs'] = X_3
        
              # Total monthly costs and cumulative costs
              df_Costs['Total Costs'] = df_Costs['New Eq Costs']+df_Costs['Diesel Costs']+df_Costs['O&M Costs']
              df_Costs['Cumulative Costs']=np.cumsum(df_Costs['Total Costs'])
    
              # Append results to final plotting data variable
    
           if Systype=='Hybrid':
        
               cumulative_cost[column+' Hybrid']=df_Costs['Cumulative Costs']

           elif Systype=='PVBatt':
        
               cumulative_cost[column+' PV-Battery']=df_Costs['Cumulative Costs']
        
           elif Systype=='Diesel':
        
               cumulative_cost[column+' Diesel']=df_Costs['Cumulative Costs']
               
           # Extract final cumulative cost and LCUE                               
           Appraisal_indexes=[30,14]        
           df_localmetrics=df_opt.iloc[-1, Appraisal_indexes]
           df_localmetrics.iloc[0]=df_opt.iloc[0,30]
           df_localmetrics=pd.DataFrame(df_localmetrics)    
           df_localmetrics=df_localmetrics.transpose()           
           df_keymetrics=pd.concat([df_keymetrics,df_localmetrics])
           
           # Save monthly cumulative costs over lifetime in a .csv file
           df_Costs.to_csv(plot_dir+'Systems monthly costs/Costs_{}_{}.csv'.format(Loadtype,Systype))
            
        print('\n LCUE and initial equipment costs for systems {} calculated.'.format(Loadtype))
        
    # Plot results: 1) Cumulative costs over lifetime for each Scenario

    # X variable as months over lifetime (15 years)    
    x=list(range(0,180))

    # Extract plotting variables
    labels=[]
    length = len(cumulative_cost.keys())
    allCosts = list(cumulative_cost.items())
    Costsforfigures=[]
             
    for n in range(0, length):

        Cost=allCosts[n]
        name=Cost[0]
        labels.append(name)
        Costsforfigures.append(list(Cost[1]))
    
    # Create 4 subplots for every Scenario    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharey=True)
    
    # Scenario 1        
    ax1.plot(x, np.divide(Costsforfigures[0],1000.0), color='lightseagreen',linestyle='dashed')
    ax1.plot(x, np.divide(Costsforfigures[1],1000.0), color='lightseagreen')
    ax1.plot(x, np.divide(Costsforfigures[2],1000.0), color='lightseagreen',linestyle=':')
    ax1.set_title('Scenario 1', fontweight="bold",fontsize=10)    
    ax1.grid()   
    
    # Scenario 2B
    ax2.plot(x, np.divide(Costsforfigures[3],1000.0), color='palevioletred',linestyle='dashed')
    ax2.plot(x, np.divide(Costsforfigures[4],1000.0), color='palevioletred')  
    ax2.plot(x, np.divide(Costsforfigures[5],1000.0), color='palevioletred',linestyle=':')
    ax2.plot(x, np.divide(Costsforfigures[2],1000.0), color='lightseagreen',linestyle=':')    
    ax2.set_title('Scenario 2B', fontweight="bold",fontsize=10)    
    ax2.grid()
    
    # Scenario 3
    ax3.plot(x, np.divide(Costsforfigures[6],1000.0), color='gold',linestyle='dashed')
    ax3.plot(x, np.divide(Costsforfigures[7],1000.0), color='gold')
    ax3.plot(x, np.divide(Costsforfigures[8],1000.0), color='gold',linestyle=':')
    ax3.plot(x, np.divide(Costsforfigures[2],1000.0), color='lightseagreen',linestyle=':')    
    ax3.set_title('Scenario 3', fontweight="bold",fontsize=10)    
    ax3.grid()

    # Scenario 4
    ax4.plot(x, np.divide(Costsforfigures[9],1000.0), color='lightsalmon',linestyle='dashed')
    ax4.plot(x, np.divide(Costsforfigures[10],1000.0), color='lightsalmon')  
    ax4.plot(x, np.divide(Costsforfigures[11],1000.0), color='lightsalmon',linestyle=':')
    ax4.plot(x, np.divide(Costsforfigures[2],1000.0), color='lightseagreen',linestyle=':')    
    ax4.set_title('Scenario 4', fontweight="bold",fontsize=10)    
    ax4.grid()
    
    # Format axes
    fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.ylabel('Cumulative cost (Thousands of $)')
    ax3.set(xlabel='Years of lifetime')
    ax4.set(xlabel='Years of lifetime')  
    
    for axs in fig.get_axes():
        
       axs.set_xticks([0,24,48,72,96,120,144,168]) 
       axs.set_xticklabels([0,2,4,6,8,10,12,14])
       axs.set_xlim(0,180)
    
    # Format legend
    from matplotlib.lines import Line2D
    custom_lines = [Line2D([0], [0], color='black', linewidth=2, linestyle=':', alpha=0.8), 
                Line2D([0], [0], color='black', linewidth=2,linestyle='dashed', alpha=0.8),
                Line2D([0], [0], color='black', linewidth=2,alpha=0.8)]  
    ax1.legend(custom_lines, ['Diesel system','Hybrid system','PV-Battery system'], loc='upper left', fontsize=8)
 
    # Format display
    plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, hspace=0.4)
       
    plt.show()    
    
    # Save figure    
    plot_name = "CumulativeCost_Re{}_OverLifetime.png".format(Reliability) 
    fig.savefig(plot_dir + plot_name,dpi=300,bbox_inches='tight')
    print(' Figure saved as '+plot_name)
    plt.show()
        
    #Save the monthly total load data in a file    
    df_CummCosts=pd.DataFrame(cumulative_cost, index=None)
    filepath=self.CLOVER_filepath + "/CLOVER-master/Locations/Refugee_Camp/Analysis/Scenario comparison/{} Re/CumulativeCosts.csv".format(Reliability)
    
    print( "\n Data saved as CumulativeCosts.csv" )

    # Plot results: 2) Barchart - Initial equipment cost and LCUE for each system and each scenario
  
    # Extract plotting variables
    df = pd.DataFrame(index=labels,columns=['LCUE','Initial new equipment costs'])
    df['LCUE']=list(df_keymetrics['LCUE ($/kWh)'])
    df['Initial new equipment costs']=list(df_keymetrics['New equipment cost ($)']/1000.0)

    fig = plt.figure() # Create matplotlib figure

    ax = fig.add_subplot(111) # Create matplotlib axes
    ax.set_xlim(['Scenario 1 Diesel','Scenario 4 Diesel'])
    ax2 = ax.twinx() # Create another axes that shares the same x-axis as ax.
    width = 0.3 # Width of the bars in the barchart

    # Plot barchart with LCUE and initial new equipment costs of each system/scenario
    df['LCUE'].plot(kind='bar', color=['lightseagreen','lightseagreen','lightseagreen','palevioletred','palevioletred','palevioletred','gold','gold','gold','lightsalmon','lightsalmon','lightsalmon'], hatch='//', alpha=0.5, edgecolor='white', ax=ax, width=width, position=1, label='LCUE')
    df['Initial new equipment costs'].plot(kind='bar', color=['lightseagreen','lightseagreen','lightseagreen','palevioletred','palevioletred','palevioletred','gold','gold','gold','lightsalmon','lightsalmon','lightsalmon'], edgecolor='white', ax=ax2, width=width, position=0, label='Initial new equipment costs')

    ax.set_ylabel('LCUE ($/kWh)')
    ax2.set_ylabel('Cost (Thousands of $)')
    
    # Format legend
    from matplotlib.patches import Patch
    custom_lines = [Patch(facecolor='black', alpha=0.5, hatch='///',edgecolor='white'),
                Patch(facecolor='black')]
    plt.legend(custom_lines, ['LCUE','Initial new equipment costs'], loc='upper center')

    # Save figure
    plot_name = "FinalCost_Re{}_Barchart.png".format(Reliability)
    fig.savefig(plot_dir + plot_name,dpi=300,bbox_inches='tight')
    print(' Figure saved as '+plot_name)
    plt.show()
  
    # Save data in .csv file
    file_name='LCUEandNewEquipmentCost_Comparison.csv'
    df.to_csv(plot_dir+file_name)

    print('\n Data saved as '+file_name)
    
def tariff_calculation(Systype, max_blackouts):
    
    """
    Calculates the tariff for refugee businesses required to recover the additional investment 
    of Approach A and B scenarios in comparison with optimised PV-Battery System over 15 years
    
    Calculates the cost recovered if refugees pay a grid tariff value and the remaining additional costs
    
    Calculates the tariff for public users to cover Scenario 1 to 2B complete system (B), and
    Scenario 1 PV-Battery system plus the remaining additional costs that refugees can't cover
        
    Input: Type of system and reliability level required
        
    Output: Calculates a number of relevant tariffs
    
    """           
    from operator import add  
    
    # Open Scenario 1 PV-Battery System optimisation file         
    Loadtype='Mix1'    
    Reliability= int((1.0 - max_blackouts)*100.0)  
    df_opt1 = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}.csv'.format(Systype, Reliability, Loadtype))    
  
    # Open Scenario 1 diesel system appraisal file
    df_diesel = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Simulation/Saved simulations/Sim_PV{}_Storage{}_{}_Re{}_Load{}_Appraisal.csv'.format(0, 0, 'Diesel', Reliability, Loadtype))
    
    # Open Scenario 1 to 2B (B) PV-Battery System optimisation file 
    Loadtype='Mix1to2B'
    df_optB = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}_{}.csv'.format(Systype, Reliability, Loadtype,'B'))
        
    # Open Scenario 1 to 2B (A) PV-Battery System optimisation file       
    df_optA = pd.read_csv(self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Optimisation/Saved optimisations/Opt_{}_Re{}_Load{}_{}.csv'.format(Systype, Reliability, Loadtype,'A'))
        
    # Get the additional cumulative discounted cost of A and B    
    CumulativeCost_1=df_opt1.iloc[-1,8]    
    LCUE_1=df_opt1.iloc[-1,14]    
    CumulativeCost_diesel=df_diesel.iloc[-1,8]    
    LCUE_diesel=df_diesel.iloc[-1,14]
    CumulativeCost_A=df_optA.iloc[-1,8]
    CumulativeCost_B=df_optB.iloc[-1,8]        
    AdditionalCost_A=CumulativeCost_A-CumulativeCost_1    
    AdditionalCost_B=CumulativeCost_B-CumulativeCost_1
    
    # Calculate total hourly energy consumption
    load_filepath=self.CLOVER_filepath + '/CLOVER-master/Locations/Refugee_Camp/Load/Device Load/{}_load.csv'.format('total')
    Total_Load=pd.read_csv(load_filepath)     
    Total_private=pd.DataFrame(Total_Load.loc[:,'Commercial'])                           
    
    # Calculate discounted hourly revenue if charged at grid tariff level    
    grid_tariff=0.0002244 # in $/Wh     
    Total_private['Revenue'] = np.multiply(Total_private['Commercial'],grid_tariff)             
    Total_discount=[]
    
    for year in range(0,15):
        
        discount_factor=(1-0.095)**year        
        yearly_factor= [discount_factor] * 8760        
        Total_discount.extend(yearly_factor)        

    Total_private['Discount factor'] = Total_discount        
    Total_private['Discounted revenue'] = np.multiply(Total_private['Revenue'],Total_private['Discount factor'])
    
    # Calculate cumulative discounted revenue over lifetime of system from businesses connected
    Total_private['Cumulative discounted revenue']=np.cumsum(Total_private['Discounted revenue'])
    Cumulative_revenue=Total_private.iloc[-1,4]

    # Create a date range column corresponding to the lifetime of the system
        
    date_rng = pd.date_range(start='1/1/2020', end='1/1/2035', freq='H')            
    Date=date_rng[:131400]    
    Total_private['Date'] = Date
    
    # Obtain remaining additional costs to pay    
    Extra_cost_A=AdditionalCost_A-Cumulative_revenue
    Extra_cost_B=AdditionalCost_B-Cumulative_revenue    
    
    # Obtain the tariff that public users need to pay to pay back for the complete system +10%ROI    
    Discounted_public_energy=np.multiply(Total_Load.loc[:,'Public'],Total_private['Discount factor'])
    Total_discounted_public_energy=Discounted_public_energy.sum()/1000.0

    Total_Cost_A_withROI=CumulativeCost_A*1.1
    Total_Cost_B_withROI=CumulativeCost_B*1.1    

    TariffA_TotalSystem=Total_Cost_A_withROI/Total_discounted_public_energy
    TariffB_TotalSystem=Total_Cost_B_withROI/Total_discounted_public_energy
    
    # Obtain LCUE for public users to pay just for Scenario 1 system + remaining from additional A/B    
    Total_Cost_A_extra_withROI=(CumulativeCost_1+Extra_cost_A)+CumulativeCost_A*0.1
    Total_Cost_B_extra_withROI=(CumulativeCost_1+Extra_cost_B)+CumulativeCost_B*0.1
    
    TariffA_extra=Total_Cost_A_extra_withROI/Total_discounted_public_energy
    TariffB_extra=Total_Cost_B_extra_withROI/Total_discounted_public_energy
    
    Savings_with_extra_A=CumulativeCost_diesel-Total_Cost_A_extra_withROI
    Savings_with_extra_B=CumulativeCost_diesel-Total_Cost_B_extra_withROI
    
    LCUE_variation_extra_A=-(LCUE_diesel-TariffA_extra)*100.0/LCUE_diesel
    LCUE_variation_extra_B=-(LCUE_diesel-TariffB_extra)*100.0/LCUE_diesel
    
    Revenue=Total_private['Discounted revenue']
    Revenue_lastyear=Revenue.iloc[-8760:].sum()
    
"""
===============================================================================
                 SUSTAINABLE MINI-GRID ANALYSIS FOR NYABIHEKE
===============================================================================

For further information contact:
    
    Javier Baranda Alonso
    MSc in Sustainable Energy Futures 2018-2019
    javier.baranda-alonso18@imperial.ac.uk
    
===============================================================================
"""    