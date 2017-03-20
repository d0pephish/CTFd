from openstack import connection
import yaml
from CTFd.plugins.externals.openstacker.openstacker_auth import *
class openstacker:

    yaml_paths = {
                    "new_user" : "yamls/student_station.yaml"
                 }

    def __init__(self):
        print "Openstacker Initialized"
        self.conn = self.authenticate()

    def authenticate(self):
        conn = connection.Connection(auth_url=AUTH_URL,
                                     user_domain_name=USER_DOMAIN_NAME,
                                     username=USERNAME,
                                     password=PASSWORD)
        return conn
    def format_student_name(self,num):
        return "Student_"+str(num)+"_Station"
    def get_network_entities(self):
        items = {}
        for network in self.conn.network.networks():
            items[network.name] = network.id
        return items
    def get_subnets(self):
        items = {}
        for subnet in self.conn.network.subnets():
            items[subnet.name] = subnet.id
        return items
    def get_servers(self):
        items = {}
        for serv in self.conn.compute.servers():
            items[serv.name] = serv
        return items
    def deploy_yaml(self,name,params,template):
        return self.conn.orchestration.create_stack(name=name, template=template, parameters=params)

    def get_dict_from_yaml(self,yaml_name):
        if yaml_name not in self.yaml_paths.keys():
            return None
        f = open(self.yaml_paths[yaml_name], "r")
        text = f.read()
        f.close()
        return yaml.load(text)
            
    def deploy_new_user(self,num,password):
        name = self.format_student_name(num)
        print "creating new user", num
        if self.stack_exists(name):
            print "Not deploying, stack already exists."
            return False
        network_items = self.get_network_entities()
        network_uuid = network_items["ex_stu_net"] 
        subnet_items =self.get_subnets()
        subnet_uuid = subnet_items["ex_stu_net_sub"]
        params = { "root_password" : "changeme", "vnc_password" : password, "student_id" : str(num), "student_network_sub_uuid" : subnet_uuid, "student_network_uuid" : network_uuid }
        template=self.get_dict_from_yaml("new_user")
        print "using params", params
        self.deploy_yaml(name=name, template=template, params=params)
        return True
    def stack_exists(self,name):
        return self.get_stack(name) is not None

    def get_stack(self,name):
        return self.conn.orchestration.find_stack(name)

    def delete_stack(self,name):
        stack = self.get_stack(name)
        if stack is not None:
            self.conn.orchestration.delete_stack(stack)

    def delete_user(self,num):
        name = self.format_student_name(num)
        self.delete_stack(name)
        
#testing = openstacker()
#template_data = yaml.load(text)
#print template_data
#print testing.get_network_entities()
#print testing.get_subnets()
#testing.deploy_new_user("220",template_data)
#testing.get_network_entities()

