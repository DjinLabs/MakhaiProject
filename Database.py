import streamlit as st
import pymongo
from Singleton import Singleton


class DatabaseManager(metaclass=Singleton):

    def __init__(self):
        self.client = None
        self.db = None
        self.config_collection = None
        self.brawlers_collection = None
        self.abilities_collection = None

        # DB Initialization
        self.initialize_connection()

    def initialize_connection(self):
        self.client = pymongo.MongoClient(
            f"mongodb+srv://{st.secrets['mongo']['username']}:{st.secrets['mongo']['password']}@cluster0.78wex.mongodb.net/UrbanTribes"
            f"?retryWrites=true&w=majority")
        self.db = self.client['UrbanTribes']
        self.config_collection = self.db.configuration
        self.brawlers_collection = self.db.brawlers
        self.abilities_collection = self.db.abilities

    def get_gods(self, tribe_key: str = ""):
        query = {"tier": 0}

        if tribe_key:
            query["tribe"] = tribe_key

        return self.brawlers_collection.find(query)

    def get_heroes(self, tribe_key: str = ""):
        query = {"tier": 1}

        if tribe_key:
            query["tribe"] = tribe_key

        return self.brawlers_collection.find(query)

    def get_general_configuration(self):
        query = {"custom_id": "general_configuration"}
        return self.config_collection.find(query)[0], query


# Tribe Manager
db_manager = DatabaseManager()
