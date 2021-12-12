import streamlit as st
import pymongo
from Singleton import Singleton
from urllib import parse


class DatabaseManager(metaclass=Singleton):

    def __init__(self):
        self.user = parse.quote(st.secrets['mongo']['username'])
        self.password = parse.quote(st.secrets['mongo']['password'])
        self.client = None
        self.db = None
        self.config_collection = None
        self.brawlers_collection = None
        self.abilities_collection = None

        # DB Initialization
        # self.initialize_connection() Does not work with streamlit

    def initialize_connection(self):
        if self.client is None:
            print('Connecting to MongoDB...')
            self.client = pymongo.MongoClient(
                f"mongodb+srv://{self.user}:{self.password}@cluster0.78wex.mongodb.net/UrbanTribes"
                f"?retryWrites=true&w=majority")
            self.db = self.client['UrbanTribes']
            self.config_collection = self.db.configuration
            self.brawlers_collection = self.db.brawlers
            self.abilities_collection = self.db.abilities
            print(self.client.server_info())
        elif self.client.server_info()['ok'] == 1.0:
            print('Already connected to MongoDB')
        else:
            print('Unkown error with MongoDB')


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
