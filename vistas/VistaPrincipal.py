from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QMenuBar, QAction,QHBoxLayout
from PyQt5.QtCore import Qt
from gestores.GestorPeliculas import GestorPeliculas

class VistaPrincipal(QMainWindow):
    def __init__(self, gestor_ventanas):
        super().__init__()
        self.setWindowTitle("Buscador de Películas")
        self.resize(1200, 800)
        self.gestor_ventanas = gestor_ventanas
        self.gestor_peliculas = GestorPeliculas()

        # Configuración de la interfaz gráfica
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Crear el menú de navegación
        self.menu_layout = QHBoxLayout()
        self.layout.addLayout(self.menu_layout)

        # Añadir botones al menú de navegación
        self.button_vista_principal = QPushButton("Vista Principal")
        self.button_vista_principal.clicked.connect(self.mostrar_vista_principal)
        self.menu_layout.addWidget(self.button_vista_principal)

        self.button_votaciones = QPushButton("Votaciones")
        self.button_votaciones.clicked.connect(self.mostrar_votaciones)
        self.menu_layout.addWidget(self.button_votaciones)

        # Cambia "Valoraciones" a "Recomendaciones"
        self.button_recomendaciones = QPushButton("Recomendaciones")
        self.button_recomendaciones.clicked.connect(
        self.mostrar_recomendaciones)  # Método para abrir las recomendaciones
        self.menu_layout.addWidget(self.button_recomendaciones)
 
        # Título
        self.label = QLabel("Buscador de Películas")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Campo de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar película...")
        self.search_input.textChanged.connect(self.buscar_peliculas)  # Conectar la señal textChanged
        self.layout.addWidget(self.search_input)

        # Lista de resultados
        self.results_list = QListWidget()
        self.results_list.itemClicked.connect(self.actualizar_pelicula_seleccionada)
        self.layout.addWidget(self.results_list)

        # Mostrar películas al azar al cargar la página
        self.mostrar_peliculas_al_azar()
        
        # Campo de texto para la película seleccionada
        self.selected_movie_edit = QLineEdit()
        self.selected_movie_edit.setPlaceholderText("Película seleccionada")
        self.selected_movie_edit.setReadOnly(True)
        self.layout.addWidget(self.selected_movie_edit)

        # Botón para ver sinopsis
        self.synopsis_button = QPushButton("Ver Sinopsis / Recomendación")
        self.synopsis_button.clicked.connect(self.ver_sinopsis)
        self.layout.addWidget(self.synopsis_button)


        # Aplicar el estilo CSS
        self.setStyleSheet("""
            QWidget {
                background-color: #2E86C1;  /* Fondo azul */
            }
            QLabel {
                color: white;              /* Texto blanco */
                text-align: center;        /* Centrar texto */
                font-size: 32px;           /* Tamaño de fuente más grande para títulos */
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
                font-weight: bold;         /* Texto en negrita */
                padding: 15px;
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
                font-size: 24px;           /* Fuente más grande */
            }
        """)

    def buscar_peliculas(self):
        """
        Realiza la búsqueda de películas y muestra los resultados.
        """
        nombre = self.search_input.text()
        resultados = self.gestor_peliculas.buscar_peliculas(nombre)
        self.results_list.clear()
        if resultados:
            for pelicula in resultados:
                self.results_list.addItem(f"{pelicula['title']} ({pelicula['year']})")
        else:
            self.results_list.addItem("No se encontraron resultados.")

    def actualizar_pelicula_seleccionada(self, item):
        """
        Actualiza el campo de texto con la película seleccionada.
        """
        nombre_pelicula = item.text().split(' (')[0]
        self.selected_movie_edit.setText(nombre_pelicula)

    def ver_sinopsis(self):
        """
        Abre la ventana de sinopsis para la película seleccionada.
        """
        item = self.results_list.currentItem()
        if item:
            nombre_pelicula = item.text().split(' (')[0]
            detalles = self.gestor_peliculas.obtener_detalles_pelicula(nombre_pelicula)
            if detalles:
                self.gestor_ventanas.mostrar_sinopsis(detalles)
            else:
                QMessageBox.warning(self, "Error", "No se encontraron detalles para la película seleccionada.")
        else:
            QMessageBox.warning(self, "Error", "Por favor, selecciona una película de la lista.")
    
     
    def mostrar_peliculas_al_azar(self):
        """
        Muestra 12 películas al azar en la lista de resultados.
        """
        peliculas_al_azar = self.gestor_peliculas.peliculas_al_azar()
        self.results_list.clear()
        for pelicula in peliculas_al_azar:
            self.results_list.addItem(pelicula)

        
    def mostrar_vista_principal(self):
        """
        Muestra la vista principal.
        """
        self.gestor_ventanas.mostrar_principal()

    def mostrar_votaciones(self):
        """
        Muestra la vista de votaciones.
        """
        self.gestor_ventanas.mostrar_votaciones()

    def mostrar_valoraciones(self):
        """
        Muestra la vista de valoraciones.
        """
        self.gestor_ventanas.mostrar_valoraciones()

    def mostrar_recomendaciones(self):
        """
        Muestra la ventana de recomendaciones.
        """
        self.gestor_ventanas.mostrar_recomendaciones(self.gestor_peliculas, self.gestor_ventanas.username)