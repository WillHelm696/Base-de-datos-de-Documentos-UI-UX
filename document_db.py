import argparse
from src.preprocessor import preprocess_text
from src.indexer import build_inverted_index
from src.tfidf import calculate_tfidf_for_all, calculate_tf, calculate_tfidf
from src.similarity import rank_documents
from src.database import save_database, load_database
from src.utils import load_documents, validate_directory

DB_PATH = "data/database.json"


def create_db_action(local_path: str) -> None:
    """Orquesta la lectura, indexación, pesado TF-IDF y persistencia."""
    if not validate_directory(local_path):
        print(f"[X] Error: La carpeta '{local_path}' no existe o no contiene archivos válidos (.txt).")
        return

    print(f"[*] Leyendo documentos desde '{local_path}'...")
    documents = load_documents(local_path)

    print("[*] Construyendo el índice invertido...")
    # build_inverted_index devuelve el índice y las longitudes de control
    inverted_index, _ = build_inverted_index(documents)

    print("[*] Calculando matriz de vectores TF-IDF globales...")
    # calculate_tfidf_for_all procesa la colección entera
    tfidf_vectors = calculate_tfidf_for_all(documents, inverted_index)

    # Para la búsqueda dinámica en CLI necesitamos el idf_global ya listo,
    # lo extraemos usando la lógica interna del módulo tfidf importado indirectamente
    from src.tfidf import calculate_idf
    idf_global = calculate_idf(inverted_index, len(documents))

    print(f"[*] Guardando base de datos en '{DB_PATH}'...")
    save_database(inverted_index, tfidf_vectors, idf_global, documents, DB_PATH)
    print("[✓] Document database created successfully.")


def search_db_action(text: str) -> None:
    """Carga el estado persistido, vectoriza la consulta y rankea los resultados."""
    if not text.strip():
        print("[X] Error: La consulta no puede estar vacía.")
        return

    try:
        # Recuperamos todo el estado guardado, incluyendo el idf_global precalculado
        inverted_index, tfidf_vectors, idf_global, documents = load_database(DB_PATH)
    except FileNotFoundError:
        print(f"[X] Error: La base de datos en '{DB_PATH}' no existe. Ejecuta primero con '-create'.")
        return

    # 1. Preprocesar y limpiar la consulta del usuario
    query_tokens = preprocess_text(text)
    if not query_tokens:
        print("document not found (la consulta solo contenía signos o stop-words)")
        return

    # 2. Calcular TF local de la consulta
    query_tf = calculate_tf(query_tokens)

    # 3. Construir vector TF-IDF de la consulta usando el idf_global de la base de datos
    query_tfidf = calculate_tfidf(query_tf, idf_global)

    # 4. Calcular similitud de coseno y rankear de mayor a menor
    ranked_docs = rank_documents(query_tfidf, tfidf_vectors)

    # 5. Desplegar resultados en consola
    # Si la lista está vacía o el mejor resultado tiene score 0, significa que no hay coincidencia
    if not ranked_docs or ranked_docs[0][1] == 0:
        print("document not found")
    else:
        print(f"\nResultados de búsqueda para: '{text}'")
        print("-" * 50)
        for doc_id, similarity in ranked_docs:
            if similarity > 0:
                print(f"-> {doc_id} (Similitud: {similarity:.4f})")
        print("-" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Sistema de Búsqueda Semántica de Documentos con TF-IDF y Similitud de Coseno."
    )
    # Cambiamos a argumentos con doble guion (--create y --search) que es la convención estándar de argparse
    parser.add_argument("--create", type=str,
                        help="Ruta de la carpeta de documentos para indexar y crear la base de datos")
    parser.add_argument("--search", type=str, help="Texto o frase clave para buscar en la base de datos")

    args = parser.parse_args()

    if args.create:
        create_db_action(args.create)
    elif args.search:
        search_db_action(args.search)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()