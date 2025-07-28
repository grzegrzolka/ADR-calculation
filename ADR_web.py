#import streamlit as st
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt


##############################
### Load file

file_name = "D-Value_A1_A2_Exempt.xlsm"
df = pd.read_excel(file_name, sheet_name = "D-Value_A1_A2_Exempted")
df = df.set_index("Radionuclide")
df.head()


##############################
### Input

isotope_1 = "Cs-137"
activity_1 = 0.3
activity_1 = activity_1 / 1000000

isotope_2 = "Am-241"
activity_2 = 1200
activity_2 = activity_2 / 1000000

isotope_3 = "Sr-90"
activity_3 = 0.8
activity_3 = activity_3 / 1000000

mass_kg = 10

activity_list = [activity_1, activity_2, activity_3 ]
selected_isotopes = df.loc[[isotope_1, isotope_2, isotope_3]]


##############################
### Process data

# Add columns with activity, activity ratio, multiple A1 and multiple A2
selected_isotopes ["Activity [TBq]"] = activity_list
selected_isotopes ["Isotope Activity Ratio"] = selected_isotopes ["Activity [TBq]"] /selected_isotopes ["Activity [TBq]"].sum()

selected_isotopes ["Isotope A1 Ratio"] = selected_isotopes ["Activity [TBq]"] /selected_isotopes ["Activity [TBq]"].sum() / selected_isotopes ["A1 [TBq]"]
selected_isotopes ["Isotope A2 Ratio"] = selected_isotopes ["Activity [TBq]"] /selected_isotopes ["Activity [TBq]"].sum() / selected_isotopes ["A2 [TBq]"]
selected_isotopes ["Isotope xxxxx"] = selected_isotopes ["Activity [TBq]"] /selected_isotopes ["Isotope A1 Ratio"]      

selected_isotopes ["Multiple A1"] = selected_isotopes ["Activity [TBq]"] / selected_isotopes ["A1 [TBq]"]
selected_isotopes ["Multiple A2"] = selected_isotopes ["Activity [TBq]"] / selected_isotopes ["A2 [TBq]"]

# Calculate sum of multiple A1
sum_A1 = selected_isotopes ["Multiple A1"].sum()
sum_Isotope_A1_ratio = selected_isotopes["Isotope A1 Ratio"].sum()

# Calculate sum of multiple A2
sum_A2 = selected_isotopes ["Multiple A2"].sum()
sum_Isotope_A2_ratio = selected_isotopes["Isotope A2 Ratio"].sum()

# Add column for LSA-1, LSA-2, Type-A Package
selected_isotopes ["Activity concentration in consignment (Bq/g)"] = selected_isotopes ["Activity [TBq]"] * 1000000000 / mass_kg
selected_isotopes["Average specific activty"] = selected_isotopes ["Activity concentration in consignment (Bq/g)"] / selected_isotopes ["Activity concentration for exempt material (Bq/g)"]
# selected_isotopes["LSA-2"] = selected_isotopes ["Activity concentration in consignment (Bq/g)"] / selected_isotopes["A2 [TBq]"] / 100000000
selected_isotopes["Type-A Package"] =  selected_isotopes ["Activity [TBq]"] / selected_isotopes ["A1 [TBq]"]

# Calculate sums
average_activity_sum = selected_isotopes["Average specific activty"].sum()
# lsa_2_sum = selected_isotopes["LSA-2"].sum()
type_A_sum = selected_isotopes["Type-A Package"].sum()
act_concent_in_package_sum = selected_isotopes ["Activity concentration in consignment (Bq/g)"].sum()



##############################
### Set Category
category_lsa = ''
#Wart A2 dla mieszaniny


if average_activity_sum  <= 30:
   category_lsa = "LSA-I"
else :
    a2_ratio = 1/sum_Isotope_A2_ratio
    specific_activity_mass = a2_ratio / mass_kg / 1000
    print(specific_activity_mass)
    if specific_activity_mass <= 0.0001:
        category_lsa = "LSA-II"
    elif specific_activity_mass <= 0.002:
        category_lsa = "LSA-III"
    else:
        category_lsa = "NOT LSA"

category_lsa