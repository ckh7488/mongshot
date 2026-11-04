from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('check-design-v5.py')),run_name='__main__')

runpy.run_path(str(Path(__file__).with_name('check-design-v6.py')),run_name='__main__')

runpy.run_path(str(Path(__file__).with_name('check-route-clearance-v6.py')),run_name='__main__')

runpy.run_path(str(Path(__file__).with_name('check-harness-v61.py')),run_name='__main__')
