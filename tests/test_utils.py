from src.utils import *
if __name__ == "__main__":
    print("=== Ejecutando pruebas de utils.py ===\n")

    carpeta_test = "data_documents_test"
    archivo_test = os.path.join(carpeta_test, "test_doc.txt")

    try:
        # 1. Crear entorno de prueba temporal
        os.makedirs(carpeta_test, exist_ok=True)
        with open(archivo_test, "w", encoding="utf-8") as f:
            f.write("Este es un documento de prueba para el módulo de utilidades.")

        # 2. Test de validación de directorio
        assert validate_directory(carpeta_test) == True, "Error: Debería haber validado la carpeta como válida."
        assert validate_directory(
            "carpeta_fantasma_seguro_no_existe") == False, "Error: Validó una carpeta inexistente."
        print("[✓] Validación de directorios comprobada.")

        # 3. Test de carga de documentos
        documentos_cargados = load_documents(carpeta_test)
        assert "test_doc.txt" in documentos_cargados, "Error: No se cargó el archivo de texto de prueba."
        assert "prueba" in documentos_cargados["test_doc.txt"], "Error: El contenido leído no es correcto."
        print("[✓] Carga de documentos e integridad de lectura comprobadas.")

    finally:
        # Limpieza
        if os.path.exists(archivo_test):
            os.remove(archivo_test)
        if os.path.exists(carpeta_test):
            os.rmdir(carpeta_test)
        print("[✓] Entorno temporal de pruebas removido.")

    print("\n¡El módulo de utilidades está listo para integrarse! 📦")