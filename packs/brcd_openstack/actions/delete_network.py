# Copyright 2016 Brocade Communications Systems, Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from base import NosDeviceAction


class DeConfigureNetwork(NosDeviceAction):
    """Implements logic to create L2 Network on Switch.
    """


    def run(self, switch_address, switch_username, switch_password, vlan):
        """Run helper methods to implement the desired state.
        """
        self.setup_connection(host=switch_address, user=switch_username, passwd=switch_password)
        changes = {}
        with self.mgr(conn=self.conn, auth=self.auth) as device:
            self.logger.info('successfully connected to %s', self.host)
            changes['delete_network'] = self._deconfigure_network(device,vlan)
            self.logger.info('closing connection to %s -- all done!', self.host)
        return changes


    def _deconfigure_network(self, device, vlan):
        """Delete L2 Network on device
        """
        device.interface.del_vlan_int(vlan)
        return True

