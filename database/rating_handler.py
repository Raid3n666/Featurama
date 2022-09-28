import os.path
import json
from .imdb_api import DAL

dal = DAL()

filename = 'database/ratings.json'

class Json:
    
    def __init__(self):
        if os.path.exists(filename):
            pass
        else:
            self.create_json()
        
    def make_dict(self):
        dictionary = {}
        for title in dal.get_all_titles():
            dictionary.update({title : []})
        return dictionary

    def create_json(self):
        dictionary = self.make_dict()
        with open(filename, "w") as file:
            json.dump(dictionary, file)
    
    def add_rating(self, title, rating):
        with open(filename, 'r') as openfile:
            json_object = json.load(openfile)
            json_object[title].append(int(rating)) 
        with open(filename, "w") as file:
            json.dump(json_object, file)

    def get_avg(self, movie):
        with open(filename, 'r') as openfile:
            json_object = json.load(openfile)
        movie_ratings = json_object[movie]
        try:
            avg = sum(movie_ratings) / len(movie_ratings)
            avg = str(avg)[:3]    
        except:
            avg = 'None'
        return avg  

