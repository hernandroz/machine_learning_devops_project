# main.py

# Importamos FastAPI
from fastapi import FastAPI

# Creamos la variable "app" que será una instancia de la clase "FastAPI"
app = FastAPI()

# Creamos nuestro primer endpoint que se tratará del clásico "Hola mundo":

# Primero, usamos un decorador creado con el objeto "app" y el tipo de petición "get"
# Además, estableceremos como parámetro la ruta del endpoint que será el index
@app.get("/")
# Definimos una función, la cual podremos nombrarla como queramos

def root():
    # Por último, retornamos la respuesta de nuestra API
    return {"Aviso": "Saludos. Ir a /docs para acceder a los endpoints de la API"}
    # FastAPI se encargará de convertir el retorno en un string con formato JSON

# Importamos pandas
import pandas as pd

# Cargamos el dataset
df = pd.read_csv("movies_dataset_limpio.csv")


@app.get("/peliculas_idioma/")
def cantidad_de_peliculas_por_idioma( Idioma: str ): 
    # Se ingresa un idioma. Debe devolver la cantidad de películas producidas en ese idioma.
    # Ejemplo de retorno: X cantidad de películas fueron estrenadas en idioma
    contador = 0
    
    for lista in df['spoken_languages_names']:
        if Idioma in lista:
            contador = contador +1

    return {"Cantidad de películas estrenadas en ese idioma": contador}

@app.get("/peliculas_duracion/")
def duracion_de_pelicula( Pelicula: str ): 
    # Se ingresa una pelicula. Debe devolver la la duracion y el año.
    # Ejemplo de retorno: X . Duración: x. Año: xx
    s = df.loc[df.title == Pelicula]
    duracion = s['runtime'].to_list()[0]
    anio = s['release_year'].to_list()[0]

    return {"Duración (en minutos) de la película": duracion, "Año de lanzamiento de la película": anio}

@app.get("/franquicia_datos/")
def datos_de_franquicia( Franquicia: str ): 
    # Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio
    # Ejemplo de retorno: La franquicia X posee X peliculas, una ganancia total de x y una ganancia promedio de xx
    s = df.loc[df.collection_name == Franquicia]
    
    # Cantidad de películas de la franquicia
    peliculas = s.shape[0]

    # Ganancia total
    ganancia_total = s['return'].sum()

    # Ganancia promedio
    ganancia_promedio = s['return'].mean()

    return {'Cantidad de películas de la franquicia': peliculas, 'Ganancia total': ganancia_total, 'Ganancia promedio': ganancia_promedio}


@app.get("/peliculas_pais/")
def cantidad_de_peliculas_por_pais( Pais: str ): 
    # Se ingresa un país, retornando la cantidad de peliculas producidas en el mismo.
    # Ejemplo de retorno: Se produjeron X películas en el país X
    contador = 0
    for lista in df['production_countries_names']:
        if Pais in lista:
            contador = contador +1
    return {'Cantidad de películas producidas en el país': contador}

@app.get("/productoras_exitosas")
def exito_de_productora( Productora: str ): 
    
    # Se ingresa la productora, entregando el revenue total y la cantidad de peliculas que realizó
    # Ejemplo de retorno: La productora X ha tenido un revenue de x


    # Creamos un dataframe en el que el nombre de la compañía es el que estamos buscando:
    
    # Para ello, primero creamos un dataframe vacío:
    s = pd.DataFrame()
    # Ubicamos los lugares en los que se encuentra el nombre de la compañía que buscamos
    for lista in df['production_companies_names']:
        if Productora in lista:
            e = df.loc[df.production_companies_names == lista]
            s = pd.concat([s,e], ignore_index=True)
            # Mediante lo anterior, hemos establecido la creación del dataframe que buscábamos obtener
         
    # Eliminamos las filas repetidas que se crearon:
    s = s.drop_duplicates()
    # Restablecemos los índices:
    s = s.reset_index(drop=True)

    # Revenue total:
    revenue_total = s['revenue'].sum()

    # Cantidad total de películas producidas por la compañía:
    peliculas = s.shape[0]

    return {'Revenue total de la productora': revenue_total, 'Cantidad de películas realizadas': peliculas}


# Cargamos el dataset que es requerido para el último endpoint:
df2 = pd.read_csv('credits_limpio.csv')
# Dado que queremos hacer merge a los dataframes df1 y df2 con la columna en común "id",
# deberemos hacer que el tipo de dato de ambas columnas coincidan.
# Dado que el tipo de los datos de la columna 'id' de df1 ya es str, trabajaremos df2:
df2['id']=df2['id'].astype(str)
# Ahora sí hacemos merge respecto a la columna 'id':
df3 = pd.merge(df, df2, on='id', how='outer')



@app.get("/get_director/")
def exito_del_director( nombre_director: str ):

    # Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo 
    # devolver el éxito del mismo medido a través del retorno. Además, deberá devolver 
    # el nombre de cada película con la fecha de lanzamiento, retorno individual, costo 
    # y ganancia de la misma, en formato lista.

    import ast

    # Crearemos un dataframe en el que el nombre del director es el que estamos buscando:


    # Pero antes, se ha observado que los tipos de datos de la columna 'crew_names' son de tipo str y de 
    # tipo list, así que los convertiremos a str para evitar problemas con el método literal_eval
    df3['crew_names']=df3['crew_names'].astype(str)


    # Ahora crearemos un dataframe vacío:
    s = pd.DataFrame()
    # Ubicamos los lugares en los que se encuentra el nombre del director que buscamos:

    for lista in df3['crew_names']:
        if nombre_director in lista:
        
            e = df3.loc[df3.crew_names == str(lista)]
            s = pd.concat([s,e], ignore_index=True)
            # Mediante lo anterior, hemos establecido la creación del dataframe que buscábamos obtener
         
    # Eliminamos las filas repetidas que se crearon:
    s = s.drop_duplicates()
    # Restablecemos los índices:
    s = s.reset_index(drop=True)

    # Return total del director:
    return_director = s['return'].sum()

    # Nombre de cada película en el que el director trabajó:
    peliculas_director = list(s['title'])

    # Fecha de estreno de cada película:
    estreno_peliculas = list(s['release_date'])

    # Return individual de cada película:
    return_peliculas = list(s['return'])

    # Costo de cada película:
    costo_peliculas = list(s['budget'])

    # Ganancia de cada película:
    ganancia_peliculas = list(s['revenue']-s['budget'])
    
    return {'Return total del director': return_director, 'Nombre de cada película': 
            peliculas_director, 'Fecha de lanzamiento': estreno_peliculas, 'Return individual':
            return_peliculas, 'Costo': costo_peliculas, 'Ganancias': ganancia_peliculas}
    


@app.get("/recomendacion/")
def recomendacion( titulo :str): 
    #Se ingresa el nombre de una película y te recomienda las similares en una lista de 5 valores.
    best_ones = df3.sort_values(by='vote_average', ascending=False).head(50)
    import random
    n = random.randrange(0, 45, 1)
    recomendacion = best_ones[n:n+5]
    lista_recomendacion = recomendacion['title'].to_list()
    return {'Películas recomendadas': lista_recomendacion}