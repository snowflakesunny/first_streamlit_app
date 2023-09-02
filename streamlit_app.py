import streamlit
import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.title("🥣My Parents New healthy Dinner.")
streamlit.header("Breakfast Menu")
streamlit.text("🥗Sooji Upma with vegetables")
streamlit.text("🐔 Idli Vada and Sambar")
streamlit.text("🥑Lenthil Payasam")
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
streamlit.dataframe(my_fruit_list)
