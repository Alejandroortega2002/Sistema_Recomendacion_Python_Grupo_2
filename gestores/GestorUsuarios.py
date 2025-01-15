import pandas as pd

class GestorUsuarios:
    def __init__(self):
        """
        Inicializa el gestor de usuarios cargando los datos desde un archivo CSV.
        """
        self.file_path = 'usuarios.csv'
        self.usuarios_df = pd.read_csv(self.file_path)

    def registrar_usuario(self, username, password):
        """
        Registra un nuevo usuario en el sistema.
        """
        if username in self.usuarios_df['Nombre de usuario'].values:
            return "El usuario ya existe."

        nuevo_usuario = {
            'Nombre de usuario': username,
            'Contraseña': password,
            'votaciones': "[]"  # Sin votaciones inicialmente
        }

        self.usuarios_df = pd.concat([self.usuarios_df, pd.DataFrame([nuevo_usuario])], ignore_index=True)
        self.guardar_datos()
        return "Usuario registrado con éxito."

    def validar_usuario(self, username, password):
        """
        Valida las credenciales del usuario.
        """
        # Recargar el archivo para asegurarse de que está actualizado
        self.usuarios_df = pd.read_csv(self.file_path) 
        
        usuario = self.usuarios_df[self.usuarios_df['Nombre de usuario'] == username]
        if usuario.empty:
            return False, "El usuario no existe."

        if usuario.iloc[0]['Contraseña'] != password:
            return False, "Contraseña incorrecta."

        return True, "Inicio de sesión exitoso."

    def guardar_datos(self):
        """
        Guarda los datos del usuario en el archivo CSV.
        """
        self.usuarios_df.to_csv(self.file_path, index=False)
