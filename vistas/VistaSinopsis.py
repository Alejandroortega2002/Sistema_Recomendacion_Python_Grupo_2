from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from gestores.GestorPeliculas import GestorPeliculas

class VistaSinopsis(QMainWindow):
    def __init__(self, gestor_ventanas, gestor_peliculas):
        """
        Inicializa la ventana de sinopsis.
        """
        super().__init__()
        self.setWindowTitle("Sinopsis de la Película")
        self.resize(1200, 800)

        # Referencia al gestor de ventanas
        self.gestor_ventanas = gestor_ventanas

        # Referencia al gestor de películas
        self.gestor_peliculas = gestor_peliculas

        # Configuración de la interfaz gráfica
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Aplicar el estilo CSS
        self.setStyleSheet("""
            QWidget {
                background-color: #2E86C1;  /* Fondo azul */
            }
            QLabel {
                color: white;              /* Texto blanco */
            }
            QLineEdit, QTextEdit {
                background-color: #F0F0F0; /* Fondo gris claro */
                border: 1px solid #DADADA;
                border-radius: 5px;
                padding: 10px;
                font-size: 24px;           /* Fuente más grande */
            }
            QPushButton {
                background-color: #3498DB; /* Azul para botones */
                color: white;
                font-size: 24px;           /* Fuente más grande */
                padding: 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980B9; /* Azul más oscuro al pasar el mouse */
            }
        """)

        # Título de la película
        self.title_label = QLabel("Título de la Película")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Sinopsis
        self.synopsis_text = QTextEdit()
        self.synopsis_text.setReadOnly(True)
        self.layout.addWidget(self.synopsis_text)
        # Layout para mostrar recomendaciones de películas
        self.recommendations_layout = QVBoxLayout()
        self.layout.addLayout(self.recommendations_layout)

        # Detalles adicionales
        self.details_layout = QGridLayout()
        self.layout.addLayout(self.details_layout)

        # Botón para volver
        self.back_button = QPushButton("Volver")
        self.back_button.clicked.connect(self.volver)
        self.layout.addWidget(self.back_button)

    def mostrar_informacion_pelicula(self, detalles):
        """
        Muestra la información de la película en la vista.

        :param detalles: Diccionario con los detalles de la película.
        """
        self.title_label.setText(detalles.get("title", "Título no disponible"))
        self.synopsis_text.setText(detalles.get("synopsis", "Sinopsis no disponible"))

        # Limpiar detalles adicionales
        for i in reversed(range(self.details_layout.count())):
            widget = self.details_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Añadir nuevos detalles
        detalles_items = {
            "Año": detalles.get("year", "No disponible"),
            "Género": detalles.get("genre", "No disponible"),
            "Director": detalles.get("director", "No disponible"),
            "Duración": detalles.get("runtime", "No disponible")
        }

        for i, (label, value) in enumerate(detalles_items.items()):
            label_widget = QLabel(f"{label}:")
            value_widget = QLabel(str(value))  # Convertir el valor a cadena
            label_widget.setStyleSheet("font-size: 18px; color: white;")
            value_widget.setStyleSheet("font-size: 18px; color: white;")
            self.details_layout.addWidget(label_widget, i, 0)
            self.details_layout.addWidget(value_widget, i, 1)

        # Mostrar recomendaciones después de cargar los detalles de la película
        self.mostrar_recomendaciones(detalles.get("title"))

    def mostrar_recomendaciones(self, title):
        """
        Muestra las películas recomendadas debajo de la sinopsis, incluyendo la similitud.

        :param title: Título de la película para generar recomendaciones.
        """
        # Limpiar recomendaciones existentes
        for i in reversed(range(self.recommendations_layout.count())):
            widget = self.recommendations_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Obtener recomendaciones
        try:
            recomendaciones = self.gestor_peliculas.recomendar_peliculas(title)
        except ValueError as e:
            recomendaciones = []

        # Añadir botones para las recomendaciones
        if recomendaciones:
            for rec in recomendaciones:
                titulo = rec["titulo"]
                similitud = rec["similitud"]
                button = QPushButton(f"{titulo} (Similitud: {similitud:.2f})")
                button.clicked.connect(lambda _, p=titulo: self.mostrar_pelicula_recomendada(p))
                button.setStyleSheet("font-size: 18px; color: white;")
                self.recommendations_layout.addWidget(button)
        else:
            no_recommendation_label = QLabel("No hay recomendaciones disponibles.")
            no_recommendation_label.setStyleSheet("font-size: 18px; color: white;")
            self.recommendations_layout.addWidget(no_recommendation_label)
    def mostrar_pelicula_recomendada(self, title):
        """
        Muestra la sinopsis y detalles de una película recomendada.

        :param title: Título de la película recomendada.
        """
        detalles = self.gestor_peliculas.obtener_detalles_pelicula(title)
        self.mostrar_informacion_pelicula(detalles)

    def volver(self):
        """
        Regresa a la ventana principal.
        """
        self.gestor_ventanas.mostrar_principal()
