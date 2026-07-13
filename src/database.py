import json
import os


def save_database(inverted_index: dict, tfidf_vectors: dict, idf_global: dict, documents: dict, filepath: str) -> None:
    """
    Persiste el estado completo del motor de búsqueda en un único archivo JSON.

    Argumentos:
        inverted_index: {término: {doc_id: frecuencia}}
        tfidf_vectors:  {doc_id: {término: peso_tfidf}}
        idf_global:     {término: valor_idf} (crucial para procesar consultas nuevas)
        documents:      {doc_id: contenido_original} o simplemente la lista de mapeos
        filepath:       Ruta destino (ej: 'data/database.json')
    """
    # Asegurar que la carpeta contenedora exista (ej: crear 'data/' si no existe)
    dir_name = os.path.dirname(filepath)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)

    data = {
        "meta": {
            "total_documents": len(documents)
        },
        "documents": documents,
        "inverted_index": inverted_index,
        "idf_global": idf_global,
        "tfidf_vectors": tfidf_vectors
    }

    with open(filepath, "w", encoding="utf-8") as f:
        # Usamos indent=2 para que sea legible en entornos académicos y ensure_ascii=False para las tildes
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_database(filepath: str) -> tuple[dict, dict, dict, dict]:
    """
    Carga el índice y los vectores desde el disco.

    Retorna:
        Una tupla con (inverted_index, tfidf_vectors, idf_global, documents)
    Raises:
        FileNotFoundError: Si la base de datos aún no ha sido generada.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"La base de datos en '{filepath}' no existe. Por favor, indexa los documentos primero.")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return (
        data["inverted_index"],
        data["tfidf_vectors"],
        data["idf_global"],
        data["documents"]
    )