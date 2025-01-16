from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from gestores.GestorUsuarios import GestorUsuarios

class VistaLogin(QMainWindow):
    def __init__(self, gestor_ventanas):
        """
        Inicializa la ventana de inicio de sesión.
        """
        super().__init__()
        self.setWindowTitle("Iniciar Sesión")
        self.resize(1200, 800)

        # Referencia al gestor de ventanas
        self.gestor_ventanas = gestor_ventanas

        # Referencia al gestor de usuarios
        self.gestor_usuarios = GestorUsuarios()

        # Configuración de la interfaz gráfica
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)  # Centrar todo el layout

        # Título
        self.label = QLabel("Inicio de Sesión")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Campo de texto para el nombre de usuario
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Nombre de usuario")
        self.layout.addWidget(self.username_edit)

        # Campo de texto para la contraseña
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Contraseña")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_edit)

        # Botón de inicio de sesión
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.iniciar_sesion)
        self.layout.addWidget(self.login_button)

        # Botón para ir al registro
        self.register_button = QPushButton("Registrarse")
        self.register_button.clicked.connect(self.ir_a_registro)
        self.layout.addWidget(self.register_button)

        self.setStyleSheet("""
            QWidget {
                background-color: #2E86C1;  /* Fondo azul */
            }
            QLabel {
                color: white;              /* Texto blanco */
                text-align: center;        /* Centrar texto */
                font-size: 32px;           /* Tamaño de fuente más grande para títulos */
            }
            QLineEdit {
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
                background-color: #2980B9; /* Azul más oscuro al pasar el ratón */
            }
            QPushButton:pressed {
                background-color: #1F618D; /* Azul aún más oscuro al hacer clic */
            }
        """)

    def iniciar_sesion(self):
        """
        Maneja la lógica de inicio de sesión.
        """
        username = self.username_edit.text()
        password = self.password_edit.text()

        valido, mensaje = self.gestor_usuarios.validar_usuario(username, password)
        if valido:
            usuario = self.gestor_usuarios.usuarios_df[self.gestor_usuarios.usuarios_df['Nombre de usuario'] == username]
            user_id = usuario.iloc[0]['ID']  # Obtener el ID del usuario
            QMessageBox.information(self, "Éxito", mensaje)
            self.gestor_ventanas.set_user_info(user_id, username)  # Establecer el ID y nombre
            self.gestor_ventanas.mostrar_principal()
        else:
            QMessageBox.warning(self, "Error", mensaje)

    def ir_a_registro(self):
        """
        Navega a la ventana de registro.
        """
        self.gestor_ventanas.mostrar_registro()
