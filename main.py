import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Importamos la lógica que construiste con tu equipo
from src.preprocessor import preprocess_text
from src.indexer import build_inverted_index
from src.tfidf import calculate_tfidf_for_all, calculate_tf, calculate_tfidf
from src.similarity import rank_documents
from src.database import save_database, load_database
from src.utils import load_documents, validate_directory

DB_PATH = "data/database.json"


class SearchEngineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Motor de Búsqueda Semántica - TF-IDF")
        self.root.geometry("650x550")
        self.root.minsize(550, 450)

        # Variable para almacenar la ruta seleccionada
        self.selected_directory = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # --- SECCIÓN 1: INDEXACIÓN ---
        frame_index = ttk.LabelFrame(self.root, text=" 1. Configuración de Base de Datos ", padding=15)
        frame_index.pack(fill="x", padx=15, pady=10)

        lbl_dir = ttk.Label(frame_index, text="Carpeta de Documentos (PDF, DOCX, TXT):")
        lbl_dir.pack(anchor="w", pady=2)

        # Sub-frame para alinear el campo de texto y el botón de examinar
        frame_path = ttk.Frame(frame_index)
        frame_path.pack(fill="x", pady=5)

        entry_dir = ttk.Entry(frame_path, textvariable=self.selected_directory)
        entry_dir.pack(side="left", fill="x", expand=True, padx=(0, 5))

        btn_browse = ttk.Button(frame_path, text="Examinar...", command=self.browse_directory)
        btn_browse.pack(side="right")

        btn_create_db = ttk.Button(frame_index, text="Indexar y Crear Base de Datos", command=self.create_db_action)
        btn_create_db.pack(fill="x", pady=(10, 0))

        # --- SECCIÓN 2: BÚSQUEDA ---
        frame_search = ttk.LabelFrame(self.root, text=" 2. Panel de Búsqueda Semántica ", padding=15)
        frame_search.pack(fill="both", expand=True, padx=15, pady=10)

        lbl_query = ttk.Label(frame_search, text="Escribe tu consulta o palabras clave:")
        lbl_query.pack(anchor="w", pady=2)

        frame_query_input = ttk.Frame(frame_search)
        frame_query_input.pack(fill="x", pady=5)

        self.entry_query = ttk.Entry(frame_query_input)
        self.entry_query.pack(side="left", fill="x", expand=True, padx=(0, 5))
        # Permite ejecutar la búsqueda al presionar la tecla Enter
        self.entry_query.bind("<Return>", lambda event: self.search_db_action())

        btn_search = ttk.Button(frame_query_input, text="Buscar", command=self.search_db_action)
        btn_search.pack(side="right")

        # --- SECCIÓN 3: RESULTADOS ---
        lbl_results = ttk.Label(frame_search, text="Resultados obtenidos (Ordenados por relevancia):")
        lbl_results.pack(anchor="w", pady=(10, 2))

        # Listbox con scrollbar para mostrar los resultados cómodamente
        frame_list = ttk.Frame(frame_search)
        frame_list.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_list, orient="vertical")
        self.listbox_results = tk.Listbox(
            frame_list,
            yscrollcommand=scrollbar.set,
            font=("Courier New", 10),
            activestyle="none"
        )
        scrollbar.config(command=self.listbox_results.yview)

        scrollbar.pack(side="right", fill="y")
        self.listbox_results.pack(side="left", fill="both", expand=True)

    def browse_directory(self):
        """Abre una ventana emergente nativa para seleccionar carpetas."""
        directory = filedialog.askdirectory(title="Selecciona la carpeta con tus documentos")
        if directory:
            self.selected_directory.set(directory)

    def create_db_action(self):
        """Orquesta la lectura e indexación de los documentos."""
        local_path = self.selected_directory.get().strip()

        if not local_path:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una carpeta primero.")
            return

        if not validate_directory(local_path):
            messagebox.showerror("Error",
                                 f"La carpeta seleccionada no existe o no contiene archivos válidos (.txt, .pdf, .docx).")
            return

        try:
            # Reutilizamos la lógica exacta de tu motor
            documents = load_documents(local_path)
            inverted_index, _ = build_inverted_index(documents)
            tfidf_vectors = calculate_tfidf_for_all(documents, inverted_index)

            from src.tfidf import calculate_idf
            idf_global = calculate_idf(inverted_index, len(documents))

            save_database(inverted_index, tfidf_vectors, idf_global, documents, DB_PATH)

            messagebox.showinfo("Éxito",
                                f"¡Base de datos creada exitosamente!\nSe procesaron {len(documents)} documentos.")
        except Exception as e:
            messagebox.showerror("Error Crítico", f"Ocurrió un error al indexar: {e}")

    def search_db_action(self):
        """Ejecuta la búsqueda semántica y despliega los resultados en la lista."""
        query_text = self.entry_query.get().strip()
        self.listbox_results.delete(0, tk.END)  # Limpiar resultados anteriores

        if not query_text:
            messagebox.showwarning("Advertencia", "Escribe algo en el cuadro de búsqueda.")
            return

        if not os.path.exists(DB_PATH):
            messagebox.showerror("Error", "No existe ninguna base de datos indexada. Por favor, crea una en el paso 1.")
            return

        try:
            # 1. Carga
            inverted_index, tfidf_vectors, idf_global, documents = load_database(DB_PATH)

            # 2. Vectorización de la consulta
            query_tokens = preprocess_text(query_text)
            if not query_tokens:
                self.listbox_results.insert(tk.END, " La consulta solo contenía palabras vacías (stop-words).")
                return

            query_tf = calculate_tf(query_tokens)
            query_tfidf = calculate_tfidf(query_tf, idf_global)

            # 3. Similitud
            ranked_docs = rank_documents(query_tfidf, tfidf_vectors)

            # 4. Renderizado en la interfaz
            coincidencias = 0
            if ranked_docs and ranked_docs[0][1] > 0:
                for doc_id, similarity in ranked_docs:
                    if similarity > 0:
                        coincidencias += 1
                        # Formateamos con espaciado limpio para simular columnas
                        linea = f"[{similarity:.4f}] -> {doc_id}"
                        self.listbox_results.insert(tk.END, linea)

            if coincidencias == 0:
                self.listbox_results.insert(tk.END, " [!] No se encontraron documentos relevantes.")

        except Exception as e:
            messagebox.showerror("Error", f"Error en la consulta: {e}")


def main():
    root = tk.Tk()
    app = SearchEngineGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()