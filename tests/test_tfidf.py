from src.tfidf import *

if __name__ == "__main__":
    print("=== Ejecutando pruebas de tfidf.py ===\n")

    # 1. Datos simulados preprocesados de dos documentos
    doc_a_tokens = ["algoritmo", "python", "algoritmo"]  # Largo: 3
    doc_b_tokens = ["python", "codigo"]  # Largo: 2

    # Simulamos el índice invertido que construiría el Integrante 2
    indice_simulado = {
        "algoritmo": {"doc_a.txt": 2},
        "python": {"doc_a.txt": 1, "doc_b.txt": 1},
        "codigo": {"doc_b.txt": 1}
    }

    documentos_simulados = {
        "doc_a.txt": "algoritmo python algoritmo",
        "doc_b.txt": "python codigo"
    }

    # Test 1: Verificar el cálculo de TF normalizado
    tf_a = calculate_tf(doc_a_tokens)
    print("TF de doc_a (debe estar normalizado):", tf_a)
    # 'algoritmo' aparece 2 de 3 veces -> 0.666...
    assert math.isclose(tf_a["algoritmo"], 2 / 3), "Error: TF de 'algoritmo' mal calculado."
    assert math.isclose(tf_a["python"], 1 / 3), "Error: TF de 'python' mal calculado."

    # Test 2: Verificar IDF global
    idf_global = calculate_idf(indice_simulado, total_docs=2)
    print("\nIDF Global calculado:", idf_global)
    # 'python' aparece en los 2 documentos, su IDF debería ser más bajo que el de 'codigo'
    assert idf_global["python"] < idf_global["codigo"], "Error: El término común debería pesar menos que el raro."

    # Test 3: Calcular la matriz completa de vectores TF-IDF
    vectores_resultado = calculate_tfidf_for_all(documentos_simulados, indice_simulado)
    print("\nMatriz Final de Vectores TF-IDF:")
    for doc_id, vector in vectores_resultado.items():
        print(f" -> {doc_id}: {vector}")

    assert "doc_a.txt" in vectores_resultado, "Error: Falta el vector de doc_a."
    assert "algoritmo" in vectores_resultado["doc_a.txt"], "Error: Falta el peso de 'algoritmo'."

    print("\n¡Todos los tests matemáticos del módulo TF-IDF pasaron exitosamente! 🎯")