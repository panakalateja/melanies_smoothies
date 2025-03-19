# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col



# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order=st.text_input('Name on smoothie:')
#st.write('The name on you smoothie will be:', name_on_order)

cnx=st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingrediants_list=st.multiselect(
    'Choose any up to 5 ingrediants:',
    my_dataframe,
    max_selections=5
)

if ingrediants_list:
    ingrediants_string=''
    for fruit_choosen in ingrediants_list:
        ingrediants_string+=fruit_choosen+' '
        st.subheader(fruit_choosen+' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_choosen)
        sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    #st.write(ingrediants_string)
    my_insert_stmt="""insert into SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS,name_on_order) 
    values ('"""+ingrediants_string+"""','"""+name_on_order+"""')"""
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")




