# <div align="center"><img src="Resources/7 E Basic.png" alt="SevenEBasic" width="200" style="margin: 0 auto;"></div> SevenEBasic: Detección y análisis de expresiones faciales asociadas a las siete emociones básicas de Paul Ekman

SevenEBasic es una aplicación diseñada para detectar y analizar las siete emociones básicas según Paul Ekman en tiempo real, ayudando a los empresarios a monitorear el bienestar emocional de sus empleados. Utilizando inteligencia artificial y tecnologías de visión por computadora como MediaPipe, la aplicación permite analizar las expresiones faciales de los empleados durante reuniones o entrevistas, proporcionando información valiosa sobre su estado emocional.

## Tecnologías Utilizadas

SevenEBasic utiliza tecnologías avanzadas para el análisis de expresiones faciales en tiempo real, integrando inteligencia artificial y visión por computadora. Además, utiliza  <a target="_blank" href="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" style="display: inline-block;"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="28" height="28" /></a> <img src="https://img.shields.io/badge/-python-blue?style=for-the-badge&color=3f7cad"> como lenguaje principal de desarrollo, aprovechando la poderosa combinación de <a target="_blank" href="https://www.vectorlogo.zone/logos/tensorflow/tensorflow-icon.svg" style="display: inline-block;"><img src="https://www.vectorlogo.zone/logos/tensorflow/tensorflow-icon.svg" alt="tensorflow" width="25" height="25" /></a> <img src="https://img.shields.io/badge/-TensorFlow-orange?style=for-the-badge&color=ff6f00"> para entrenar y ejecutar modelos de aprendizaje automático que mejoran la precisión del análisis facial.


### <a target="_blank" href="https://viz.mediapipe.dev/logo.png" style="display: inline-block;"><img src="https://viz.mediapipe.dev/logo.png" alt="mediapipe" width="28" height="28" /></a> MediaPipe y FaceMesh

MediaPipe es una biblioteca de código abierto desarrollada por Google, especializada en el procesamiento de datos en tiempo real. En SevenEBasic, se utiliza el modelo **FaceMesh**, que permite detectar hasta 468 puntos clave en el rostro humano, proporcionando una representación detallada de las expresiones faciales.

FaceMesh destaca por:

- **Precisión y velocidad:** Procesa datos faciales en tiempo real con alta eficiencia.
- **Compatibilidad multiplataforma:** Funciona en dispositivos de escritorio y móviles.
- **Facilidad de integración:** Se combina perfectamente con TensorFlow para tareas de análisis avanzado.
<div align="center"><img src="Resources/FaceMesh.webp" alt="FaceMesh" width="400" style="margin: 0 auto;"></div>

## Entrenamiento del Modelo IA con TensorFlow

Para el análisis de emociones en tiempo real, SevenEBasic utiliza un modelo de inteligencia artificial previamente entrenado con TensorFlow. Este modelo fue entrenado utilizando dos conjuntos de imágenes específicas, lo que permitió mejorar progresivamente su precisión en la detección de las emociones básicas:

### Facial Expressions Training Data
<a href="https://www.kaggle.com/datasets/noamsegal/affectnet-training-data" target="_blank">![Kaggle](https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white)</a>

- **Cantidad de imágenes:** 26,061 
- **Resolución:** 96x96 píxeles
- **Formato:** PNG
- **Resultados iniciales:** Una precisión del 54.04% y val_accuracy del 56.41%.

<div align="center"><img src="Resources/dataset1.png" alt="dataset" width="150" style="margin: 0 auto;"></div>

Aunque este dataset permitió construir un modelo funcional, su baja precisión inicial llevó a un reentrenamiento con un segundo conjunto de datos.

### Extended and Augmented Google FER
<a href="https://www.kaggle.com/datasets/prajwalsood/google-fer-image-format" target="_blank">![Kaggle](https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white)</a>

- **Cantidad de imágenes:** 35,887 
- **Resolución:** 48x48 píxeles
- **Formato:** PNG
- **Resultados tras el reentrenamiento:** Una precisión mejorada del 76.16% y val_accuracy del 80.30%.

<div align="center"><img src="Resources/dataset2.png" alt="dataset" width="150" style="margin: 0 auto;"></div>

Este proceso de reentrenamiento ajustó el modelo inicial para mejorar su capacidad de clasificar las emociones básicas: felicidad, tristeza, sorpresa, miedo, ira, disgusto y neutral.

Es importante destacar que **SevenEBasic utiliza este modelo preentrenado**, el cual se integra directamente en la aplicación para ofrecer análisis en tiempo real.

## Factores Clave para el Correcto Funcionamiento

Para garantizar un análisis preciso y efectivo de las emociones básicas en tiempo real, es importante tener en cuenta los siguientes factores:

### 📷 Resolución de la Cámara

- Se recomienda el uso de cámaras con una resolución mínima de **480p**.
- Cámaras de menor resolución pueden comprometer la detección de puntos faciales clave, afectando la precisión del análisis.

### 💡 Iluminación

- Una iluminación adecuada es esencial para capturar detalles faciales de calidad.
- Se sugiere usar luz natural o artificial que ilumine uniformemente el rostro del usuario, evitando sombras fuertes.

### 🧑 Posición del Usuario

- El rostro debe estar bien centrado y orientado hacia la cámara.
- El usuario debe estar a una distancia adecuada para asegurar que los puntos clave faciales sean detectados correctamente.

### 🖥️ Capacidad de Procesamiento

- La aplicación ha sido probada en equipos con especificaciones mínimas (Intel Celeron N4500, 8 GB RAM) y óptimas (Intel Core i5-8300H, 16 GB RAM).
- Aunque puede ejecutarse en dispositivos de gama baja, se recomienda usar equipos con mayor capacidad de procesamiento para mejorar la fluidez y minimizar el uso de CPU y RAM.

## Pantallas de la Aplicación

*(Aquí se pueden incluir imágenes o descripciones de las pantallas principales de la aplicación, como Login, Gestión de Usuarios, Análisis Interno y Externo, etc.)*

## Cómo Iniciar la Aplicación

### Descargar e instalar Python 3.8:

Para garantizar el funcionamiento adecuado de la aplicación, descarga e instala Python 3.8 desde el siguiente enlace: [Python 3.8](https://www.python.org/ftp/python/3.8.0/python-3.8.0-amd64.exe).

**IMPORTANTE:** Asegúrate de marcar el checkbox **"Add Python to PATH"** durante la instalación.

### Pasos para iniciar la aplicación:

#### 2.1 Iniciar XAMPP:

- Abre el panel de control de XAMPP y asegúrate de iniciar **Apache** y **MySQL**.

#### 2.2 Ejecutar la aplicación:

- Abre una IDE (se recomienda Visual Studio Code) y accede a la terminal integrada.
- Escribe el siguiente comando para iniciar la aplicación:

```bash
python .\app.py
```

## Bibliotecas necesarias

Las siguientes bibliotecas se descargarán automáticamente cuando inicies la aplicación:

- `Pillow==10.3.0`
- `customtkinter==5.2.2`
- `mysql-connector-python==9.0.0`
- `tensorflow==2.13.0`
- `matplotlib==3.7.5`
- `tkcalendar==1.6.1`
- `opencv-python==4.9.0.80`
- `mediapipe==0.10.11`

## Base de Datos

La base de datos necesaria para la aplicación se creará automáticamente la primera vez que inicies la aplicación.
