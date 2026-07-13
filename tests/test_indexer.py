from src.indexer import *

if __name__ == "__main__":
    print("=== Ejecutando pruebas de indexer.py ===\n")

    # 1. Simular nuestra base de datos de documentos de prueba (data/documents/)
    documentos_prueba = {
        "doc_algoritmos.txt": "El algoritmo de ordenamiento es eficiente y rápido.",
        "doc_python.txt": "Python es un lenguaje excelente para desarrollo de algoritmos.",
        "doc_vacio.txt": "!!! ???"  # Caso borde: un documento sin palabras útiles
    }

    # 2. Construir el índice
    indice, longitudes = build_inverted_index(documentos_prueba)

    print("Índice Invertido Construido:")
    print(json.dumps(indice, indent=2, ensure_ascii=False))
    print("\nLongitudes de Documentos:")
    print(longitudes)

    # 3. Validaciones de la estructura lógica
    assert "algoritmo" in indice, "Error: El término 'algoritmo' debería estar indexado."
    assert "doc_algoritmos.txt" in indice["algoritmo"], "Error: 'algoritmo' no se asoció a doc_algoritmos.txt"
    assert "doc_python.txt" in indice["algoritmo"], "Error: 'algoritmo' no se asoció a doc_python.txt"

    # Comprobar que las stop-words ('el', 'de', 'es') no están en el índice
    assert "el" not in indice, "Error: El índice contiene stop-words filtradas."

    # Comprobar longitudes (frecuencia de tokens reales)
    # doc_algoritmos.txt filtrado: ['algoritmo', 'ordenamiento', 'eficiente', 'rapido'] -> 4 tokens
    assert longitudes[
               "doc_algoritmos.txt"] == 4, f"Error en longitud: esperado 4, obtenido {longitudes['doc_algoritmos.txt']}"
    assert longitudes["doc_vacio.txt"] == 0, "Error en documento vacío"

    # 4. Probar persistencia en disco
    archivo_temporal = "data_database_test.json"
    try:
        save_index_state(indice, longitudes, archivo_temporal)
        print(f"\n[✓] Estado guardado exitosamente en '{archivo_temporal}'")

        indice_cargado, longitudes_cargadas = load_index_state(archivo_temporal)
        assert indice_cargado == indice, "Error: El índice cargado no coincide con el original."
        assert longitudes_cargadas == longitudes, "Error: Las longitudes cargadas no coinciden."
        print("[✓] Estado cargado y verificado correctamente desde el disco.")

    finally:
        # Limpieza del archivo de pruebas
        import os

        if os.path.exists(archivo_temporal):
            os.remove(archivo_temporal)

    print("\n¡Todos los tests del indexador pasaron exitosamente! 🚀")