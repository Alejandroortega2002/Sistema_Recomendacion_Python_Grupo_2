import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class GestorPeliculas:
    """
    Clase para gestionar un sistema de películas. Proporciona funcionalidades para buscar,
    recomendar y registrar votaciones de películas.
    """

    # Constructor de la clase
    """
    Inicializa la clase, cargando los datos de las películas y usuarios desde archivos CSV.
    También calcula las similitudes entre películas basadas en sus sinopsis y características combinadas.

    Excepciones manejadas:
        - FileNotFoundError: Si los archivos CSV no existen.
        - Exception: Cualquier otro error durante la inicialización.
    """
    def __init__(self):
        try:
            # Definimos las rutas de los archivos
            self.file_path = 'peliculas_final_imagenes.csv'
            self.file_path_usuarios = 'usuarios.csv'

            # Cargamos los datos de las películas y usuarios
            self.peliculas_df = pd.read_csv(self.file_path)
            self.usuarios_df = pd.read_csv(self.file_path_usuarios)

            # Calculamos las similitudes al cargar los datos
            self._calcular_similitudes()
            self._calcular_similitudes_recomendaciones()
        except FileNotFoundError as e:
            # Si no encontramos el archivo, inicializamos con DataFrames vacíos
            print(f"Error: Archivo no encontrado. {e}")
            self.peliculas_df = pd.DataFrame()
            self.usuarios_df = pd.DataFrame()
        except Exception as e:
            # Manejo de otros errores inesperados
            print(f"Error inesperado durante la inicialización: {e}")
            self.peliculas_df = pd.DataFrame()
            self.usuarios_df = pd.DataFrame()

    # Método privado para calcular similitudes basadas en la sinopsis
    """
    Calcula las similitudes entre las películas utilizando la sinopsis como base.

    Notas:
        - Utiliza TF-IDF para convertir el texto en vectores.
        - Utiliza la similitud coseno para medir la similitud entre vectores.

    Excepciones manejadas:
        - Exception: Cualquier error al calcular las similitudes.
    """
    def _calcular_similitudes(self):
        try:
            # Verificamos si existe la columna de sinopsis
            if 'synopsis' not in self.peliculas_df.columns:
                print("Advertencia: No se encontró la columna 'synopsis'.")
                self.cosine_sim_synopsis = []
                return

            # Creamos un vectorizador TF-IDF con límites de frecuencia y número de características
            tfidf_vectorizer = TfidfVectorizer(
                stop_words='english',
                max_df=0.9,
                min_df=0.01,
                max_features=1000
            )
            
            # Rellenamos los valores nulos de sinopsis con cadenas vacías
            self.peliculas_df['synopsis'] = self.peliculas_df['synopsis'].fillna('')
            
            # Convertimos las sinopsis a una matriz TF-IDF
            tfidf_matrix = tfidf_vectorizer.fit_transform(self.peliculas_df['synopsis'])

            # Calculamos la matriz de similitud coseno entre las películas
            self.cosine_sim_synopsis = cosine_similarity(tfidf_matrix, tfidf_matrix)
        except Exception as e:
            # En caso de error, asignamos una lista vacía
            print(f"Error al calcular similitudes de sinopsis: {e}")
            self.cosine_sim_synopsis = []

    # Método privado para calcular similitudes usando características combinadas
    """
    Calcula similitudes entre películas utilizando las características combinadas
    de sinopsis, director y género.

    Notas:
        - Combina múltiples columnas para formar una representación textual única.
        - Utiliza TF-IDF y similitud coseno para medir la similitud.

    Excepciones manejadas:
        - Exception: Cualquier error al calcular las similitudes.
    """
    def _calcular_similitudes_recomendaciones(self):
        try:
            # Verificamos que las columnas necesarias existan, si no, las rellenamos con cadenas vacías
            for col in ['synopsis', 'director', 'genre']:
                if col not in self.peliculas_df.columns:
                    print(f"Advertencia: No se encontró la columna '{col}'.")
                    self.peliculas_df[col] = ''

            # Creamos una nueva columna combinando sinopsis, director y género
            self.peliculas_df['combined_features'] = self.peliculas_df['synopsis'].fillna('') + ' ' + \
                                                     self.peliculas_df['director'].fillna('') + ' ' + \
                                                     self.peliculas_df['genre'].fillna('')

            # Vectorizamos las características combinadas
            tfidf_vectorizer = TfidfVectorizer(
                stop_words='english',
                max_df=0.9,
                min_df=0.01,
                max_features=1000
            )
            tfidf_matrix = tfidf_vectorizer.fit_transform(self.peliculas_df['combined_features'])

            # Calculamos la matriz de similitud coseno
            self.cosine_sim_recomendaciones = cosine_similarity(tfidf_matrix, tfidf_matrix)
        except Exception as e:
            # En caso de error, asignamos una lista vacía
            print(f"Error al calcular similitudes combinadas: {e}")
            self.cosine_sim_recomendaciones = []

    # Método público para obtener una lista de películas
    """
    Devuelve una lista de películas con sus títulos e imágenes asociadas.

    Retorno:
        - List[dict]: Lista de diccionarios con las claves `title` y `poster_image_y`.

    Excepciones manejadas:
        - KeyError: Si las columnas requeridas no están disponibles.
    """
    def obtener_peliculas(self):
        try:
            return self.peliculas_df[['title', 'poster_image_y']].to_dict(orient='records')
        except KeyError as e:
            print(f"Error: Columnas necesarias no encontradas. {e}")
            return []

    # Método público para buscar películas por nombres exactos
    """
    Busca películas que coincidan exactamente con los nombres proporcionados.

    Parámetros:
        - nombres_peliculas (List[str]): Lista de nombres de películas a buscar.

    Retorno:
        - List[dict]: Lista de diccionarios con información de las películas encontradas.

    Excepciones manejadas:
        - KeyError: Si las columnas necesarias no están disponibles.
    """
    def buscar_peliculas(self, nombres_peliculas):
        try:
            # Filtramos el DataFrame usando los nombres proporcionados
            resultado = self.peliculas_df[self.peliculas_df['title'].isin(nombres_peliculas)]
            return resultado[['title', 'poster_image_y']].to_dict(orient='records') if not resultado.empty else []
        except KeyError as e:
            print(f"Error: Columnas necesarias no encontradas. {e}")
            return []

    # Método público para buscar películas por nombre parcial
    """
    Busca películas cuyos títulos contengan el texto proporcionado (búsqueda parcial).

    Parámetros:
        - nombre_pelicula (str): Texto parcial del título de la película.

    Retorno:
        - List[dict]: Lista de diccionarios con información de las películas encontradas.

    Excepciones manejadas:
        - Exception: Cualquier error durante la búsqueda.
    """
    def buscar_peliculas2(self, nombre_pelicula):
        try:
            if not nombre_pelicula:
                # Si no se proporciona un título, devolvemos una lista vacía
                return []
            # Buscamos películas cuyo título contenga el texto proporcionado
            resultado = self.peliculas_df[self.peliculas_df['title'].str.contains(nombre_pelicula, case=False, na=False)]
            return resultado[['title', 'poster_image_y']].to_dict(orient='records') if not resultado.empty else []
        except Exception as e:
            print(f"Error al buscar películas: {e}")
            return []

    # Método público para seleccionar películas al azar
    """
    Selecciona una cantidad especificada de películas de forma aleatoria.

    Parámetros:
        - cantidad (int): Número de películas a seleccionar.

    Retorno:
        - List[str]: Lista con los títulos de las películas seleccionadas.

    Excepciones manejadas:
        - ValueError: Si no hay suficientes películas para seleccionar.
    """
    def peliculas_al_azar(self, cantidad=12):
        try:
            # Seleccionamos películas de forma aleatoria
            return self.peliculas_df.sample(n=cantidad)['title'].tolist()
        except ValueError as e:
            # Si no hay suficientes películas, devolvemos una lista vacía
            print(f"Advertencia: No hay suficientes películas para seleccionar. {e}")
            return []

    # Método público para obtener detalles de una película específica
    """
    Devuelve los detalles de una película, dado su nombre parcial.

    Parámetros:
        - nombre_pelicula (str): Nombre (o parte del nombre) de la película.

    Retorno:
        - dict: Diccionario con los detalles de la película si se encuentra, de lo contrario `None`.

    Excepciones manejadas:
        - Exception: Cualquier error durante la búsqueda.
    """
    def obtener_detalles_pelicula(self, nombre_pelicula):
        try:
            # Filtramos el DataFrame por el título proporcionado
            resultado = self.peliculas_df[self.peliculas_df['title'].str.contains(nombre_pelicula, case=False, na=False)]
            # Devolvemos el primer resultado como un diccionario
            return resultado.iloc[0].to_dict() if not resultado.empty else None
        except Exception as e:
            print(f"Error al obtener detalles de la película: {e}")
            return None

    # Método público para recomendar películas basadas en otra película
    """
    Genera una lista de películas recomendadas en función de las similitudes con una película dada.

    Parámetros:
        - title (str): Título de la película base para las recomendaciones.

    Retorno:
        - List[dict]: Lista de diccionarios con las películas recomendadas y sus similitudes.

    Excepciones manejadas:
        - ValueError: Si la película no está en el sistema.
        - Exception: Cualquier error durante el cálculo de recomendaciones.
    """
    def recomendar_peliculas(self, title):
        try:
            # Verificamos que la película esté en el sistema
            if title not in self.peliculas_df['title'].values:
                raise ValueError(f"La película '{title}' no se encuentra en el sistema.")

            # Obtenemos el índice de la película
            idx = self.peliculas_df.index[self.peliculas_df['title'] == title][0]

            # Obtenemos los puntajes de similitud para la película
            sim_scores = list(enumerate(self.cosine_sim_synopsis[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # Preparamos la lista de recomendaciones
            recomendaciones = []
            for sim_idx, sim_score in sim_scores[1:6]:  # Excluir la película actual
                recomendaciones.append({
                    "titulo": self.peliculas_df.iloc[sim_idx]['title'],
                    "similitud": sim_score
                })
            return recomendaciones
        except Exception as e:
            print(f"Error al recomendar películas: {e}")
            return []

    # Método público para recomendar películas a un usuario
    """
    Genera una lista de películas recomendadas basándose en las votaciones del usuario.

    Parámetros:
        - username (str): Nombre de usuario.

    Retorno:
        - List[dict]: Lista de recomendaciones ajustadas según las votaciones del usuario.

    Excepciones manejadas:
        - ValueError: Si el usuario no está en el sistema.
        - Exception: Cualquier error durante el cálculo de recomendaciones.
    """
    def recomendar_peliculas_por_usuario(self, username):
        try:
            # Verificamos que el usuario exista
            if username not in self.usuarios_df["Nombre de usuario"].values:
                raise ValueError(f"El usuario '{username}' no se encuentra en el sistema.")
    
            # Obtenemos las votaciones del usuario
            usuario_row = self.usuarios_df[self.usuarios_df["Nombre de usuario"] == username].iloc[0]
            votaciones_usuario = ast.literal_eval(usuario_row["votaciones"]) if pd.notna(usuario_row["votaciones"]) else []
    
            # Crear un diccionario para agrupar las películas votadas por prioridad (5 a 1)
            peliculas_por_prioridad = {rating: [] for rating in range(5, 0, -1)}
            for v in votaciones_usuario:
                if v['rating'] in peliculas_por_prioridad:
                    peliculas_por_prioridad[v['rating']].append(v['title'])
    
            recomendaciones = []
            # Pesos ajustados para cada valoración (normalizados para no exceder 1)
            pesos = {5: 1.0, 4: 0.8, 3: 0.6, 2: 0.4, 1: 0.2}
    
            for rating in range(5, 0, -1):  # Iterar desde las valoraciones más altas (5) a las más bajas (1)
                for pelicula_votada in peliculas_por_prioridad[rating]:
                    indices = self.peliculas_df.index[self.peliculas_df['title'] == pelicula_votada]
    
                    if len(indices) == 0:
                        print(f"Advertencia: La película '{pelicula_votada}' no se encuentra en el sistema.")
                        continue
    
                    idx = indices[0]
                    sim_scores = list(enumerate(self.cosine_sim_recomendaciones[idx]))
                    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
                    for sim_idx, sim_score in sim_scores[1:]:
                        titulo_pelicula = self.peliculas_df.iloc[sim_idx]['title']
                        if titulo_pelicula not in [v['title'] for v in votaciones_usuario]:
                            recomendaciones.append({
                                'titulo': titulo_pelicula,
                                'similitud': sim_score,  # Guardar la similitud real
                                'similitud_ajustada': sim_score * pesos[rating]  # Guardar la similitud ajustada
                            })
    
            recomendaciones_unicas = {}
            for rec in recomendaciones:
                if rec['titulo'] not in recomendaciones_unicas or rec['similitud_ajustada'] > recomendaciones_unicas[rec['titulo']]['similitud_ajustada']:
                    recomendaciones_unicas[rec['titulo']] = {
                        'similitud': rec['similitud'],
                        'similitud_ajustada': rec['similitud_ajustada']
                    }
    
            recomendaciones = [
                {'titulo': titulo, 'similitud': valores['similitud'], 'similitud_ajustada': valores['similitud_ajustada']}
                for titulo, valores in recomendaciones_unicas.items()
            ]
            recomendaciones.sort(key=lambda x: x['similitud_ajustada'], reverse=True)
            return recomendaciones
        except Exception as e:
            print(f"Error al recomendar películas para el usuario: {e}")
            return []
    
     # Método público para registrar una votación de película por un usuario
    """
    Permite a un usuario registrar una votación para una película.

    Parámetros:
        - username (str): Nombre de usuario.
        - pelicula (str): Nombre de la película a votar.
        - puntuacion (int): Puntuación otorgada por el usuario.

    Retorno:
        - str: Mensaje indicando si la votación fue registrada exitosamente.

    Excepciones manejadas:
        - Exception: Cualquier error durante el registro de la votación.
    """
    def votar_pelicula(self, username, pelicula, puntuacion):
        try:
            # Verificamos si el usuario ya existe en el sistema
            if username in self.usuarios_df['Nombre de usuario'].values:
                # Obtenemos las votaciones del usuario existente
                usuario_row = self.usuarios_df[self.usuarios_df['Nombre de usuario'] == username].iloc[0]
                votaciones_usuario = ast.literal_eval(usuario_row['votaciones']) if pd.notna(usuario_row['votaciones']) else []

                # Buscamos si ya votó por esta película
                pelicula_existente = next((v for v in votaciones_usuario if v['title'] == pelicula), None)
    
                if pelicula_existente:
                    # Si ya existe, actualizamos la puntuación
                    pelicula_existente['rating'] = puntuacion
                else:
                    # Si no existe, agregamos una nueva entrada
                    votaciones_usuario.append({'title': pelicula, 'rating': puntuacion})

                # Actualizamos la información del usuario
                self.usuarios_df.loc[self.usuarios_df['Nombre de usuario'] == username, 'votaciones'] = str(votaciones_usuario)
            else:
                # Si el usuario no existe, creamos un nuevo registro
                nuevas_votaciones = [{'title': pelicula, 'rating': puntuacion}]
                nueva_fila = pd.DataFrame([{'Nombre de usuario': username, 'votaciones': str(nuevas_votaciones)}])
                self.usuarios_df = pd.concat([self.usuarios_df, nueva_fila], ignore_index=True)

            # Guardamos los cambios en el archivo CSV
            self.usuarios_df.to_csv(self.file_path_usuarios, index=False)
            return f"Votación registrada: {pelicula} - {puntuacion}/5"
        except Exception as e:
            print(f"Error al registrar votación: {e}")
            return f"No se pudo registrar la votación para {pelicula}."

    # Método público para obtener las valoraciones de un usuario
    """
    Devuelve las películas valoradas por un usuario específico junto con sus puntuaciones.

    Parámetros:
        - username (str): Nombre de usuario.

    Retorno:
        - List[dict]: Lista de diccionarios con los títulos de las películas y sus puntuaciones.

    Excepciones manejadas:
        - Exception: Cualquier error al obtener las valoraciones.
    """
    def obtener_valoraciones_usuario(self, username):
        try:
            # Verificamos si el usuario existe en el sistema
            if username in self.usuarios_df['Nombre de usuario'].values:
                # Obtenemos la fila correspondiente al usuario
                usuario_row = self.usuarios_df[self.usuarios_df['Nombre de usuario'] == username].iloc[0]
                # Convertimos la cadena de votaciones en una lista de diccionarios
                votaciones_usuario = ast.literal_eval(usuario_row['votaciones']) if pd.notna(usuario_row['votaciones']) else []
                return votaciones_usuario
            return []  # Si el usuario no existe, devolvemos una lista vacía
        except Exception as e:
            print(f"Error al obtener las valoraciones del usuario: {e}")
            return []