from flask import Flask, render_template, request
from db2.new_api import DAL

dal = DAL()

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    objects = dal.get_all_objects()
    if request.method == 'POST':
        for item in objects:
            try:
                rating = request.form[item.title]
                dal.add_rating(item.title, int(rating))
                objects = dal.get_all_objects()
            except:
                pass
        return render_template('index.html', movies = objects)
    else: 

        return render_template('index.html', movies = objects)

@app.route('/top_movies')
def top_movies():
    objects = dal.objects_by_rating()
    return render_template('list.html', movies = objects)

@app.route('/random')
def random():
    random_film = dal.random_film()
    summary = dal.get_summary(random_film.title)
    if summary:
        pass
    else:
        summary = 'No results found'
    return render_template('random.html', movie = random_film, summary = summary)

if __name__ == '__main__':
    app.run(debug = True, port = 80, host = '0.0.0.0')