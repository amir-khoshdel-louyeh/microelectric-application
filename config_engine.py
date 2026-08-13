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

    @staticmethod
    def create_project_workspace(project_path: str) -> Dict[str, Dict[str, Any]]:
        """Initialize a new project directory and copy default .dat templates into it."""
        os.makedirs(project_path, exist_ok=True)
        config_data = {}
        for filename in CONFIG_FILES:
            dest_path = os.path.join(project_path, filename)
            src_path = os.path.join(TEMPLATE_DIR, filename)
            if os.path.exists(src_path) and not os.path.exists(dest_path):
                shutil.copy(src_path, dest_path)
            # Parse configured file
            category = filename.replace('.dat', '')
            config_data[category] = ConfigEngine.parse_dat_file(dest_path)
        return config_data

    @staticmethod
    def load_project_workspace(project_path: str) -> Dict[str, Dict[str, Any]]:
        """Load an existing project directory and parse all available .dat configuration files."""
        config_data = {}
        if not os.path.exists(project_path):
            return config_data

        for filename in CONFIG_FILES:
            file_path = os.path.join(project_path, filename)
            category = filename.replace('.dat', '')
            if os.path.exists(file_path):
                config_data[category] = ConfigEngine.parse_dat_file(file_path)
            else:
                # If missing, fall back to template default
                src_path = os.path.join(TEMPLATE_DIR, filename)
                if os.path.exists(src_path):
                    config_data[category] = ConfigEngine.parse_dat_file(src_path)
                else:
                    config_data[category] = {}
        return config_data

    @staticmethod
    def validate_parameters(config_data: Dict[str, Dict[str, Any]]) -> Dict[str, List[str]]:
        """Run physical parameter sanity checks across all loaded dataset modules."""
        errors = []
        warnings = []

        # Check Ferro Geometry bounds
        fg = config_data.get('Ferro_Geometry', {})
        for dim in ('Nx', 'Ny', 'Nz'):
            val = fg.get(dim)
            if val is not None and (not isinstance(val, int) or val <= 0):
                errors.append(f"Grid dimension '{dim}' must be a positive integer (got {val}).")

        for spacing in ('dx', 'dy', 'dz'):
            val = fg.get(spacing)
            if val is not None and (not isinstance(val, (int, float)) or val <= 0):
                errors.append(f"Grid spacing '{spacing}' must be a positive number (got {val}).")

        # Check Electrostatics
        el = config_data.get('Electrostatic', {})
        vac_p = el.get('vacuum_permittivity')
        if vac_p is not None and (not isinstance(vac_p, (int, float)) or vac_p <= 0):
            warnings.append("Vacuum permittivity should be a positive physical constant (~8.854e-12).")

        for rel in ('relative_permittivity_xx', 'relative_permittivity_yy', 'relative_permittivity_zz'):
            val = el.get(rel)
            if val is not None and (not isinstance(val, (int, float)) or val <= 0):
                errors.append(f"Relative permittivity '{rel}' must be positive (got {val}).")

        # Check Temperature in Landau Free Energy
        lf = config_data.get('Landau_Free', {})
        temp = lf.get('Temperature')
        if temp is not None and (not isinstance(temp, (int, float)) or temp < 0):
            errors.append(f"Temperature must be non-negative in Kelvin (got {temp}).")

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }


