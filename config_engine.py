import os
import shutil
from typing import Dict, Any, List, Tuple

CONFIG_FILES = [
    'Landau_Free.dat',
    'Electrostatic.dat',
    'Ferro_Geometry.dat',
    'Gradient_Field.dat',
    'Initial_Polarization.dat',
    'External_Field.dat'
]

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'file_configuration')


class ConfigEngine:
    """Parser, serializer, and validator engine for microelectric simulation .dat configuration files."""

    @staticmethod
    def parse_dat_file(file_path: str) -> Dict[str, Any]:
        """Parse a .dat parameter file into a Python dictionary."""
        params = {}
        if not os.path.exists(file_path):
            return params

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    parts = line.split('=', 1)
                    key = parts[0].strip()
                    raw_val = parts[1].strip()
                    # Parse numerical values if possible
                    params[key] = ConfigEngine._parse_value(raw_val)
        return params

    @staticmethod
    def _parse_value(val_str: str) -> Any:
        """Helper to cast string values to int, float, or raw string."""
        if val_str.lower() in ('true', 'false'):
            return val_str.lower() == 'true'
        try:
            if '.' in val_str or 'e' in val_str.lower():
                return float(val_str)
            return int(val_str)
        except ValueError:
            return val_str

    @staticmethod
    def write_dat_file(file_path: str, params: Dict[str, Any], header_comment: str = "") -> None:
        """Serialize a parameter dictionary back into a formatted .dat text file."""
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            if header_comment:
                f.write(f"# {header_comment}\n\n")
            for key, val in params.items():
                if isinstance(val, float):
                    # Format scientific notation cleanly if needed
                    val_str = f"{val:.6e}" if (abs(val) < 1e-3 or abs(val) >= 1e5) and val != 0 else str(val)
                else:
                    val_str = str(val)
                f.write(f"{key} = {val_str}\n")
