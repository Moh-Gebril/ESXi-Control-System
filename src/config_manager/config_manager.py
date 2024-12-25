from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path
import json
from tabulate import tabulate


@dataclass
class VMConfig:
    name: str
    ip: str
    username: str
    password: str


@dataclass
class ESXiConfig:
    name: str
    ip: str
    username: str
    password: str
    vms: List[VMConfig]


class ConfigManager:
    def __init__(self, config_path: str):
        """Initialize the configuration manager.

        Args:
            config_path: Path to the configuration file
        """
        self.config_path = Path(config_path)
        self.esxi_servers: List[ESXiConfig] = []

    def load_config(self) -> None:
        """Load and parse the configuration file."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}")

        try:
            with open(self.config_path, 'r') as f:
                config_data = json.load(f)

            self.esxi_servers = []
            for server in config_data.get('esxi_servers', []):
                vms = [
                    VMConfig(
                        name=vm['name'],
                        ip=vm['ip'],
                        username=vm['username'],
                        password=vm['password']
                    )
                    for vm in server.get('vms', [])
                ]

                self.esxi_servers.append(
                    ESXiConfig(
                        name=server['name'],
                        ip=server['ip'],
                        username=server['username'],
                        password=server['password'],
                        vms=vms
                    )
                )

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in config file: {e}")
        except KeyError as e:
            raise ValueError(f"Missing required field in config file: {e}")

    def get_server_by_name(self, server_name: str) -> Optional[ESXiConfig]:
        """Get server configuration by server name."""
        return next((server for server in self.esxi_servers
                    if server.name == server_name), None)

    def get_vm_by_name(self, server_name: str, vm_name: str) -> Optional[VMConfig]:
        """Get VM configuration by server name and VM name."""
        server = self.get_server_by_name(server_name)
        if server:
            return next((vm for vm in server.vms if vm.name == vm_name), None)
        return None

    def display_all_servers(self, show_passwords: bool = False) -> None:
        """Display all ESXi servers and their VMs in a formatted table.

        Args:
            show_passwords: Whether to display password information
        """
        print("\n=== ESXi Servers Configuration ===\n")

        for server in self.esxi_servers:
            # Server information
            server_headers = ["Server Name", "IP", "Username"]
            server_data = [[server.name, server.ip, server.username]]

            if show_passwords:
                server_headers.append("Password")
                server_data[0].append(server.password)

            print(tabulate(server_data, headers=server_headers, tablefmt="grid"))

            # VMs information
            vm_headers = ["VM Name", "IP", "Username"]
            if show_passwords:
                vm_headers.append("Password")

            vm_data = []
            for vm in server.vms:
                vm_row = [vm.name, vm.ip, vm.username]
                if show_passwords:
                    vm_row.append(vm.password)
                vm_data.append(vm_row)

            print("\nVirtual Machines:")
            print(tabulate(vm_data, headers=vm_headers, tablefmt="grid"))
            print("\n" + "="*50 + "\n")

    def display_server(self, server_name: str, show_passwords: bool = False) -> None:
        """Display configuration for a specific ESXi server and its VMs.

        Args:
            server_name: Name of the server to display
            show_passwords: Whether to display password information
        """
        server = self.get_server_by_name(server_name)
        if not server:
            print(f"Server '{server_name}' not found in configuration.")
            return

        print(f"\n=== Configuration for ESXi Server: {server_name} ===\n")

        # Server information
        server_headers = ["Server Name", "IP", "Username"]
        server_data = [[server.name, server.ip, server.username]]

        if show_passwords:
            server_headers.append("Password")
            server_data[0].append(server.password)

        print(tabulate(server_data, headers=server_headers, tablefmt="grid"))

        # VMs information
        vm_headers = ["VM Name", "IP", "Username"]
        if show_passwords:
            vm_headers.append("Password")

        vm_data = []
        for vm in server.vms:
            vm_row = [vm.name, vm.ip, vm.username]
            if show_passwords:
                vm_row.append(vm.password)
            vm_data.append(vm_row)

        print("\nVirtual Machines:")
        print(tabulate(vm_data, headers=vm_headers, tablefmt="grid"))
        print()

    def get_servers_summary(self) -> None:
        """Display a summary of all ESXi servers and their VM counts."""
        print("\n=== ESXi Servers Summary ===\n")

        headers = ["Server Name", "IP", "Total VMs"]
        data = [[server.name, server.ip, len(server.vms)]
                for server in self.esxi_servers]

        print(tabulate(data, headers=headers, tablefmt="grid"))
        print()
