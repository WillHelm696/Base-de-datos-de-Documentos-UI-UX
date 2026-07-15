import os
import sys
import json

# Corrección dinámica del path para desarrollo local
root_path = os.path.abspath(os.path.dirname(__file__))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox
from src.gui_view import SearchEngineView

# Importaciones del motor analítico
from src.preprocessor import preprocess_text
from src.indexer import build_inverted_index
from src.tfidf import calculate_tfidf_for_all, calculate_tf, calculate_tfidf
from src.similarity import rank_documents
from src.database import save_database, load_database
from src.utils import load_documents, validate_directory

DB_PATH = "data/database.json"
CONFIG_PATH = "data/config.json"  # <--- Ruta para almacenar las preferencias


class SearchEngineController(SearchEngineView):
    def __init__(self):
        super().__init__()

        self.current_results_mapping = {}
        self.loaded_documents_cache = {}

        # Conectar las señales y acciones (Eventos)
        self.btn_browse.clicked.connect(self.handle_browse)
        self.btn_create_db.clicked.connect(self.handle_create_db)
        self.btn_search.clicked.connect(self.handle_search)
        self.entry_query.returnPressed.connect(self.handle_search)
        self.list_results.currentTextChanged.connect(self.handle_preview_change)

        # Cargar las preferencias guardadas apenas se inicializa la app
        self.load_preferences()

    def load_preferences(self):
        """Carga la última carpeta guardada en el archivo JSON si existe."""
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    last_dir = config.get("last_directory", "")

                    # Validamos que la carpeta guardada aún exista físicamente en el disco
                    if last_dir and os.path.isdir(last_dir):
                        self.entry_dir.setText(last_dir)
            except Exception as e:
                print(f"No se pudieron cargar las preferencias: {e}")

    def save_preferences(self, directory_path):
        """Guarda la ruta del directorio seleccionado en el archivo JSON dentro de data/."""
        try:
            # Asegura que la carpeta 'data/' exista antes de escribir el archivo
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

            config_data = {"last_directory": directory_path}
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(config_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"No se pudieron guardar las preferencias: {e}")

    def handle_browse(self):
        directory = QFileDialog.getExistingDirectory(self, "Selecciona la carpeta con tus documentos")
        if directory:
            self.entry_dir.setText(directory)
            # Guardamos la preferencia inmediatamente cuando el usuario selecciona una carpeta con éxito
            self.save_preferences(directory)

    def handle_create_db(self):
        local_path = self.entry_dir.text().strip()
        if not local_path or not validate_directory(local_path):
            QMessageBox.critical(self, "Error", "Ruta inválida o sin archivos (.txt, .pdf, .docx).")
            return

        try:
            documents = load_documents(local_path)
            inverted_index, _ = build_inverted_index(documents)
            tfidf_vectors = calculate_tfidf_for_all(documents, inverted_index)

            from src.tfidf import calculate_idf
            idf_global = calculate_idf(inverted_index, len(documents))

            save_database(inverted_index, tfidf_vectors, idf_global, documents, DB_PATH)
            self.loaded_documents_cache = documents

            # Guardamos la preferencia también al indexar por si el usuario editó la ruta a mano
            self.save_preferences(local_path)

            QMessageBox.information(self, "Éxito", f"Base de datos creada con {len(documents)} archivos.")
        except Exception as e:
            QMessageBox.critical(self, "Error Crítico", f"Error al indexar: {e}")

    def handle_search(self):
        query_text = self.entry_query.text().strip()
        self.list_results.clear()
        self.text_preview.clear()
        self.current_results_mapping.clear()

        if not query_text:
            return

        if not os.path.exists(DB_PATH):
            QMessageBox.warning(self, "Error", "Debes inicializar la base de datos primero.")
            return

        try:
            inverted_index, tfidf_vectors, idf_global, documents = load_database(DB_PATH)
            self.loaded_documents_cache = documents

            query_tokens = preprocess_text(query_text)
            if not query_tokens:
                self.list_results.addItem("La consulta solo contiene conectores o stop-words.")
                return

            query_tf = calculate_tf(query_tokens)
            query_tfidf = calculate_tfidf(query_tf, idf_global)
            ranked_docs = rank_documents(query_tfidf, tfidf_vectors)

            has_matches = False
            if ranked_docs and ranked_docs[0][1] > 0:
                for doc_id, similarity in ranked_docs:
                    if similarity > 0:
                        has_matches = True
                        display_text = f"[{similarity:.4f}] - {doc_id}"
                        self.list_results.addItem(display_text)
                        self.current_results_mapping[display_text] = doc_id

            if not has_matches:
                self.list_results.addItem("No se encontraron documentos correlativos.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en la búsqueda: {e}")

    def handle_preview_change(self, selected_item_text):
        if not selected_item_text or selected_item_text not in self.current_results_mapping:
            self.text_preview.clear()
            return

        real_doc_id = self.current_results_mapping[selected_item_text]
        document_text = self.loaded_documents_cache.get(real_doc_id, "No se encontró el contenido del archivo.")
        self.text_preview.setPlainText(document_text)


def main():
    app = QApplication(sys.argv)
    controller = SearchEngineController()
    controller.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()