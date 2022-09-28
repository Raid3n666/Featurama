import requests
import json
import sqlite3
from random import shuffle
import wikipedia

## Get Results
file = requests.get('https://imdb-api.com/eSn/API/Top250Movies/k_5i9egs1n')
file = json.loads(file.text)
items = file['items']

## Make db File
con = sqlite3.connect('db2/movies.db', check_same_thread = False)
cur = con.cursor()


class DAL:
    def __init__(self) -> None:
        cur.execute('CREATE TABLE IF NOT EXISTS movies (title TEXT, year TEXT, img TEXT, dir TEXT, star TEXT, co_star TEXT, avg_rate FLOAT, rate_count INT)')
        cur.execute('CREATE TABLE IF NOT EXISTS ratings (title TEXT, rating INT)')

    def first_run(self):
        ## USE ONLY ON FIRST RUN ##
        ###  CORRUPTS DATA !!!  ###
        for key in items:
            title = key['title']
            year = key['year']
            crew = key['crew']
            crew = crew.split(',')
            dir = crew[0][:-7]
            star = crew[1]
            co_star = crew[2]
            image = key['image']
            avg_rate = 0
            rate_count = 0
            cur.execute(f'INSERT INTO movies VALUES ("{title}", "{year}", "{image}", "{dir}", "{star}", "{co_star}", {avg_rate}, {rate_count})')
            con.commit()
    
    def get_all_objects(self):
        objects_list = []
        cur.execute('SELECT * FROM movies')
        results = cur.fetchall()
        results = list(results)
        for item in results:
            title = item[0]
            year = item[1]
            img = item[2]
            dir = item[3]
            star = item[4]
            co_star = item[5]
            avg_rate = item[6]
            rate_count = item[7]
            movie = Movie(title, year, img, dir, star, co_star, avg_rate, rate_count)
            objects_list.append(movie)
        return objects_list
    
    def select_ratings(self, title):
        cur.execute(f'SELECT rating FROM ratings WHERE title = "{title}"')
        results = cur.fetchall()
        list_res = []
        for rating in results:
            list_res.append(int(rating[0]))
        return list_res
    
    def count_ratings(self,title):
        cur.execute(f'SELECT rating FROM ratings WHERE title = "{title}"')
        results = cur.fetchall()
        list_res = list(results)
        rating_count = len(list_res)
        return rating_count

    def get_avg(self, title):
        ratings = self.select_ratings(title)
        try:
            avg = sum(ratings) / len(ratings)
            avg = str(avg)[:3]
        except:
            avg = 'None'
        if str(avg)[-1] == '.':
            avg = avg.strip(".")
        return float(avg)

    def add_rating(self, title, rating):
        cur.execute(f'INSERT INTO ratings VALUES ("{title}", {rating})')
        con.commit()
        new_avg = self.get_avg(title)
        new_count = self.count_ratings(title)
        cur.execute(f'UPDATE movies SET avg_rate = {new_avg} WHERE title = "{title}"')
        cur.execute(f'UPDATE movies SET rate_count = {new_count} WHERE title = "{title}"')
        con.commit()
    
    def objects_by_rating(self):
        objects = self.get_all_objects()
        only_ranked = []
        for item in objects:
            if item.avg_rate > 0:
                only_ranked.append(item)
        sorted_list = sorted(only_ranked, key = lambda x: float(x.avg_rate), reverse = True)
        return sorted_list[:15]
    
    def random_film(self):
        all_flims = self.get_all_objects()
        shuffle(all_flims)
        return all_flims[0]
     
    def get_summary(self, title):
        movie = []
        for item in self.get_all_objects():
            if item.title == title:
                movie.append(item)
        if len(movie) > 0:
            try:
                result = wikipedia.page(f"{movie[0].title} film")
                return result.summary
            except:
                try:
                    result = wikipedia.page(f"{movie[0].title} {movie[0].year}")
                    return result.summary
                except:
                    return None
        else:
            return None



class Movie:

    def __init__(self, title, year, img, dir, star, co_star, avg_rate, rate_count) -> None:
        self.title = title
        self.year = year
        self.img = img
        self.dir = dir
        self.star = star
        self.co_star = co_star
        self.avg_rate = avg_rate
        self.rate_count = rate_count
    

