from tmdbv3api import TMDb
from django.shortcuts import render


tmdb = TMDb()
tmdb.api_key = 'a44fb00a7a5378a01021a69f28e57cae'


tmdb.language = 'pt'
tmdb.debug = True

from tmdbv3api import Movie

movie = Movie()



def movies_search_management(request):

    query  = request.GET.get('search', None)   
    if query :        
        movie_data =  movie.search(query)
        return render(request,'movies/search.html', {'query':query,'movie_data':movie_data})

    return render(request, 'movies/search.html')
 
