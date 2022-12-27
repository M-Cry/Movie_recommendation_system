import csv
import cv2
import os
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

"""
    Machine learning Engine 
    By GUtech students
"""

class Db:
    def __init__(self) -> None:
        self.graph_name = "generated graphs"
        self.history_file = "user_history.txt"
        self.db_name = "movies.csv"

    def get_graph(self):
        try:
            cv2.imshow("Generated Graph", cv2.imread(self.graph_name))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except:
            self.graph.savefig(self.graph_name)
            self.graph.show()

    def history(self) -> dict:
        try:
            with open(self.history_file) as file:
                lines = file.readlines()
                return lines
        except FileNotFoundError:
            # No movies has been watched
            return None     
            
    def rmv_old_graph(self, src):
        try:
            os.rename(src, f"generated graphs/old_{datetime.datetime.now().timestamp()}.jpg")
        except:
            pass

class Collabrative(Db):
    def __init__(self) -> None:
        super().__init__()
        self.graph = None
        self.graph_name = "generated graphs/col_fig.jpg"

    def filter(self):
        """
            Collabrative filtering algorithm implementation
        """
        try:
            df = pd.read_csv('user_rating.csv', sep=',')

            ratings = pd.DataFrame(df.groupby('title')['user_rating'].mean())

            # get how many times a title has been rated
            ratings['number_of_ratings'] = df.groupby('title')['user_rating'].count()

            # plotting the joinplot to show the distribution of ratings and most ratring scores
            sns.jointplot(x = 'user_rating', y = 'number_of_ratings', data = ratings)
            self.graph = plt

            data_matrix = df.pivot_table(index='user_id', columns='title', values='user_rating')

            # most rated movies list
            ratings.sort_values('user_rating', ascending=False).head(10)

            np.seterr(divide='ignore', invalid='ignore')
            aliens_user_ratings = data_matrix['Aliens in the Attic']

            # find similar movies to (Aliens in the Attic) using correlation with other movies ratings
            similar_to_aliens = data_matrix.corrwith(aliens_user_ratings)

            # better display the recommendations
            corr_aliens = pd.DataFrame(similar_to_aliens, columns = ['Correlation'])
            corr_aliens.dropna(inplace=True)
            corr_aliens.sort_values('Correlation', ascending=False).head()

            # set up to refine the recommendations
            corr_aliens = corr_aliens.join(ratings['number_of_ratings'])
            recommendations = corr_aliens[corr_aliens['number_of_ratings'] > 3].sort_values(by='Correlation', ascending=False).head(9)

            # get recommendations info
            file = pd.read_csv(self.db_name, sep=",")
            movie_info = []

            # Get movie info from dataset via the movie title
            for movie_title in [movie_title[0] for movie_title in recommendations.iterrows()]:
                row = file[file.eq(movie_title)["title"]].to_string(header=False,index=True,index_names=False).split('\n')
                movie_info.append(int(row[0].split()[0]) +1)
                
            with open(self.db_name) as file:
                lines = file.readlines()
                for index, movie_pos in enumerate(movie_info):
                    movie_info[index] = lines[movie_pos].strip().split(",")
            
            self.rmv_old_graph(self.graph_name)
            return movie_info
            
        except Exception as e:
            print(str(e))
            return None

class ContentBased(Db):
    def __init__(self) -> None:
        super().__init__()

        self.num_mov_to_generate = 9
        self.elimination_threshold = 0.13
        self.graph = None
        self.graph_name = "generated graphs/cont.jpg"

        self.statistics = {
            'Step 1': [],
            'Step 2': [],
            'Step 3': []
        }
        self.recomendation_info = {}

    def filter(self) -> dict:
        self.total_genre_watched = {}
        try:
            with open(self.history_file) as file:
                movies = file.readlines()
                for movie in movies:
                    movie = movie.split(",")
                    if movie[1] in self.total_genre_watched:
                        self.total_genre_watched[movie[1]] += 1
                    else:
                        self.total_genre_watched[movie[1]] = 1
        except FileNotFoundError:
            return None

        total_mov = sum(self.total_genre_watched.values())
        result = {}

        mov_left = self.num_mov_to_generate
        highest_watched = ["", 0]
        for genre, num_watched in self.total_genre_watched.items():
            num = num_watched / total_mov
            rounded_num = round(num, 2)
            self.statistics["Step 1"].append(rounded_num)

            if rounded_num <= self.elimination_threshold:
                x = 0
            else:
                x = int(rounded_num * self.num_mov_to_generate)

            result[genre] = x
            self.statistics["Step 2"].append(x)
            
            if num >= highest_watched[1]: 
                highest_watched[0] = genre
                highest_watched[1] = num
            mov_left -= x

        if mov_left > 0:
            result[highest_watched[0]] += mov_left
        self.recomendation_info = result

        # Generate graph 
        with open("history_by_genre.csv", "w+") as file:
            writer = csv.writer(file, lineterminator="\n")
            writer.writerow(["Movie Genre","Total Watched"])
            writer.writerows(list(zip(self.total_genre_watched.keys(), self.total_genre_watched.values())))

        data = pd.read_csv("history_by_genre.csv", sep=",")
            
        sns.barplot(data=data, x="Movie Genre", y="Total Watched")
        self.graph = plt
        
        self.rmv_old_graph(self.graph_name)

        return self.recomendation_info

    def get_statistics(self) -> None:
        if len(self.total_genre_watched) > 0:
            
            self.statistics["Step 3"] = [x for x in self.recomendation_info.values()]
            category_names = self.total_genre_watched
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
        else:
            return None

class Movie(Db):
    def __init__(self) -> None:
        super().__init__()

        self.header = {}
        self.top_movies = []
        self.posts = pd.read_csv("movies_posters.csv")

    def get_top_movies_by_genre(self, genre, recomendation_num):
        rec_movies = []

        with open(self.db_name, encoding="utf-8") as data:
            header = dict(enumerate(data.readline().split(",")))    # {0: 'title', ...}
            header = {value:key for key, value in header.items()}   # {'title': 0, ...}
            self.header = header

            movies = csv.reader(data)
            rec_movies = [movie for movie in movies if genre in movie[self.header["genre"]]]

            # sorted => TimSort Algo. | O(n*log(n))
            # first 9 movies by slicing the list
            self.top_movies = sorted(rec_movies, key = lambda x: x[self.header["rating"]], reverse = True)[ : recomendation_num]

        return self.get_movies_with_posters(self.top_movies)

    def get_movies_with_posters(self, movies):
        """ Fetch movie post """
        posters = []
        for movie_data in movies:
            data = self.posts[self.posts['title'] == movie_data[0]]
            posters.append(data.values[0][1])

        return list(zip(movies, posters))

    def watch(self, movie_info):
        with open(self.history_file, "a") as file:
            file.write(movie_info + "\n")
        return movie_info.split(",")[:2]

    def get_history(self):
        return self.history()