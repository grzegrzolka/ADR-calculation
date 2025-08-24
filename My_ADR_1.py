import pandas as pd
import numpy as np
import math
from datetime import date, datetime, timedelta
import streamlit as st

#Class Isotope
class Isotopes_in_Package:  #class named Isotopes_in_waste to store isotope name and activity
    def __init__(self, isotope, activity):  #__init__() method to initialize the attributes (to assign values isotope name and activity)
        #The self parameter is a reference to the current instance of the class, and is used to access variables that belong to the class.
        #It does not have to be named self, you can call it whatever you like, but it has to be the first parameter of any function in the class:
        self.isotope_name = isotope
        self.activity = activity

def manager():  #function to manage adding and clearing isotopes
    isotope_name = st.selectbox(label="Select isotope: ", options = isotopes_names)
    activity = st.number_input("Enter isotope activity [MBq: ]") / 1000000  # Convert MBq to TBq
    add_button = st.button("Add isotope", key='add_button', type="primary")
    clear_button = st.button("Clear isotopes", key='clear', type="primary")
    selected_isotope_names = [isotope.isotope_name for isotope in st.session_state['radionuclides']]
    if add_button:
        if activity == 0:
            st.warning("Isotope not added. Activity must be greater than 0")
        elif activity > 0 and isotope_name not in selected_isotope_names:
            new_isotope = Isotopes_in_Package(isotope_name, activity)
            isotopes_in_package[isotope_name] = new_isotope
            st.session_state['radionuclides'] += [new_isotope]   #add new isotope to the session state list
            selected_isotope_names.append(isotope_name)
        else:
            st.warning("You have already selected this isotope")
    if clear_button:
        st.session_state['radionuclides'] = []
        selected_isotope_names = [isotope.isotope_name for isotope in st.session_state['radionuclides']]


