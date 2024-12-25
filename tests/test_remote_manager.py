import unittest
from unittest.mock import patch, MagicMock
import subprocess
from src.remote_manager.remote_manager import RemoteDeviceManager


class TestRemoteDeviceManager(unittest.TestCase):
    @patch('subprocess.run')
    def test_is_device_online_success(self, mock_subprocess):
        mock_subprocess.return_value.returncode = 0
        self.assertTrue(RemoteDeviceManager.is_device_online('192.168.1.100'))

    @patch('subprocess.run')
    def test_is_device_online_timeout(self, mock_subprocess):
        mock_subprocess.side_effect = subprocess.TimeoutExpired('ping', 1)
        self.assertFalse(RemoteDeviceManager.is_device_online('192.168.1.100'))

    @patch('subprocess.run')
    def test_is_device_online_error(self, mock_subprocess):
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'ping')
        self.assertFalse(RemoteDeviceManager.is_device_online('192.168.1.100'))

    @patch('paramiko.SSHClient')
    def test_ssh_connect_success(self, mock_ssh_client):
        ssh_client = RemoteDeviceManager.ssh_connect(
            '192.168.1.100', 'admin', 'password')
        self.assertIsInstance(ssh_client, MagicMock)

    @patch('src.remote_manager.remote_manager.RemoteDeviceManager.is_device_online')
    @patch('src.remote_manager.remote_manager.RemoteDeviceManager.ssh_connect')
    def test_poweroff_ubuntu_vm_success(self, mock_ssh_connect, mock_is_device_online):
        mock_is_device_online.return_value = True
        mock_ssh_client = MagicMock()
        mock_ssh_connect.return_value = mock_ssh_client
        mock_ssh_client.exec_command.return_value = (
            MagicMock(), MagicMock(), MagicMock(read=lambda: b'[sudo] password for'))

        self.assertTrue(RemoteDeviceManager.poweroff_ubuntu_vm(
            '192.168.1.101', 'admin', 'password'))

    @patch('src.remote_manager.remote_manager.RemoteDeviceManager.is_device_online')
    @patch('src.remote_manager.remote_manager.RemoteDeviceManager.ssh_connect')
    def test_poweroff_ubuntu_vm_offline(self, mock_ssh_connect, mock_is_device_online):
        mock_is_device_online.return_value = False
        self.assertFalse(RemoteDeviceManager.poweroff_ubuntu_vm(
            '192.168.1.101', 'admin', 'password'))

    @patch('src.remote_manager.remote_manager.RemoteDeviceManager.is_device_online')
    @patch('src.remote_manager.remote_manager.RemoteDeviceManager.ssh_connect')
    def test_poweroff_esxi_server_success(self, mock_ssh_connect, mock_is_device_online):
        mock_is_device_online.return_value = True
        mock_ssh_client = MagicMock()
        mock_ssh_connect.return_value = mock_ssh_client

        self.assertTrue(RemoteDeviceManager.poweroff_esxi_server(
            '192.168.1.100', 'admin', 'password'))

    @patch('src.remote_manager.remote_manager.RemoteDeviceManager.is_device_online')
    @patch('src.remote_manager.remote_manager.RemoteDeviceManager.ssh_connect')
    def test_poweroff_esxi_server_offline(self, mock_ssh_connect, mock_is_device_online):
        mock_is_device_online.return_value = False
        self.assertFalse(RemoteDeviceManager.poweroff_esxi_server(
            '192.168.1.100', 'admin', 'password'))


if __name__ == '__main__':
    unittest.main()
