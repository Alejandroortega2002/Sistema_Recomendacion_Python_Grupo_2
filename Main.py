from PyQt5.QtWidgets import QApplication
from gestores.GestorVentanas import GestorVentanas

def main():
    """
    Punto de entrada principal para la aplicación.
    """
    app = QApplication([])

    # Crear instancia del gestor de ventanas
    gestor = GestorVentanas()

    # Mostrar la ventana de login al inicio
    gestor.mostrar_login()

    # Ejecutar la aplicación
    app.exec_()

if __name__ == "__main__":
    main()