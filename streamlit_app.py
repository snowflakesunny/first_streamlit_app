import streamlit
#import pandas
#import requests
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

#Requests from fruityvice
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
try:
	fruit_choice = streamlit.text_input('What fruit would you like information about?')
	if not fruit_choice:
		streamlit.error("Please select a fruit to get information.")
	else:
	fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
	fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
	streamlit.dataframe(fruityvice_normalized)
except URLError as e:
	streamlit.error()
_ = """
#import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

#streamlit.text(fruityvice_response.json())
# Displaying the furitvise json response using Pandas
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Showing in a dataframe to beautify it
streamlit.dataframe(fruityvice_normalized)
"""
streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit list contains:")
streamlit.dataframe(my_data_row)
streamlit.header("The complee fruit list:")
streamlit.dataframe(my_data_rows)
#streamlit.text("Hello from Snowflake:")

fruit_choice_to_add = streamlit.text_input('What fruit would you like to add?','Orange')
streamlit.write('Thanks for adding ', fruit_choice_to_add)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
