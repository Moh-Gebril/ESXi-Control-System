"""
Module for managing remote devices via SSH.
"""
import subprocess
import logging
import paramiko

# pylint: disable=W0718
class RemoteDeviceManager:
    """
    A class with static methods to manage remote devices through SSH.
    """
    @staticmethod
    def is_device_online(host):
        """
        Check if the device is online by pinging it with minimal overhead.

        Args:
            host (str): The hostname or IP address of the remote device.

        Returns:
            bool: True if the device responds to the ping, False otherwise.
        """
        try:
            result = subprocess.run(
                ["ping", "-c", "2", "-W", "1", host],
                stdout=subprocess.DEVNULL,  
                stderr=subprocess.DEVNULL,
                timeout=3,  
                check=True
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            logging.warning("Ping command timed out for %s.", host)
            return False
        except subprocess.CalledProcessError:
            logging.warning("Ping command failed for %s.", host)
            return False
        except Exception as e:
            logging.error(
                "An unexpected error occurred while pinging %s: %s", host, str(e))
            return False

    @staticmethod
    def ssh_connect(host, username, password, port=22):
        """
            Establish an SSH connection to the remote device.

        Args:
            host (str): The hostname or IP address of the remote device.
            username (str): The SSH username.
            password (str): The SSH password.
            port (int): The SSH port. Default is 22.

        Returns:
            paramiko.SSHClient: The SSH client instance or False if connection fails.
        """
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh_client.connect(hostname=host, port=port, username=username,
                               password=password, allow_agent=False, look_for_keys=False)
            return ssh_client
        except paramiko.AuthenticationException:
            logging.error(
                "Failed to connect to %s: Authentication failed.", host)
            return False
        except paramiko.SSHException as e:
            logging.error("Failed to connect to %s: %s", host, str(e))
            return False
        except Exception as e:
            logging.error("Failed to connect to %s: %s", host, str(e))
            return False

    @staticmethod
    def poweroff_ubuntu_vm(host, username, password, port=22):  # pylint: disable=R0911
        """
        Power off the remote server.

        Args:
            host (str): The hostname or IP address of the remote device.
            username (str): The SSH username.
            password (str): The SSH password.
            port (int): The SSH port. Default is 22.

        Returns:
            bool: True if the poweroff command was sent successfully, False otherwise.
        """
        if not RemoteDeviceManager.is_device_online(host):
            logging.warning(
                "%s is offline. Cannot proceed with power off.", host)
            return False

        try:
            ssh_client = RemoteDeviceManager.ssh_connect(
                host, username, password, port)
            if not ssh_client:
                return False

            stdin, _, stderr = ssh_client.exec_command('sudo -S poweroff')

            stdin.write(password + '\n')
            stdin.flush()

            error = stderr.read().decode('utf-8')

            if '[sudo] password for' in error:
                logging.info("%s poweroff command sent successfully.", host)
                ssh_client.close()
                return True

            logging.error(
                "Error executing poweroff command on %s: %s", host, error.strip())
            ssh_client.close()
            return False

        except paramiko.AuthenticationException:
            logging.error(
                "Failed to connect to %s: Authentication failed.", host)
            return False
        except paramiko.SSHException as e:
            logging.error("Failed to connect to %s: %s", host, str(e))
            return False
        except Exception as e:
            logging.error("Failed to power off %s: %s", host, str(e))
            return False

    @staticmethod
    def poweroff_esxi_server(host, username, password, port=22):  # pylint: disable=R0911
        """
            Power off the remote server.

            Args:
                host (str): The hostname or IP address of the remote device.
                username (str): The SSH username.
                password (str): The SSH password.
                port (int): The SSH port. Default is 22.

            Returns:
                bool: True if the poweroff command was sent successfully, False otherwise.
            """
        if not RemoteDeviceManager.is_device_online(host):
            logging.warning(
                "%s is offline. Cannot proceed with power off.", host)
            return False

        try:
            ssh_client = RemoteDeviceManager.ssh_connect(
                host, username, password, port)
            if not ssh_client:
                return False

            ssh_client.exec_command('poweroff')

            logging.info("%s poweroff command sent successfully.", host)
            ssh_client.close()
            return True

        except paramiko.AuthenticationException:
            logging.error(
                "Failed to connect to %s: Authentication failed.", host)
            return False
        except paramiko.SSHException as e:
            logging.error("Failed to connect to %s: %s", host, str(e))
            return False
        except Exception as e:
            logging.error("Failed to power off %s: %s", host, str(e))
            return False
