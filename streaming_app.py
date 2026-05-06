# Import python packages.
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import *
import requests  
import pandas as pd

# Write directly to the app.
st.title(f":cup_with_straw: Custom Your Smoothie :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom Smoothie ! """
)


name_order = st.text_input("Name on Your Fabulous Smoothie", "Name")
st.write("Helloooo !!! ", name_order)

# session = get_active_session()
cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# change to pandas for use iloc
pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    'Choose up to 5 ingedients : '
    ,my_dataframe
    ,max_selections=5
)


if ingredients_list and name_order:
    ingredients_str = ''
    for fruit_chosen in ingredients_list:
        ingredients_str += fruit_chosen + ' '

        # Correspondance nom au pluriel ou singulier
        # search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        value = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        search_on = value if pd.notna(value) else fruit_chosen
 
        #all information smoothies
        all_smoothies_api_details = requests.get(f"http://my.smoothiefroot.com/api/fruit/all" )  
        res_all_smoothies = all_smoothies_api_details.json()
        
        for key, value_fruits in res_all_smoothies.items():
          st.write(value_fruits.name)
        st.stop()
      
        st.subheader(fruit_chosen + ' : Nutrition Information') 
        smoothiefroot_response = requests.get(f"http://my.smoothiefroot.com/api/fruit/{search_on}" )  
        res_api = smoothiefroot_response.json()
        df_apismoothie = st.dataframe(data=res_api, use_container_width=True)

    st.write(ingredients_str)

    # requete préparation insert data
    my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS,NAME_ON_ORDER)
                    values ('""" + ingredients_str + """','""" + name_order + """')"""

   
    # bouton 
    button_click = st.button('Submit Order')
    
    # requete  insertion data
    if button_click:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is orderd ! ', icon=':material/check:')



    
