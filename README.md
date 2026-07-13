
# Sistema de Búsqueda Semántica de Documentos con TF-IDF y Similitud de Coseno

Este proyecto es un motor de búsqueda semántica a nivel de documentos desarrollado para la materia **Algoritmos II**. Permite indexar colecciones de archivos de múltiples formatos (`.pdf`, `.docx`, `.txt`) y realizar consultas de lenguaje natural mediante una Interfaz Gráfica de Usuario (GUI) intuitiva.

El motor calcula la relevancia de los documentos utilizando el modelo vectorial de recuperación de información basado en **TF-IDF (Term Frequency - Inverse Document Frequency)** y la **Similitud de Coseno** en un espacio multidimensional disperso.

---

## 🎯 Características Principales

*   **Soporte Multiformato:** Extracción nativa y robusta de texto desde documentos PDF (`.pdf`), Microsoft Word (`.docx`) y texto plano (`.txt`).
*   **Procesamiento de Lenguaje Natural (NLP):** Tokenización, remoción estricta de signos de puntuación, filtrado inteligente de *stop-words* y normalización de caracteres especiales (remoción adaptativa de tildes mediante codificación `NFKD`).
*   **Modelo de Recuperación Espacial:** Ponderación TF-IDF con suavizado de IDF para evitar divisiones por cero ante términos fuera del vocabulario indexado.
*   **Similitud de Coseno Optimizada:** Algoritmo optimizado para vectores dispersos, calculando el producto punto únicamente sobre dimensiones activas y precalculando normas para reducir la complejidad temporal.
*   **Persistencia de Datos:** Almacenamiento eficiente del estado del motor (índice invertido, vectores de peso globales, matriz de documentos y valores IDF) en disco en formato JSON.
*   **Interfaz Gráfica de Usuario (GUI):** Ventana interactiva creada con Tkinter que permite seleccionar directorios mediante el explorador nativo y visualizar los resultados ordenados por relevancia semántica.

---

## 📂 Estructura del Proyecto

```text
proyecto-algoritmos-ii/
├── document_db.py          # Punto de entrada principal (GUI)
├── README.md               # Documentación del proyecto
├── requirements.txt        # Librerías externas para lectura de binarios
├── src/
│   ├── __init__.py
│   ├── preprocessor.py     # Tokenización, minúsculas, tildes y stop-words
│   ├── indexer.py          # Construcción del Índice Invertido
│   ├── tfidf.py            # Cálculo de TF, IDF y vectores TF-IDF
│   ├── similarity.py       # Similitud de coseno y ranking de resultados
│   ├── database.py         # Serialización y persistencia en disco (JSON)
│   └── utils.py            # Lectores específicos de formatos (.txt, .pdf, .docx)
└── data/
    ├── documents/          # Carpeta para colocar los documentos a indexar
    └── database.json       # Base de datos generada e indexada

```

---

## 🛠️ Instalación y Requisitos

El proyecto requiere Python 3.8 o superior. Para leer archivos PDF y Word, es necesario instalar las dependencias incluidas en `requirements.txt`.

1. **Clona este repositorio:**
```bash
git clone https://github.com/WillHelm696/Base-de-datos-de-Documentos-UI-UX.git
cd Base-de-datos-de-Documentos-UI-UX

```


2. **Instala las dependencias necesarias:**
```bash
pip install -r requirements.txt

```



*Nota: Tkinter se incluye de manera estándar en las instalaciones oficiales de Python. Si estás en una distribución Linux tipo Debian/Ubuntu y tienes problemas al abrir la GUI, puedes instalarlo usando: `sudo apt-get install python3-tk`.*

---

## 🚀 Guía de Uso

Para iniciar el sistema, simplemente ejecuta el archivo principal en la raíz del proyecto:

```bash
python document_db.py

```

### Flujo de Trabajo en la Interfaz:

1. **Configurar la Base de Datos:**
* Haz clic en el botón **Examinar...** para abrir el explorador de archivos nativo de tu sistema operativo.
* Selecciona la carpeta donde guardas tus documentos (por ejemplo, `data/documents/`).
* Haz clic en **"Indexar y Crear Base de Datos"**. El motor analizará los archivos, construirá el índice invertido y calculará los vectores en segundo plano. Al finalizar, saltará una ventana emergente de confirmación.


2. **Buscar:**
* Escribe tu consulta en el cuadro de búsqueda (ej. *"algoritmos de ordenamiento eficientes"*).
* Presiona **Enter** o haz clic en **Buscar**.
* Los resultados aparecerán ordenados de mayor a menor relevancia en la sección de abajo con su puntaje de similitud matemática `[Score] -> Nombre_Documento`.



---

## 🧪 Arquitectura y Conceptos Matemáticos

### 1. Preprocesamiento de Texto

Para garantizar que palabras similares coincidan sin importar su formato tipográfico, se aplica el siguiente pipeline:

* Conversión de caracteres Unicode a su forma descompuesta (`NFKD`) para remover tildes y diacríticos (`Árbol` $\rightarrow$ `arbol`).
* Eliminación de puntuación mediante mapas de traducción de C.
* Filtrado de *stop-words* locales con búsquedas optimizadas en complejidad $O(1)$ usando un set estático en memoria.

### 2. Ponderación TF-IDF con Suavizado

La relevancia de un término dentro de un documento se calcula mediante:

$$TF = \frac{\text{Frecuencia del término en el Doc}}{\text{Total de términos del Doc}}$$

$$IDF = \ln\left(\frac{1 + N}{1 + DF}\right) + 1$$

*Donde $N$ es el total de documentos y $DF$ (Document Frequency) es el número de documentos que contienen el término.*

### 3. Similitud de Coseno

La métrica matemática para comparar la consulta ($Q$) con un documento ($D$) se define como:

$$\text{Similitud}(Q, D) = \frac{\sum Q_i D_i}{\sqrt{\sum Q_i^2} \sqrt{\sum D_i^2}}$$

El código optimiza esta comparación evaluando únicamente las dimensiones donde $Q_i > 0$ y reutilizando la norma de la consulta en cada iteración del bucle del ranking.

