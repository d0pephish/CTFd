import hashlib
import os
import re
GUAC_CONF = "/etc/guacamole/user-mapping.xml"
OPENSTACK_STU_IP = "172.16.%s.101"
EXTERNALS_DIR = "externals_data"
def load(app):
    if not os.path.isdir(EXTERNALS_DIR):
         os.mkdir(EXTERNALS_DIR,750)
    for i in range(app.config['MIN_STU_NUM'],app.config['MAX_STU_NUM']):
        open("%s/%03d" % (EXTERNALS_DIR,i), 'a').close()
    pass
def get_next_user_num():
    items = os.listdir(EXTERNALS_DIR)
    if len(items) > 0:
        num = items[0]
        os.remove(EXTERNALS_DIR+"/"+num)
        return num
    else:
        return "---"
def get_openstack_stu_net_uuid():
    pass
def get_openstac_stu_sub_uuid():
    pass
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
    else:
        print config

def deploy_new_openstack_user(num,password):
    pass

def deploy_new_user(name,password):
    new_student_num = get_next_user_num()
    deploy_new_openstack_user(new_student_num,password)
    create_new_guac_user(name,password,num)
    return new_student_num
def delete_user(name,num):
    if os.path.isfile(GUAC_CONF):
        f = open(GUAC_CONF,"r")
        config_text = f.read()
        f.close()
        new_text = re.sub('<authorize\W*?username="test".*?</authorize>','',config_text, flags=re.DOTALL)
        f = open(GUAC_CONF,"w")
        f.write(new_text)
        f.close()
    open("%s/%s" % (EXTERNALS_DIR,num), 'a').close()
    

