import string
import unicodedata

def load_stop_words() -> set[str]:
    """Carga una lista optimizada de stop words en español con y sin tildes."""
    return {
        "el", "la", "los", "las", "un", "una", "unos", "unas", "lo", "al", "del",
        "de", "a", "en", "para", "por", "con", "sin", "sobre", "tras", "durante",
        "y", "e", "o", "u", "que", "pero", "porque", "como", "mas", "más",
        "su", "sus", "es", "son", "fue", "eran", "este", "esta", "estos", "estas",
        "el", "él", "ella", "ellos", "mi", "mis", "tu", "tus", "un", "unificado"
    }

# OPTIMIZACIÓN: Se carga una sola vez al importar el módulo (Complejidad O(1) en búsquedas)
STOP_WORDS = load_stop_words()

def remove_accents(text: str) -> str:
    """
    Transforma caracteres como 'Árból' o 'Niño' en 'arbol' y 'nino' o mantiene la ñ
    según prefieras. Para motores de búsqueda estándar, remover todo es lo más eficiente.
    """
    # Descompone caracteres con tilde en su letra base + el acento flotante
    text = unicodedata.normalize('NFKD', text)
    # Filtra y descarta los caracteres que sean puramente acentos/diacríticos
    return "".join([c for c in text if not unicodedata.combining(c)])

def preprocess_text(text: str) -> list[str]:
    """
    Preprocesamiento robusto de nivel de producción.
    """
    if not text:
        return []

    # 1. Convertir a minúsculas y normalizar tildes/acentos
    text = text.lower()
    text = remove_accents(text)

    # 2. Reemplazar saltos de línea y tabulaciones por espacios comunes
    text = text.replace("\n", " ").replace("\t", " ")

    # 3. Eliminar signos de puntuación de forma ultra-eficiente
    # Nota: string.punctuation cubre !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)

    # 4. Tokenizar por espacios en blanco continuos
    tokens = text.split()

    # 5. Filtrar Stop Words
    filtered_tokens = [token for token in tokens if token not in STOP_WORDS]

    return filtered_tokens