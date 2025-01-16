import pandas as pd

class GestorUsuarios:
    """
    Clase para gestionar usuarios en un sistema.
    Permite registrar, validar y administrar usuarios junto con sus votaciones.
    """

    # Constructor de la clase
    """
    Inicializa el gestor de usuarios cargando los datos desde un archivo CSV.

    Excepciones manejadas:
        - FileNotFoundError: Si el archivo de usuarios no existe, se crea un nuevo archivo.
        - pd.errors.EmptyDataError: Si el archivo está vacío, se inicializa una estructura vacía.
        - Exception: Cualquier otro error durante la inicialización.
    """
    def __init__(self):
        self.file_path = 'usuarios.csv'
        try:
            # Intentamos cargar los datos desde el archivo CSV
            self.usuarios_df = pd.read_csv(self.file_path)
            # Convertimos la columna 'ID' a tipo numérico para evitar errores
            self.usuarios_df['ID'] = pd.to_numeric(self.usuarios_df['ID'], errors='coerce').fillna(0).astype(int)
        except FileNotFoundError:
            # Creamos un nuevo archivo si no existe
            print(f"Advertencia: Archivo '{self.file_path}' no encontrado. Creando un nuevo archivo.")
            self.usuarios_df = pd.DataFrame(columns=['ID', 'Nombre de usuario', 'Contraseña', 'votaciones'])
        except pd.errors.EmptyDataError:
            # Inicializamos la estructura de datos si el archivo está vacío
            print(f"Advertencia: Archivo '{self.file_path}' vacío. Inicializando estructura de datos.")
            self.usuarios_df = pd.DataFrame(columns=['ID', 'Nombre de usuario', 'Contraseña', 'votaciones'])
        except Exception as e:
            print(f"Error inesperado al inicializar el gestor de usuarios: {e}")
            self.usuarios_df = pd.DataFrame(columns=['ID', 'Nombre de usuario', 'Contraseña', 'votaciones'])

    # Método para registrar un nuevo usuario
    """
    Registra un nuevo usuario en el sistema.

    Parámetros:
        - username (str): Nombre de usuario.
        - password (str): Contraseña del usuario.

    Retorno:
        - str: Mensaje indicando si el usuario fue registrado exitosamente o si ocurrió un error.
    """
    def registrar_usuario(self, username, password):
        try:
            # Validamos que el nombre de usuario y la contraseña no estén vacíos
            if username.strip() == "" or password.strip() == "":
                return "El nombre de usuario y la contraseña no pueden estar vacíos."

            # Verificamos si el usuario ya existe
            if username in self.usuarios_df['Nombre de usuario'].values:
                return "El usuario ya existe."

            # Calculamos el próximo ID disponible
            nuevo_id = 1 if self.usuarios_df.empty else self.usuarios_df['ID'].max() + 1

            # Creamos un nuevo registro de usuario
            nuevo_usuario = {
                'ID': nuevo_id,
                'Nombre de usuario': username,
                'Contraseña': password,
                'votaciones': "[]"  # Sin votaciones inicialmente
            }

            # Agregamos el nuevo usuario al DataFrame
            self.usuarios_df = pd.concat([self.usuarios_df, pd.DataFrame([nuevo_usuario])], ignore_index=True)
            self.guardar_datos()
            return "Usuario registrado con éxito."
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return "No se pudo registrar el usuario debido a un error interno."

    # Método para validar las credenciales de un usuario
    """
    Valida las credenciales de un usuario.

    Parámetros:
        - username (str): Nombre de usuario.
        - password (str): Contraseña del usuario.

    Retorno:
        - Tuple[bool, str]: Un booleano indicando el éxito de la validación y un mensaje asociado.
    """
    def validar_usuario(self, username, password):
        try:
            # Validamos que los campos no estén vacíos
            if username.strip() == "" or password.strip() == "":
                return False, "El nombre de usuario y la contraseña no pueden estar vacíos."

            # Recargamos el archivo para asegurarnos de que los datos estén actualizados
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

            # Buscamos el usuario en el DataFrame
            usuario = self.usuarios_df[self.usuarios_df['Nombre de usuario'] == username]
            if usuario.empty:
                return False, "El usuario no existe."

            # Validamos la contraseña
            if usuario.iloc[0]['Contraseña'] != password:
                return False, "Contraseña incorrecta."

            return True, "Inicio de sesión exitoso."
        except Exception as e:
            print(f"Error al validar usuario: {e}")
            return False, "Error interno al validar usuario."

    # Método para guardar los datos de usuarios
    """
    Guarda los datos de los usuarios en el archivo CSV.

    Excepciones manejadas:
        - Exception: Cualquier error al intentar guardar los datos.
    """
    def guardar_datos(self):
        try:
            self.usuarios_df.to_csv(self.file_path, index=False)
        except Exception as e:
            print(f"Error al guardar datos en el archivo '{self.file_path}': {e}")

    # Método para obtener un usuario por su ID
    """
    Obtiene la información de un usuario dado su ID.

    Parámetros:
        - user_id (int): ID del usuario.

    Retorno:
        - Tuple[Optional[dict], str]: Un diccionario con los datos del usuario y un mensaje asociado.
    """
    def obtener_usuario_por_id(self, user_id):
        try:
            # Verificamos si la columna 'ID' existe
            if 'ID' not in self.usuarios_df.columns:
                return None, "El campo 'ID' no existe en los datos."

            # Buscamos el usuario por ID
            usuario = self.usuarios_df[self.usuarios_df['ID'] == user_id]
            if usuario.empty:
                return None, "No se encontró un usuario con el ID especificado."

            return usuario.iloc[0].to_dict(), "Usuario encontrado."
        except Exception as e:
            print(f"Error al obtener usuario por ID: {e}")
            return None, "Error al buscar el usuario."

    # Método para obtener todos los usuarios
    """
    Devuelve todos los usuarios registrados en el sistema.

    Retorno:
        - List[dict]: Lista de diccionarios con los datos de los usuarios.

    Excepciones manejadas:
        - Exception: Cualquier error al intentar obtener los datos.
    """
    def obtener_usuarios(self):
        try:
            return self.usuarios_df.to_dict(orient='records')
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []
