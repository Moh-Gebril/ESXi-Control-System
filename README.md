# ESXi Control System

ESXi Control System is a cutting-edge Python-based tool designed for centralized management of ESXi servers and their virtual machines (VMs). It is particularly suited for IT administrators, system engineers, and DevOps professionals who require efficient and secure management of their virtualized infrastructure.

The system currently features a robust orchestration mechanism for the graceful shutdown of ESXi servers and their associated VMs. Built with modularity and extensibility in mind, the architecture allows seamless integration of additional functionalities like performance monitoring, network configuration, backup operations, and more.

With support for Docker, detailed logging, and comprehensive unit testing, the tool ensures reliability and cross-platform compatibility. It also prioritizes security by leveraging SSH-based remote management and structured JSON configuration files for defining infrastructure setups.

## Features

### Current Features

- 🔄 Orchestrated shutdown of ESXi servers and their VMs
- 🔒 Secure SSH-based remote management
- ⚙️ JSON-based configuration for easy infrastructure setup
- 🐳 Docker support for cross-platform compatibility
- 🧪 Comprehensive unit testing
- 📝 Detailed logging system

### Extensible Architecture

The tool is designed with modularity in mind, enabling easy implementation of additional features such as:

- VM Management (create, delete, clone, snapshot)
- Resource Management (CPU, memory, storage allocation)
- Performance Monitoring
- Network Configuration
- Backup and Recovery Operations
- Health Checks and Diagnostics
- Automated Maintenance Tasks
- Bulk Operations and Scheduling
- Custom Command Execution
- Template Management

## Prerequisites

- Python 3.11 or higher
- SSH access to ESXi servers and VMs
- Sudo privileges on target VMs
- Docker (optional, for containerized builds)

[Rest of the README remains the same until Project Structure]

## Project Structure

```
esxi-control-system/
├── src/
│   ├── config_manager/      # Infrastructure configuration management
│   │   └── config_manager.py
│   ├── remote_manager/      # Remote operations handling
│   │   └── remote_manager.py
│   └── esxi_control_system.py
├── tests/                   # Comprehensive test suite
│   ├── test_config_manager.py
│   └── test_remote_manager.py
├── conf/                    # Configuration files
│   └── conf.json
├── Dockerfile              # Cross-platform build support
├── Makefile               # Build and development automation
└── requirements.txt
```

## Extending the Tool

The tool's modular architecture makes it easy to add new functionality:

1. **Command Line Interface**: Add new commands in `esxi_control_system.py`
2. **Remote Operations**: Extend `remote_manager.py` with new SSH commands
3. **Configuration Management**: Enhance `config_manager.py` for new configuration needs

Example of adding new functionality:

```python
# In remote_manager.py
@staticmethod
def create_vm_snapshot(host, username, password, vm_name, snapshot_name):
    """
    Create a snapshot of a virtual machine.
    """
    # Implementation here
```

## Installation

### Standard Installation

```bash
# Clone the repository
git clone https://github.com/Moh-Gebril/esxi-control-system.git
cd esxi-control-system

# Set up the development environment
make install
```

### Docker-based Installation

```bash
# Build using Docker (cross-platform support)
make build_with_docker
```

## Configuration

Create a `conf/conf.json` file based on the provided example:

```json
{
  "esxi_servers": [
    {
      "name": "prod-esxi-01",
      "ip": "192.168.1.100",
      "username": "admin",
      "password": "your_password",
      "vms": [
        {
          "name": "web-server-01",
          "ip": "192.168.1.101",
          "username": "webadmin",
          "password": "vm_password"
        }
      ]
    }
  ]
}
```

## Usage

### Shutdown Infrastructure

```bash
# Using the built executable
./esxi_control_system -s

# Using Python directly
python3 esxi_control_system.py -s
```

### View Infrastructure Configuration

```python
from config_manager.config_manager import ConfigManager

config = ConfigManager('conf/conf.json')
config.load_config()
config.display_all_servers()
```

## Development

### Setup Development Environment

```bash
make setup
make activate
make install
```

### Running Tests

```bash
make test
```

### Available Make Targets

- `setup`: Set up the development environment
- `activate`: Activate the virtual environment
- `install`: Install dependencies
- `test`: Run unit tests
- `build`: Build the project locally
- `build_with_docker`: Build using Docker for cross-platform support
- `clean`: Clean temporary files
- `create_docs`: Generate project documentation

## Security Considerations

- All passwords are stored in the configuration file. Ensure proper file permissions and encryption at rest.
- SSH connections use paramiko with AutoAddPolicy for host key handling.
- Sudo privileges are required for VM shutdown operations.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

Mohamed Gebril
