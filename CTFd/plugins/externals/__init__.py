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
        <protocol>vnc</protocol>
        <param name="hostname">%s</param>
        <param name="port">5901</param>
        <param name="password">%s</param>
    </authorize>"""
    config = field % (name,h,hostname,h)
    if os.path.isfile(GUAC_CONF):
        f = open(GUAC_CONF,"r")
        config_text = f.read()
        f.close()
        config_text = config_text.replace("</user-mapping>",config+"\n</user-mapping>")
        f = open(GUAC_CONF,"w")
        f.write(config_text)
        f.close()
        restart_guac()

def deploy_new_openstack_user(num,password):
    openstacked =  openstacker()
    trunc_password = hashlib.md5(password).hexdigest()[:8]
    print "truncating password to ", trunc_password
    openstacked.deploy_new_user(num,trunc_password)
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
    
def delete_guac_user(name,num):
    if os.path.isfile(GUAC_CONF):
        f = open(GUAC_CONF,"r")
        config_text = f.read()
        f.close()
        new_text = re.sub('<authorize\W*?username="test".*?</authorize>','',config_text, flags=re.DOTALL)
        f = open(GUAC_CONF,"w")
        f.write(new_text)
        f.close()
    if str(num) != "000" and num != "---":
        open("%s/%s" % (EXTERNALS_DIR,num), 'a').close()
    restart_guac()
    openstacked = openstacker()
    openstacked.delete_user(num)

def update_guac_password(name,password,num):
    delete_guac_user(name,num)
    create_new_guac_user(name,password,num)
    
