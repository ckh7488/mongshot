"""Build v6 beside the immutable v5.3 workbench; do not overwrite its records."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
for script in ['build_v6.py']:
 subprocess.run([sys.executable,str(ROOT/'tools'/script)],cwd=ROOT,check=True)
print('v6 rebuilt. v5.3 preserved. Historical PDF belongs to v5.3; v6 uses CSV/SVG coordinates.')
