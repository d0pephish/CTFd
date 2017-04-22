import hashlib
import os
import re
from CTFd.plugins.externals.openstacker import openstacker
GUAC_CONF = "/etc/guacamole/user-mapping.xml"
OPENSTACK_STU_IP = "172.16.%s.101"
EXTERNALS_DIR = "externals_data"
def load(app):
    if not os.path.isdir(EXTERNALS_DIR):
         os.mkdir(EXTERNALS_DIR,750)
         for i in range(app.config['MIN_STU_NUM'],app.config['MAX_STU_NUM']):
             open("%s/%d" % (EXTERNALS_DIR,i), 'a').close()
    pass
def get_next_user_num():
    items = os.listdir(EXTERNALS_DIR)
    if len(items) > 0:
        num = items[0]
        os.remove(EXTERNALS_DIR+"/"+num)
        return num
    else:
        return "---"
def create_new_guac_user(name,password,num):
    h = hashlib.md5(password).hexdigest()
    hostname = OPENSTACK_STU_IP % (num)
    field = """    <authorize
            username="%s"
            password="%s"
            encoding="md5">
        <connection name="GUI">
        <protocol>vnc</protocol>
        <param name="hostname">%s</param>
        <param name="port">5901</param>
        <param name="password">%s</param>
        </connection>
        <connection name="SSH">
            <protocol>ssh</protocol>
            <param name="hostname">%s</param>
        </connection>
    </authorize>"""
    config = field % (name,h,hostname,h,hostname)
    if os.path.isfile(GUAC_CONF):
        f = open(GUAC_CONF,"r")
        config_text = f.read()
        f.close()
        config_text = config_text.replace("</user-mapping>",config+"\n</user-mapping>")
        f = open(GUAC_CONF,"w")
        f.write(config_text)
        f.close()
        restart_guac()
def get_yamls_contents(name):
    if name in list_available_yamls():
        return openstacker.get_yaml_contents(openstacker,name)
    else:
        return ""
def delete_yaml(name):
    if name in list_available_yamls():
        path = os.path.join(openstacker.yaml_paths["lanes"], name)
        if os.path.exists(path):
            try:
                os.remove(path)
                return '1'
            except:
                return '0'
    return '-1'
def list_available_yamls():
    return openstacker.list_available_lanes(openstacker)
def get_deployed_lanes(user,num):
    openstacked = openstacker()
    stacks = openstacked.get_deployed_stacks_by_string(user+"_"+str(num)+"_")
    new_stacks = []
    for x in stacks:
        new_stacks.append(x.replace(user+"_"+str(num)+"_","",1))
    return new_stacks
def teardown_user_lanes(user,num):
    openstacked = openstacker()
    stacks = openstacked.get_deployed_stacks_by_string(user+"_"+str(num)+"_")
    for x in stacks:
        openstacked.delete_stack(x)
def deploy_new_openstack_user(num,password):
    openstacked =  openstacker()
    trunc_password = hashlib.md5(password).hexdigest()[:8]
    print "truncating password to ", trunc_password
    openstacked.deploy_new_user(num,trunc_password)

def deploy_openstack_lane(user,num,lane):
    if lane in list_available_yamls():
        openstacked = openstacker()
        return openstacked.deploy_new_lane(user,num,lane)
def is_openstack_lane_deployed(user,num,lane):
    openstacked = openstacker()
    return openstacked.is_lane_deployed(user,num,lane)

def restart_guac():
    os.system("service guacd restart")

def deploy_new_user(name,password):
    new_student_num = get_next_user_num()
    print "generated num", new_student_num
    deploy_new_openstack_user(new_student_num,password)
    create_new_guac_user(name,password,new_student_num)
    return new_student_num

def update_guac_name(old,new):
    f = open(GUAC_CONF, "r")
    config_old = f.read()
    f.close()
    config_new = config_old.replace('username="'+old+'"','username="'+new+'"')
    f = open(GUAC_CONF, "w")
    f.write(config_new)
    f.close()
    restart_guac()
    
def delete_guac_user(name,num,station=True):
    if os.path.isfile(GUAC_CONF):
        f = open(GUAC_CONF,"r")
        config_text = f.read()
        f.close()
        new_text = re.sub('<authorize\W*?username="'+name+'".*?</authorize>','',config_text, flags=re.DOTALL)
        f = open(GUAC_CONF,"w")
        f.write(new_text)
        f.close()
    if str(num) != "000" and num != "---":
        open("%s/%s" % (EXTERNALS_DIR,num), 'a').close()
    restart_guac()
    if(station):
        openstacked = openstacker()
        openstacked.delete_user(num)

def update_guac_password(name,password,num):
    delete_guac_user(name,num, station=False)
    create_new_guac_user(name,password,num)
    
