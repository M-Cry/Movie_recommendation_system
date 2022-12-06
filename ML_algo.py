import csv
import datetime
import numpy as np
import requests as rq
import matplotlib.pyplot as plt
"""
    Machine learning algo. -> Supervised Learning (data = user watch history)
    By GUtech students
"""
class Db:
    def __init__(self) -> None:
        self.history_file = "user watch history"
        
    def get_history(self):
        try:
            with open(self.history_file) as file:
                lines = file.readlines()
                return lines
        except FileNotFoundError:
            # No movies has been watched yet
            return "NONE"

    def movie_watched(self, movie_info):
        with open(self.history_file, "a") as file:
            file.write(movie_info + "\n")
        return movie_info.split(",")[:2]

    def run_algo(self):
        genres = {}
        try:
            with open(self.history_file) as file:
                movies = file.readlines()
                for movie in movies:
                    movie = movie.split(",")
                    if movie[1] in genres:
                        genres[movie[1]] += 1
                    else:
                        genres[movie[1]] = 1
        except FileNotFoundError:
            pass
        return genres

class Movie:
    def __init__(self, rec_type: str, rec: str, rec_num: int) -> None:
        self.headers = {}

        self.rec = rec              # rec = Recommended genre
        self.rec_num = rec_num      # rec_num = Number of movies to recommend
        self.rec_type = rec_type    # rec_type = Recommendation type i.e. genre, release date, rating ...
        
        self.api_url = "https://api.themoviedb.org/3/movie/550?api_key="
        self.api_key = "bff8376d6367c86f36682ec21870f938"
        self.api = self.api_url + self.api_key
        
        self.posters = []
        self.top_movies = []

    def get_top_movies_by_genre(self) -> list:
        """
        ##############################################################
        #####   Get movies specified in __init__ func
        ##############################################################
        """
        rec_movies = []

        with open("movies.csv", encoding="utf-8") as data:
            headers = dict(enumerate(data.readline().split(",")))       #{0: 'title', ...}
            headers = {value:key for key, value in headers.items()}     #{'title': 0, ...}
            self.headers = headers

            movies = csv.reader(data)
            for movie in movies:
                if self.rec in movie[self.headers[self.rec_type]]:
                    rec_movies.append(movie)

            # sorted => TimSort Algo. | O(n*log(n))
            self.top_movies = sorted(rec_movies, key = lambda x: x[self.headers["rating"]], reverse = True)[ : self.rec_num]

        """
        ##################################################################
        #####   Fetch movie posters from API if server returns OK status
        ##################################################################
        """
        for movie in self.top_movies:
            # self.posters.append("test")
            movie_title = movie[self.headers["title"]]
            query = f"https://api.themoviedb.org/3/search/movie?api_key=bff8376d6367c86f36682ec21870f938&query={movie_title.replace(' ', '%20')}&page=1"
            respond = rq.get(query)
            
            if respond.status_code == 200: # Connection established
                json = respond.text 
                start_index = '"poster_path":"/'
                end_index = '","release_date":"'
                
                poster_path = json[ json.find(start_index) + len(start_index) : json.find(end_index) ]
                poster = f'https://image.tmdb.org/t/p/w500/{poster_path}'
                self.posters.append(poster)
            else:
                self.posters.append("Server Error")
            
    def get_movies_with_posters(self):
        self.get_top_movies_by_genre()
        return list(zip(self.top_movies, self.posters))

class History:
    def __init__(self, mov_watched:dict) -> None:
        self.mov_watched = mov_watched  # {"Action" : 2, ...
        self.num_mov_to_generate = 9
        self.genres = mov_watched.keys()
        self.watch_time = mov_watched.values()

        self.statistics = {
            'Step 1': [],
            'Step 2': [],
            'Step 3': []
        }

        self.recomendation_info = {}
        self.generate_recomendation_info()

    def generate_recomendation_info(self) -> dict:
        total_mov = sum(self.mov_watched.values())
        result = {}

        mov_left = self.num_mov_to_generate
        highest_watched = ["", 0]
        for genre, num_watched in self.mov_watched.items():
            num = num_watched / total_mov
            rounded_num = round(num, 2)
            self.statistics["Step 1"].append(rounded_num)

            if rounded_num <= 0.12:
                x = 0
            else:
                x = int(round(num, 2) * self.num_mov_to_generate)
            result[genre] = x
            self.statistics["Step 2"].append(x)
            
            if num >= highest_watched[1]: 
                highest_watched[0] = genre
                highest_watched[1] = num
            mov_left -= x

        if mov_left > 0:
            result[highest_watched[0]] += mov_left
        
        self.recomendation_info = result

    def get_graph(self) -> None:
        _, ax = plt.subplots()

        bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']
        ax.bar(self.genres, self.watch_time, label = self.genres, color = bar_colors)
        ax.set_ylabel('NO. of movies watched')
        ax.set_title(f'User Watch history as ({datetime.datetime.now()})')
        ax.legend(title='Genre')

        plt.show() 

    def get_statistics(self):
        if len(self.mov_watched) > 0:
            
            self.statistics["Step 3"] = [x for x in self.recomendation_info.values()]
            category_names = self.mov_watched

            labels = list(self.statistics.keys())
            data = np.array(list(self.statistics.values()))
            data_cum = data.cumsum(axis=1)
            category_colors = plt.colormaps['RdYlGn'](
                np.linspace(0.15, 0.85, data.shape[1]))

            _, ax = plt.subplots()
            ax.invert_yaxis()
            ax.xaxis.set_visible(False)
            ax.set_xlim(0, np.sum(data, axis=1).max())

            for i, (colname, color) in enumerate(zip(category_names, category_colors)):
                widths = data[:, i]
                starts = data_cum[:, i] - widths
                rects = ax.barh(labels, widths, left=starts, height=0.7,
                                label=colname, color=color)

                r, g, b, _ = color
                text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
                ax.bar_label(rects, label_type='center', color=text_color)

            ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
                    loc='lower left', fontsize='small')

            plt.show()

    def get_num_of_recommended_movies(self):
        return self.recomendation_info