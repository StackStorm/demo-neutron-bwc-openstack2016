=========================
Setup of Openstack Plugin
=========================

Pre-requisites
--------------
Brocade Plugins require a specific version of ncclient (Net conf library). It can be obtained from the following github location.

```
git clone https://github.com/brocade/ncclient
cd ncclient
sudo python setup.py install
```

Install Plugin
--------------
```
git clone https://github.com/StackStorm/demo-neutron-bwc-openstack2016.git
cd demo-neutron-bwc-openstack2016/neutron/networking-brocade
sudo python setup.py install
```

Upgrade the Database
Upgrade the database so that Brocade specific table entries are created in neutron database
```
 neutron-db-manage  --config-file /etc/neutron/neutron.conf  
  --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head
```

Openstack Controller Configurations 
------------------------------------
Following configuration lines needs to be available in ‘/etc/neutron/plugins/ml2/ml2_conf.ini’ to start Brocade VDX Mechanism driver (brocade_vdx_bwc).

```

[ml2]
tenant_network_types = vlan
type_drivers = vlan
mechanism_drivers = openvswitch,brocade_vdx_bwc
[ml2_type_vlan]
network_vlan_ranges = physnet1:2:500
[ovs]
bridge_mappings = physnet1:br1

```
Here,

mechanism driver needs to be set to ‘brocade_vdx_bwc’ along with openvswitch.
- ‘br1’ is the openvswitch bridge.
- 2:500’ is the vlan range used
Following configuration lines for the VDX Fabric needs to be added to either ‘/etc/neutron/plugins/ml2/ml2_conf_brocade.ini’ or ‘/etc/neutron/plugins/ml2/ml2_conf.ini’. 

If added to ‘/etc/neutron/plugins/ml2/ml2_conf_brocade.ini’ then this file should be given as config parameter during neutron-server startup.

```

[ml2_brocade]
bwc_username = admin
bwc_password = StackSt0rm
bwc_address  = 10.37.21.147
bwc_api_key = NGNhYzUxMzc4MGVhNjEzMzc1NTYyMTdjMDBlMWRkMmMxYzI0N2RiZDY3OWI2NmNjYTYzNjZjYmIxOTRhZTQ3Nw
username = admin 
password = password 
address  = 10.37.18.139
ostype   = NOS 
physical_networks = physnet1 
osversion=5.0.0
initialize_vcs = False
nretries = 5
ndelay = 10
nbackoff = 2

[switch]
#connections=<host-name> : <physical network name>: <PORT-SPEED> <NOS PORT>
link_info = controller:10.37.18.135:admin:password, compute:10.37.18.136:admin:password

[topology]
#connections=<host-name> : <physical network name>: <PORT-SPEED> <NOS PORT>
connections = controller:physnet1:Te:135/0/10, compute:physnet1:Te:136/0/10

```

Here, 
[ml2_brocade] - entries

- 10.37.18.139 is the VCS Virtual IP (IP for the seed switch).
- osversion - NOS version 
- nretries - number of netconf to the switch will be retried in case of failure
- ndelay - time delay in seconds between successive netconf commands in case of failure 

[topology] - entries

Here physical connectivity between NIC, PhysNet (Host side) and Switch Interfaces are provided
Openstack Compute Configurations 

Following configuration lines needs to be available in one of the configuration files used by openvswitch agent. 
e.g /etc/neutron/plugins/openvswitch/ovs_neutron_plugin.ini

```
[ovs]
bridge_mappings = physnet1:br1
network_vlan_ranges = 2:500
tenant_network_type = vlan
```
Here,

- ‘br1’ is the openvswith bridge.
- ‘2:500’ is the vlan range used