def classification(isotopes_in_package):    #define function to classify the package based on isotopes and their activities def=define
    sumActivity= 0
    sum_act_concent_mixture = 0
    fi = 0 #fraction of isotope activity in mixture
    sum_fi = 0
    
    fi_A1i = 0 # Initialize to avoid division by zero, fraction of isotope activity in mixture to A1 [TBq]
    fi_A2i = 0 # Initialize to avoid division by zero, fraction of isotope activity in mixture to A2 [TBq]
    fi_Ti = 0 # Initialize to avoid division by zero, fraction of isotope activity in mixture to Transport Security Threshold [TBq]
    fi_Di = 0 # Initialize to avoid division by zero, fraction of isotope activity in mixture to D-Value [TBq]
    fi_conc= 0 # Initialize to avoid division by zero, fraction of isotope activity in mixture to Activity concentration for exempt material (kBq/kg)

    A1_mixture = 0
    A2_mixture = 0
    T_mixture = 0
    act_conc_limit_mixture = 0

    # f(i) - fraction of isotope activity in mixture - add value to the list
    for my_isotope in isotopes_in_package:   
        sumActivity += my_isotope.activity # activity sum all isotopes [TBq]        
        sum_act_concent_mixture += my_isotope.activity * 1000000000 / mass # [TBq/kg] convert to [kBq/kg]

        # f(i) - fraction of isotope activity in mixture - add value to the list
    for my_isotope in isotopes_in_package:
        fi = my_isotope.activity / sumActivity # fraction of isotope activity in mixture [TBq]
        fi_A1i += fi / float(df.loc[my_isotope.isotope_name]["A1 [TBq]"]) # fraction of isotope activity in mixture to A1 [TBq]
        fi_A2i += fi / float(df.loc[my_isotope.isotope_name]["A2 [TBq]"]) # fraction of isotope activity in mixture to A2 [TBq]
        fi_Ti += fi / float(df.loc[my_isotope.isotope_name]["Transport Security Threshold [TBq]"]) # fraction of isotope activity in mixture to Transport Security Threshold [TBq]
        fi_Di += fi / float(df.loc[my_isotope.isotope_name]["D-Value [TBq]"]) # fraction of isotope activity in mixture to D-Value [TBq]
        fi_conc += fi / float(df.loc[my_isotope.isotope_name]["Activity concentration for exempt material (kBq/kg)"]) # fraction of isotope activity in mixture to Activity concentration for exempt material (kBq/kg)
        sum_fi += fi
    
    if sumActivity != 0:

        A1_mixture = 1 / fi_A1i
        A2_mixture = 1 / fi_A2i
        T_mixture = 1 / fi_Ti
        D_mixture = 1 / fi_Di
        act_conc_limit_mixture = 1 / fi_conc
        
        st.divider() 
        
        st.markdown(f"###### :red[sum of isotopes activity:  {round(sumActivity*1000000, 9)} [ MBq]]")
        st.markdown(f"###### :red[sum of isotopes activity:  {round(sumActivity, 12)} [ TBq]]")

        st.divider()
        
        st.markdown(f"###### :blue[A1 for the mixture of isotopes: ] {round(A1_mixture, 7)} [TBq]")
        st.text(f"- multiple of A1: {round(sumActivity/A1_mixture, 7)}")

        st.markdown(f"###### :blue[A2 for the mixture of isotopes: ] {round(A2_mixture, 7)} [TBq]")
        st.text(f"- multiple of A2: {round(sumActivity/A2_mixture, 7)}")

        st.markdown(f"###### :blue[Transport security threshold for the mixture of isotopes: ] {round(T_mixture, 7)} [TBq]")
        st.text(f"- A/T ratio: {round(sumActivity/T_mixture, 7)}")

        st.markdown(f"###### :blue[D-Value for the mixture of isotopes:]  {round(D_mixture, 7)} [TBq]")
        st.text(f"- A/D ratio: {round(sumActivity/D_mixture, 7)}")

        st.markdown(f"###### :blue[Activity concentration limit for exempt material for mixture of isotopes: ] {round(act_conc_limit_mixture, 7)} [kBq/kg]")
        st.text(f"- activity concentration limit for exempt material for mixture of isotopes / activity concentration of isotopes in mixture: {format(round(sum_act_concent_mixture/act_conc_limit_mixture, 7))}")

        st.divider()

        if sumActivity <= A1_mixture / 1000:
            st.markdown(f"###### :blue[Excepted package special form: ] 0.001*A1 = {round(sumActivity / A1_mixture * 1000, 7)}")

        else:
            st.markdown(f"###### :red[Not excepted package special form:] 0.001*A1 = {round(sumActivity / A1_mixture * 1000, 7)}")

        if sumActivity <= A2_mixture/1000:
            st.markdown(f"###### :blue[Excepted package solid:] 0.001*A2 = {round(sumActivity / A2_mixture * 1000, 7)}")        

        else:
            st.markdown(f"###### :red[Not excepted package solid:] 0.001*A2 = {round(sumActivity / A2_mixture * 1000, 7)}")


        if sumActivity <= A2_mixture/10000:
            st.markdown(f"###### :blue[Excepted package liquid:] 0.0001*A2 = {round(sumActivity / A2_mixture * 10000, 7)}")

        else:
            st.markdown(f"###### :red[Not excepted package liquid:] 0.0001*A2 = {round(sumActivity / A2_mixture * 10000, 7)}")


        if sum_act_concent_mixture <= 30 * act_conc_limit_mixture:
            st.markdown(f"###### :blue[LSA-I:] 30*activity concentration limit = {round(sum_act_concent_mixture / act_conc_limit_mixture /30, 7)}")
        else: 
            st.markdown(f"###### :red[Not LSA-I:] 30*activity concentration limit = {round(sum_act_concent_mixture / act_conc_limit_mixture /30, 7)}")

        if sum_act_concent_mixture/1000000000000 <= A2_mixture * 0.0001:
            st.markdown(f"###### :blue[LSA-II:] 0.0001*A2 = {round(sum_act_concent_mixture/1000000000000 / A2_mixture  / 0.0001, 7)}")
        else:
            st.markdown(f"###### :red[Not LSA-II:] 0.0001*A2 = {round(sum_act_concent_mixture/1000000000000 / A2_mixture  / 0.0001, 7)}")
            st.text(f"0.0001*A2 = {round(sum_act_concent_mixture/1000000000000 / A2_mixture  / 0.0001, 7)}")

        if sum_act_concent_mixture/1000000000000 <= A2_mixture * 0.00001:
            st.markdown(f"###### :blue[Liquid LSA-II:] 0.00001*A2 = {round(sum_act_concent_mixture/1000000000000 /  A2_mixture / 0.00001, 7)}")
        else: 
            st.markdown(f"###### :red[Not Liquid LSA-II:] 0.00001*A2 = {round(sum_act_concent_mixture/1000000000000 / A2_mixture /0.00001, 7)}")

        if sum_act_concent_mixture/1000000000000 <= A2_mixture * 0.002:
            st.markdown(f"###### :blue[LSA-III:] 0.002*A2 = {round(sum_act_concent_mixture / 1000000000000 / 0.002 / A2_mixture, 7)}")
        else:
            st.markdown(f"###### :red[Not LSA-III:] 0.002*A2 = {round(sum_act_concent_mixture / 1000000000000 / 0.002 / A2_mixture, 7)}")

        if sumActivity <= A1_mixture:
            st.markdown(f"###### :blue[TYPE-A:] multiple of A1 = {round(sumActivity/A1_mixture, 7)}")
        else:
            st.markdown(f"###### :red[Not TYPE-A:] multiple of A1 = {round(sumActivity/A1_mixture, 7)}")

        if sumActivity/T_mixture <=1:
            st.markdown(f"###### :blue[Not Dangerous Goods:] sumActivity/T_mixture = {round(sumActivity/T_mixture, 7)}")
        else:
            st.markdown(f"###### :red[Dangerous Goods:] sumActivity/T_mixture = {round(sumActivity/T_mixture, 7)}")
            
        if sumActivity/D_mixture <= 1:
            st.markdown(f"###### :blue[Activity / D-Value <= 1:] sumActivity/D_mixture = {round(sumActivity/D_mixture, 7)}")
        else:
            st.markdown(f"###### :red[Activity / D-Value > 1:] sumActivity/D_mixture = {round(sumActivity/D_mixture, 7)}")


