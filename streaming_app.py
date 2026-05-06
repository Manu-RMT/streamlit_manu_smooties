# Import python packages.
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import *
import requests  

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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))


ingredients_list = st.multiselect(
    'Choose up to 5 ingedients : '
    ,my_dataframe
    ,max_selections=5
)


if ingredients_list and name_order:
    ingredients_str = ''
    for fruit_choosen in ingredients_list:
        ingredients_str += fruit_choosen + ' '

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


smoothiefroot_response = requests.get("http://my.smoothiefroot.com/api/fruit/watermelon")  
st.text(smoothiefroot_response)
    
