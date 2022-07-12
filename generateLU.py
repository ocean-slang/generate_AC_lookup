# Written by Sarah Lang from University of RI, thank you to Mollie Passacantando for python help and Yulun Wu for recommending this procedure. 

import matplotlib
import numpy as np
import csv
from matplotlib.pyplot import *
import copy
import math
import pandas as pd
from Py6S import *

path2 = '/Volumes/slangSSD/hyperspectral/MASS_wavelengths.csv'
with open(path2, 'r') as f:
    reader = csv.reader(f, delimiter=',')
    headers = next(reader)
    data = np.array(list(reader)).astype(float)

waves=data/1000
wavey=np.squeeze(waves[0:140]) #using sensor specific wavelengths
zenith=np.arange(50,100,5) #calculate for every 5˚ - will interpolate rest
a=200 #average azimuth since it didnt affect output
refl = np.arange(0.005,.031,.001) #calculate for every 0.001 surface reflectance, will interpolate rest

#note: as is this script generates ~ 500,000 combos

df = pd.DataFrame(columns=('radiosonde_id','wavelength','zenith','apparent_refl','atmo_corr_refl'))

import os
path_of_the_directory= '/Volumes/slangSSD/hyperspectral/radiosondes/csv/overlap' #i have a folder of radiosonde profiles. i attached an example. 
print("Files and directories in a specified path:")
for ind,filename in enumerate(os.listdir(path_of_the_directory)):
    f = os.path.join(path_of_the_directory,filename)
    with open(f, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        headers = next(reader)
        data = np.array(list(reader)).astype(float)
        pressure=data[:,0]
        altitude=data[:,1]
        temperature=data[:,2]
        mixing_ratio=data[:,3]
    for j in wavey:
        for z in zenith:
            for t in refl:
                s=SixS()
                base_profile=AtmosProfile.MidlatitudeWinter
                s.wavelength=Wavelength(j)
                s.atmos_profile = SixSHelpers.Radiosonde._import_from_arrays(pressure, altitude, temperature, mixing_ratio, base_profile)
                s.aero_profile = AeroProfile.PredefinedType(AeroProfile.Maritime)
                s.altitudes.set_target_sea_level()
                s.altitudes.set_sensor_custom_altitude(1)
                s.geometry = Geometry.User()
                s.geometry.solar_z = z
                s.geometry.solar_a = a
                s.geometry.latitude = 37.3
                s.geometry.longitude = -123
                yup=t*(math.pi/math.cos(z)) #apparent refl from surface refl
                s.atmos_corr = AtmosCorr.AtmosCorrBRDFFromReflectance(yup)
                s.run()
                values_to_add={'radiosonde_id':ind,'wavelength':j,'zenith':z,'apparent_refl':t,'atmo_corr_refl':s.outputs.atmos_corrected_reflectance_brdf}
                row_to_add = pd.Series(values_to_add, name=ind)
                df = df.append(row_to_add)
df.to_csv('py6s_ac_lookup_overlap.csv')
