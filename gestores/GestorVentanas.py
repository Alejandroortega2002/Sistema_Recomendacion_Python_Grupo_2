from PyQt5.QtWidgets import QApplication, QMessageBox
from vistas.VistaLogin import VistaLogin
from vistas.VistaPrincipal import VistaPrincipal
from vistas.VistaRecomendaciones import VistaRecomendaciones
from vistas.VistaRegistro import VistaRegistro
from vistas.VistaSinopsis import VistaSinopsis
from vistas.VistaVotaciones import VistaVotaciones
from vistas.VistaMisValoraciones import VistaMisValoraciones
from gestores.GestorPeliculas import GestorPeliculas

class GestorVentanas:
    """
    Clase para gestionar las ventanas de la aplicación.
    Proporciona métodos para cambiar entre vistas y manejar la navegación.
    """

    # Constructor de la clase
    """
    Inicializa el gestor de ventanas y crea las vistas necesarias.

    Excepciones manejadas:
        - Exception: Cualquier error durante la inicialización.
    """
    def __init__(self):
        try:
            self.app = QApplication([])

            # Inicializar vistas
            self.vista_login = None
            self.vista_principal = None
            self.vista_registro = None
            self.vista_sinopsis = None
            self.vista_votaciones = None
            self.vista_mis_valoraciones = None
            self.vista_recomendaciones = None

            self.user_id = None
            self.username = None

            # Instancia del GestorPeliculas
            self.gestor_peliculas = GestorPeliculas()
        except Exception as e:
            print(f"Error al inicializar GestorVentanas: {e}")
            QMessageBox.critical(None, "Error Crítico", f"No se pudo iniciar la aplicación: {e}")

    # Método para establecer información del usuario
    """
    Establece el ID y el nombre de usuario del usuario actual.

    Parámetros:
        - user_id (int): ID del usuario.
        - username (str): Nombre de usuario.

    Notas:
        - Si los parámetros son inválidos, no se establece la información.
    """
    def set_user_info(self, user_id, username):
        if not user_id or not username:
            print("Advertencia: user_id o username no válidos.")
            return
        self.user_id = user_id
        self.username = username

    # Método para mostrar la ventana de inicio de sesión
    """
    Muestra la ventana de inicio de sesión.

    Excepciones manejadas:
        - Exception: Cualquier error al cargar la ventana.
    """
    def mostrar_login(self):
        try:
            if not self.vista_login:
                self.vista_login = VistaLogin(self)
            self._cambiar_ventana(self.vista_login)
        except Exception as e:
            print(f"Error al mostrar la ventana de inicio de sesión: {e}")
            QMessageBox.critical(None, "Error", f"Error al cargar la ventana de inicio de sesión: {e}")

    # Método para mostrar la ventana principal
    """
    Muestra la ventana principal.

    Excepciones manejadas:
        - Exception: Cualquier error al cargar la ventana.
    """
    def mostrar_principal(self):
        try:
            if not self.vista_principal:
                self.vista_principal = VistaPrincipal(self)
            self._cambiar_ventana(self.vista_principal)
        except Exception as e:
            print(f"Error al mostrar la ventana principal: {e}")
            QMessageBox.critical(None, "Error", f"Error al cargar la ventana principal: {e}")

    # Método para mostrar la ventana de votaciones
    """
    Muestra la ventana de votaciones.

    Excepciones manejadas:
        - Exception: Cualquier error al cargar la ventana.
    """
    def mostrar_votaciones(self):
        try:
            if not self.vista_votaciones:
                self.vista_votaciones = VistaVotaciones(self, self.username)
            self._cambiar_ventana(self.vista_votaciones)
        except Exception as e:
            print(f"Error al mostrar la ventana de votaciones: {e}")
            QMessageBox.critical(None, "Error", f"Error al cargar la ventana de votaciones: {e}")

    # Método para mostrar la ventana de valoraciones del usuario
    """
    Muestra la ventana de "Mis Valoraciones" para el usuario actual.

    Parámetros:
        - username (str): Nombre de usuario.

    Excepciones manejadas:
        - Exception: Cualquier error al cargar la ventana.
    """
    def mostrar_mis_valoraciones(self, username):
        try:
            if not self.vista_mis_valoraciones:
                self.vista_mis_valoraciones = VistaMisValoraciones(self, username)
            self.vista_mis_valoraciones.show()
        except Exception as e:
            print(f"Error al mostrar la ventana de mis valoraciones: {e}")
            QMessageBox.critical(None, "Error", f"Error al cargar la ventana de mis valoraciones: {e}")

    # Método para mostrar la ventana de registro
    """
    Muestra la ventana de registro.

    Excepciones manejadas:
        - Exception: Cualquier error al cargar la ventana.
    """
    def mostrar_registro(self):
        try:
            if not self.vista_registro:
                self.vista_registro = VistaRegistro(self)
            self._cambiar_ventana(self.vista_registro)
        except Exception as e:
            print(f"Error al mostrar la ventana de registro: {e}")
            QMessageBox.critical(None, "Error", f"Error al cargar la ventana de registro: {e}")

    # Método para mostrar la ventana de sinopsis
    """
    Muestra la ventana de sinopsis para una película específica.

    Parámetros:
        - detalles_pelicula (dict): Diccionario con los detalles de la película.

    Excepciones manejadas:
        - ValueError: Si no se proporcionan detalles de la película.
        - Exception: Cualquier error al cargar la ventana.
    """
    def mostrar_sinopsis(self, detalles_pelicula):
        try:
            if not detalles_pelicula:
                raise ValueError("Detalles de la película no proporcionados.")
            if not self.vista_sinopsis:
                self.vista_sinopsis = VistaSinopsis(self, self.gestor_peliculas)
            self.vista_sinopsis.mostrar_informacion_pelicula(detalles_pelicula)
            self._cambiar_ventana(self.vista_sinopsis)
        except Exception as e:
            print(f"Error al mostrar la ventana de sinopsis: {e}")
            QMessageBox.critical(None, "Error", f"Error al cargar la ventana de sinopsis: {e}")

    # Método para mostrar la ventana de recomendaciones
    """
    Muestra la ventana de recomendaciones para el usuario actual.

    Parámetros:
        - gestor_peliculas (GestorPeliculas): Instancia del gestor de películas.
        - username (str): Nombre de usuario.

    Excepciones manejadas:
        - Exception: Cualquier error al cargar la ventana.
    """
    def mostrar_recomendaciones(self, gestor_peliculas, username):
        try:
            # Siempre reinicia la vista de recomendaciones para garantizar datos actualizados
            self.vista_recomendaciones = VistaRecomendaciones(self, gestor_peliculas, username)
            self._cambiar_ventana(self.vista_recomendaciones)
        except Exception as e:
            print(f"Error al mostrar la ventana de recomendaciones: {e}")
            QMessageBox.critical(None, "Error", f"Error al cargar la ventana de recomendaciones: {e}")

    # Método privado para cambiar entre ventanas
    """
    Cierra la ventana actual y abre una nueva.

    Parámetros:
        - nueva_ventana: Instancia de la nueva ventana a mostrar.

    Excepciones manejadas:
        - Exception: Cualquier error al cambiar entre ventanas.
    """
    def _cambiar_ventana(self, nueva_ventana):
        try:
            # Cierra todas las ventanas visibles
            for ventana in [
                self.vista_login,
                self.vista_principal,
                self.vista_registro,
                self.vista_sinopsis,
                self.vista_recomendaciones,
                self.vista_votaciones,
                self.vista_mis_valoraciones
            ]:
                if ventana and ventana.isVisible():
                    ventana.close()  # Cierra la ventana completamente
            nueva_ventana.show()  # Muestra la nueva ventana
        except Exception as e:
            print(f"Error al cambiar ventana: {e}")
            QMessageBox.critical(None, "Error", f"Error al cambiar de ventana: {e}")

    # Método para ejecutar la aplicación
    """
    Ejecuta la aplicación mostrando inicialmente la ventana de login.

    Excepciones manejadas:
        - Exception: Cualquier error crítico durante la ejecución.
    """
    def ejecutar(self):
        try:
            self.mostrar_login()
            self.app.exec_()
        except Exception as e:
            print(f"Error crítico al ejecutar la aplicación: {e}")
            QMessageBox.critical(None, "Error Crítico", f"La aplicación no pudo iniciar: {e}")

if __name__ == "__main__":
    gestor = GestorVentanas()
    gestor.ejecutar()
