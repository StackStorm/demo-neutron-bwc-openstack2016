### **Brocade OpenStack Neutron ML2 Automation Pack**

OpenStack Neutron comes with pluggable infrastructure, Neutron plugins extend the use and capabilities of Neutron within a cloud.  Neutron plugin is a critical piece of the OpenStack deployment affecting the network features, supported network topologies as well as the scale, performance, high availability.  

Brocade Neutron ML2 Plugin ties the Virtual Machine lifecycle events (Network, Port) to physical switch port and VLAN configurations as well as overlay operations like establishing and disconnecting VXLAN tunnels.  To provide flexibility and scale, this plugin leverages Brocade Workflow Composer with customizable workflows, key features of this plugin include:  

 - Brocade ML2 plugin redirects Neutron APIs to Brocade Work Flow Composer (BWC).  
 - BWC Workflows map Neutron virtual networks, ports to physical switch ports and configures the network.
 - Using IP Fabric network, plugin supports tenancy spanning multiple racks.  Plugin leverages the VTEP (VXLAN Termination End Point) capabilities of VDX switch to originate tunnels on behalf of hypervisors and thus offloading all VXLAN processing on to the hardware providing better performance and scalability.

[Openstack ML2 plugin for StackStorm/BWC](https://github.com/StackStorm/demo-neutron-bwc-openstack2016/tree/master/neutron/networking-brocade) triggers workflows that use actions defined in this [pack](https://github.com/StackStorm/demo-neutron-bwc-openstack2016/tree/master/packs/brcd_openstack) for automation of network configuration. With this plugin, the network is automatically provisioned or de-provisioned depending on changes done in Openstack!

The Opentack ML2 plugin for StackStorm/BWC supports the following:

 - **Creation & Deletion of Openstack Network**: When a Tenant Network is created in OpenStack, this action is triggered, which in response configures the VLAN on leaf switches. Similarly, when a Network is deleted in OpenStack, VLAN is deletedd automatically from the leaf switches.
 - **Addition and Removal of VLAN from switch interfaces**: VLAN's are automatically added to or removed from approriate interfaces on switches based on location of the VM created or deleted using OpenStack. 

#### **Actions** 

Default actions as part of the pack. Actions add or remove relevant configuration on Brocade VDX switches.

 - bwc_create_network				: Creates a VLAN (L2 Network)
 - bwc_delete_network				: Deletes a VLAN (L2 Network)
 - bwc_configure_trunk_vlan_on_interface	: Adds a VLAN (trunk mode) on a switch interface
 - bwc_deconfigure_trunk_vlan_on_interface	: Removes a VLAN (trunk mode) from a switch interface

#### **Workflows**
Demo workflows call the above actions as well as actions from other integration packs such as ChatOps, JIRA etc. 

Besides configuring/deconfiguring Brocade VDX swiches part of IP Fabric network, each workflow also integrates with Chatops ([Slack](https://slack.com/)) to notify of event occurance and post relavant logs from the switches, and IT ticketing Systems ([JIRA](https://jira.atlassian.com/secure/Dashboard.jspa)) to log a ticket for any automation failures.

 - create_network							
 - delete_network
 - configure_trunk_vlan_on_interface
 - deconfigure_trunk_vlan_on_interface

**Dependencies for Demo Workflows**

The demo workflows need to following integration packs to be installed and setup beforehand:

1. [JIRA](https://github.com/StackStorm/st2contrib/tree/master/packs/jira)
2. [Chatops](https://docs.stackstorm.com/chatops/chatops.html#configuration)
3. [CLICRUD](https://github.com/StackStorm/demo-neutron-bwc-openstack2016/tree/master/packs/clicrud)

You can leave any of these out if you modify the workflows accordingly.

#### **Installation**

1. Log in to your ST2/BWC
2. Execute `https://github.com/StackStorm/demo-neutron-bwc-openstack2016.git`
3. Copy `/demo-neutron-bwc-openstack2016/packs/brcd_openstack` directory to `/opt/stackstorm/packs/`
4. Go to the ``/opt/stackstorm/packs/`` directory
5. Execute ``st2 run packs.setup_virtualenv packs=brcd_openstack``
6. Execute ``st2 run packs.load register=brcd_openstack``
7. Verify the install with `st2 action list --pack=brcd_openstack`

Same steps can be used for installation of CLICRUD pack as well with change of pack name to "clicrud".

