🎥 Sistema de Recomendación en Python

Este proyecto implementa un sistema de recomendación de películas desarrollado en Python, utilizando técnicas de aprendizaje automático y procesamiento de datos. Proporciona recomendaciones personalizadas basadas en la información de los usuarios y las películas disponibles.

🔢 Características

Algoritmos de Recomendación: Implementa técnicas como filtrado colaborativo y contenido basado en el perfil del usuario.

Dataset de Películas: Utiliza un conjunto de datos enriquecido con información adicional como imágenes.

Interfaz Modular: División clara de la lógica del sistema en módulos bien organizados.

Soporte Multiusuario: Diseñado para manejar recomendaciones personalizadas para diferentes perfiles.

🌐 Estructura del Proyecto

Main.py: Archivo principal para ejecutar el sistema.

gestores/: Contiene la lógica principal del sistema de recomendación.

vistas/: Módulos relacionados con la visualización de los resultados o interacción del usuario.

usuarios.csv: Dataset de usuarios, con información relevante para generar recomendaciones.

peliculas_final_imagenes.csv: Dataset de películas con información adicional (por ejemplo, imágenes).

requirements.txt: Archivo con las dependencias necesarias para ejecutar el proyecto.

🔧 Instalación

Para instalar y ejecutar el proyecto localmente:

Clona el repositorio:

git clone https://github.com/Alejandroortega2002/Sistema_Recomendacion_Python_Grupo_2.git

Navega al directorio del proyecto:

cd Sistema_Recomendacion_Python_Grupo_2

Crea un entorno virtual (opcional pero recomendado):

python -m venv venv

Activa el entorno virtual:

En Windows:

venv\Scripts\activate

En macOS/Linux:

source venv/bin/activate

Instala las dependencias:

pip install -r requirements.txt

🚀 Uso

Ejecuta el archivo principal para iniciar el sistema:

python Main.py

Asegúrate de que los datasets (usuarios.csv y peliculas_final_imagenes.csv) estén correctamente configurados en las rutas requeridas.

Sigue las instrucciones en la consola o interfaz para interactuar con el sistema.

📚 Contribuciones

¡Las contribuciones son bienvenidas! Si deseas colaborar en este proyecto, sigue estos pasos:

Haz un fork del repositorio.

Crea una nueva rama para tu funcionalidad:

git checkout -b feature/nueva-funcionalidad

Realiza tus cambios y haz un commit:

git commit -m "Agrego nueva funcionalidad"

Haz push a tu rama:

git push origin feature/nueva-funcionalidad

Abre un Pull Request y describe tus cambios.

📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más información.

🔗 Enlaces

Repositorio en GitHub

Documentación Oficial de Python

🙏¡Gracias por tu interés en este proyecto! No dudes en abrir un issue si tienes preguntas o sugerencias.

