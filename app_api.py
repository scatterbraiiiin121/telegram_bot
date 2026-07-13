import requests

def get_movies_by_id(movie_id):
    URL= f'https://moviesapi.ir/api/v1/movies/{movie_id}'

    response= requests.get(URL)

    if response.status_code != 200:
        return 'ERROR'
    else:
        response= response.json()
        title= response['title']
        year= response['year']
        genres= response['genres']
        imdb_rating= response['imdb_rating']
        return title, year, genres, imdb_rating
    
def get_movie_by_name(movie_name):
    url= 'https://moviesapi.ir/api/v1/movies'
    my_dict= {'q': movie_name}
    response= requests.get(url, params=my_dict)

    if response.status_code !=200:
        return 'Error'
    else:
        response = response.json()
        response= response['data'][0]
        title= response['title']
        year= response['year']
        genres= response['genres']
        imdb_rating= response['imdb_rating']
        return title, year, genres, imdb_rating


if __name__== '__main__':
    id_movie= int(input('enter id:'))
    result= get_movies_by_id(id_movie)
    print(f'result: {result}')

    name_movie= input('enter name:')
    result2= get_movie_by_name(name_movie)
    print(f'result: {result2}')

