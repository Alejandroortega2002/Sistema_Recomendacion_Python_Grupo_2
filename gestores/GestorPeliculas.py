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
        self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    def buscar_peliculas(self, nombre_pelicula):
        """
        Busca películas cuyo título contenga el texto proporcionado.
        """
        resultado = self.peliculas_df[self.peliculas_df['title'].str.contains(nombre_pelicula, case=False, na=False)]
        if resultado.empty:
            return []
        return resultado[['title', 'year', 'synopsis']].to_dict(orient='records')

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
        Recomienda películas similares a la proporcionada.
        """
        if title not in self.peliculas_df['title'].values:
            raise ValueError(f"La película '{title}' no se encuentra en el sistema.")

        idx = self.peliculas_df.index[self.peliculas_df['title'] == title][0]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_indices = [i[0] for i in sim_scores[1:6]]
        return self.peliculas_df['title'].iloc[sim_indices].tolist()

    def votar_pelicula(self, username, pelicula, puntuacion):
        """
        Permite a un usuario votar una película.
        """
        if username in self.usuarios_df['Nombre de usuario'].values:
            usuario_row = self.usuarios_df[self.usuarios_df['Nombre de usuario'] == username].iloc[0]

            votaciones_usuario = ast.literal_eval(usuario_row['votaciones']) if pd.notna(usuario_row['votaciones']) else []
            pelicula_existente = next((v for v in votaciones_usuario if v['title'] == pelicula), None)

            if pelicula_existente:
                pelicula_existente['rating'] = puntuacion
            else:
                votaciones_usuario.append({'title': pelicula, 'rating': puntuacion})

            self.usuarios_df.loc[self.usuarios_df['Nombre de usuario'] == username, 'votaciones'] = str(votaciones_usuario)
        else:
            nuevas_votaciones = [{'title': pelicula, 'rating': puntuacion}]
            nueva_fila = pd.DataFrame([{'Nombre de usuario': username, 'votaciones': str(nuevas_votaciones)}])
            self.usuarios_df = pd.concat([self.usuarios_df, nueva_fila], ignore_index=True)

        self.usuarios_df.to_csv(self.file_path_usuarios, index=False)
        return f"Votación registrada: {pelicula} - {puntuacion}/10"
    
    def obtener_valoraciones_usuario(self, username):
        """
        Obtiene las valoraciones del usuario.
        """
        if username in self.usuarios_df['Nombre de usuario'].values:
            usuario_row = self.usuarios_df[self.usuarios_df['Nombre de usuario'] == username].iloc[0]
            votaciones_usuario = ast.literal_eval(usuario_row['votaciones']) if pd.notna(usuario_row['votaciones']) else []
            return votaciones_usuario
        return []