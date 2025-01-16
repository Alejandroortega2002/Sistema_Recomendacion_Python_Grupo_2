from PyQt5 import QtCore, QtGui, QtNetwork
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout, QComboBox, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt

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

        # Inicializar active_requests para manejar imágenes
        self.active_requests = {}

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
        
        self.button_mostrar_votaciones = QPushButton("Votaciones")
        self.button_mostrar_votaciones.clicked.connect(self.mostrar_votaciones)
        self.menu_layout.addWidget(self.button_mostrar_votaciones)  # Aquí se usa el nombre correcto
        
        self.button_mostrar_recomendaciones = QPushButton("Recomendaciones")
        self.button_mostrar_recomendaciones.clicked.connect(self.ir_mostrar_recomendaciones)
        self.menu_layout.addWidget(self.button_mostrar_recomendaciones)


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

        # Área de desplazamiento para las recomendaciones
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Widget de contenido para las recomendaciones
        self.recommendations_content = QWidget()
        self.scroll_area.setWidget(self.recommendations_content)

        # Diseño de cuadrícula para las recomendaciones
        self.grid_layout = QGridLayout(self.recommendations_content)

        # Aplicar el estilo CSS
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
            QScrollArea {
                background-color: #F0F0F0;
            }
        """)

    def generar_recomendaciones(self):
        """
        Genera las recomendaciones basadas en las votaciones del usuario y las muestra en formato de cuadrícula.
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

            # Mostrar las recomendaciones
            self.mostrar_recomendaciones(recomendaciones_ordenadas)

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error inesperado", f"Ocurrió un error: {str(e)}")

    def mostrar_recomendaciones(self, recomendaciones):
        """
        Muestra las recomendaciones en formato de cuadrícula con imágenes, títulos y similitudes.
        """
        # Limpiar la cuadrícula de recomendaciones
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if not recomendaciones:
            no_recommendation_label = QLabel("No se encontraron recomendaciones.")
            no_recommendation_label.setStyleSheet("font-size: 18px; color: white;")
            self.grid_layout.addWidget(no_recommendation_label, 0, 0, 1, 4)
            return

        # Mostrar las recomendaciones
        row, col = 0, 0
        for rec in recomendaciones:
            titulo = rec["titulo"]
            similitud = rec["similitud"]
            image_button = QPushButton()
            image_button.setFixedSize(150, 225)  # Tamaño fijo para la imagen
            image_url = self.gestor_peliculas.obtener_detalles_pelicula(titulo).get('poster_image_y', '')

            if image_url and QtCore.QUrl(image_url).isValid():
                manager = QtNetwork.QNetworkAccessManager(self)
                request = QtNetwork.QNetworkRequest(QtCore.QUrl(image_url))
                reply = manager.get(request)

                # Asociar el reply al botón
                self.active_requests[reply] = image_button

                # Conectar el manejador general
                manager.finished.connect(self.onFinished)
            else:
                image_button.setText("Sin Imagen")

            image_button.clicked.connect(lambda _, p=titulo: self.mostrar_pelicula_recomendada(p))

            # Crear el widget para el título y la similitud
            title_label = QLabel(f"{titulo}\nSimilitud: {similitud:.2f}")
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setWordWrap(True)
            title_label.setFixedWidth(150)
            title_label.setStyleSheet("font-size: 16px; color: white;")

            # Añadir los widgets a la cuadrícula
            self.grid_layout.addWidget(image_button, row, col)
            self.grid_layout.addWidget(title_label, row + 1, col)

            col += 1
            if col == 4:  # Máximo 4 columnas
                col = 0
                row += 2

    @QtCore.pyqtSlot(QtNetwork.QNetworkReply)
    def onFinished(self, reply):
        """
        Maneja la finalización de la solicitud de imagen y asigna la imagen al botón correspondiente.
        """
        button = self.active_requests.pop(reply, None)
        if button:
            image = QtGui.QImage.fromData(reply.readAll())
            if not image.isNull():
                button.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(image).scaled(150, 225, QtCore.Qt.KeepAspectRatio)))
                button.setIconSize(button.size())
            else:
                button.setText("Imagen no disponible")
        reply.deleteLater()

    def mostrar_pelicula_recomendada(self, titulo):
        """
        Muestra la sinopsis y detalles de una película recomendada.

        :param titulo: Título de la película recomendada.
        """
        detalles = self.gestor_peliculas.obtener_detalles_pelicula(titulo)
        self.gestor_ventanas.mostrar_sinopsis(detalles)

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

    def ir_mostrar_recomendaciones(self):
        """
        Muestra la vista de recomendaciones.
        """
        gestor_peliculas = self.gestor_peliculas  # Asegúrate de que esto esté inicializado
        username = self.gestor_ventanas.username  # Asegúrate de que username esté definido
        self.gestor_ventanas.mostrar_recomendaciones(gestor_peliculas, username)
