import os
from pathlib import Path
import pdfplumber

INPUT_DIR = Path("data/pdfs")
OUTPUT_DIR = Path("data/processed_txt")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def convertir_pdf_a_texto(pdf_path: Path):
    """Convierte un PDF a texto plano usando pdfplumber."""
    txt_path = OUTPUT_DIR / (pdf_path.stem + ".txt")
    with pdfplumber.open(pdf_path) as pdf:
        texto = ""
        for page in pdf.pages:
            texto += page.extract_text() or ""
    txt_path.write_text(texto, encoding="utf-8")
    print(f"✅ {pdf_path.name} → {txt_path.name}")

def main():
    pdfs = list(INPUT_DIR.glob("*.pdf"))
    if not pdfs:
        print("⚠️ No se encontraron PDFs en data/pdfs/")
        return
    print(f"📄 Convirtiendo {len(pdfs)} documentos...")
    for pdf in pdfs:
        convertir_pdf_a_texto(pdf)
    print("🏁 Conversión completa.")

if __name__ == "__main__":
    main()
