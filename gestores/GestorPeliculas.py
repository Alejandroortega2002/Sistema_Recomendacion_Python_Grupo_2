import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class GestorPeliculas:
    def __init__(self):
        """
        Inicializa el gestor de películas cargando los datos y calculando similitudes.
        """
        try:
            self.file_path = 'peliculas_final_imagenes.csv'
            self.file_path_usuarios = 'usuarios.csv'
            self.peliculas_df = pd.read_csv(self.file_path)
            self.usuarios_df = pd.read_csv(self.file_path_usuarios)

            # Calcular similitudes entre películas al cargar los datos
            self._calcular_similitudes()
            self._calcular_similitudes_recomendaciones()
        except FileNotFoundError as e:
            print(f"Error: Archivo no encontrado. {e}")
            self.peliculas_df = pd.DataFrame()
            self.usuarios_df = pd.DataFrame()
        except Exception as e:
            print(f"Error inesperado durante la inicialización: {e}")
            self.peliculas_df = pd.DataFrame()
            self.usuarios_df = pd.DataFrame()

    
            
    def _calcular_similitudes(self):
        """
        Calcula la matriz de similitud de coseno basada en las sinopsis de las películas.
        """
        try:
            if 'synopsis' not in self.peliculas_df.columns:
                print("Advertencia: No se encontró la columna 'synopsis'.")
                self.cosine_sim_synopsis = []
                return

            tfidf_vectorizer = TfidfVectorizer(
                stop_words='english',
                max_df=0.9,
                min_df=0.01,
                max_features=1000
            )
            self.peliculas_df['synopsis'] = self.peliculas_df['synopsis'].fillna('')
            tfidf_matrix = tfidf_vectorizer.fit_transform(self.peliculas_df['synopsis'])
            self.cosine_sim_synopsis = cosine_similarity(tfidf_matrix, tfidf_matrix)
        except Exception as e:
            print(f"Error al calcular similitudes de sinopsis: {e}")
            self.cosine_sim_synopsis = []

    def _calcular_similitudes_recomendaciones(self):
        """
        Calcula la matriz de similitud de coseno basada en los sinopsis, director y género de las películas.
        """
        try:
            for col in ['synopsis', 'director', 'genre']:
                if col not in self.peliculas_df.columns:
                    print(f"Advertencia: No se encontró la columna '{col}'.")
                    self.peliculas_df[col] = ''

            self.peliculas_df['combined_features'] = self.peliculas_df['synopsis'].fillna('') + ' ' + \
                                                     self.peliculas_df['director'].fillna('') + ' ' + \
                                                     self.peliculas_df['genre'].fillna('')

            tfidf_vectorizer = TfidfVectorizer(
                stop_words='english',
                max_df=0.9,
                min_df=0.01,
                max_features=1000
            )
            tfidf_matrix = tfidf_vectorizer.fit_transform(self.peliculas_df['combined_features'])
            self.cosine_sim_recomendaciones = cosine_similarity(tfidf_matrix, tfidf_matrix)
        except Exception as e:
            print(f"Error al calcular similitudes combinadas: {e}")
            self.cosine_sim_recomendaciones = []

    def obtener_peliculas(self):
        try:
            return self.peliculas_df[['title', 'poster_image_y']].to_dict(orient='records')
        except KeyError as e:
            print(f"Error: Columnas necesarias no encontradas. {e}")
            return []

    def buscar_peliculas(self, nombres_peliculas):
        try:
            resultado = self.peliculas_df[self.peliculas_df['title'].isin(nombres_peliculas)]
            return resultado[['title', 'poster_image_y']].to_dict(orient='records') if not resultado.empty else []
        except KeyError as e:
            print(f"Error: Columnas necesarias no encontradas. {e}")
            return []

    def buscar_peliculas2(self, nombre_pelicula):
        try:
            if not nombre_pelicula:
                return []
            resultado = self.peliculas_df[self.peliculas_df['title'].str.contains(nombre_pelicula, case=False, na=False)]
            return resultado[['title', 'poster_image_y']].to_dict(orient='records') if not resultado.empty else []
        except Exception as e:
            print(f"Error al buscar películas: {e}")
            return []

    def peliculas_al_azar(self, cantidad=12):
        try:
            return self.peliculas_df.sample(n=cantidad)['title'].tolist()
        except ValueError as e:
            print(f"Advertencia: No hay suficientes películas para seleccionar. {e}")
            return []

    def obtener_detalles_pelicula(self, nombre_pelicula):
        try:
            resultado = self.peliculas_df[self.peliculas_df['title'].str.contains(nombre_pelicula, case=False, na=False)]
            return resultado.iloc[0].to_dict() if not resultado.empty else None
        except Exception as e:
            print(f"Error al obtener detalles de la película: {e}")
            return None

    def recomendar_peliculas(self, title):
        try:
            if title not in self.peliculas_df['title'].values:
                raise ValueError(f"La película '{title}' no se encuentra en el sistema.")

            idx = self.peliculas_df.index[self.peliculas_df['title'] == title][0]
            sim_scores = list(enumerate(self.cosine_sim_synopsis[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

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

    def recomendar_peliculas_por_usuario(self, username):
        try:
            if username not in self.usuarios_df["Nombre de usuario"].values:
                raise ValueError(f"El usuario '{username}' no se encuentra en el sistema.")
    
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
    
    

    def votar_pelicula(self, username, pelicula, puntuacion):
        try:
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
            return f"Votación registrada: {pelicula} - {puntuacion}/5"
        except Exception as e:
            print(f"Error al registrar votación: {e}")
            return f"No se pudo registrar la votación para {pelicula}."
    
    def obtener_valoraciones_usuario(self, username):
        try:
            if username in self.usuarios_df['Nombre de usuario'].values:
                usuario_row = self.usuarios_df[self.usuarios_df['Nombre de usuario'] == username].iloc[0]
                votaciones_usuario = ast.literal_eval(usuario_row['votaciones']) if pd.notna(usuario_row['votaciones']) else []
                return votaciones_usuario
            return []
        except Exception as e:
            print(f"Error al obtener las valoraciones del usuario: {e}")
            return []
