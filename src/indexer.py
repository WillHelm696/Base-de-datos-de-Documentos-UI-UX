import json
from collections import defaultdict
from src.preprocessor import preprocess_text


def build_inverted_index(documents: dict[str, str]) -> tuple[dict, dict]:
    """
    Construye el índice invertido y calcula la longitud de cada documento.

    Argumentos:
        documents: Diccionario con formato {nombre_archivo: contenido_texto}

    Retorna:
        Una tupla (inverted_index, doc_lengths) donde:
        - inverted_index: {término: {nombre_archivo: frecuencia}}
        - doc_lengths: {nombre_archivo: total_tokens_filtrados}
    """
    inverted_index = defaultdict(dict)
    doc_lengths = {}

    for doc_id, text in documents.items():
        # Pasamos el texto por nuestro preprocesador optimizado
        tokens = preprocess_text(text)

        # Guardamos la longitud total del documento (necesaria para el cálculo de TF)
        doc_lengths[doc_id] = len(tokens)

        # Si el documento quedó vacío tras el filtrado, continuamos
        if not tokens:
            continue

        # Poblamos el índice invertido contando frecuencias locales
        for token in tokens:
            inverted_index[token][doc_id] = inverted_index[token].get(doc_id, 0) + 1

    return dict(inverted_index), doc_lengths


def save_index_state(index: dict, doc_lengths: dict, filepath: str) -> None:
    """
    Persiste el índice invertido y las metadatas en un único archivo JSON.
    """
    state = {
        "meta": {
            "total_documents": len(doc_lengths)
        },
        "doc_lengths": doc_lengths,
        "inverted_index": index
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def load_index_state(filepath: str) -> tuple[dict, dict]:
    """
    Carga el estado del índice desde el disco.

    Retorna:
        Tupla con (inverted_index, doc_lengths)
    """
    with open(filepath, "r", encoding="utf-8") as f:
        state = json.load(f)
    return state["inverted_index"], state["doc_lengths"]