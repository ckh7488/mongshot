"""Rebuild the current v5 isolated compact cabinet and tested AVR workbench."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
for script in ['draw_cabinet.py','draw_frontpanel.py','redesign_v5.py']:
 subprocess.run([sys.executable,str(ROOT/'tools'/script)],cwd=ROOT,check=True)
print('Current two-bay project regenerated. PDF: tools/build_mounting_templates.py')
