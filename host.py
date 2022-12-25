import eel
import ML_algo as algo
eel.init('UI')

is_content_based = True # Default algo content-based
collabrative = algo.Collabrative()
content_based = algo.ContentBased()
movies = algo.Movie()

history = movies.get_history()

@eel.expose
def run_collabrative_filter_algo():
    global is_content_based, collabrative
    data = collabrative.filter()
    is_content_based = False 
    return data

@eel.expose
def run_content_filter_algo():
    global history, is_content_based, content_based, movies
    if len(history) == 0:
        return "NONE"

    recomendation_info = content_based.filter()

    # Get the num of movies to be recommended
    recommended_movies = []

    for genre, num in recomendation_info.items():
        m = movies.get_top_movies_by_genre(genre, num)
        recommended_movies.append(m)

    is_content_based = True
    return recommended_movies
    
@eel.expose
def movie_watched(movie_info):
    global movies, history
    movie = movies.watch(movie_info)
    history = movies.get_history()
    return movie
    
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