# Mikrotik Podman and Library

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




