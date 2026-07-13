import math


def cosine_similarity(vec_a: dict[str, float], vec_b: dict[str, float], norm_a: float = None) -> float:
    """
    Calcula la similitud de coseno entre dos vectores dispersos (diccionarios).

    Argumentos:
        vec_a: Vector A, ej: {'algoritmo': 0.5, 'python': 0.2}
        vec_b: Vector B, ej: {'python': 0.8, 'codigo': 0.1}
        norm_a: Precalculada opcionalmente de la magnitud de vec_a para ahorrar CPU.
    """
    # 1. Producto escalar eficiente usando los términos de la consulta (vec_a)
    dot_product = sum(vec_a[token] * vec_b.get(token, 0.0) for token in vec_a)

    if dot_product == 0:
        return 0.0

    # 2. Magnitudes (Normas Euclidianas)
    if norm_a is None:
        norm_a = math.sqrt(sum(val ** 2 for val in vec_a.values()))

    norm_b = math.sqrt(sum(val ** 2 for val in vec_b.values()))

    # 3. Control de división por cero
    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def rank_documents(query_tfidf: dict[str, float], tfidf_vectors: dict[str, dict[str, float]]) -> list[
    tuple[str, float]]:
    """
    Compara el vector de una consulta contra todos los documentos y los ordena
    de mayor a menor relevancia.

    Retorna:
        Una lista de tuplas con el formato [('nombre_doc.txt', score_similitud), ...]
    """
    similarities = []

    # Precalculamos la norma de la consulta una sola vez para optimizar el bucle
    norm_query = math.sqrt(sum(val ** 2 for val in query_tfidf.values()))

    for doc_id, doc_vector in tfidf_vectors.items():
        # Pasamos norm_query para ahorrar recursos de cómputo repetitivos
        similarity = cosine_similarity(query_tfidf, doc_vector, norm_query)
        similarities.append((doc_id, similarity))

    # Ordenar por similitud de mayor a menor (reverse=True)
    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities