import os
import pypdf
import docx


def validate_directory(directory: str) -> bool:
    """Valida que la carpeta exista y tenga archivos soportados."""
    if not os.path.isdir(directory):
        return False
    try:
        formatos = (".txt", ".pdf", ".docx")
        return any(f.lower().endswith(formatos) for f in os.listdir(directory))
    except Exception:
        return False


def _read_txt(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _read_pdf(filepath: str) -> str:
    """Extrae texto de archivos PDF de múltiples páginas."""
    text_content = []
    try:
        reader = pypdf.PdfReader(filepath)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)
        return "\n".join(text_content)
    except Exception as e:
        print(f"[!] Error leyendo el PDF {os.path.basename(filepath)}: {e}")
        return ""


def _read_docx(filepath: str) -> str:
    """Extrae texto de archivos estructurados de Microsoft Word."""
    try:
        doc = docx.Document(filepath)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        print(f"[!] Error leyendo el archivo Word {os.path.basename(filepath)}: {e}")
        return ""


def load_documents(directory: str) -> dict[str, str]:
    """Scanea la carpeta objetivo y lee dinámicamente según la extensión."""
    documents = {}
    if not os.path.exists(directory):
        return documents

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isdir(filepath):
            continue

        ext = filename.lower()
        text = ""

        if ext.endswith(".txt"):
            text = _read_txt(filepath)
        elif ext.endswith(".pdf"):
            text = _read_pdf(filepath)
        elif ext.endswith(".docx"):
            text = _read_docx(filepath)

        if text.strip():  # Solo añade si logramos extraer texto real
            documents[filename] = text

    return documents