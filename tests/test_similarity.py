from src.similarity import *

if __name__ == "__main__":
    print("=== Ejecutando pruebas de similarity.py ===\n")

    # 1. Vectores de prueba simulados (TF-IDF)
    # Consulta del usuario: "algoritmo python"
    vector_consulta = {"algoritmo": 0.5, "python": 0.5}

    # Documentos indexados en la base de datos
    vectores_documentos = {
        "doc_exacto.txt": {"algoritmo": 0.5, "python": 0.5},  # Idéntico a la consulta (Similitud = 1.0)
        "doc_medio.txt": {"python": 0.8, "codigo": 0.4},  # Comparte solo "python"
        "doc_irrelevante.txt": {"cocina": 0.9, "receta": 0.3}  # No comparte nada (Similitud = 0.0)
    }

    # Test 1: Verificar cálculo de similitud idéntica
    sim_perfecta = cosine_similarity(vector_consulta, vectores_documentos["doc_exacto.txt"])
    print(f"Similitud idéntica: {sim_perfecta}")
    assert math.isclose(sim_perfecta, 1.0), "Error: Vectores idénticos deberían dar similitud 1.0"

    # Test 2: Verificar cálculo de similitud ortogonal (sin términos en común)
    sim_nula = cosine_similarity(vector_consulta, vectores_documentos["doc_irrelevante.txt"])
    print(f"Similitud ortogonal: {sim_nula}")
    assert sim_nula == 0.0, "Error: Vectores sin palabras en común deberían dar similitud 0.0"

    # Test 3: Probar el ranking global de documentos
    ranking = rank_documents(vector_consulta, vectores_documentos)
    print("\nRanking Generado:")
    for posicion, (doc, score) in enumerate(ranking, 1):
        print(f" {posicion}. {doc} -> Score: {score:.4f}")

    # Validaciones del orden de relevancia
    assert ranking[0][0] == "doc_exacto.txt", "Error: El documento exacto debe quedar en 1° lugar."
    assert ranking[1][0] == "doc_medio.txt", "Error: El documento medio debe quedar en 2° lugar."
    assert ranking[2][0] == "doc_irrelevante.txt", "Error: El documento irrelevante debe quedar al final."

    print("\n¡Todos los tests de ordenamiento y similitud pasaron exitosamente! 🏁")