import requests
import mysql.connector
import pandas as pd

movies = []
column_names = ["Original_title", "Release_date", "Original_language", "Popularity", "Poster_path"]
file_path = r"C:\Users\HP\OneDrive\Desktop\sqlconn\movie_data.csv"

def fetchdata(page_number):
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page_number}&sort_by=popularity.desc"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer **JhbGciOiJIUzI1NiJ9.*yJhdWQiOiJkZGI4YWQ3ZTk3N2MzOGI0ZmQwNjZkYjlmYzUxMTAyNCIsIm5iZiI6MTczMzI5OTAyNi45NDIwMDAyLCJzdWIiOiI2NzUwMGI1MjliZWU2NDY5YzE0NTcyOTIiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.l1dBHGeQRZA_ESyXoqWsbN_W13A19IlzmjvEmVrH1i*"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def insert_data(movie):
    conn = mysql.connector.connect(
        host="",
        user="",
        password= "",
        database=""
    )
    connecting = conn.cursor()
    if "results" in movie:
        for item in movie["results"]:
            original_title = item.get("original_title")
            release_date = item.get("release_date")
            original_language = item.get("original_language")
            popularity = item.get("popularity")
            poster_path = item.get("poster_path")
            connecting.execute(
                "INSERT INTO datapi_ (original_title, release_date, original_language, popularity, poster_path) VALUES (%s, %s, %s, %s, %s)",
                (original_title, release_date, original_language, popularity, poster_path)
            )
            movies.append({"Original_title": original_title, "Release_date": release_date, "Original_language": original_language, "Popularity": popularity, "Poster_path": poster_path})
    conn.commit()
    conn.close()
def fetch_moviedata(search_pattern):
    conn = mysql.connector.connect(
        host="",
        user="",
        password="",
        database=""
    )
    connecting = conn.cursor()
    query = "SELECT * FROM datapi_ WHERE original_title LIKE %s"
    connecting.execute(query, (search_pattern,))
    rows = connecting.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("Data not found!")
    conn.close()
choice = int(input("Enter what you want to do (1 to insert data, 2 to search): "))
if choice == 1:
    for page in range(1, 501): #loop to extract all pages
        movie = fetchdata(page)
        insert_data(movie)
    # Save to CSV after all data has been fetched and inserted
    df = pd.DataFrame(movies, columns=column_names)
    df.to_csv(file_path, index=False)
    print("DONE!")
elif choice == 2:
    search_option = '%' + input("Enter the name of your movie here: ") + '%'
    fetch_moviedata(search_option)
else:
    print("No valid parameter passed")