################################## STREAMLIT APP #####################################
#######################################################################################


# title of the application
st.subheader(':blue[ADR package classification]')
st.markdown('###### :green[This app classifies the package according to ADR regulations based on activity of isotopes in the package and the mass of package content.]')

# dataframe loading
df = pd.read_csv('A1 A2 TS D ActConcent.csv', sep = ";", index_col = 0, names = ["Activity concentration for exempt material (kBq/kg)", 
                                                                                 "Activity limit for an exempt consignment (Bq)", "A1 [TBq]", "A2 [TBq]", 
                                                                                 "Transport Security Threshold [TBq]", "D-Value [TBq]", "Desintegration [Years]"])
df['A1 [TBq]'] = df['A1 [TBq]'].str.replace(',', '.')
df['A2 [TBq]'] = df['A2 [TBq]'].str.replace(',', '.')
df['Transport Security Threshold [TBq]'] = df['Transport Security Threshold [TBq]'].str.replace(',', '.')
df['D-Value [TBq]'] = df['D-Value [TBq]'].str.replace(',', '.')
df['Desintegration [Years]'] = df['Desintegration [Years]'].str.replace(',', '.')
#st.write(df)

mass = st.number_input("Enter the mass of the waste in package [kg]: ", step=0.5, format="%0.1f")
isotopes_in_package = {} #dictionary to store isotopes and their activities

isotopes_names = df.index.to_list()

if 'radionuclides' not in st.session_state:  # initialize session state list to store selected isotopes if it doesn"t exist. It allows to store data that persists across reruns of the application
    st.session_state['radionuclides'] = []

manager() #call the function to execute the isotope selection and activity input management,
#it will display the selectbox, number input, and buttons, and handle adding/clearing isotopes
st.markdown(f"###### :blue[package content mass: {mass} kg]")

istope_names = [isotope.isotope_name for isotope in st.session_state['radionuclides']]
df_selected_isotopes = df.loc[istope_names]

activities = [isotope.activity * 1000000 for isotope in st.session_state['radionuclides']]
df_selected_isotopes.insert(0, 'Activity in package [MBq]', activities)

st.dataframe( df_selected_isotopes.T,  column_config= {"_index": st.column_config.Column("",width=300)})  #display dataframe with selected isotopes

# st.write(df.loc[istope_names])

# for isotope in st.session_state['radionuclides']:
#     st.markdown(f"###### :red[{isotope.isotope_name}:  {isotope.activity*1000000} MBq]")
#     st.text(f"- A1 [TBq]: {df.loc[isotope.isotope_name]['A1 [TBq]']}")
#     st.text(f"- A2 [TBq]: {df.loc[isotope.isotope_name]['A2 [TBq]']}")
#     st.text(f"- Transport Security Threshold [TBq]: {df.loc[isotope.isotope_name]['Transport Security Threshold [TBq]']}")
#     st.text(f"- D-Value [TBq]: {df.loc[isotope.isotope_name]['D-Value [TBq]']}")
#     st.text(f"- activity concentration limit for exempt material [kBq/kg]: {df.loc[isotope.isotope_name]['Activity concentration for exempt material (kBq/kg)']}")    
#     st.text(f"- desintegration [years]: {df.loc[isotope.isotope_name]['Desintegration [Years]']}")


classification(st.session_state['radionuclides']) #call the function to classify the package based on isotopes and their activities


st.divider()
st.text("Made by: Andrzej Grzegrzółka")

