
**Introducción :**

Este modelo de visión artificial, desarrollado con YOLOv8, OpenCV y Roboflow, es capaz de detectar, clasificar y contar en tiempo real frutas como maracuyá, tomate de árbol, pitahaya y aguacate, las cuales son algunas de las principales frutas no tradicionales exportadas desde Ecuador. Diseñado específicamente para pequeñas y medianas exportadoras que operan en el campo y no cuentan con los recursos para adquirir sistemas avanzados, el software es liviano, pero mantiene alta precisión.

**Uso :**

El sistema simula una cinta transportadora en constante movimiento, donde las frutas pasan para su detección. Se requiere una PC de recursos medios y una cámara de alta resolución para minimizar errores y falsos positivos.

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F9906144%2F60a9cb59dcc7f73ec24a5905e05bcd2b%2FScreenshot%202024-09-04%20172726.png?generation=1725488953389802&alt=media)


**Características :**

El modelo fue entrenado con 1000 imágenes de cada fruta, considerando variaciones de ángulo, iluminación y posición, lo que mejora su precisión y evita sobreajustes. Para resaltar las características de las frutas, se utilizó un fondo blanco, lo que facilita la detección de color, forma y tamaño. Además, se desarrolló una página web para que cualquier usuario pueda acceder al sistema sin necesidad de conocimientos técnicos. La interfaz muestra el video en vivo y un contador de las frutas que atraviesan la línea de detección, proporcionando un control preciso del conteo.

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F9906144%2Ff19450b217a69a3d27ecbe1dd5793f9f%2Fval_batch2_labels%20(2).jpg?generation=1725489976945460&alt=media)

El sistema también incluye estadísticas detalladas, con el total de cada producto, fechas y la opción de descargar informes. Toda la información se almacena en una base de datos local, lo que asegura el funcionamiento incluso sin conexión a internet. Si hay acceso a internet, los datos se replican en una base de datos en la nube, garantizando la seguridad de la información y permitiendo su análisis.

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F9906144%2F0216e1d7d5d3eb479c0e03c97c1b0e75%2FScreenshot%202024-09-04%20174639.png?generation=1725490013095936&alt=media)
