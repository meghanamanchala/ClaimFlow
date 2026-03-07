from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parent / "claims-management" / "backend"
BACKEND_MAIN = BACKEND_DIR / "main.py"

sys.path.insert(0, str(BACKEND_DIR))

spec = spec_from_file_location("claimflow_backend_main", BACKEND_MAIN)
if spec is None or spec.loader is None:
	raise RuntimeError("Unable to load backend main module")

module = module_from_spec(spec)
spec.loader.exec_module(module)
app = module.app
