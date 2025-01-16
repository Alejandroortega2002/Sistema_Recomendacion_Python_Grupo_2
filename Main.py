from PyQt5.QtWidgets import QApplication, QMessageBox
from gestores.GestorVentanas import GestorVentanas

def main():
    """
    Punto de entrada principal para la aplicación.
    Inicializa la aplicación, configura el gestor de ventanas y maneja errores críticos.

    Excepciones manejadas:
        - Exception: Cualquier error inesperado durante el arranque de la aplicación.
    """
    try:
        app = QApplication([])

        # Crear instancia del gestor de ventanas
        gestor = GestorVentanas()

        # Mostrar la ventana de login al inicio
        gestor.mostrar_login()

        # Ejecutar la aplicación
        app.exec_()

    except Exception as e:
        # Manejo de errores críticos que podrían ocurrir en el arranque de la aplicación
        QMessageBox.critical(None, "Error Crítico", f"Ocurrió un error inesperado: {str(e)}")

if __name__ == "__main__":
    main()
