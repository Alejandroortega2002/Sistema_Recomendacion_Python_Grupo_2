import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class GestorPeliculas:
    def __init__(self):
        """
        Inicializa el gestor de películas cargando los datos y calculando similitudes.
        """
        self.file_path = 'peliculas_final_imagenes.csv'
        self.file_path_usuarios = 'usuarios.csv'
        self.peliculas_df = pd.read_csv(self.file_path)
        self.usuarios_df = pd.read_csv(self.file_path_usuarios)

        # Calcular similitudes entre películas al cargar los datos
        self._calcular_similitudes()
        self._calcular_similitudes_recomendaciones()

    def _calcular_similitudes(self):
        """
        Calcula la matriz de similitud de coseno basada en las sinopsis de las películas.
        """
        tfidf_vectorizer = TfidfVectorizer(
            stop_words='english',
            max_df=0.9,
            min_df=0.01,
            max_features=1000
        )
        self.peliculas_df['synopsis'] = self.peliculas_df['synopsis'].fillna('')
        tfidf_matrix = tfidf_vectorizer.fit_transform(self.peliculas_df['synopsis'])
        self.cosine_sim_synopsis = cosine_similarity(tfidf_matrix, tfidf_matrix)

    def _calcular_similitudes_recomendaciones(self):
        """
        Calcula la matriz de similitud de coseno basada en los sinopsis, director y género de las películas.
        """
        # Rellenar valores nulos en las columnas necesarias
        self.peliculas_df['synopsis'] = self.peliculas_df['synopsis'].fillna('')
        self.peliculas_df['director'] = self.peliculas_df['director'].fillna('')
        self.peliculas_df['genre'] = self.peliculas_df['genre'].fillna('')

        # Combinar características relevantes para la recomendación
        self.peliculas_df['combined_features'] = self.peliculas_df['synopsis'] + ' ' + \
                                                 self.peliculas_df['director'] + ' ' + \
                                                 self.peliculas_df['genre']

        tfidf_vectorizer = TfidfVectorizer(
            stop_words='english',
            max_df=0.9,
            min_df=0.01,
            max_features=1000
        )

        # Calcular la matriz TF-IDF combinada
        tfidf_matrix = tfidf_vectorizer.fit_transform(self.peliculas_df['combined_features'])

        # Calcular la similitud de coseno entre las películas
        self.cosine_sim_recomendaciones = cosine_similarity(tfidf_matrix, tfidf_matrix)

    def obtener_peliculas(self):
        return self.peliculas_df[['title', 'poster_image_y']].to_dict(orient='records')


    def buscar_peliculas(self, nombres_peliculas):
        """
        Busca películas cuyos títulos estén en la lista proporcionada.
        """
        resultado = self.peliculas_df[self.peliculas_df['title'].isin(nombres_peliculas)]
        if resultado.empty:
            return []
        return resultado[['title', 'poster_image_y']].to_dict(orient='records')
    
    def buscar_peliculas2(self, nombre_pelicula):
        """
        Busca películas cuyo título contenga el texto proporcionado.
        """
        if not nombre_pelicula:
            return []
    
        # Filtrar películas cuyo título contenga el texto, ignorando mayúsculas/minúsculas
        resultado = self.peliculas_df[self.peliculas_df['title'].str.contains(nombre_pelicula, case=False, na=False)]
        
        if resultado.empty:
            return []
    
        # Retornar solo las columnas necesarias
        return resultado[['title', 'poster_image_y']].to_dict(orient='records')
    


    def peliculas_al_azar(self, cantidad=12):
        """
        Selecciona una muestra aleatoria de películas.
        """
        return self.peliculas_df.sample(n=cantidad)['title'].tolist()

    def obtener_detalles_pelicula(self, nombre_pelicula):
        """
        Devuelve los detalles completos de una película específica.
        """
        resultado = self.peliculas_df[self.peliculas_df['title'].str.contains(nombre_pelicula, case=False, na=False)]
        if resultado.empty:
            return None
        return resultado.iloc[0].to_dict()

    def recomendar_peliculas(self, title):
        """
        Recomienda películas similares a la proporcionada, incluyendo sus valores de similitud.
        """
        if title not in self.peliculas_df['title'].values:
            raise ValueError(f"La película '{title}' no se encuentra en el sistema.")

        idx = self.peliculas_df.index[self.peliculas_df['title'] == title][0]
        sim_scores = list(enumerate(self.cosine_sim_synopsis[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Retornar títulos y similitudes de las películas recomendadas
        recomendaciones = []
        for sim_idx, sim_score in sim_scores[1:6]:  # Excluir la película actual
            recomendaciones.append({
                "titulo": self.peliculas_df.iloc[sim_idx]['title'],
                "similitud": sim_score
            })

        return recomendaciones

    def recomendar_peliculas_por_usuario(self, username):
        """
        Recomienda películas basadas en las valoraciones de un usuario específico.
        Incluye las similitudes del coseno para cada recomendación y pondera según la valoración del usuario.
        """
        if username not in self.usuarios_df["Nombre de usuario"].values:
            raise ValueError(f"El usuario '{username}' no se encuentra en el sistema.")

        usuario_row = self.usuarios_df[self.usuarios_df["Nombre de usuario"] == username].iloc[0]

        # Convertir las votaciones en una lista de diccionarios
        votaciones_usuario = []
        if not pd.isna(usuario_row["votaciones"]):
            votaciones_usuario = ast.literal_eval(usuario_row["votaciones"])

        # Filtrar solo las películas con valoraciones altas (por ejemplo, >= 4)
        peliculas_votadas = [
            {'title': v['title'], 'rating': v['rating']}
            for v in votaciones_usuario if v['rating'] >= 4
        ]

        if not peliculas_votadas:
            raise ValueError("El usuario no tiene películas con valoraciones altas.")

        # Crear una lista para almacenar las películas recomendadas con sus similitudes
        recomendaciones = []

        # Recomendamos películas basadas en la similitud con las películas votadas
        for pelicula in peliculas_votadas:
            pelicula_votada = pelicula['title']
            rating = pelicula['rating']  # Usar el rating como factor de ponderación

            # Verificar si la película existe en el DataFrame
            indices = self.peliculas_df.index[self.peliculas_df['title'] == pelicula_votada]

            if len(indices) == 0:
                print(f"Advertencia: La película '{pelicula_votada}' no se encuentra en el sistema.")
                continue

            # Obtener el índice de la película
            idx = indices[0]

            # Obtener las puntuaciones de similitud para esa película
            sim_scores = list(enumerate(self.cosine_sim_recomendaciones[idx]))

            # Ordenar las películas por similitud (de mayor a menor)
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # Obtener los índices y valores de similitud de las películas más similares
            for sim_idx, sim_score in sim_scores[1:]:  # Excluir la película actual
                titulo_pelicula = self.peliculas_df.iloc[sim_idx]['title']
                if titulo_pelicula not in [v['title'] for v in votaciones_usuario]:
                    recomendaciones.append({
                        'titulo': titulo_pelicula,
                        'similitud': sim_score * (rating / 5)  # Ponderar por la valoración del usuario
                    })

        # Eliminar duplicados manteniendo el mayor valor de similitud
        recomendaciones_unicas = {}
        for rec in recomendaciones:
            if rec['titulo'] not in recomendaciones_unicas or rec['similitud'] > recomendaciones_unicas[rec['titulo']]:
                recomendaciones_unicas[rec['titulo']] = rec['similitud']

        # Convertir el diccionario de nuevo a una lista de recomendaciones
        recomendaciones = [{'titulo': titulo, 'similitud': similitud} for titulo, similitud in
                           recomendaciones_unicas.items()]

        # Ordenar la lista final por similitud de mayor a menor
        recomendaciones.sort(key=lambda x: x['similitud'], reverse=True)

        return recomendaciones

    def votar_pelicula(self, username, pelicula, puntuacion):
        """
        Permite a un usuario votar una película.
        """
        if username in self.usuarios_df['Nombre de usuario'].values:
            usuario_row = self.usuarios_df[self.usuarios_df['Nombre de usuario'] == username].iloc[0]

            votaciones_usuario = ast.literal_eval(usuario_row['votaciones']) if pd.notna(
                usuario_row['votaciones']) else []
            pelicula_existente = next((v for v in votaciones_usuario if v['title'] == pelicula), None)

            if pelicula_existente:
                pelicula_existente['rating'] = puntuacion
            else:
                votaciones_usuario.append({'title': pelicula, 'rating': puntuacion})

            self.usuarios_df.loc[self.usuarios_df['Nombre de usuario'] == username, 'votaciones'] = str(
                votaciones_usuario)
        else:
            nuevas_votaciones = [{'title': pelicula, 'rating': puntuacion}]
            nueva_fila = pd.DataFrame([{'Nombre de usuario': username, 'votaciones': str(nuevas_votaciones)}])
            self.usuarios_df = pd.concat([self.usuarios_df, nueva_fila], ignore_index=True)

        self.usuarios_df.to_csv(self.file_path_usuarios, index=False)
        return f"Votación registrada: {pelicula} - {puntuacion}/5"

    def obtener_valoraciones_usuario(self, username):
        """
        Obtiene las valoraciones del usuario.
        """
        if username in self.usuarios_df['Nombre de usuario'].values:
            usuario_row = self.usuarios_df[self.usuarios_df['Nombre de usuario'] == username].iloc[0]
            votaciones_usuario = ast.literal_eval(usuario_row['votaciones']) if pd.notna(
                usuario_row['votaciones']) else []
            return votaciones_usuario
        return []