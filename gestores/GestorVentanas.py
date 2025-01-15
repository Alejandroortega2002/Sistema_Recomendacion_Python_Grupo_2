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
    def __init__(self):
        """
        Inicializa el gestor de ventanas y crea las vistas necesarias.
        """
        self.app = QApplication([])

        # Inicializar vistas
        self.vista_login = None
        self.vista_principal = None
        self.vista_registro = None
        self.vista_sinopsis = None
        self.vista_votaciones = None
        self.vista_mis_valoraciones = None
        self.username = None
        self.vista_recomendaciones = None

        # Instancia del GestorPeliculas
        self.gestor_peliculas = GestorPeliculas()

    def set_username(self, username):
        """
        Establece el nombre de usuario del usuario actual.
        """
        self.username = username

    def mostrar_login(self):
        """
        Muestra la ventana de inicio de sesión.
        """
        if not self.vista_login:
            self.vista_login = VistaLogin(self)
        self._cambiar_ventana(self.vista_login)

    def mostrar_principal(self):
        """
        Muestra la ventana principal.
        """
        if not self.vista_principal:
            self.vista_principal = VistaPrincipal(self)
        self._cambiar_ventana(self.vista_principal)

    def mostrar_votaciones(self):
        """
        Muestra la ventana de votaciones.
        """
        if not self.vista_votaciones:
            self.vista_votaciones = VistaVotaciones(self, self.username)
        self._cambiar_ventana(self.vista_votaciones)

    def mostrar_mis_valoraciones(self, username):
        """
        Muestra la ventana de mis valoraciones.
        """
        if not self.vista_mis_valoraciones:
            self.vista_mis_valoraciones = VistaMisValoraciones(self, username)
        self.vista_mis_valoraciones.show()

    def mostrar_registro(self):
        """
        Muestra la ventana de registro.
        """
        if not self.vista_registro:
            self.vista_registro = VistaRegistro(self)
        self._cambiar_ventana(self.vista_registro)

    def mostrar_sinopsis(self, detalles_pelicula):
        """
        Muestra la ventana de sinopsis para una película específica.

        :param detalles_pelicula: Diccionario con los detalles de la película.
        """
        if not self.vista_sinopsis:
            self.vista_sinopsis = VistaSinopsis(self, self.gestor_peliculas)
        self.vista_sinopsis.mostrar_informacion_pelicula(detalles_pelicula)
        self._cambiar_ventana(self.vista_sinopsis)
    def mostrar_recomendaciones(self, gestor_peliculas, username):
        """
        Muestra la ventana de recomendaciones.
        """
        if not self.vista_recomendaciones:
            self.vista_recomendaciones = VistaRecomendaciones(self, gestor_peliculas, username)
        self._cambiar_ventana(self.vista_recomendaciones)

    def _cambiar_ventana(self, nueva_ventana):
        """
        Cierra la ventana actual y abre una nueva.

        :param nueva_ventana: Instancia de la nueva ventana a mostrar.
        """
        for ventana in [self.vista_login, self.vista_principal, self.vista_registro, self.vista_sinopsis,self.vista_recomendaciones]:
            if ventana and ventana.isVisible():
                ventana.hide()
        nueva_ventana.show()

    def ejecutar(self):
        """
        Ejecuta la aplicación mostrando inicialmente la ventana de login.
        """
        self.mostrar_login()
        self.app.exec_()


if __name__ == "__main__":
    gestor = GestorVentanas()
    gestor.ejecutar()
