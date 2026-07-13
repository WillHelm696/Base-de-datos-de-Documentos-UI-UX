import math
from collections import defaultdict
from src.preprocessor import preprocess_text


def calculate_tf(tokens: list[str]) -> dict[str, float]:
    """
    Calcula la frecuencia normalizada de cada término en un documento.
    TF = (conteo del término) / (total de términos en el documento)
    """
    total_tokens = len(tokens)
    if total_tokens == 0:
        return {}

    tf_counts = defaultdict(int)
    for token in tokens:
        tf_counts[token] += 1

    # Normalizamos para evitar que documentos largos sesguen el peso
    return {token: count / total_tokens for token, count in tf_counts.items()}


def calculate_idf(inverted_index: dict, total_docs: int) -> dict[str, float]:
    """
    Calcula el IDF para cada término utilizando un suavizado estándar.
    Fórmula con suavizado: ln( (1 + N) / (1 + DF) ) + 1
    Esto evita divisiones por cero si un término no aparece en ningún documento.
    """
    idf = {}
    for token, doc_mappings in inverted_index.items():
        df = len(doc_mappings)  # Cuántos documentos contienen este token
        # Aplicamos suavizado estándar de motores de búsqueda
        idf[token] = math.log((1 + total_docs) / (1 + df)) + 1
    return idf


def calculate_tfidf(tf: dict[str, float], idf: dict[str, float]) -> dict[str, float]:
    """
    Calcula el vector TF-IDF cruzando las frecuencias locales con el IDF global.
    """
    tfidf = {}
    for token, tf_value in tf.items():
        # .get(token, 1.0) maneja palabras de consultas que no están en el IDF global
        tfidf[token] = tf_value * idf.get(token, 1.0)
    return tfidf


def calculate_tfidf_for_all(documents: dict[str, str], inverted_index: dict) -> dict[str, dict[str, float]]:
    """
    Genera la matriz completa de vectores TF-IDF para toda la colección de documentos.
    """
    tfidf_vectors = {}
    total_docs = len(documents)

    if total_docs == 0:
        return tfidf_vectors

    # 1. Calculamos el IDF global una sola vez
    idf_global = calculate_idf(inverted_index, total_docs)

    # 2. Procesamos cada documento individualmente
    for doc_id, text in documents.items():
        tokens = preprocess_text(text)
        tf = calculate_tf(tokens)
        tfidf_vectors[doc_id] = calculate_tfidf(tf, idf_global)

    return tfidf_vectors