# Reloj Multifunción - Proyecto de Estructuras de Datos

¡Hola! Bienvenido a la explicación de este **Reloj Multifunción**. Este proyecto es una aplicación de escritorio completa, moderna y visualmente atractiva, construida en **Python** utilizando **PySide6** (el framework de Qt para Python) para la interfaz gráfica.

Más allá de ser un reloj visual, el proyecto está diseñado para poner en práctica conceptos avanzados de desarrollo de software, como la arquitectura MVC (Modelo-Vista-Controlador), la separación de responsabilidades a través de servicios, y la implementación de estructuras de datos personalizadas.

## ¿Qué herramientas incluye?
La aplicación es una "navaja suiza" de la gestión del tiempo. Sus características principales son:

*   **Reloj Digital y Analógico:** Una pantalla principal que no solo muestra la hora y la fecha, sino que se adapta dinámicamente según la herramienta que estés usando (por ejemplo, el reloj analógico puede transformarse visualmente en un cronómetro o un pomodoro).
*   **Gestor de Alarmas:** Permite añadir, editar, encender/apagar y eliminar alarmas.
*   **Cronómetro:** Un sistema de precisión que te permite iniciar, pausar, y registrar "vueltas" (laps), guardando el historial de tiempos.
*   **Técnica Pomodoro:** Un temporizador especializado para la productividad, con fases configurables para periodos de enfoque, descansos cortos y descansos largos.
*   **Zonas Horarias:** Una función para navegar rápidamente entre diferentes ciudades del mundo y ver su hora local actual.
*   **Personalización (Configuración):** Soporte para múltiples temas visuales y estilos del reloj analógico (mostrar/ocultar segunderos, formato de 24 horas, etc).

## ¿Cómo está organizado el código? (Arquitectura)
El código está excelentemente estructurado para que sea fácil de leer y escalar. Sigue el patrón **MVC** vitaminado con una capa de **Servicios**:

1.  **`ui/` (Vistas):** Aquí vive todo lo que el usuario ve y toca (botones, ventanas, diálogos). Es la "cara" de la aplicación.
2.  **`models/` (Modelos):** Son representaciones de los datos puros. Por ejemplo, qué propiedades tiene una alarma (hora, minuto, etiqueta, si está encendida o no).
3.  **`services/` (Lógica de Negocio):** Aquí está el cerebro de cada herramienta. Hay un servicio para las alarmas, otro para el pomodoro, otro para manejar el tiempo, etc. Las vistas no hacen cálculos complejos, de eso se encargan los servicios.
4.  **`controllers/appController.py`:** Es el "director de orquesta". Se encarga de conectar la interfaz (`ui/`) con la lógica (`services/`). Si haces clic en "Iniciar Cronómetro" en la interfaz, el controlador recibe ese clic y le dice al servicio del cronómetro que empiece a contar.
5.  **`main.py`:** Es el punto de entrada. El archivo que debes ejecutar para iniciar todo el programa.

## Lista Circular Doble
Dado que este proyecto nace en un entorno académico/práctico de Estructuras de Datos, implementa desde cero su propia **Lista Circular Doblemente Enlazada** (`dataStructures/doublyCircularList.py`).



*   **Navegar por las Alarmas o Vueltas:** Si estás viendo la última alarma y presionas "Siguiente", la interfaz no se bloquea ni da error; simplemente vuelve a mostrarte la primera alarma de forma cíclica.
*   **Explorar Zonas Horarias:** Puedes ir pasando ciudades hacia adelante o hacia atrás infinitamente en un ciclo continuo sin llegar nunca a un "límite" en la interfaz.

