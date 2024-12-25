import os
import sys
import argparse
import logging
import time
from typing import List, Tuple
from config_manager.config_manager import ConfigManager
from remote_manager.remote_manager import RemoteDeviceManager


LOG_FILE = "logs/esxi_control_system.logs"
CONF_FILE = "conf/conf.json"


# Determine the directory where the executable is located
if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller bundled executable
    base_dir = os.path.dirname(sys.executable)
else:  # Running in a regular Python environment
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure the logs directory exists
log_dir = os.path.dirname(LOG_FILE)
if not os.path.exists(log_dir):
    print(f'[-] Error: logs directory does not exists.')
    sys.exit(0)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_command_line_arguments():
    """
    Parse and retrieve command-line arguments for the UPS Control System Agent tool.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments.

    Raises:
        argparse.ArgumentError: If there are issues with argument parsing.
    """
    parser = argparse.ArgumentParser(
        description="ESXI Control System tool: A command-line tool for controlling remote devices."
    )

    parser.add_argument(
        "-s", "--shutdown",
        help="Send a shut down command to a remote terminal.\nExample usage: esxi_control_system -s",
        action="store_true",  # Use store_true to set shutdown as a boolean flag
        required=False
    )

    return parser.parse_args()


def shutdown_infrastructure(wait_time: int = 20) -> bool:
    """Shutdown all VMs and ESXi servers in the correct order.

    Args:
        wait_time: Time to wait between VM shutdown and ESXi shutdown (seconds)

    Returns:
        bool: True if shutdown was successful, False if critical errors occurred
    """
    try:
        config = ConfigManager(CONF_FILE)
        config.load_config()
    except Exception as e:
        logging.error("Failed to load configuration: %s", str(e))
        return False

    shutdown_results: List[Tuple[str, bool]] = []
    critical_error = False

    # First, shutdown all VMs across all ESXi servers
    logging.info("Starting VM shutdown sequence...")
    for server in config.esxi_servers:
        logging.info("Processing VMs on ESXi server: %s", server.name)

        for vm in server.vms:
            logging.info("Attempting to shutdown VM: %s (%s)",
                         vm.name, vm.ip)
            success = RemoteDeviceManager.poweroff_ubuntu_vm(
                vm.ip, vm.username, vm.password
            )
            shutdown_results.append((f"VM {vm.name}", success))

            if not success:
                logging.warning(
                    "Failed to shutdown VM: %s (%s)", vm.name, vm.ip
                )

    # Wait for VMs to shutdown completely
    logging.info(
        "Waiting %s seconds for VMs to shutdown completely...", wait_time)
    time.sleep(wait_time)

    # Then, shutdown ESXi servers
    logging.info("Starting ESXi servers shutdown sequence...")
    for server in config.esxi_servers:
        logging.info("Attempting to shutdown ESXi server: %s", server.name)
        success = RemoteDeviceManager.poweroff_esxi_server(
            server.ip, server.username, server.password
        )
        shutdown_results.append((f"ESXi {server.name}", success))

        if not success:
            logging.error(
                "Failed to shutdown ESXi server: %s (%s)",
                server.name, server.ip
            )
            critical_error = True

    # Log summary
    logging.info("\nShutdown Summary:")
    for device, success in shutdown_results:
        status = "SUCCESS" if success else "FAILED"
        logging.info("%s: %s", device, status)

    return not critical_error


def main():
    """
    Main function to handle command-line arguments and execute appropriate actions.

    Returns:
        bool: True if the command was executed successfully, False otherwise.

    Raises:
        argparse.ArgumentError: If there are issues with argument parsing.
        Exception: For unexpected errors during execution.
    """
    try:
        args = get_command_line_arguments()

        if args.shutdown:
            if shutdown_infrastructure():
                print(True)
                return True
            else:
                logging.error(
                    f"Error: Failed to shutdown the infrastructure.")
                print(False)
                return False

        else:
            logging.error("Error: No valid command provided.")
            print(False)
            return False

    except argparse.ArgumentError as e:
        logging.error(f"Argument parsing error: {e}")
        print(False)
        return False

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(False)
        return False


if __name__ == "__main__":
    main()
