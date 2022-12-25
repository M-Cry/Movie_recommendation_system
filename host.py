import eel
import ML_algo as algo
eel.init('UI')

history = {}
is_content_based = True # Default algo content-based
collabrative = algo.Collabrative()
content_based = algo.ContentBased(history)
movies = algo.Movie()

@eel.expose
def run_collabrative_filter_algo():
    global is_content_based, collabrative
    data = collabrative.filter()
    is_content_based = False 
    return data

@eel.expose
def run_content_filter_algo():
    global history, is_content_based, content_based, movies
    data = content_based

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

    is_content_based = True
    return movies
    
@eel.expose
def movie_watched(movie_info):
    global movies
    return movies.watch(movie_info)
    
@eel.expose
def get_graph():
    """ Get latest graph generated"""
    global content_based, is_content_based, collabrative

    if is_content_based:
        return content_based.get_graph()
    return collabrative.get_graph()

@eel.expose
def get_statistics():
    global history, content_based

    if len(history) == 0:
        return "NONE"
    return content_based.get_statistics()

eel.start('home.html', port=9764, host='localhost',  mode='chrome', size=(1920, 1080))