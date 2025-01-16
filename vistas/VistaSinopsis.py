from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QGridLayout, QScrollArea, QMessageBox
from PyQt5 import QtCore, QtGui, QtNetwork
from PyQt5.QtCore import Qt


class VistaSinopsis(QMainWindow):
    def __init__(self, gestor_ventanas, gestor_peliculas):
        """
        Inicializa la ventana de sinopsis.
        """
        super().__init__()
        self.setWindowTitle("Sinopsis de la Película")
        self.resize(1200, 800)

        # Referencia al gestor de ventanas y películas
        self.gestor_ventanas = gestor_ventanas
        self.gestor_peliculas = gestor_peliculas

        # Inicializar active_requests para manejar imágenes de recomendaciones
        self.active_requests = {}

        try:
            # Crear un área de scroll para todo el contenido
            self.scroll_area = QScrollArea()
            self.scroll_area.setWidgetResizable(True)
            self.setCentralWidget(self.scroll_area)

            # Widget contenedor dentro del scroll
            self.scroll_content = QWidget()
            self.scroll_area.setWidget(self.scroll_content)

            # Layout principal del contenido
            self.layout = QVBoxLayout(self.scroll_content)

            # Aplicar estilo CSS
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

            # Detalles adicionales centrados
            self.details_layout = QVBoxLayout()
            self.details_widget = QWidget()
            self.details_widget.setLayout(self.details_layout)
            self.layout.addWidget(self.details_widget, alignment=Qt.AlignCenter)

            # Título para las recomendaciones
            self.recommendations_label = QLabel("Otras Películas Que Podrían Interesarte")
            self.recommendations_label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(self.recommendations_label)

            # Área de recomendaciones
            self.recommendations_scroll_area = QScrollArea()
            self.recommendations_scroll_area.setWidgetResizable(True)
            self.layout.addWidget(self.recommendations_scroll_area)

            # Widget de contenido para las recomendaciones
            self.recommendations_content = QWidget()
            self.recommendations_scroll_area.setWidget(self.recommendations_content)

            # Diseño de cuadrícula para las recomendaciones
            self.recommendations_layout = QGridLayout(self.recommendations_content)

            # Botón para volver
            self.back_button = QPushButton("Volver")
            self.back_button.clicked.connect(self.volver)
            self.layout.addWidget(self.back_button)

        except Exception as e:
            QMessageBox.critical(self, "Error Crítico", f"Error al inicializar la ventana: {str(e)}")

    def mostrar_informacion_pelicula(self, detalles):
        """
        Muestra la información de la película en la vista.

        :param detalles: Diccionario con los detalles de la película.
        """
        try:
            self.title_label.setText(detalles.get("title", "Título no disponible"))
            self.synopsis_text.setText(detalles.get("synopsis", "Sinopsis no disponible"))

            # Limpiar detalles adicionales
            while self.details_layout.count():
                item = self.details_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

            # Añadir nuevos detalles centrados
            detalles_items = {
                "Año": detalles.get("year", "No disponible"),
                "Género": detalles.get("genre", "No disponible"),
                "Director": detalles.get("director", "No disponible"),
                "Duración": detalles.get("runtime", "No disponible")
            }

            for label, value in detalles_items.items():
                detail_label = QLabel(f"{label}: {value}")
                detail_label.setStyleSheet("font-size: 18px; color: white; text-align: center;")
                detail_label.setAlignment(Qt.AlignCenter)
                self.details_layout.addWidget(detail_label)

            # Mostrar recomendaciones después de cargar los detalles de la película
            self.mostrar_recomendaciones(detalles.get("title"))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar información de la película: {str(e)}")

    def mostrar_recomendaciones(self, title):
        """
        Muestra las películas recomendadas en formato de cuadrícula.
        """
        try:
            # Limpiar la cuadrícula de recomendaciones
            while self.recommendations_layout.count():
                item = self.recommendations_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

            # Obtener recomendaciones (máximo 8 películas)
            recomendaciones = self.gestor_peliculas.recomendar_peliculas(title)[:8]

            if recomendaciones:
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

                    title_label = QLabel(f"{titulo}\n(Similitud: {similitud:.2f})")
                    title_label.setAlignment(Qt.AlignCenter)
                    title_label.setWordWrap(True)
                    title_label.setFixedWidth(150)

                    self.recommendations_layout.addWidget(image_button, row, col)
                    self.recommendations_layout.addWidget(title_label, row + 1, col)

                    col += 1
                    if col == 4:
                        col = 0
                        row += 2
            else:
                raise ValueError("No se encontraron recomendaciones para esta película.")

        except ValueError as ve:
            no_recommendation_label = QLabel(str(ve))
            no_recommendation_label.setStyleSheet("font-size: 18px; color: white;")
            self.recommendations_layout.addWidget(no_recommendation_label)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar recomendaciones: {str(e)}")

    @QtCore.pyqtSlot(QtNetwork.QNetworkReply)
    def onFinished(self, reply):
        """
        Maneja la finalización de la solicitud de imagen y asigna la imagen al botón correspondiente.
        """
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
            QMessageBox.critical(self, "Error", f"Error al cargar imagen: {str(e)}")

    def mostrar_pelicula_recomendada(self, title):
        """
        Muestra la sinopsis y detalles de una película recomendada.

        :param title: Título de la película recomendada.
        """
        try:
            detalles = self.gestor_peliculas.obtener_detalles_pelicula(title)
            self.mostrar_informacion_pelicula(detalles)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al mostrar la película recomendada: {str(e)}")

    def volver(self):
        """
        Regresa a la ventana principal.
        """
        try:
            self.gestor_ventanas.mostrar_principal()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al volver a la ventana principal: {str(e)}")
