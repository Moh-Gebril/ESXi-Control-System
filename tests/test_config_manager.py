import unittest
from unittest.mock import mock_open, patch
from src.config_manager.config_manager import ConfigManager, VMConfig, ESXiConfig


class TestConfigManager(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='{"esxi_servers": []}')
    def test_load_config_success(self, mock_file):
        config_manager = ConfigManager('conf/conf.json')
        config_manager.load_config()
        self.assertEqual(config_manager.esxi_servers, [])

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_config_file_not_found(self, mock_file):
        config_manager = ConfigManager('config.json')
        with self.assertRaises(FileNotFoundError):
            config_manager.load_config()

    @patch('builtins.open', new_callable=mock_open, read_data='{"esxi_servers": [{"name": "prod-esxi-01", "ip": "192.168.1.100", "username": "admin", "password": "esxi_password", "vms": [{"name": "web-server-01", "ip": "192.168.1.101", "username": "webadmin", "password": "web_password"}]}]}')
    def test_load_config_with_valid_data(self, mock_file):
        config_manager = ConfigManager('conf/conf.json')
        config_manager.load_config()

        self.assertEqual(len(config_manager.esxi_servers), 1)
        esxi_server = config_manager.esxi_servers[0]
        self.assertEqual(esxi_server.name, "prod-esxi-01")
        self.assertEqual(esxi_server.ip, "192.168.1.100")
        self.assertEqual(esxi_server.username, "admin")
        self.assertEqual(esxi_server.password, "esxi_password")
        self.assertEqual(len(esxi_server.vms), 1)
        vm = esxi_server.vms[0]
        self.assertEqual(vm.name, "web-server-01")
        self.assertEqual(vm.ip, "192.168.1.101")
        self.assertEqual(vm.username, "webadmin")
        self.assertEqual(vm.password, "web_password")

    @patch('builtins.open', new_callable=mock_open, read_data='{"esxi_servers": [{"name": "prod-esxi-01", "ip": "192.168.1.100", "username": "admin"}]}')
    def test_load_config_with_missing_field(self, mock_file):
        config_manager = ConfigManager('conf/conf.json')
        with self.assertRaises(ValueError):
            config_manager.load_config()


if __name__ == '__main__':
    unittest.main()
