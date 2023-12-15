import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2

# Connecting to our DataBase
db_host='localhost'
db_name='BdIMDb'
db_user='postgres'
db_password='*'
db_port='5432'
connection = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
cursor = connection.cursor()

cursor.execute("SELECT *  FROM IMDb0")

records = cursor.fetchall()

df = pd.DataFrame(records, columns=['Id','Title', 'Release year', 'Genre', 'Runtime(min)', 'Rating', 'Votes'])


while True:

    # 1: Top 5 Most Popular Genres
    def show_1():
        plt.style.use('dark_background')  # Set the plot style for a visually appealing dark background
        top_genre = df['Genre'].value_counts().head(5)  # Count the occurrences of each genre and select the top 5
        plt.figure(figsize=(12, 6))  # Set the figure size
        sns.barplot(data=top_genre, palette='winter')  # Create a bar plot using Seaborn
        plt.title('Top 5 Most Popular Genres')  # Set the title of the plot
        plt.xlabel('Genres')  # Set the Label for x-axis
        plt.ylabel('Amount')  # Set the Label for y-axis
        plt.show()  # Display the plot


    # 2: Top 5 Most Popular Genres By Votes
    def show_2():
        plt.style.use('dark_background')  # Set the plot style for a visually appealing dark background
        top_film = df.groupby('Genre')['Votes'].sum().reset_index()  # Group the DataFrame and calculate the sum of 'Votes'
        top_film1 = top_film.sort_values(by='Votes', ascending=False).head(5) # Sort the grouped data and select the top 5 genres
        plt.figure(figsize=(21,10))  # Set the figure size
        sns.barplot(x='Votes', y='Genre', data=top_film1, orient='h', palette='winter')  # Create a horizontal bar plot
        plt.title('Top 5 Most Popular Genres By Votes')  # Set the title of the plot
        plt.xlabel('Votes (x10mln)')  # Set the Label for x-axis
        plt.xlim(10000000, 27500000)  # Set the limits of the x-axis on a plot.
        plt.ylabel('Genre')  # Set the Label for y-axis
        plt.show()  # Display the plot


    # 3: Top 10 Movies By Rating
    def show_3():
        plt.style.use('dark_background')  # Set the plot style for a visually appealing dark background
        sort_film = df.sort_values(by='Rating', ascending=False)  # Sort the DataFrame in descending order
        top_films = sort_film[['Title', 'Rating']].head(10)  # Select the top 10 films with the highest ratings
        plt.figure(figsize=(17, 13))  # Set the figure size
        plt.scatter(top_films['Title'], top_films['Rating'], color='lime', marker='o', s=100)  # Create a scatter plot
        plt.title('Top 10 Movies by Rating')  # Set the title of the plot
        plt.xlabel('Movie Title')  # Set the Label for x-axis
        plt.ylabel('Rating')  # Set the Label for y-axis
        plt.xlim(0, 10)  # Set the limits of the x-axis on a plot.
        plt.grid(axis='x', linestyle='--', alpha=0.6)  # Add gridlines for the x-axis
        plt.xticks(rotation=20)  # Rotate x-axis labels for better readability
        plt.show()  # Display the plot


    # 4: Which Decade Released The Most Movies
    def show_4():
        plt.style.use('dark_background')  # Set the plot style for a visually appealing dark background
        df['Release year'] = pd.to_numeric(df['Release year'], errors='coerce')  # Convert the column in DF to numeric values
        year_intervals = [(1900,1909), (1910,1919), (1920,1929), (1930,1939), (1940,1949), (1950,1959), (1960,1969),
                          (1970,1979), (1980,1989), (1990,1999), (2000,2009), (2010,2019)]  # Define a list of year intervals
        interval_counts = {}  # Initialize an empty dictionary to store counts of movies within each year interval

        for interval in year_intervals:  # Iterate over each defined year interval and calculate the number of movies released
            start_year, end_year = interval
            filtered = df[(df['Release year'] >= start_year) & (df['Release year'] <= end_year)]
            movies_interval = len(filtered)
            interval_counts[f"{start_year}-{end_year}"] = movies_interval

        plt.figure(figsize=(15, 8))  # Set the figure size
        sns.barplot(data=interval_counts, palette='winter')  # Create a bar plot using Seaborn
        plt.title('Which Decade Released The Most Movies')  # Set the title of the plot
        plt.xlabel('Decade')  # Set the Label for x-axis
        plt.ylabel('Amount of Movies')  # Set the Label for y-axis
        plt.show()  # Display the plot


    # 5: Top Genres With The Longest Movies
    def show_5():
        plt.style.use('dark_background')  # Set the plot style for a visually appealing dark background
        longest_movies = df.groupby('Genre')['Runtime(min)'].mean().reset_index()  # Group DF and find the average runtime
        # Sort the grouped data by maximum runtime in descending order and select the top 15 genres
        longest_genre_movies = longest_movies.sort_values(by='Runtime(min)', ascending=False).head(15)
        plt.figure(figsize=(21,9))  # Set the figure size
        # Create a horizontal bar plot using Seaborn, representing the top 15 genres with the longest movies
        # X-axis represents the runtime, and y-axis represents the genres, using a winter color palette
        sns.barplot(x='Runtime(min)', y='Genre', data=longest_genre_movies, orient='h', palette='winter')
        plt.title('Top Genres With The Longest Movies')  # Set the title of the plot
        plt.xlabel('Average Movie Runtime (min)')  # Set the Label for x-axis
        plt.ylabel('Genre')  # Set the Label for y-axis
        plt.show()  # Display the plot


    # 6: Voting Tendency By Rating
    def show_6():
        plt.style.use('dark_background')  # Set the plot style for a visually appealing dark background
        plt.figure(figsize=(8,6))  # Set the figure size
        sns.histplot(df['Rating'], bins=20, kde=True, color='mediumspringgreen', edgecolor= 'lime')  # Create a histogram plot
        plt.title('Voting Tendency By Rating')  # Set the title of the plot
        plt.ylabel('Amount')  # Set the Label for y-axis
        plt.show()  # Display the plot


    # 7: Correlation Heatmap Between Movie Rating, Runtime, Release Year And Votes
    def show_7():
        plt.style.use('dark_background')  # Set the plot style for a visually appealing dark background
        correlation = df[['Rating', 'Runtime(min)', 'Votes', 'Release year']].corr()  # Create a correlation matrix
        plt.figure(figsize=(8,6))  # Set the figure size
        # Generate a heatmap using Seaborn to visually represent the correlation matrix
        # Include numerical annotations, use the 'winter' color map, and set linewidth between cells to 0.5
        sns.heatmap(correlation, annot=True, cmap='winter', linewidths=0.5)
        plt.title('Correlation Heatmap Between Movie Rating, Runtime, Release Year And Votes')  # Set the title of the plot
        plt.show()  # Display the plot


    # 8: Top Rated Genres By The Average Rating
    def show_8():
        filmai_pagal_žanrą = df.groupby('Genre')['Rating'].mean()  # Group Df and calculate the mean rating for each genre
        # Sort the mean ratings in descending order and select the top 10 genres
        sort_filmai_pagal_žanrą = filmai_pagal_žanrą.sort_values(ascending=False).head(10)
        plt.style.use('dark_background')  # Set the plot style for a visually appealing dark background
        plt.figure(figsize=(10,11))  # Set the figure size
        plots = sns.barplot(data=sort_filmai_pagal_žanrą, palette='winter')  # Create a bar plot using Seaborn
        # Iterate through each bar in the bar plot created using Seaborn
        for bar in plots.patches:
            # Annotate each bar with its height (formatted to two decimal places)
            # Position the annotation at the center of the bar's x-coordinate and its height
            # Set horizontal and vertical alignment to 'center', and font size to 15
            # Add a vertical offset of 8 points to improve the annotation's position
            plots.annotate(format(bar.get_height(), '.2f'),
                            (bar.get_x() + bar.get_width() / 2,
                            bar.get_height()), ha='center', va='center',
                            size=15, xytext=(0, 8),
                            textcoords='offset points')

        plt.xticks(rotation=20)  # Rotate x-axis labels by 20 degrees for better readability
        plt.ylim(8, 9)  # Set the limits of the y-axis on a plot.
        plt.title("Top Rated Genres By The Average Rating")  # Set the title of the plot
        plt.show()  # Display the plot

    # Creating a system that allows the user to choose which of the graphs should be displayed
    print("Select the graph that you want to be displayed:")
    print("1: Top 5 Most popular genres")
    print("2: Top 5 Most Popular Genres By Votes")
    print("3: Top 10 Movies By Rating")
    print("4: Which Decade Released The Most Movies")
    print("5: Top Genres With The Longest Movies")
    print("6: Voting Tendency By Rating")
    print("7: Correlation Heatmap Between Movie Rating, Runtime, Release Year and Votes")
    print("8: Top Rated Categories By The Average Rating")
    print("9: Exit program")
    print("Enter the number of your choice: \n")
    choice = input()

    # According to the users choice, we select the appropriate action
    if choice == '1':
        show_1()
    elif choice == '2':
        show_2()
    elif choice == '3':
        show_3()
    elif choice == '4':
        show_4()
    elif choice == '5':
        show_5()
    elif choice == '6':
        show_6()
    elif choice == '7':
        show_7()
    elif choice == '8':
        show_8()
    elif choice == '9':
        print('The program is closing. Goodbye')
        break
    else:
        print('Incorrect choice. Try again: \n')
