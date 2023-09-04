import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title("🥣My Parents New healthy Dinner.")
streamlit.header("Breakfast Menu")
streamlit.text("🥗Sooji Upma with vegetables")
streamlit.text("🐔 Idli Vada and Sambar")
streamlit.text("🥑Lenthil Payasam")
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected= streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Banana'])

# Display the table on the page.
fruits_to_show = my_fruit_list.loc[fruits_selected]
# streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

#Create the repeatable code block (Called a function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#Requests from fruityvice response from an API
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
       streamlit.error("Please select a fruit to get information.")
  else:
       back_from_function = get_fruityvice_data(fruit_choice)
       streamlit.dataframe(back_from_function)
       #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
       #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
       #streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()

#Creating Function to look up for add fruits to the list using Snowflake related Functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from fruit_load_list")
         return my_cur.fetchall()

# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   streamlit.dataframe(my_data_rows)

#streamlit.text("Hello from Snowflake:")

