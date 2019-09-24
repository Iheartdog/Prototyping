"""
Movie Rating System V3.py
Author: Rachel Given
Date Created: 28/08/2019
Last Edited: 25/09/2019
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
        self.rate_frame = Frame(__parent)
        title = Label(self.main_frame, text="Movie Recommendation System",
                      font = ("fixedsys", "18"))
        title.grid(row=0, column=0, columnspan=6, pady=5)

        # Search Bar
        self.movie_var = StringVar()
        search_entry = Entry(self.main_frame, textvariable=self.movie_var)
        search_entry.grid(row=1, column=0,columnspan=5, pady=5, sticky=EW)
        search_label = Button(self.main_frame, text="Search", font=("Arial", "10"), command = lambda:self.find_movie(self.movie_var))
        search_label.grid(row = 1, column = 5, sticky = EW)
        
        # Movie not found message
        self.message = Label(self.main_frame, text = "Movie not found or already rated", font=("Arial", "9"), fg='red')

        # Rating Buttons
        like_button = Button(self.rate_frame, text="Like", command = lambda: self.add_rating("5", CURRENT_MOVIE.id),
                             width = 32)
        like_button.grid(row=2, column=0, columnspan=3)
        dislike_button = Button(self.rate_frame, text="Dislike", command = lambda: self.add_rating("3", CURRENT_MOVIE.id),
                                width = 32)
        dislike_button.grid(row=2, column=3, columnspan=3)

        # Recommendations labels
        recommendation_title = Label(self.rate_frame, text="Recommended Movies:",
                                     font=("Arial", "11", "bold"))
        recommendation_title.grid(row=3,column=0, columnspan=6, pady=5)

        reco_movie_title = Label(self.rate_frame, text="Movie Title:",
                                 font=("Arial", "10", "bold"))
        reco_movie_title.grid(row=4, column=0, columnspan=3, pady=3)

        reco_movie_title = Label(self.rate_frame, text="Genres:",
                                 font=("Arial", "10", "bold"))
        reco_movie_title.grid(row=4, column=3, columnspan=3, pady=3)

        self.top_movies = Label(self.rate_frame, text="Shawshank Redemption, The \nRobots \nCars \nIsle of Dogs \nHarry Potter and the Philosopher's Stone",
                           font=("Arial", "10"))
        self.top_movies.grid(row=5, column=0, columnspan=3, sticky=EW)

    def find_movie(self, movie_title, *args):
        """
        Finds the movie from search entry
        """
        # Makes list of possible movie the user wanted
        self.possible_entry = []
        self.possible_entry_titles = []
        
        for movie in return_unrated(CURRENT_USER):
            if (movie_title.get()).lower() in (movie.title).lower():
                self.possible_entry.append(movie)
                self.possible_entry_titles.append(movie.title)
        
        if len(self.possible_entry) == 1:
            set_current_movie(self.possible_entry[0])
            self.display_movie(CURRENT_MOVIE)
                      
        elif len(self.possible_entry) == 0:
            self.message.grid(row=2, column=0, columnspan=6, sticky=EW)

        else:
            self.movie_selected = StringVar()
            self.movie_options = OptionMenu(self.main_frame, self.movie_selected, *self.possible_entry_titles,
                                            command = lambda x: self.current_movie_func(self.movie_selected.get()))
            self.movie_submit = Button(self.main_frame, text="Submit",
                                       command = lambda: self.display_movie(CURRENT_MOVIE))
            self.movie_options.grid(row=2, column=0, columnspan=5, sticky=EW)
            self.movie_submit.grid(row=2, column=5)

    def current_movie_func(self, movie_var):
        """
        Sets movie id variable
        """
        global CURRENT_MOVIE
        for movie in movies:
            if movie_var == movie.title:
                CURRENT_MOVIE = movie
                 
    def display_movie(self, CURRENT_MOVIE):
        """
        Displays chosen movie and genres
        """
        try:
            self.message.grid_forget()
            self.movie_options.grid_forget()
            self.movie_submit.grid_forget()

        except:
            pass

        # Label Variables
        movie_title_var = StringVar()
        movie_title_var.set(CURRENT_MOVIE.title)
        movie_genre_var = StringVar()
        movie_genre_var.set(CURRENT_MOVIE.genres)

        # Labels of movie titles and genres
        title_label = Label(self.rate_frame, text = "Movie Title:", font=("Arial","10", "bold"))
        title_label.grid(row=0, column=0,columnspan=3, sticky=EW, pady = 5 )
        movie_title_label = Label(self.rate_frame, textvariable = movie_title_var, font=("Arial","10"))
        movie_title_label.grid(row=0, column=3, columnspan=3,sticky=EW)
        genre_label = Label(self.rate_frame, text = "Genres:", font=("Arial","10", "bold"))
        genre_label.grid(row=1, column=0, columnspan=3, sticky=EW, pady = 5)
        movie_genre_label = Label(self.rate_frame, textvariable = movie_genre_var, font=("Arial","10"))
        movie_genre_label.grid(row=1, column=3, columnspan=3,sticky=EW)

        self.rate_frame.grid(row=1,column=0)

    def add_rating(self, rating, movie_id):
        """
        Adds movie rated by user to data base
        """
        exists = False
            
        # Checks user has selected movie or it has already been rated
        for movie in user_movies(CURRENT_USER):
            if movie_id == movie:
                exists = True
                    
        if int(movie_id) > 0 and exists == False:
            #Adds users rating to CSV
            import csv
            with open('Ratings.csv', mode='a', encoding='utf-8', newline='') as rating_file:
                rating_writer = csv.writer(rating_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                rating_writer.writerow(['0',movie_id,rating])

            rating_file.close()

            self.generate_movie(movie_id, rating)
       
    def generate_movie(self, movie, rating):
        """
        Generates recommendations and instanciates all new data
        """
        import_ratings(LIKED_RATING)
        
        #Find all the users who have rated the movies watched by current user
        similar_users = find_similar_users(CURRENT_USER)
        
        # Generate recommended movies
        recommendations, genres = generate_recommendations(CURRENT_USER, num_of_recommendations, similar_users, movie, rating)
        
        movie_labels = []
        genre_labels = []
        
        self.top_movies.grid_forget()
        
        movie = StringVar()
        genre = StringVar()
        
        del movie_labels[:]
        del genre_labels[:]
        
        # Makes labels of movie recommendations
        i = 0
        for i in range(len(recommendations)):
            movie.set(recommendations[i])
            movie_labels.append(Label(self.rate_frame, text=movie.get(),
                                      font=("Arial", "10")))                    
            movie_labels[i].grid(row=(i+5), column=0, columnspan=3, sticky=EW)
            self.main_frame.update()
            i+=1

        i = 0
        # Makes labels of movie genres
        for i in range(len(genres)):
            genre.set(genres[i])
            genre_labels.append(Label(self.rate_frame, text=genre.get(),
                                      font=("Arial", "10")))                    
            genre_labels[i].grid(row=(i+5), column=3, columnspan=3, sticky=EW, padx=3)
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

def set_current_movie(movie):
    """
    Sets CURRENT_MOVIE
    """
    global CURRENT_MOVIE
    CURRENT_MOVIE = movie

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
    unrated_movies = [] #_titles = []
    
    for movie in movies:
        if movie.id not in user_movies(CURRENT_USER):
            unrated_movies.append(movie)#.title)

    return unrated_movies #_titles

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

def genre_recommendations(sorted_movies, rated_movie, movie_rating):

    recommended_movie_object = []
    rated_movie_object = None
    genre_score_dict = {}

    # Gets object of each movie
    for key,value in sorted_movies:
        for movie in movies:
            if movie.id == rated_movie:
                rated_movie_object = movie
            elif key == movie.id:
                recommended_movie_object.append(movie)

    # Compares genre of recommended movies and creates a genre score and stores in dictionary
    for movie in recommended_movie_object:
        movie_genre_score = 0
        for genre in movie.genres:
            for rated_genre in rated_movie_object.genres:
                if movie_rating == "5":
                    if rated_genre == genre:
                        movie_genre_score += 1

        movie_genre_score = movie_genre_score/(len(movie.genres))
        genre_score_dict.update({movie : (movie_genre_score/10)})

    return genre_score_dict
                         
def generate_recommendations(CURRENT_USER, num_of_recommendations, similar_users, rated_movie, movie_rating):
    """
    Generate movie recommendations
    """
    # Get dictionary of unrated movies to be recommended
    recommended_movies = unrated_movie_possibilities(CURRENT_USER, similar_users)

    movie_counter = 0
    recommended_movies_title = []
    recommended_movies_genres = []
    new_recommended_movies = {}

    genre_recommended_movies = genre_recommendations(recommended_movies.items(), rated_movie, movie_rating)

    # Changes dictionary key to title
    for key,value in recommended_movies.items():
        for movie in movies:
            if key == movie.id:
                recommended_movies.update({movie.title:value})
                del recommended_movies[key]

    # Adds possibility index and genre score together
    for movie_title, prob_index in recommended_movies.items():
        for genre_title, genre_score in genre_recommended_movies.items():
            new_value = 0
            if movie_title == genre_title.title:
                new_value = prob_index + genre_score
                new_recommended_movies.update({movie_title:new_value})

    #Sorts new dictionary and chooses top 5 recommendedations
    for key,value in sorted(new_recommended_movies.items(), key=lambda x:x[1], reverse = True):
        if movie_counter <= num_of_recommendations:
            recommended_movies_title.append(key)
            #print(value)
            movie_counter +=1
            for genre_object in genre_recommended_movies.keys():
                if genre_object.title == key:
                    recommended_movies_genres.append(genre_object.genres)
            

    return recommended_movies_title, recommended_movies_genres
        
if __name__ == "__main__":
    LIKED_RATING = 4 # Movies rated this score and above are liked
    movies = [] # List of all Movies
    ratings = [] # List of all Ratings
    users = [] # List of all Users

    #Store current movie selected
    CURRENT_MOVIE = None
    
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

    
    

    


            
