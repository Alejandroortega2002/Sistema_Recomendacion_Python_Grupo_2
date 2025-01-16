from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QGridLayout,
    QMessageBox
)
from PyQt5 import QtCore, QtGui, QtNetwork
from PyQt5.QtCore import Qt
from gestores.GestorPeliculas import GestorPeliculas


class VistaMisValoraciones(QMainWindow):
    def __init__(self, gestor_ventanas, username):
        """
        Inicializa la ventana de mis valoraciones.
        """
        super().__init__()
        self.setWindowTitle("Mis Valoraciones")
        self.resize(1200, 800)

        # Referencia al gestor de ventanas
        self.gestor_ventanas = gestor_ventanas

        try:
            # Referencia al gestor de películas
            self.gestor_peliculas = GestorPeliculas()
        except Exception as e:
            QMessageBox.critical(self, "Error Crítico", f"Error al cargar el gestor de películas: {e}")
            return

        # Nombre de usuario
        self.username = username

        # Inicializar active_requests para manejar imágenes de recomendaciones
        self.active_requests = {}

        # Configuración de la interfaz gráfica
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Título
        self.label = QLabel("Mis Valoraciones")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Crear un área de desplazamiento para mostrar las valoraciones
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Crear un widget de contenido para las valoraciones
        self.grid_widget = QWidget()
        self.scroll_area.setWidget(self.grid_widget)

        # Crear un diseño de cuadrícula para las valoraciones
        self.grid_layout = QGridLayout(self.grid_widget)

        # Botón para volver
        self.back_button = QPushButton("Volver")
        self.back_button.clicked.connect(self.volver)
        self.layout.addWidget(self.back_button)

        # Cargar las valoraciones del usuario
        try:
            self.cargar_valoraciones()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar las valoraciones: {e}")

        # Aplicar el estilo CSS
        self.setStyleSheet("""
            QWidget {
                background-color: #2E86C1;  /* Fondo azul */
            }
            QLabel {
                color: white;              /* Texto blanco */
                text-align: center;        /* Centrar texto */
                font-size: 32px;           /* Tamaño de fuente más grande para títulos */
                margin-bottom: 20px;       /* Espacio debajo del título */
            }
            QPushButton {
                background-color: #3498DB; /* Azul para botones */
                color: white;
                font-size: 24px;           /* Tamaño de fuente más grande */
                font-weight: bold;         /* Texto en negrita */
                padding: 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980B9; /* Azul más oscuro al pasar el mouse */
            }
        """)

    def cargar_valoraciones(self):
        """
        Carga las valoraciones del usuario en el diseño de cuadrícula.
        """
        valoraciones = self.gestor_peliculas.obtener_valoraciones_usuario(self.username)
        self.limpiar_grid_layout()

        if not valoraciones:
            no_valoraciones_label = QLabel("No tienes valoraciones registradas.")
            no_valoraciones_label.setStyleSheet("font-size: 18px; color: white;")
            self.layout.addWidget(no_valoraciones_label)
            return

        row, col = 0, 0
        for valoracion in valoraciones:
            try:
                titulo = valoracion.get('title', 'Sin título')
                rating = valoracion.get('rating', 0)

                # Crear un botón para la imagen de la película
                image_button = QPushButton()
                image_button.setFixedSize(150, 225)
                image_url = self.gestor_peliculas.obtener_detalles_pelicula(titulo).get('poster_image_y', '')

                if image_url and QtCore.QUrl(image_url).isValid():
                    manager = QtNetwork.QNetworkAccessManager(self)
                    request = QtNetwork.QNetworkRequest(QtCore.QUrl(image_url))
                    reply = manager.get(request)

                    # Asociar el reply al botón
                    self.active_requests[reply] = image_button

                    # Conectar la señal para cargar la imagen
                    manager.finished.connect(self.onFinished)
                else:
                    image_button.setText("Sin Imagen")

                # Crear un widget para el título y la valoración
                title_label = QLabel(f"{titulo}\nValoración: {rating}/5")
                title_label.setAlignment(Qt.AlignCenter)
                title_label.setWordWrap(True)
                title_label.setFixedWidth(150)

                # Añadir los widgets a la cuadrícula
                self.grid_layout.addWidget(image_button, row, col)
                self.grid_layout.addWidget(title_label, row + 1, col)

                col += 1
                if col == 4:  # Cambiar de fila cada 4 columnas
                    col = 0
                    row += 2
            except Exception as e:
                QMessageBox.warning(self, "Advertencia", f"No se pudo cargar la valoración: {e}")

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
            QMessageBox.warning(self, "Advertencia", f"Error al cargar la imagen: {e}")

    def limpiar_grid_layout(self):
        """
        Limpia el diseño de cuadrícula eliminando todos los widgets.
        """
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def volver(self):
        """
        Regresa a la ventana principal.
        """
        try:
            self.gestor_ventanas.mostrar_principal()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo regresar a la ventana principal: {e}")
