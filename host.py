import eel
import ML_algo as algo
eel.init('UI')

history = {}
current_user = ""

@eel.expose
def run_content_filter_algo():
    global history, current_user
    obj = algo.Db(current_user)
    data = obj.run_content_filter_algo()

    if len(data) == 0:
        return "NONE"
    history = data

    # Get the num of movies to be recommended
    data = algo.History(history)
    recomendation_info = data.get_num_of_recommended_movies()

    # Generate movies from class Movie by using the data from the num of movies recommeded
    movies = []
    for genre, num in recomendation_info.items():
        movie = algo.Movie("genre", genre, num).get_movies_with_posters()
        movies.append(movie)
        print(movie)
    return movies
    
@eel.expose
def set_user(user):
    global current_user
    current_user = user
    
@eel.expose
def get_graph():
    global history
    obj = algo.History(history)
    if len(history) == 0:
        return "NONE"
    return obj.get_graph()

@eel.expose
def get_statistics():
    global history
    obj = algo.History(history)
    if len(history) == 0:
        return "NONE"
    return obj.get_statistics()

@eel.expose
def movie_watched(movie_info):
    global current_user
    obj = algo.Db(current_user)
    return obj.movie_watched(movie_info)

eel.start('home.html', port=9764, host='localhost',  mode='chrome', size=(1920, 1080))