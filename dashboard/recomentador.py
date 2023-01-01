from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from genero.models import Genero, Categoria
from livros.models import Ebook, Review
from nltk.corpus import stopwords
from author.models import Author
import pandas as pd
import json




ebooks = Ebook.objects.all()
reviews = Review.objects.all()

X = []
Y = []


for ebook in ebooks:
    X = [ ebook.id, ebook.Title, ebook.Descricao, ebook.Publish, ebook.Genero,
          ebook.Paginas, ebook.Average_Rating, ebook.Average_Count,
          ebook.Votes_Count, ebook.Likes
          ]
    Y += [X]
    ebook_data = pd.DataFrame(Y, columns=['id', 'title','descricao','publish',
                                          'genero', 'paginas','average_rating',
                                          'average_count','votes_count','likes',
                                          ])
    for genero in ebook.Genero.all():
        ebook_data['genero']= genero
    ebook_data['average_rating'] = ebook_data['average_rating'].astype(float, errors = 'raise')
    ebook_data['average_count']= ebook_data['average_count'].astype(float, errors = 'raise')




    
#Define um Objeto Vetorizador TF-IDF. Remova todas as palavras irrelevantes em inglês
tf_vectorizer = TfidfVectorizer(stop_words=stopwords.words('portuguese'), analyzer='word', ngram_range=(1, 1), lowercase=True, use_idf=True)

#Substitui NaN por uma string vazia
ebook_data['descricao'] = ebook_data['descricao'].fillna('')

#Construa a matriz TF-IDF necessária aplicando o método fit_transform no recurso de visão geral
matrix = tf_vectorizer.fit_transform(ebook_data['descricao'])

#Exibe a forma de tfidf_matrix
#print(matrix.shape)

#calculando a matriz de similaridade de cosseno
cosine_sim = linear_kernel( matrix, matrix)


#Construa um mapeamento reverso de índices e títulos de filmes e descarte títulos duplicados, se houver

indices = pd.Series(ebook_data.index, index = ebook_data['title']).drop_duplicates()



#Sistema de recomendação Baseado em conteúdo
def content_recommender(title, cosine_sim = cosine_sim, ebook_data=ebook_data , indices=indices, ebooks = ebooks):

    recommender = []



    # Obtenha o índice do livro que corresponde ao título
    try:
        id_livro = indices[title].astype(str, errors = 'raise')
    except:
        try:
            id_livro = indices[str(title)]
        except:
            id_livro = indices[title]

   
    
    #Obtenha as pontuações de semelhança de pares de todos os filmes com esse filme.
    #E converta em uma lista de tuplas conforme descrito acima
    sim_scores = list(enumerate(cosine_sim[id_livro]))

    #Classificação dos livros com base nas pontuações de similaridade de cosseno.
    sim_scores = sim_scores[1:13]

    #Obtenha a pontuação dos 10 livros mais semelhantes e Ignore o primeiro livro
    livro_indices = [i[0] for i in sim_scores]
    

    #Retorne os 10 livros mais semelhantes
    for ebook in ebook_data['title'].iloc[livro_indices]:        
        if ebooks.filter(Title = ebook).exists():
            for livro in ebooks.filter(Title = ebook):                
                recommender.append({

                    'id':livro.id, 'Title':livro.Title,'Poster':livro.Poster,'Average_Rating':livro.Average_Rating,
                    'Average_Count':livro.Average_Count,


                    })

    return recommender
                                           




#Sitema de recomendação IMDB top 20

def recommender_20():

    top_20 = []

    m = ebook_data['votes_count'].quantile(0.80)
    ebook_data['average_rating'] = ebook_data['average_rating'].astype(float, errors = 'raise')
    ebook_data['average_count'] = ebook_data['average_count'].astype(float, errors = 'raise')

    #Considere apenas livros com pontuação mais 7 e menos que 9
    q_m = ebook_data[(ebook_data['average_rating'] >= 7) & (ebook_data['average_rating']<= 9)]


    #Considere apenas livros que obtiveram mais de m votos
    q_m = q_m[q_m['votes_count'] >= m]


    C = ebook_data['average_count'].mean()



    # Função para calcular a classificação ponderada do IMDB para cada filme.
    def classificacao_ponderada(x, m = m, C = C):
        V = x['votes_count']
        R = x['average_count']
        # Calcula a pontuação ponderada
        return (V/(V + m )* R) + (m/(m + V) * C)




    # Calcula a pontuação usando a função  definida acima.
    q_m['score'] = q_m.apply(classificacao_ponderada, axis = 1)

    for livro_id in q_m['id']:
        if ebooks.filter(id = livro_id).exists():
            for livro in ebooks.filter(id = livro_id):
                top_20.append({

                    'id':livro.id, 'Title':livro.Title,'Poster':livro.Poster,'Average_Rating':livro.Average_Rating,
                    'Average_Count':livro.Average_Count,


                    })

    return top_20





