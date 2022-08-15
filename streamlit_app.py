
import streamlit
import pandas
import snowflake.connector
from urllib.request import URLError
import requests
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado and Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect('Pick some fruit',list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruitvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice )
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

   
    
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select fruit to get information.")
    else:
        back_from_function = get_fruitvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
        
except URLError as e:
    streamlit.error()
    
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("View our fruit list - Add Your Favorites!")
streamlit.text(my_data_row)
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list (FRUIT_NAME) "
        "VALUES(%s)", (
        new_fruit    
        ))

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to list'): 
    streamlit.write('The user entered ', add_my_fruit)
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
    #my_curinsert = my_cnxinsert.cursor()

if streamlit.button('Get Fruit List'):
    my_cnx2 = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_cur2 = my_cnx2.cursor()
    my_cur2.execute("select * from fruit_load_list")
    my_data_row2 = my_cur2.fetchall()
    streamlit.header("The fruit load list contains after insert:")
    streamlit.text(my_data_row2)
