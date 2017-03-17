import hashlib
import os
import re
GUAC_CONF = "/etc/guacamole/user-mapping.xml"
OPENSTACK_STU_IP = "172.16.%s.101"
def get_next_user_num():
    pass
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

def return_user_num(num):
    pass
def deploy_new_openstack_user(num,password):
    pass

def deploy_new_user(name,password):
    new_student_num = get_next_user_num()
    deploy_new_openstack_user(new_student_num,password)
    create_new_guac_user(name,password,num)
create_new_guac_user("test","test","101")
def delete_user(name):
    config_text = """
    <authorize
            username="first"
            password="%s"
            encoding="md5">
        <protocol>vnc</protocol>
        <param name="hostname">%s</param>
        <param name="port">5901</param>
        <param name="password">%s</param>
    </authorize>"
<authorize
            username="test"
            password="%s"
            encoding="md5">
        <protocol>vnc</protocol>
        <param name="hostname">%s</param>
        <param name="port">5901</param>
        <param name="password">%s</param>
    </authorize>
<authorize
            username="lasts"
            password="%s"
            encoding="md5">
        <protocol>vnc</protocol>
        <param name="hostname">%s</param>
        <param name="port">5901</param>
        <param name="password">%s</param>
    </authorize>"""
    if os.path.isfile(GUAC_CONF):
        f = open(GUAC_CONF,"r")
        config_text = f.read()
        f.close()
        new_text = re.sub('<authorize\W*?username="test".*?</authorize>','',config_text, flags=re.DOTALL)
        f = open(GUAC_CONF,"w")
        f.write(new_text)
        f.close()
    else:
        print config_text
        new_text = re.sub('<authorize\W*?username="test".*?</authorize>','',config_text, flags=re.DOTALL)
        print "result"
        print new_text

delete_user("test")
