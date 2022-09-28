import requests
import json
import sqlite3

## Get Results
file = requests.get('https://imdb-api.com/eSn/API/Top250Movies/k_5i9egs1n')
file = json.loads(file.text)
items = file['items']

## Make db File
con = sqlite3.connect('database/movies.db', check_same_thread = False)
cur = con.cursor()

class DAL:

    def __init__(self):
        cur.execute('CREATE TABLE IF NOT EXISTS movies (title TEXT, rank TEXT, year TEXT, image TEXT, dir TEXT, star TEXT, coStar TEXT, ratingCount TEXT)')
        cur.execute('CREATE TABLE IF NOT EXISTS ratings (title TEXT, rating INTEGER)')

    def make_all(self):
        for key in items:
            title = key['title']
            rank = key['imDbRating']
            year = key['year']
            crew = key['crew']
            crew = crew.split(',')
            dir = crew[0][:-7]
            star = crew[1]
            co_star = crew[2]
            image = key['image']
            site_rating = "none"
            movie = Movie(title, rank, year, image, dir, star, co_star, site_rating)
            movie.add()
    
    def get_all_titles(self):
        cur.execute('SELECT title FROM movies')
        all = cur.fetchall()
        list_all = list(all)
        title_list = []
        for item in list_all:
            item = str(item)
            item = item.strip("'(,)'")
            title_list.append(item)
        return title_list

    def all_objects(self):
        objects_list = []
        cur.execute('SELECT * FROM movies')
        all = cur.fetchall()
        list_all = list(all)
        for item in list_all:
            title = item[0]
            rank = item[1]
            year = item[2]
            image = item[3]
            dir = item[4]
            star = item[5]
            co_star = item[6]
            site_rating = self.get_avg(title)
            movie = Movie(title, rank , year, image, dir, star, co_star, site_rating)
            objects_list.append(movie)
        return objects_list
    
    def add_rating(self, title, rating:int):
        cur.execute(f'INSERT INTO ratings VALUES ("{title}", {rating})')
        con.commit()
        new_rating = self.get_avg(title)
        cur.execute(f'UPDATE movies SET siteRating = "{new_rating}" WHERE title = "{title}"')
        con.commit()
        
    def select_ratings(self, title):
        cur.execute(f'SELECT rating FROM ratings WHERE title = "{title}"')
        results = cur.fetchall()
        list_res = []
        for rating in results:
            list_res.append(int(rating[0]))
        return list_res
    
    def get_avg(self, title):
        ratings = self.select_ratings(title)
        try:
            avg = sum(ratings) / len(ratings)
            avg = str(avg)[:3]
        except:
            avg = 'None'
        if avg[-1] == '.':
            avg = avg.strip(".")
        return avg

    def objects_by_rating(self):
        objects = self.all_objects()
        only_ranked = []
        for item in objects:
            try:
                float(item.site_rating)
                only_ranked.append(item)
            except:
                pass
        sorted_list = sorted(only_ranked, key = lambda x: float(x.site_rating), reverse = True)
        return sorted_list[:15]



class Movie:

    def __init__(self, title, rank, year, image, dir, star, co_star, site_rating):
        self.title = title
        self.rank = rank
        self.year = year
        self.dir = dir
        self.star = star
        self.co_star = co_star
        self.image = image
        self.site_rating = site_rating

    def add(self):
        cur.execute(f'INSERT INTO movies VALUES ("{self.title}", "{self.rank}", "{self.year}", "{self.image}", "{self.dir}", "{self.star}", "{self.co_star}", "{self.site_rating}")')
        con.commit()
         
## WARNING : DON'T USE ###    
# if __name__ == '__main__':
#     init = DAL()
#     init.make_all()
