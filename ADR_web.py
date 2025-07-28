import streamlit as st
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

class Isotope:
    def __init__(self, isotope_name, activity):
        self.isotope_name = isotope_name
        self.activity = activity / 1000000 # Convert MBq to TBq



st.title('Obliczanie LSA')

##############################
### Load file

file_name = "D-Value_A1_A2_Exempt.xlsm"
df = pd.read_excel(file_name, sheet_name = "D-Value_A1_A2_Exempted")
df = df.set_index("Radionuclide")

mass_kg = st.number_input("Podaj masę odpadu w kg", min_value=0.0, value=100.0, step=1.0)
st.divider()

# Get Isotope names
isotopes_names = df.index.to_list()
if 'isotopes' not in st.session_state:
    st.session_state['isotopes'] = []
isotopes_in_waste = {}

def manager():
    isotope_name = st.selectbox(label="podaj izotop", options = isotopes_names)
    activity = st.number_input("Podaj aktywność")
    add_button = st.button("Add", key='add_button')
    clear_button = st.button("Clear", key='clear', type="primary")
    selected_isotope_names = [isotope.isotope_name for isotope in st.session_state['isotopes']]
    if add_button:
        if activity > 0 and isotope_name not in selected_isotope_names:
            new_isotope = Isotope(isotope_name, activity)
            isotopes_in_waste[isotope_name] = new_isotope
            st.session_state['isotopes'] += [new_isotope]
            selected_isotope_names.append(isotope_name)
        else:
            st.warning("Juz wybrales ten izotop")
        
    if clear_button:
        st.session_state['isotopes'] = []
        selected_isotope_names = [isotope.isotope_name for isotope in st.session_state['isotopes']]


manager()

isotopes_names = [isotope.isotope_name for isotope in st.session_state['isotopes']]
activity_list = [isotope.activity for isotope in st.session_state['isotopes']]

selected_isotopes = df.loc[isotopes_names]


##############################
### Input

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

st.write(selected_isotopes)


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
if len(selected_isotopes) == 0:
    category_lsa = " "

st.divider()
category_str = f"Category of LSA: :green[{category_lsa}]"
st.header(category_str, divider="green")
