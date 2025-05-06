# Mkpod Container Library - For Mikrotik Rose Appliance

## Overview
This consists of two components:

### mkpod.py Library
This implements methods to execute container operations on a mikrotik rose appliance. Its uses ssh to issue commands to do operations.
It assumes there is a sata drive in 0 slot, for container storage. It will use 192.168.88.x network for veths for each pod.

### Direct Pods (Implemented)
Direct pods have a direct interface on the l2 bridge. As long as you have added a route on your main network and one back on the rose appliance,
this works perfect. You can add any of the physical connections on the appliance to this bridge for access from the containers.



### Indirect Pods (WIP - Not Started)
This will create a load balancer direct pod, and then proxy traffic to containers in the same group. This allows for higher security.




## MKPod Library Documentation
A Python library for managing containers on MikroTik devices using RouterOS API. This library facilitates container deployment and management on MikroTik RouterOS devices.

### Features
Create and manage containers on MikroTik devices

Manage virtual ethernet interfaces (veth)

Handle container networking

Backup RouterOS configurations

Container registry management

### Installation
pip install mkpod


### Prerequisites
MikroTik device running RouterOS 7.x or later

### SSH access to the MikroTik device

Python 3.6+

SATA drive in slot 0 for container storage

### Basic Usage
from mkpod import direct_pod, delete_pod, containers

#### Create a container
direct_pod("alpine:latest", "alpine", "alpine.gw.lo")

#### Delete a container
delete_pod("alpine.gw.lo")

#### List all containers
cons = containers()
for name, info in cons.items():
    print(f"Container: {name}")
    print(f"Status: {info['status']}")


#### Container Management
##### direct_pod(image, rootdir, thename)
Creates and deploys a container with direct network access.

Parameters:

image (str): Container image name (e.g., "alpine:latest")

rootdir (str): Root directory for container storage

thename (str): Name for the container

Example:

direct_pod("nginx:latest", "nginx", "web.gw.lo")

add_direct_pod(image, interface, rootdir, thename)
Adds a container with a specific network interface.

Parameters:

image (str): Container image name

interface (str): Network interface name

rootdir (str): Root directory for container

thename (str): Container name

Example:

add_direct_pod("mysql:5.7", "veth1", "mysql", "db.gw.lo")


##### delete_pod(thename)
Removes a container and its associated interface.

Parameters:

thename (str): Name of container to delete

Example:

delete_pod("web.gw.lo")



### Network Interface Management
#### findnextveth()
Finds the next available virtual ethernet interface name.

Returns:

str: Next available veth name (e.g., 'veth1', 'veth2')

Example:

next_veth = findnextveth()
print(f"Next available interface: {next_veth}")

#### createveth(theveth)
Creates a new virtual ethernet interface.

Parameters:

theveth (str): The veth interface name to create

Example:

createveth("veth1")


### System Operations
#### executecmd(hostname, cmd)
Executes a command on the MikroTik device via SSH.

Parameters:

hostname (str): The hostname in format 'user@host'

cmd (str): The command to execute

Returns:

str: Command output or empty string if failed

Example:

result = executecmd("admin@192.168.88.1", "/system resource print")


#### backup_config()
Creates a backup of the current RouterOS configuration.

Example:

backup_config()



### Container Information
#### containers()
Retrieves information about all containers.

Returns:

dict: Dictionary of container information indexed by name

Example:

cons = containers()
for name, info in cons.items():
    print(f"Container: {name}")
    print(f"Status: {info['status']}")
    print(f"Image: {info['image']}")


### Configuration
Default Settings
Default host: rose1.gw.lo

Container storage: sata1/images/

Network: 192.168.88.x for container veth interfaces

Bridge: All container interfaces are added to 'bridge'

Environment Variables
No environment variables are required, but SSH credentials may be needed for connection.

Network Architecture
Direct Pods
Direct pods have a direct interface on the L2 bridge. This requires:

Route on main network to the container

Return route on the RouterOS device

Example network setup:

Main Network (192.168.88.0/24)
         |
    RouterOS Bridge
         |
    Container veth


Copy

Insert at cursor
Error Handling
The library includes comprehensive error handling for:

SSH connection failures

Container creation errors

Network interface issues

Storage problems

Example error handling:

try:
    direct_pod("alpine:latest", "alpine", "test.gw.lo")
except Exception as e:
    print(f"Failed to create container: {str(e)}")

###Best Practices
Always use unique container names

Backup configuration before major changes

Monitor container resource usage

Use appropriate network segmentation

Maintain regular backups

### Limitations
Requires RouterOS 7.x or later

Single SATA drive support

Limited to bridge networking

Docker Hub registry by default

### Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Create a Pull Request

### License
This project is licensed under the MIT License - see the LICENSE file for details.

Support
For support and questions:

Open an issue on GitHub

Contact the maintainers

### Check the RouterOS documentation

### Changelog
#### Version 1.0.0
Initial release

Basic container management

Network interface handling

Configuration backup

#### Version 1.1.0
Added direct pod support

Improved error handling

Network management enhancements

### Acknowledgments
MikroTik for RouterOS

Container community

Open source contributors
   gwest - glennwest - gwest@redhat.com
