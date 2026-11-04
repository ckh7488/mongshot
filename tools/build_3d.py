"""Rebuild the local/offline Three.js viewer with esbuild; never loads a CDN."""
from pathlib import Path
import subprocess,shutil,os
R=Path(__file__).resolve().parents[1]
choices=[os.environ.get('MONGSHOT_ESBUILD'),str(R/'node_modules/.bin/esbuild.cmd'),str(R.parent/'mongshot_review/.tools/esbuild.exe'),shutil.which('esbuild')]
exe=next((x for x in choices if x and Path(x).exists()),None)
if not exe:raise SystemExit('esbuild is needed to rebuild 3D. Install the package or set MONGSHOT_ESBUILD. The included offline HTML/bundle remains usable.')
subprocess.run([exe,'simulation/source/cabinet3d.js','--bundle','--format=iife','--global-name=Mongshot3D','--minify','--legal-comments=inline','--alias:three='+str(R/'simulation/vendor/three/three.module.js'),'--outfile=simulation/vendor/cabinet3d.bundle.js'],cwd=R,check=True)
