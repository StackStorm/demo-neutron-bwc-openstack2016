import os
import sys
import time
import json

from st2client.client import Client
from st2client import models
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

END_STATES = ['succeeded', 'failed']


class BWCDriver(object):

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.client = None
        self.auth_token = None
        self.auth_url = 'https://' + self.host + '/auth'
        self.api_url = 'https://' + self.host + '/api'

    def _authenticate_and_retrieve_token(self):
        manager = models.ResourceManager(models.Token,
                                      self.client.endpoints['auth'],
                                      cacert=self.client.cacert,
                                      debug=self.client.debug)
        instance = models.Token()
        instance = manager.create(instance,
                                 auth=(self.username, self.password))
        print instance
        self.auth_token = instance.token

    def login(self):
        self.client = Client(auth_url=self.auth_url, api_url=self.api_url)
        self._authenticate_and_retrieve_token()
        os.environ['ST2_AUTH_TOKEN'] = self.auth_token

    def set_api_key(self,api_key):
        self.client = Client(auth_url=self.auth_url, api_url=self.api_url,
            api_key=api_key)
        
    def _run_action(self, action, params):

        action_exec_mgr = self.client.managers['LiveAction']

        execution = models.LiveAction()
        execution.action = action
        execution.parameters = params
        actionexec = action_exec_mgr.create(execution)

        while actionexec.status not in END_STATES:
            time.sleep(0.01)
            actionexec = action_exec_mgr.get_by_id(actionexec.id)

        return actionexec

    def create_network(self,switch_address,
                      switch_username,switch_password,vlan):
      
       params = {'switch_address':switch_address,
                 'switch_username':switch_username,
                 'switch_password':switch_password,
                 'vlan':str(vlan)}
       actionexec = self._run_action('brcd_openstack.create_network',
                    params = params)   
       output = {'operation': actionexec.result}
       return output
  
    def delete_network(self,switch_address,
                       switch_username,switch_password,vlan):
       params = {'switch_address':switch_address,
                 'switch_username':switch_username,
                 'switch_password':switch_password,
                 'vlan':str(vlan)}

       actionexec = self._run_action('brcd_openstack.delete_network',
                    params = params)
       output = {'operation': actionexec.result}
       return output

    def configure_trunk_vlan_on_interface(self,switch_address,
         switch_username,switch_password,vlan,
         interface_name,interface_type):

       params = {'switch_address':switch_address,
                 'switch_username':switch_username,
                 'switch_password':switch_password,
                 'vlan':str(vlan),
                 'interface_name':interface_name,
                 'interface_type':interface_type}
       actionexec = self._run_action('brcd_openstack.configure_trunk_vlan_on_interface',
                    params = params)
       
       output = {'operation': actionexec.result}
       return output 


    def deconfigure_trunk_vlan_on_interface(self,switch_address,
         switch_username,switch_password,vlan,
         interface_name,interface_type):

       params = {'switch_address':switch_address,
                 'switch_username':switch_username,
                 'switch_password':switch_password,
                 'vlan':str(vlan),
                 'interface_name':interface_name,
                 'interface_type':interface_type}
       actionexec = self._run_action('brcd_openstack.deconfigure_trunk_vlan_on_interface',
                    params = params)

       output = {'operation': actionexec.result}
       return output


if __name__ == "__main__":
    driver = BWCDriver('172.22.10.101','admin','StackSt0rm')
    driver.login()
    for i in range(4,6):
        print 'Creating Network ' , i
        driver.create_network('10.37.18.135','admin','password',str(i))

     


  

      

