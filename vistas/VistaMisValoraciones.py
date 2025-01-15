from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
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

        # Referencia al gestor de películas
        self.gestor_peliculas = GestorPeliculas()

        # Nombre de usuario
        self.username = username

        # Configuración de la interfaz gráfica
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Título
        self.label = QLabel("Mis Valoraciones")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Tabla de valoraciones
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Título", "Nota"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.layout.addWidget(self.table)

        # Cargar las valoraciones del usuario
        self.cargar_valoraciones()

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
            QTableWidget {
                background-color: #F0F0F0; /* Fondo gris claro */
                border: 1px solid #DADADA;
                border-radius: 5px;
                font-size: 24px;           /* Fuente más grande */
                margin: 20px;              /* Margen alrededor de la tabla */
            }
            QHeaderView::section {
                background-color: #3498DB; /* Azul para encabezados */
                color: white;
                font-size: 24px;           /* Fuente más grande */
                font-weight: bold;         /* Texto en negrita */
                padding: 10px;
                border: 1px solid #DADADA;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #3498DB; /* Azul para la esquina */
                border: 1px solid #DADADA;
            }
            QTableWidget::item {
                padding: 10px;             /* Espacio dentro de las celdas */
            }
        """)

    def cargar_valoraciones(self):
        """
        Carga las valoraciones del usuario en la tabla.
        """
        valoraciones = self.gestor_peliculas.obtener_valoraciones_usuario(self.username)
        self.table.setRowCount(len(valoraciones))
        for row, valoracion in enumerate(valoraciones):
            self.table.setItem(row, 0, QTableWidgetItem(valoracion['title']))
            self.table.setItem(row, 1, QTableWidgetItem(str(valoracion['rating'])))