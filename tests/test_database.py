from src.database import *

if __name__ == "__main__":
    print("=== Ejecutando pruebas de database.py ===\n")

    # Datos de prueba simulando la interacción de los integrantes 2 y 3
    indice_mock = {"python": {"doc1.txt": 1}}
    vectores_mock = {"doc1.txt": {"python": 0.5}}
    idf_mock = {"python": 1.2}
    docs_mock = {"doc1.txt": "Python es genial."}

    ruta_test = "data/database_test.json"

    try:
        # Test 1: Guardar base de datos
        save_database(indice_mock, vectores_mock, idf_mock, docs_mock, ruta_test)
        print(f"[✓] Base de datos de prueba guardada correctamente en '{ruta_test}'.")

        # Test 2: Cargar y verificar integridad
        idx, vec, idf, docs = load_database(ruta_test)

        assert idx == indice_mock, "Error: El índice invertido cambió al persistirse."
        assert vec == vectores_mock, "Error: En los vectores TF-IDF."
        assert idf == idf_mock, "Error: En el diccionario IDF Global."
        assert docs == docs_mock, "Error: Los documentos originales difieren."
        print("[✓] Carga e integridad de datos validadas con éxito.")

    finally:
        # Limpieza automática del entorno de pruebas
        if os.path.exists(ruta_test):
            os.remove(ruta_test)
            # Si la carpeta 'data' quedó vacía y se creó solo para el test, puedes optar por quitarla
            print("[✓] Limpieza de archivos temporales finalizada.")

    print("\n¡El módulo de persistencia funciona perfectamente! 💾")