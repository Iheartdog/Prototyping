"""
Movie Rating System V2.py
Author: Rachel Given
Date Created: 28/08/2019
Last Edited: 12/09/2019
Make a system where a user can be recommended movies based on movie ratings 
"""
from tkinter import *

class GUI:
    """
    This is the class containing the GUI
    """
    def __init__(self, __parent, *args):

        # Main Frame
        self.main_frame = Frame(__parent)
        self.main_frame.grid(row=0, column=0)
        title = Label(self.main_frame, text="Movie Recommendation System",
                      font = ("fixedsys", "14"))
        title.grid(row=0, column=0, columnspan=2, pady=5)
    
        # Makes list of movies not rated by Current User
        self.movie_titles = {}
        for movie in movies:
            self.movie_titles.update({movie.title:movie.id})
            
        # Option Menu        
        self.movie_var = StringVar()
        self.movie_id = StringVar()
        self.movie_var.set("Choose a Movie to Rate")
        movie_options = OptionMenu(self.main_frame, self.movie_var, *self.movie_titles.keys(),
                                   command = self.movie_id_func)
        movie_options.grid(row=1, column=0,columnspan=2, pady=5)

        # Rating Buttons
        like_button = Button(self.main_frame, text="Like", command = lambda: self.add_rating("5", self.movie_id.get()))
        like_button.grid(row=2, column=0, sticky=E+W)
        dislike_button = Button(self.main_frame, text="Dislike", command = lambda: self.add_rating("3", self.movie_id.get()))
        dislike_button.grid(row=2, column=1, stick=E+W)

        # Recommendations
        recommendation_title = Label(self.main_frame, text="Recommended Movies:",
                                     font=("Arial", "11", "bold"))
        recommendation_title.grid(row=3,column=0, columnspan=2, pady=5)
        
    def movie_id_func(self, *args):
        self.movie_id.set(self.movie_titles.get(self.movie_var.get()))

    def add_rating(self, rating, movie):
        """
        Adds movie rated by user to data base
        """
        #Adds users rating to CSV
        import csv
        with open('Ratings.csv', mode='a', encoding='utf-8', newline='') as rating_file:
            rating_writer = csv.writer(rating_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            rating_writer.writerow(['0',movie,rating])

        rating_file.close()

        self.generate_movie()

    def generate_movie(self):
        """
        Generates recommendations and instanciates all new data
        """
        import_ratings(LIKED_RATING)
        
        #Find all the users who have rated the movies watched by current user
        similar_users = find_similar_users(CURRENT_USER)
        
        # Generate recommended movies
        recommendations = generate_recommendations(CURRENT_USER, num_of_recommendations, similar_users)

        movie_labels = []
        movie = StringVar()
        
        del movie_labels[:]
        # Makes labels of recommendations
        for i in range(len(recommendations)):
            movie.set(recommendations[i])
            print(movie.get())
            movie_labels.append(Label(self.main_frame, textvariable= movie.get(),
                                      font=("Arial", "10")))                    
            movie_labels[i].grid(row=(i+4), column=0, columnspan=2, sticky=W)
            self.main_frame.update()
            i+=1
            

"""*** Recommendation Engine ***"""

class Movies:
    """
    This is a class for movies
    """
    def __init__(self, id, title, year, genres):
        """
        The constructor for Movies

        Parameters:
            id (int): ID for a movie
            title (str): Name of movie
            year (int): Year movie was released
            genres (list): Movies genres
        """
        self.id = id
        self.title = title
        self.year = year
        self.genres = genres
        movies.append(self)

class Ratings:
    """
    This is a class for ratings
    """
    def __init__(self, user_id, movie_id, rating):
        """
        The constructor for Ratings

        Parameters:
            user_id (str): User identification number
            movie_id (str): Movie identification number
            rating (str): Ratings given to a movie by the user
        """
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating
        ratings.append(self)

class User:
    """
    This is a class holds the user id and
    all the movies they've liked and disliked
    """
    def __init__(self, id):
        self.id = id
        self.liked = set()
        self.disliked = set()
        users.append(self)
        
    def add_liked(self, movie_id):
        self.liked.add(movie_id)

    def return_liked(self):
        return self.liked

    def add_disliked(self, movie_id):
        self.disliked.add(movie_id)

    def return_disliked(self):
        return self.disliked

def import_movies():
    """
    Load movie csv files to movies class
    """
    import csv
    with open('Movies.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        
        for row in csv_reader:
            if line_count == 0: #Header row
                line_count += 1
            else:
                line_count += 1
                
                Movies(row[0], row[1], row[2], row[3])

    csv_file.close()

def import_ratings(LIKED_RATING):
    """
    Load ratings csv files to ratings and user classes
    """
    import csv
    with open('Ratings.csv', mode = 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        
        for row in csv_reader:
            if line_count == 0: #Header row
                line_count += 1
            else:
                line_count += 1
                Ratings(row[0], row[1], row[2])

                # Sorts users and their liked/disliked movies into sets
                user_id = row[0]
                exists = False
                
                for user in users:
                    if user.id == user_id:
                        exists = True
                        # Adds movies to liked or disliked for already present user
                        if int(row[2]) >= LIKED_RATING:
                            user.add_liked(row[1])
                        else:
                            user.add_disliked(row[1])

                if not exists:
                    user = User(row[0])
                    # Adds movies to liked or disliked for new user
                    if int(row[2]) >= LIKED_RATING:
                        user.add_liked(row[1])
                    else:
                        user.add_disliked(row[1])

    csv_file.close()

def set_current_user(user_id):
    """
    Assign the current user to an instance
    """
    # Set the current user to do recommendations for
    CURRENT_USER = "" # Var to store instances of current user
    for user in users:
        if user.id == user_id:
            CURRENT_USER = user

    return CURRENT_USER

""" *** FINDING SIMILAR USERS *** """

def user_movies(user):
    """
    Return the liked and disliked movie sets for user
    """
    #Makes a set of all movies the user has rated
    movies = (user.return_liked() | user.return_disliked())
    return movies

def return_users_liked(movie):
    """
    Return the set of all the users who like a movie
    """
    # Create set if users liked movies
    users_liked = set()
    # Finds all users which like a movie
    for user in users:
        if movie in user.return_liked():
            users_liked.add(user)

    return users_liked

def return_users_disliked(movie):
    """
    Return the set of all the users who disliked a movie
    """
    # Create set if users dislike movies
    users_disliked = set()
    # Finds all users which dislike a movie
    for user in users:
        if movie in user.return_disliked():
            users_disliked.add(user)

    return users_disliked

def return_unrated(CURRENT_USER):
    """
    Returns a list of unrated movies
    """
    # Create a lsit to store unrated movies
    unrated_movies_titles = []
    
    for movie in movies:
        if movie.id not in user_movies(CURRENT_USER):
            unrated_movies_titles.append(movie.title)

    return unrated_movies_titles

def find_similar_users(CURRENT_USER):
    """
    Given a user, compute a list of other users who are similar
    Store the list in a database (in this case a dictionary), along with their
    similarity indicies
    Return the list of similar user in order of most to least similar
    """
    similar_users_set = set()
    similar_user_list = []
    similar_users_dict = {}

    # Create similar user set with all users who have rated a certain movie
    rated_movies = user_movies(CURRENT_USER)
    for movie in rated_movies:
        similar_users_set.update(return_users_liked(movie)|return_users_liked(movie))

    for user in similar_users_set:
        if user.id != CURRENT_USER.id:
            similarity_value = similarity_index(CURRENT_USER, user)
            similar_users_dict.update({user:similarity_value})

    # Transfer the dictionary into an ordered list of users most similar to least
    for user, value in sorted(similar_users_dict.items(), key=lambda x:x[1], reverse=True):
        similar_user_list.append(user)

    return similar_user_list

def similarity_index(CURRENT_USER, user):
    """
    Return the similarity index of two users  
    """
    # Calculates value between 1.0 and -1.0 shows the similarity of users movie taste
    similarity_value = ((len(CURRENT_USER.return_liked() & user.return_liked()))
    + (len(CURRENT_USER.return_disliked() & user.return_disliked()))
    - (len(CURRENT_USER.return_liked() & user.return_disliked()))
    - (len(CURRENT_USER.return_disliked() & user.return_liked()))
    ) / (
    len(CURRENT_USER.return_liked() | user.return_liked() | 
    CURRENT_USER.return_disliked() | user.return_disliked()))

    return similarity_value

def possibility_index_func(CURRENT_USER, movie):
    """
    Given a user and an unrated movie
    Find all users who have rated the movie
    Compare the similarity index and recommend a movie
    """

    # Finds the sum of the similarity indicies of all users who like a movie
    similarity_sum_liked = 0
    for user in return_users_liked(movie):
        if user.id != CURRENT_USER.id:
            similarity_sum_liked += similarity_index(CURRENT_USER, user)

    # Finds the sum of the similarity indicies of all users who dislike a movie
    similarity_sum_disliked = 0
    for user in return_users_disliked(movie):
        if user.id != CURRENT_USER.id:
            similarity_sum_disliked += similarity_index(CURRENT_USER, user)

    #Caluculate and return the possibility of the user liking a movie
    possibility_index = ((similarity_sum_liked - similarity_sum_disliked)/(
                        len(return_users_liked(movie)) + len(return_users_disliked(movie))))

    return possibility_index

""" *** GENERATING RECOMMENDATIONS *** """

def return_similar_unrated(CURRENT_USER, similar_users):
    """
    Returns a list of unrated movies
    """
    # Create a lsit to store unrated movies
    similar_unrated_movies_ids = []
    for user in similar_users:
        movies = user_movies(user)-user_movies(CURRENT_USER)
        for movie in movies:
            if movie not in similar_unrated_movies_ids:
                similar_unrated_movies_ids.append(movie)
    
    return similar_unrated_movies_ids

def unrated_movie_possibilities(CURRENT_USER, similar_users):
    """
    Store all items the user has not rated with possibility index
    and return dictionary
    """
    # Compute possibilities of a user liking a movie
    recommended_movies = {}

    for unrated in return_similar_unrated(CURRENT_USER, similar_users):
        possibility_index = possibility_index_func(CURRENT_USER, unrated)
        recommended_movies.update({unrated : possibility_index})

    return recommended_movies

def generate_recommendations(CURRENT_USER, num_of_recommendations, similar_users):
    """
    Generate movie recommendations
    """
    # Get dictionary of unrated movies to be recommended
    recommended_movies = unrated_movie_possibilities(CURRENT_USER, similar_users)

    movie_counter = 0
    recommended_movies_title = []
    
    print("**Recommended Movies**\n")
    for key,value in sorted(recommended_movies.items(), key=lambda x:x[1], reverse = True):
        if movie_counter <= num_of_recommendations:
            for movie in movies:
                if key == movie.id:
                    recommended_movies_title.append(movie.title)
                    movie_counter +=1

    return recommended_movies_title
        
if __name__ == "__main__":
    LIKED_RATING = 4 # Movies rated this score and above are liked
    movies = [] # List of all Movies
    ratings = [] # List of all Ratings
    users = [] # List of all Users

    # Import movie csv
    import_movies()

    # GUI
    root = Tk()
    root.title("Movie Rating System")
    root.geometry("+300+300")
    GUI(root)
    
    # Set the current user and number of recommendations
    current_user_id = "0"
    num_of_recommendations = 4

    # Store current user instance
    User(current_user_id)
    CURRENT_USER = set_current_user(current_user_id)
    

    


            
