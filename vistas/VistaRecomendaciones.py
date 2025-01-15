from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QListWidget, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from gestores.GestorPeliculas import GestorPeliculas

class VistaRecomendaciones(QMainWindow):
    def __init__(self, gestor_ventanas, gestor_peliculas, username):
        """
        Inicializa la ventana de Recomendaciones.
        """
        super().__init__()
        self.setWindowTitle("Recomendaciones Según las Votaciones")
        self.resize(1200, 800)

        # Referencia al gestor de ventanas
        self.gestor_ventanas = gestor_ventanas

        # Referencia al gestor de películas
        self.gestor_peliculas = gestor_peliculas

        # Nombre de usuario
        self.username = username

        # Asegurarse de que las similitudes estén calculadas
        self.gestor_peliculas._calcular_similitudes_recomendaciones()

        # Configuración de la interfaz gráfica
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Crear el menú de navegación
        self.menu_layout = QHBoxLayout()
        self.layout.addLayout(self.menu_layout)

        # Título de la sección
        self.label_title = QLabel("Recomendaciones Personalizadas")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_title)

        # Selección de la cantidad de películas
        self.label_quantity = QLabel("¿Cuántas películas deseas que te recomendemos?")
        self.label_quantity.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_quantity)

        self.combo_quantity = QComboBox()
        self.combo_quantity.addItems(["5", "10", "15", "20"])
        self.layout.addWidget(self.combo_quantity)

        # Botón para generar recomendaciones
        self.button_recommend = QPushButton("Generar Recomendaciones")
        self.button_recommend.clicked.connect(self.generar_recomendaciones)
        self.layout.addWidget(self.button_recommend)

        # Lista para mostrar las recomendaciones
        self.recommendations_list = QListWidget()
        self.layout.addWidget(self.recommendations_list)

        # Botón para regresar a la vista principal
        self.button_back = QPushButton("Volver a la Vista Principal")
        self.button_back.clicked.connect(self.volver_vista_principal)
        self.layout.addWidget(self.button_back)

        # Aplicar el estilo CSS para mantener la consistencia
        self.setStyleSheet("""
            QWidget {
                background-color: #2E86C1;  /* Fondo azul */
            }
            QLabel {
                color: white;              /* Texto blanco */
                text-align: center;        /* Centrar texto */
                font-size: 28px;           /* Tamaño de fuente */
            }
            QComboBox {
                background-color: #F0F0F0; /* Fondo gris claro */
                border: 1px solid #DADADA;
                border-radius: 5px;
                padding: 10px;
                font-size: 18px;
            }
            QPushButton {
                background-color: #3498DB; /* Azul para botones */
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980B9; /* Azul más oscuro al pasar el ratón */
            }
            QPushButton:pressed {
                background-color: #1F618D; /* Azul aún más oscuro al hacer clic */
            }
            QListWidget {
                background-color: #F0F0F0; /* Fondo gris claro */
                border: 1px solid #DADADA;
                border-radius: 5px;
                font-size: 18px;
            }
        """)

    def generar_recomendaciones(self):
        """
        Genera las recomendaciones basadas en las votaciones del usuario y las muestra en la lista.
        """
        try:
            cantidad = int(self.combo_quantity.currentText())
            recomendaciones = self.gestor_peliculas.recomendar_peliculas_por_usuario(self.username)

            # Ordenar las recomendaciones por similitud de mayor a menor
            recomendaciones_ordenadas = sorted(
                recomendaciones,
                key=lambda x: x['similitud'],
                reverse=True
            )

            # Limitar el número de recomendaciones según la selección
            recomendaciones_ordenadas = recomendaciones_ordenadas[:cantidad]

            # Mostrar las recomendaciones con su similitud
            self.recommendations_list.clear()
            if recomendaciones_ordenadas:
                for pelicula in recomendaciones_ordenadas:
                    self.recommendations_list.addItem(
                        f"{pelicula['titulo']} - Similitud: {pelicula['similitud']:.2f}"
                    )
            else:
                self.recommendations_list.addItem("No se encontraron recomendaciones.")
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error inesperado", f"Ocurrió un error: {str(e)}")

    def volver_vista_principal(self):
        """
        Regresa a la vista principal.
        """
        self.gestor_ventanas.mostrar_principal()
