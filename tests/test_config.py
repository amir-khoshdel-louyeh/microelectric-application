import os
import shutil
import tempfile
import unittest
from config_engine import ConfigEngine
from app import app


class TestConfigEngine(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix='microelectric_test_')
        self.app = app.test_client()

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_create_workspace(self):
        config_data = ConfigEngine.create_project_workspace(self.test_dir)
        self.assertIn('Landau_Free', config_data)
        self.assertIn('Electrostatic', config_data)
        self.assertIn('Ferro_Geometry', config_data)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'Landau_Free.dat')))

    def test_parse_and_write_dat(self):
        file_path = os.path.join(self.test_dir, 'sample.dat')
        params = {'alpha1': -1.25e8, 'Nx': 64, 'mode': 'random_noise'}
        ConfigEngine.write_dat_file(file_path, params, header_comment="Test Header")

        parsed = ConfigEngine.parse_dat_file(file_path)
        self.assertAlmostEqual(parsed['alpha1'], -1.25e8)
        self.assertEqual(parsed['Nx'], 64)
        self.assertEqual(parsed['mode'], 'random_noise')

    def test_parameter_validation(self):
        valid_data = {
            'Ferro_Geometry': {'Nx': 64, 'Ny': 64, 'Nz': 32, 'dx': 1.0, 'dy': 1.0, 'dz': 1.0},
            'Electrostatic': {'relative_permittivity_xx': 100.0, 'vacuum_permittivity': 8.854e-12},
            'Landau_Free': {'Temperature': 298.15}
        }
        res_valid = ConfigEngine.validate_parameters(valid_data)
        self.assertTrue(res_valid['valid'])

        invalid_data = {
            'Ferro_Geometry': {'Nx': -10, 'dx': 0},
            'Landau_Free': {'Temperature': -50}
        }
        res_invalid = ConfigEngine.validate_parameters(invalid_data)
        self.assertFalse(res_invalid['valid'])
        self.assertGreater(len(res_invalid['errors']), 0)

    def test_flask_routes(self):
        res = self.app.get('/')
        self.assertEqual(res.status_code, 200)

        res_ws = self.app.get(f'/workspace?path={self.test_dir}')
        self.assertEqual(res_ws.status_code, 200)

        # Test save endpoint
        save_payload = {
            'project_path': self.test_dir,
            'config_data': {
                'Landau_Free': {'alpha1': -1.5e8, 'Temperature': 300.0}
            }
        }
        res_save = self.app.post('/api/config/save', json=save_payload)
        self.assertEqual(res_save.status_code, 200)
        json_data = res_save.get_json()
        self.assertEqual(json_data['status'], 'success')


if __name__ == '__main__':
    unittest.main()
