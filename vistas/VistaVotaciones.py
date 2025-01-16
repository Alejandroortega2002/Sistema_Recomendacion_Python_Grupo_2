from PyQt5 import QtCore, QtGui, QtNetwork
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout, QHBoxLayout, QLineEdit, QMessageBox,QComboBox
from PyQt5.QtCore import Qt
from gestores.GestorPeliculas import GestorPeliculas

class VistaVotaciones(QMainWindow):
    def __init__(self, gestor_ventanas, username):
        """
        Inicializa la ventana de votaciones.
        """
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

        # Título
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
        
        # Crear un área de desplazamiento
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Crear un widget de contenido para el área de desplazamiento
        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)

        # Crear un diseño de cuadrícula para el contenido
        self.grid_layout = QGridLayout(self.scroll_content)
        
        # Campo de texto para la película seleccionada
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
        # Mostrar películas al azar al cargar la página
        self.mostrar_peliculas_al_azar()

    def cargar_peliculas(self, peliculas):
        """
        Carga las películas y las muestra en la cuadrícula.
        """
        self.limpiar_grid_layout()
        if not peliculas:
            QMessageBox.warning(self, "Advertencia", "No hay películas disponibles para mostrar.")
            return
    
        # Crear un diccionario para asociar solicitudes con botones
        self.active_requests = {}
    
        row = 0
        col = 0
        for pelicula in peliculas:
            # Crear un botón para la imagen
            image_button = QPushButton()
            image_button.setFixedSize(150, 225)  # Tamaño fijo para la imagen
            image_url = pelicula.get('poster_image_y', '')
    
            # Validar que la URL sea válida
            if image_url and QtCore.QUrl(image_url).isValid():
                manager = QtNetwork.QNetworkAccessManager(self)
    
                # Asociar el botón con la solicitud
                request = QtNetwork.QNetworkRequest(QtCore.QUrl(image_url))
                reply = manager.get(request)
                self.active_requests[reply] = image_button
    
                # Conectar la señal de finalización
                manager.finished.connect(self.onFinished)
            else:
                image_button.setText("Imagen no disponible")
    
            # Conectar el evento de clic al título de la película
            image_button.clicked.connect(lambda _, p=pelicula['title']: self.seleccionar_pelicula(p))
    
            # Crear un widget para el título
            title_label = QLabel(pelicula['title'])
            title_label.setAlignment(QtCore.Qt.AlignCenter)
            title_label.setWordWrap(True)  # Habilitar el ajuste de texto
            title_label.setFixedWidth(150)  # Igualar el ancho al de la imagen
    
            # Añadir los widgets a la cuadrícula
            self.grid_layout.addWidget(image_button, row, col)
            self.grid_layout.addWidget(title_label, row + 1, col)
            col += 1
            if col == 4:
                col = 0
                row += 2



    @QtCore.pyqtSlot(QtNetwork.QNetworkReply)
    def onFinished(self, reply):
        """
        Maneja la finalización de la solicitud de imagen.
        """
        # Obtener el botón asociado a esta solicitud
        button = self.active_requests.pop(reply, None)

        if button is not None:
            image = QtGui.QImage.fromData(reply.readAll())
            if not image.isNull():
                button.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(image).scaled(150, 225, QtCore.Qt.KeepAspectRatio)))
                button.setIconSize(button.size())
            else:
                button.setText("Imagen no disponible")

        reply.deleteLater()


    def buscar_peliculas(self):
        """
        Realiza la búsqueda de películas basándose en el texto ingresado en el campo de búsqueda
        y muestra los resultados en el área de resultados.
        """
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
    

    def seleccionar_pelicula(self, titulo):
        """
        Actualiza el campo de texto con la película seleccionada al hacer clic en una imagen.
        """
        self.selected_movie_edit.setText(titulo)

    def enviar_valoracion(self):
        """
        Envía la valoración de la película seleccionada.
        """
        pelicula = self.selected_movie_edit.text().strip()
        valoracion = self.rating_combo.currentIndex() + 1  # Obtener la valoración seleccionada

        if not pelicula:
            QMessageBox.warning(self, "Error", "Por favor, selecciona una película de la lista.")
            return

        mensaje = self.gestor_peliculas.votar_pelicula(self.username, pelicula, valoracion)
        QMessageBox.information(self, "Valoración Enviada", mensaje)

    def mostrar_peliculas_al_azar(self):
        """
        Muestra 12 películas al azar en la cuadrícula.
        """
        try:
            peliculas_al_azar = self.gestor_peliculas.peliculas_al_azar()
            peliculas = self.gestor_peliculas.buscar_peliculas(peliculas_al_azar)
            self.cargar_peliculas(peliculas)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al cargar películas al azar: {str(e)}")


    def limpiar_grid_layout(self):
        """
        Elimina todos los widgets del grid layout.
        """
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
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

    def mostrar_recomendaciones(self):
        """
        Muestra la vista de recomendaciones.
        """
        gestor_peliculas = self.gestor_peliculas  # Asegúrate de que esto esté inicializado
        username = self.gestor_ventanas.username  # Asegúrate de que username esté definido
        self.gestor_ventanas.mostrar_recomendaciones(gestor_peliculas, username)
 

    def mostrar_mis_valoraciones(self):
        self.gestor_ventanas.mostrar_mis_valoraciones(self.username)