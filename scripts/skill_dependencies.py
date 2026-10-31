#!/usr/bin/env python3
"""Repository shim; the installed tk-setup-skills package owns implementation."""
import importlib.util
from pathlib import Path
import sys

_IMPL = Path(__file__).resolve().parents[1] / 'skills/tk-setup-skills/scripts/skill_dependencies.py'
_SPEC = importlib.util.spec_from_file_location('_tk_skill_dependencies', _IMPL)
assert _SPEC is not None and _SPEC.loader is not None
_BYTECODE = sys.dont_write_bytecode
try:
    sys.dont_write_bytecode = True
    _MODULE = importlib.util.module_from_spec(_SPEC)
    _SPEC.loader.exec_module(_MODULE)
finally:
    sys.dont_write_bytecode = _BYTECODE
validate_dependencies = _MODULE.validate_dependencies
main = _MODULE.main

if __name__ == '__main__':
    sys.exit(main())
