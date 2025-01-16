from PyQt5 import QtCore, QtGui, QtNetwork
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout, QHBoxLayout, QLineEdit, QMessageBox, QComboBox
from PyQt5.QtCore import Qt
from gestores.GestorPeliculas import GestorPeliculas

class VistaVotaciones(QMainWindow):
    """
    Clase que representa la ventana de votaciones de películas.
    Permite a los usuarios buscar, seleccionar y valorar películas.
    """

    # Constructor de la clase
    """
    Inicializa la ventana de votaciones, configura la interfaz gráfica
    y conecta los eventos de los botones y campos.

    Parámetros:
        - gestor_ventanas: Instancia del gestor de ventanas para manejar la navegación.
        - username: Nombre del usuario actual que está interactuando con la ventana.

    Excepciones manejadas:
        - Exception: Cualquier error durante la inicialización de la interfaz o el gestor de películas.
    """
    def __init__(self, gestor_ventanas, username):
        super().__init__()
        self.setWindowTitle("Votaciones de Películas")
        self.resize(1200, 800)

        # Referencia al gestor de ventanas
        self.gestor_ventanas = gestor_ventanas

        # Referencia al gestor de películas
        self.gestor_peliculas = GestorPeliculas()

        # Nombre de usuario
        self.username = username

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

        self.button_recomendaciones = QPushButton("Recomendaciones")
        self.button_recomendaciones.clicked.connect(self.mostrar_recomendaciones)
        self.menu_layout.addWidget(self.button_recomendaciones)

        # Título de la ventana
        self.label = QLabel("Votaciones de Películas")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Campo de búsqueda
        search_layout = QHBoxLayout()
        self.layout.addLayout(search_layout)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar película...")
        search_layout.addWidget(self.search_input)

        # Botón de búsqueda
        self.button_buscar = QPushButton("Buscar")
        self.button_buscar.clicked.connect(self.buscar_peliculas)
        search_layout.addWidget(self.button_buscar)

        # Crear un área de desplazamiento para mostrar películas
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Crear un widget de contenido para el área de desplazamiento
        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)

        # Crear un diseño de cuadrícula para el contenido
        self.grid_layout = QGridLayout(self.scroll_content)

        # Campo de texto para mostrar la película seleccionada
        self.selected_movie_edit = QLineEdit()
        self.selected_movie_edit.setPlaceholderText("Película seleccionada")
        self.selected_movie_edit.setReadOnly(True)
        self.layout.addWidget(self.selected_movie_edit)

        # ComboBox para seleccionar la valoración
        self.rating_combo = QComboBox()
        self.rating_combo.addItems(["1 estrella", "2 estrellas", "3 estrellas", "4 estrellas", "5 estrellas"])
        self.layout.addWidget(self.rating_combo)

        # Botón para enviar la valoración
        self.submit_button = QPushButton("Enviar Valoración")
        self.submit_button.clicked.connect(self.enviar_valoracion)
        self.layout.addWidget(self.submit_button)

        # Botón para ver mis valoraciones
        self.button_mis_valoraciones = QPushButton("Ver Mis Valoraciones")
        self.button_mis_valoraciones.clicked.connect(self.mostrar_mis_valoraciones)
        self.layout.addWidget(self.button_mis_valoraciones)

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
            QComboBox {
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
        """)

        # Mostrar películas al azar al cargar la página
        self.mostrar_peliculas_al_azar()

    # Método para cargar películas en la cuadrícula
    """
    Carga las películas proporcionadas en el diseño de cuadrícula.

    Parámetros:
        - peliculas (list): Lista de diccionarios que contienen información de las películas.

    Excepciones manejadas:
        - Exception: Si ocurre un error al cargar las películas.
    """
    def cargar_peliculas(self, peliculas):
        self.limpiar_grid_layout()
        if not peliculas:
            QMessageBox.warning(self, "Advertencia", "No hay películas disponibles para mostrar.")
            return

        self.active_requests = {}
        row, col = 0, 0
        for pelicula in peliculas:
            try:
                image_button = QPushButton()
                image_button.setFixedSize(150, 225)
                image_url = pelicula.get('poster_image_y', '')

                if image_url and QtCore.QUrl(image_url).isValid():
                    manager = QtNetwork.QNetworkAccessManager(self)
                    request = QtNetwork.QNetworkRequest(QtCore.QUrl(image_url))
                    reply = manager.get(request)
                    self.active_requests[reply] = image_button
                    manager.finished.connect(self.onFinished)
                else:
                    image_button.setText("Imagen no disponible")

                image_button.clicked.connect(lambda _, p=pelicula['title']: self.seleccionar_pelicula(p))

                title_label = QLabel(pelicula['title'])
                title_label.setAlignment(Qt.AlignCenter)
                title_label.setWordWrap(True)
                title_label.setFixedWidth(150)

                self.grid_layout.addWidget(image_button, row, col)
                self.grid_layout.addWidget(title_label, row + 1, col)

                col += 1
                if col == 4:
                    col = 0
                    row += 2

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar película: {str(e)}")

    # Método para manejar la finalización de solicitudes de imagen
    """
    Maneja la finalización de las solicitudes de imagen asociadas a las películas.

    Parámetros:
        - reply (QtNetwork.QNetworkReply): Respuesta de la solicitud de imagen.

    Excepciones manejadas:
        - Exception: Cualquier error al procesar la imagen recibida.
    """
    @QtCore.pyqtSlot(QtNetwork.QNetworkReply)
    def onFinished(self, reply):
        button = self.active_requests.pop(reply, None)
        if button:
            image = QtGui.QImage.fromData(reply.readAll())
            if not image.isNull():
                button.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(image).scaled(150, 225, QtCore.Qt.KeepAspectRatio)))
                button.setIconSize(button.size())
            else:
                button.setText("Imagen no disponible")
        reply.deleteLater()


    # Método para buscar películas
    """
    Realiza la búsqueda de películas basándose en el texto ingresado en el campo de búsqueda
    y muestra los resultados en el área de resultados.

    Excepciones manejadas:
        - Exception: Si ocurre un error durante la búsqueda o al cargar los resultados.
    """
    def buscar_peliculas(self):
        nombre = self.search_input.text().strip()  # Eliminar espacios en blanco al inicio y al final
        if not nombre:
            # Si no hay texto, limpia la cuadrícula y muestra todas las películas
            self.mostrar_peliculas_al_azar()
            return

        try:
            # Realizar la búsqueda en el gestor
            resultados = self.gestor_peliculas.buscar_peliculas2(nombre)

            # Limpia la cuadrícula antes de mostrar los nuevos resultados
            self.limpiar_grid_layout()

            if resultados:
                # Cargar los resultados en la cuadrícula
                self.cargar_peliculas(resultados)
            else:
                QMessageBox.information(self, "Sin resultados", f"No se encontraron películas que coincidan con: '{nombre}'")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al buscar películas: {str(e)}")

    # Método para seleccionar una película
    """
    Actualiza el campo de texto con la película seleccionada al hacer clic en una imagen.

    Parámetros:
        - titulo (str): Título de la película seleccionada.
    """
    def seleccionar_pelicula(self, titulo):
        self.selected_movie_edit.setText(titulo)

    # Método para enviar valoración
    """
    Envía la valoración de la película seleccionada.

    Excepciones manejadas:
        - QMessageBox: Si no se ha seleccionado ninguna película.
    """
    def enviar_valoracion(self):
        pelicula = self.selected_movie_edit.text().strip()
        valoracion = self.rating_combo.currentIndex() + 1  # Obtener la valoración seleccionada

        if not pelicula:
            QMessageBox.warning(self, "Error", "Por favor, selecciona una película de la lista.")
            return

        mensaje = self.gestor_peliculas.votar_pelicula(self.username, pelicula, valoracion)
        QMessageBox.information(self, "Valoración Enviada", mensaje)

    # Método para mostrar películas al azar
    """
    Muestra 12 películas al azar en la cuadrícula.

    Excepciones manejadas:
        - Exception: Si ocurre un error al cargar las películas al azar.
    """
    def mostrar_peliculas_al_azar(self):
        try:
            peliculas_al_azar = self.gestor_peliculas.peliculas_al_azar()
            peliculas = self.gestor_peliculas.buscar_peliculas(peliculas_al_azar)
            self.cargar_peliculas(peliculas)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al cargar películas al azar: {str(e)}")

    # Método para limpiar el diseño de cuadrícula
    """
    Elimina todos los widgets del diseño de cuadrícula.
    """
    def limpiar_grid_layout(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    # Método para mostrar la vista principal
    """
    Muestra la vista principal.
    """
    def mostrar_vista_principal(self):
        self.gestor_ventanas.mostrar_principal()

    # Método para mostrar la vista de votaciones
    """
    Muestra la vista de votaciones.
    """
    def mostrar_votaciones(self):
        self.gestor_ventanas.mostrar_votaciones()

    # Método para mostrar la vista de recomendaciones
    """
    Muestra la vista de recomendaciones.
    """
    def mostrar_recomendaciones(self):
        gestor_peliculas = self.gestor_peliculas  # Asegúrate de que esto esté inicializado
        username = self.gestor_ventanas.username  # Asegúrate de que username esté definido
        self.gestor_ventanas.mostrar_recomendaciones(gestor_peliculas, username)

    # Método para mostrar mis valoraciones
    """
    Muestra la ventana de mis valoraciones del usuario actual.
    """
    def mostrar_mis_valoraciones(self):
        self.gestor_ventanas.mostrar_mis_valoraciones(self.username)
