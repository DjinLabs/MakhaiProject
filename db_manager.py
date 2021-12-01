import streamlit as st
import pymongo

# Initialize connection.
client = pymongo.MongoClient(**st.secrets["mongo"])

db = client.heroes
items = db.mycollection.find()
items = list(items)  # make hashable for st.cache


def print_creation_time():
    print('Not implemented yet')


def database_widget():
    print_creation_time()
    st.write(items)
    for item in items:
        st.write(f"Hero with name: {item['name']}")
