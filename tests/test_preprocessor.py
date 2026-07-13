from src.preprocessor import *

if __name__ == "__main__":
    print("=== Ejecutando pruebas de preprocessor.py ===\n")

    # Caso 1: Texto estándar con puntuación mixta y mayúsculas
    texto_1 = "¡Hola Mundo! Este es un proyecto de Algoritmos II, escrito en Python."
    resultado_1 = preprocess_text(texto_1)
    print(f"Test 1 (Estándar):\n -> Entrada: '{texto_1}'\n -> Resultado: {resultado_1}\n")
    # Esperado: ['hola', 'mundo', 'proyecto', 'algoritmos', 'ii', 'escrito', 'python']

    # Caso 2: Manejo de espacios múltiples, tabulaciones y saltos de línea
    texto_2 = "Texto con   muchos    espacios,\nlineas nuevas\ty tabulaciones."
    resultado_2 = preprocess_text(texto_2)
    print(f"Test 2 (Espaciado):\n -> Resultado: {resultado_2}\n")
    # Esperado: ['texto', 'muchos', 'espacios', 'lineas', 'nuevas', 'tabulaciones']

    # Caso 3: String vacío o con solo puntuación
    texto_3 = "!!! ... ??? ---"
    resultado_3 = preprocess_text(texto_3)
    print(f"Test 3 (Borde - Solo puntuación):\n -> Resultado: {resultado_3}\n")
    # Esperado: []

    # Verificaciones lógicas rápidas
    assert "el" not in resultado_1, "Error: Las stop words no se están filtrando."
    assert "Algoritmos" not in resultado_1, "Error: No se está convirtiendo a minúsculas."
    print("¡Todos los tests pasaron exitosamente! 🎉")