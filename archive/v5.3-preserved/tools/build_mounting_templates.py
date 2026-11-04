"""Current PDF generator entry point (PyMuPDF)."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("build_mounting_templates_fitz.py")),run_name="__main__")
