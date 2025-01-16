from PyQt5 import QtCore, QtGui, QtNetwork
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout, QComboBox, QMessageBox, QHBoxLayout
import pandas as pd
from PyQt5.QtCore import Qt

class VistaRecomendaciones(QMainWindow):
    """
    Clase que representa la ventana de Recomendaciones personalizadas basada en las votaciones del usuario.
    """

    # Constructor de la clase
    """
    Inicializa la ventana de Recomendaciones, configura la interfaz gráfica
    y conecta los eventos necesarios para generar recomendaciones.

    Parámetros:
        - gestor_ventanas: Instancia del gestor de ventanas para manejar la navegación.
        - gestor_peliculas: Instancia del gestor de películas para manejar los datos.
        - username: Nombre de usuario del cliente actual.

    Excepciones manejadas:
        - Exception: Cualquier error durante la inicialización del gestor de películas o la interfaz.
    """
    def __init__(self, gestor_ventanas, gestor_peliculas, username):
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
        try:
            self.gestor_peliculas._calcular_similitudes_recomendaciones()
        except Exception as e:
            QMessageBox.critical(self, "Error Crítico", f"Error al calcular similitudes: {str(e)}")

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
        self.menu_layout.addWidget(self.button_mostrar_votaciones)

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

    # Método para generar recomendaciones
    """
    Genera las recomendaciones basadas en las votaciones del usuario y las muestra en formato de cuadrícula.

    Excepciones manejadas:
        - ValueError: Si no se encuentran recomendaciones.
        - Exception: Cualquier error durante el cálculo o visualización de las recomendaciones.
    """
    def generar_recomendaciones(self):
        try:
            # Recargar usuarios_df para obtener las votaciones más recientes
            self.gestor_peliculas.usuarios_df = pd.read_csv(self.gestor_peliculas.file_path_usuarios)

            cantidad = int(self.combo_quantity.currentText())
            recomendaciones = self.gestor_peliculas.recomendar_peliculas_por_usuario(self.username)

            if not recomendaciones:
                raise ValueError("No se encontraron recomendaciones para este usuario.")

            recomendaciones_ordenadas = sorted(
                recomendaciones,
                key=lambda x: x['similitud_ajustada'],  # Ordenar por similitud ajustada
                reverse=True
            )[:cantidad]

            self.mostrar_recomendaciones(recomendaciones_ordenadas)
        except ValueError as e:
            QMessageBox.warning(self, "Advertencia", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error inesperado al generar recomendaciones: {str(e)}")

    # Método para mostrar recomendaciones
    """
    Muestra las recomendaciones en formato de cuadrícula con imágenes, títulos y similitudes.

    Parámetros:
        - recomendaciones (list): Lista de diccionarios con información de las películas recomendadas.

    Excepciones manejadas:
        - Exception: Cualquier error durante la visualización de las recomendaciones.
    """
    def mostrar_recomendaciones(self, recomendaciones):
        try:
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
                try:
                    titulo = rec["titulo"]
                    similitud = rec["similitud"]

                    # Botón para la imagen
                    image_button = QPushButton()
                    image_button.setFixedSize(150, 225)
                    image_url = self.gestor_peliculas.obtener_detalles_pelicula(titulo).get('poster_image_y', '')

                    if image_url and QtCore.QUrl(image_url).isValid():
                        manager = QtNetwork.QNetworkAccessManager(self)
                        request = QtNetwork.QNetworkRequest(QtCore.QUrl(image_url))
                        reply = manager.get(request)
                        self.active_requests[reply] = image_button
                        manager.finished.connect(self.onFinished)
                    else:
                        image_button.setText("Sin Imagen")

                    image_button.clicked.connect(lambda _, p=titulo: self.mostrar_pelicula_recomendada(p))

                    # Título y similitud
                    title_label = QLabel(f"{titulo}\nSimilitud: {similitud:.2f}")
                    title_label.setAlignment(Qt.AlignCenter)
                    title_label.setWordWrap(True)
                    title_label.setFixedWidth(150)
                    title_label.setStyleSheet("font-size: 16px; color: white;")

                    # Añadir a la cuadrícula
                    self.grid_layout.addWidget(image_button, row, col)
                    self.grid_layout.addWidget(title_label, row + 1, col)

                    col += 1
                    if col == 4:  # Máximo 4 columnas
                        col = 0
                        row += 2
                except Exception as e:
                    QMessageBox.warning(self, "Advertencia", f"Error al procesar recomendación: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error Crítico", f"Error al mostrar recomendaciones: {str(e)}")

    # Método: onFinished
    # Maneja la finalización de una solicitud de imagen y asigna la imagen descargada a un botón correspondiente.
    #
    # Parámetros:
    #     - reply (QtNetwork.QNetworkReply): Respuesta de la solicitud HTTP que contiene los datos de la imagen.
    #
    # Funcionalidad:
    #     - Recupera el botón asociado a la solicitud HTTP.
    #     - Carga los datos de la imagen desde la respuesta.
    #     - Asigna la imagen al botón si es válida, o muestra un mensaje de error en el botón si no lo es.
    #
    # Excepciones manejadas:
    #     - Exception: Cualquier error que ocurra durante el procesamiento de la imagen.
    @QtCore.pyqtSlot(QtNetwork.QNetworkReply)
    def onFinished(self, reply):
        try:
            button = self.active_requests.pop(reply, None)
            if button:
                image = QtGui.QImage.fromData(reply.readAll())
                if not image.isNull():
                    button.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(image).scaled(150, 225, QtCore.Qt.KeepAspectRatio)))
                    button.setIconSize(button.size())
                else:
                    button.setText("Imagen no disponible")
            reply.deleteLater()
        except Exception as e:
            QMessageBox.warning(self, "Advertencia", f"Error al cargar imagen: {str(e)}")
    
    # Método: mostrar_pelicula_recomendada
    # Muestra la sinopsis y los detalles de una película recomendada.
    #
    # Parámetros:
    #     - titulo (str): Título de la película cuya información se mostrará.
    #
    # Funcionalidad:
    #     - Recupera los detalles de la película usando el gestor de películas.
    #     - Llama a un método del gestor de ventanas para mostrar la sinopsis y los detalles.
    #
    # Excepciones manejadas:
    #     - ValueError: Si no se encuentran detalles para la película seleccionada.
    #     - Exception: Si ocurre un error inesperado durante el proceso.
    def mostrar_pelicula_recomendada(self, titulo):
        try:
            detalles = self.gestor_peliculas.obtener_detalles_pelicula(titulo)
            if not detalles:
                raise ValueError("No se encontraron detalles para la película seleccionada.")
            self.gestor_ventanas.mostrar_sinopsis(detalles)
        except ValueError as e:
            QMessageBox.warning(self, "Advertencia", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al mostrar detalles de la película: {str(e)}")
    
    # Método: mostrar_vista_principal
    # Navega y muestra la vista principal de la aplicación.
    #
    # Funcionalidad:
    #     - Utiliza el gestor de ventanas para cambiar a la vista principal.
    #
    # Excepciones manejadas:
    #     - Exception: Si ocurre un error al mostrar la vista principal.
    def mostrar_vista_principal(self):
        try:
            self.gestor_ventanas.mostrar_principal()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al mostrar la vista principal: {str(e)}")
    
    # Método: mostrar_votaciones
    # Navega y muestra la vista de votaciones.
    #
    # Funcionalidad:
    #     - Utiliza el gestor de ventanas para cambiar a la vista de votaciones.
    #
    # Excepciones manejadas:
    #     - Exception: Si ocurre un error al mostrar la vista de votaciones.
    def mostrar_votaciones(self):
        try:
            self.gestor_ventanas.mostrar_votaciones()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al mostrar la vista de votaciones: {str(e)}")
    
    # Método: ir_mostrar_recomendaciones
    # Navega y muestra la vista de recomendaciones personalizadas para el usuario actual.
    #
    # Funcionalidad:
    #     - Utiliza el gestor de ventanas para mostrar la vista de recomendaciones.
    #     - Asegura que el gestor de películas y el nombre de usuario estén correctamente inicializados.
    #
    # Excepciones manejadas:
    #     - Exception: Si ocurre un error al cargar o mostrar las recomendaciones.
    def ir_mostrar_recomendaciones(self):
        try:
            gestor_peliculas = self.gestor_peliculas  # Asegúrate de que esto esté inicializado
            username = self.gestor_ventanas.username  # Asegúrate de que username esté definido
            self.gestor_ventanas.mostrar_recomendaciones(gestor_peliculas, username)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al mostrar recomendaciones: {str(e)}")
    
       