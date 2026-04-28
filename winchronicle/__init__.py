"""Repository-root bootstrap for `python -m winchronicle`.

The implementation package lives in `src/winchronicle`. This tiny wrapper makes
the command work from a fresh checkout before an editable install exists.
"""

from pathlib import Path

_SRC_PACKAGE = Path(__file__).resolve().parent.parent / "src" / "winchronicle"
if _SRC_PACKAGE.exists():
    __path__.append(str(_SRC_PACKAGE))

from ._version import __version__
