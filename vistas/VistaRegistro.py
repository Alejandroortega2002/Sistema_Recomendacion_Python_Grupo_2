from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from gestores.GestorUsuarios import GestorUsuarios


class VistaRegistro(QMainWindow):
    def __init__(self, gestor_ventanas):
        """
        Inicializa la ventana de registro de usuarios.
        """
        super().__init__()
        self.setWindowTitle("Registro de Usuario")
        self.resize(1200, 800)

        # Referencia al gestor de ventanas
        self.gestor_ventanas = gestor_ventanas

        # Referencia al gestor de usuarios
        self.gestor_usuarios = GestorUsuarios()

        # Configuración de la interfaz gráfica
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

          # Estilo general de la ventana y sus elementos
        self.setStyleSheet("""
            QWidget {
                background-color: #2E86C1;  /* Fondo azul */
            }
            QLabel {
                color: white;              /* Texto blanco */
            }
            QLineEdit {
                background-color: #F0F0F0; /* Fondo gris claro */
                border: 1px solid #DADADA;
                border-radius: 5px;
                padding: 15px;
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

        # Título
        self.label = QLabel("Registrarse")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Campo de nombre de usuario
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nombre de usuario")
        self.layout.addWidget(self.username_input)

        # Campo de contraseña
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        # Botón de registro
        self.register_button = QPushButton("Registrarse")
        self.register_button.clicked.connect(self.registrar_usuario)
        self.layout.addWidget(self.register_button)

        # Botón para volver al login
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.volver_a_login)
        self.layout.addWidget(self.login_button)

    def registrar_usuario(self):
        """
        Maneja la lógica de registro de un nuevo usuario.
        """
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            mensaje = self.gestor_usuarios.registrar_usuario(username, password)
            if "éxito" in mensaje.lower():
                QMessageBox.information(self, "Éxito", mensaje)
                self.gestor_ventanas.mostrar_login()
            else:
                QMessageBox.warning(self, "Error", mensaje)
        else:
            QMessageBox.warning(self, "Error", "Por favor, completa todos los campos.")

    def volver_a_login(self):
        """
        Cierra la ventana de registro y muestra la ventana de login.
        """
        self.gestor_ventanas.mostrar_login()
