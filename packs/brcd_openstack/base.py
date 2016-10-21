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

import pynos.device

from st2actions.runners.pythonrunner import Action


class NosDeviceAction(Action):

    def __init__(self, config=None, action_service=None):
        super(NosDeviceAction, self).__init__(config=config, action_service=action_service)
        self.result = {'changed': False, 'changes': {}}
        self.mgr = pynos.device.Device
        self.host = None
        self.conn = None
        self.auth = None

    def setup_connection(self, host, user=None, passwd=None):
        self.host = host
        self.conn = (host, '22')
        self.auth = self._get_auth(host=host, user=user, passwd=passwd)

    def _get_auth(self, host, user, passwd):
        if not user:
            lookup_key = self._get_lookup_key(host=self.host, lookup='user')
            user_kv = self.action_service.get_value(name=lookup_key, local=False)
            if not user_kv:
                raise Exception('username for %s not found.' % host)
            user = user_kv
        if not passwd:
            lookup_key = self._get_lookup_key(host=self.host, lookup='passwd')
            passwd_kv = self.action_service.get_value(name=lookup_key, local=False, decrypt=True)
            if not passwd_kv:
                raise Exception('password for %s not found.' % host)
            passwd = passwd_kv
        return (user, passwd)

    def _get_lookup_key(self, host, lookup):
        return 'switch.%s.%s' % (host, lookup)

