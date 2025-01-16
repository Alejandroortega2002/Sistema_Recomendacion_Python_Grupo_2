import pandas as pd

class GestorUsuarios:
    def __init__(self):
        """
        Inicializa el gestor de usuarios cargando los datos desde un archivo CSV.
        """
        self.file_path = 'usuarios.csv'
        try:
            self.usuarios_df = pd.read_csv(self.file_path)
            self.usuarios_df['ID'] = pd.to_numeric(self.usuarios_df['ID'], errors='coerce').fillna(0).astype(int)
        except FileNotFoundError:
            print(f"Advertencia: Archivo '{self.file_path}' no encontrado. Creando un nuevo archivo.")
            self.usuarios_df = pd.DataFrame(columns=['ID', 'Nombre de usuario', 'Contraseña', 'votaciones'])
        except pd.errors.EmptyDataError:
            print(f"Advertencia: Archivo '{self.file_path}' vacío. Inicializando estructura de datos.")
            self.usuarios_df = pd.DataFrame(columns=['ID', 'Nombre de usuario', 'Contraseña', 'votaciones'])
        except Exception as e:
            print(f"Error inesperado al inicializar el gestor de usuarios: {e}")
            self.usuarios_df = pd.DataFrame(columns=['ID', 'Nombre de usuario', 'Contraseña', 'votaciones'])

    def registrar_usuario(self, username, password):
        """
        Registra un nuevo usuario en el sistema.
        """
        try:
            if username.strip() == "" or password.strip() == "":
                return "El nombre de usuario y la contraseña no pueden estar vacíos."

            if username in self.usuarios_df['Nombre de usuario'].values:
                return "El usuario ya existe."

            # Calcular el próximo ID disponible
            nuevo_id = 1 if self.usuarios_df.empty else self.usuarios_df['ID'].max() + 1

            nuevo_usuario = {
                'ID': nuevo_id,  # ID numérico autoincremental
                'Nombre de usuario': username,
                'Contraseña': password,
                'votaciones': "[]"  # Sin votaciones inicialmente
            }

            self.usuarios_df = pd.concat([self.usuarios_df, pd.DataFrame([nuevo_usuario])], ignore_index=True)
            self.guardar_datos()
            return "Usuario registrado con éxito."
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return "No se pudo registrar el usuario debido a un error interno."

    def validar_usuario(self, username, password):
        """
        Valida las credenciales del usuario.
        """
        try:
            if username.strip() == "" or password.strip() == "":
                return False, "El nombre de usuario y la contraseña no pueden estar vacíos."

            # Recargar el archivo para asegurarse de que está actualizado
            try:
                self.usuarios_df = pd.read_csv(self.file_path)
                self.usuarios_df['ID'] = pd.to_numeric(self.usuarios_df['ID'], errors='coerce').fillna(0).astype(int)
            except FileNotFoundError:
                return False, "No se encontraron usuarios registrados."
            except pd.errors.EmptyDataError:
                return False, "No hay datos en el archivo de usuarios."
            except Exception as e:
                print(f"Error al leer el archivo de usuarios: {e}")
                return False, "Error al validar usuario."

            usuario = self.usuarios_df[self.usuarios_df['Nombre de usuario'] == username]
            if usuario.empty:
                return False, "El usuario no existe."

            if usuario.iloc[0]['Contraseña'] != password:
                return False, "Contraseña incorrecta."

            return True, "Inicio de sesión exitoso."
        except Exception as e:
            print(f"Error al validar usuario: {e}")
            return False, "Error interno al validar usuario."

    def guardar_datos(self):
        """
        Guarda los datos del usuario en el archivo CSV.
        """
        try:
            self.usuarios_df.to_csv(self.file_path, index=False)
        except Exception as e:
            print(f"Error al guardar datos en el archivo '{self.file_path}': {e}")

    def obtener_usuario_por_id(self, user_id):
        """
        Obtiene la información de un usuario dado su ID.
        """
        try:
            if 'ID' not in self.usuarios_df.columns:
                return None, "El campo 'ID' no existe en los datos."

            usuario = self.usuarios_df[self.usuarios_df['ID'] == user_id]
            if usuario.empty:
                return None, "No se encontró un usuario con el ID especificado."

            return usuario.iloc[0].to_dict(), "Usuario encontrado."
        except Exception as e:
            print(f"Error al obtener usuario por ID: {e}")
            return None, "Error al buscar el usuario."

    def obtener_usuarios(self):
        """
        Devuelve todos los usuarios registrados en el sistema.
        """
        try:
            return self.usuarios_df.to_dict(orient='records')
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []
