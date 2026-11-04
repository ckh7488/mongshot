"""Compatibility entry: validate the current two-bay target."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("check-design.py")),run_name="__main__")
