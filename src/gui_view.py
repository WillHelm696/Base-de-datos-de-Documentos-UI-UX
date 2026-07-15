from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QListWidget, QGroupBox, QTextEdit, QSplitter
)
from PyQt6.QtCore import Qt


class SearchEngineView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Motor de Búsqueda Semántica v2.0 - UI/UX")
        self.resize(1000, 650)
        self.setMinimumSize(800, 500)
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # --- SECCIÓN 1: CONFIGURACIÓN DE BASE DE DATOS ---
        group_index = QGroupBox(" 1. Configuración de Base de Datos ")
        layout_index = QVBoxLayout(group_index)

        layout_index.addWidget(QLabel("Carpeta de Documentos (PDF, DOCX, TXT):"))

        row_path = QHBoxLayout()
        self.entry_dir = QLineEdit()
        self.entry_dir.setPlaceholderText("Selecciona una carpeta para escanear...")
        self.btn_browse = QPushButton("Examinar...")
        row_path.addWidget(self.entry_dir)
        row_path.addWidget(self.btn_browse)
        layout_index.addLayout(row_path)

        self.btn_create_db = QPushButton("Indexar y Crear Base de Datos")
        layout_index.addWidget(self.btn_create_db)
        main_layout.addWidget(group_index)

        # --- SECCIÓN 2: PANEL DE BÚSQUEDA ---
        group_search = QGroupBox(" 2. Panel de Búsqueda Semántica ")
        layout_search = QVBoxLayout(group_search)

        layout_search.addWidget(QLabel("Escribe tu consulta o palabras clave:"))

        row_query = QHBoxLayout()
        self.entry_query = QLineEdit()
        self.entry_query.setPlaceholderText("Ej: algoritmos de ordenamiento...")
        self.btn_search = QPushButton("Buscar")
        row_query.addWidget(self.entry_query)
        row_query.addWidget(self.btn_search)
        layout_search.addLayout(row_query)

        # --- SECCIÓN 3: VISTA DE RESULTADOS DIVIDIDA (SPLITTER) ---
        # El QSplitter permite al usuario arrastrar el borde para agrandar/achicar la vista previa
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Sub-panel Izquierdo: Lista de Resultados
        widget_left = QWidget()
        layout_left = QVBoxLayout(widget_left)
        layout_left.setContentsMargins(0, 0, 0, 0)
        layout_left.addWidget(QLabel("Documentos Relevantes:"))
        self.list_results = QListWidget()
        layout_left.addWidget(self.list_results)

        # Sub-panel Derecho: Vista Previa del Documento
        widget_right = QWidget()
        layout_right = QVBoxLayout(widget_right)
        layout_right.setContentsMargins(0, 0, 0, 0)
        layout_right.addWidget(QLabel("Vista Previa del Contenido:"))
        self.text_preview = QTextEdit()
        self.text_preview.setReadOnly(True)  # No editable
        self.text_preview.setPlaceholderText("Haz clic en un documento de la lista para ver su contenido aquí...")
        layout_right.addWidget(self.text_preview)

        # Añadir al splitter
        splitter.addWidget(widget_left)
        splitter.addWidget(widget_right)

        # Proporción inicial de la división (50% y 50%)
        splitter.setSizes([450, 550])

        layout_search.addWidget(splitter)
        main_layout.addWidget(group_search)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { 
                background-color: #f8f9fa; 
            }
            QGroupBox {
                font-weight: bold; 
                font-size: 13px; 
                border: 1px solid #ced4da;
                border-radius: 6px; 
                margin-top: 10px; 
                padding-top: 15px; background-color: #ffffff;
            }
            QGroupBox::title { 
                subcontrol-origin: margin; 
                left: 10px; padding: 0 5px; 
                color: #495057; 
            }
            QLabel { 
                color: #495057; 
                font-size: 12px; 
            }
            QLineEdit { 
                padding: 6px 10px; 
                border: 1px solid #ced4da; 
                border-radius: 4px; 
                font-size: 12px; 
            }
            QLineEdit:focus { 
                border: 1px solid #4dabf7; 
            }
            QPushButton {
                background-color: #228be6; 
                color: white; 
                font-weight: bold;
                padding: 7px 14px; 
                border-radius: 4px; 
                border: none; 
                font-size: 12px;
            }
            QPushButton:hover { 
                background-color: #1c7ed6; 
            }
            QListWidget {
                border: 1px solid #ced4da; 
                border-radius: 4px; 
                background-color: #404040;
                font-family: 'Segoe UI', sans-serif; 
                font-size: 12px;
            }
            QTextEdit {
                border: 1px solid #ced4da; 
                border-radius: 4px; 
                background-color: #f1f3f5;
                font-family: 'Courier New', monospace; 
                font-size: 12px; 
                color: #212529;
            }
        """)