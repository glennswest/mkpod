from fabric import Connection
from datetime import datetime
import datetime
import time

# mgmt1

# result = Connection('admin@rose1.gw.lo').run('/log/print',hide=True)
# msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
# print(msg.format(result))

default_host="rose1.gw.lo"
cbase="sata1/images/"

def executecmd(hostname,cmd):
    try:
      result = Connection(hostname).run(cmd,hide=True)
      msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
      return(msg.format(result))
    except:
      return("")

def findnextveth():
    #[admin@MikroTik] > /interface/veth/print
    #Flags: X - disabled; R - running 
    #0  R name="veth1" address=192.168.88.2/24 gateway=192.168.88.1 gateway6="" 
    result=executecmd("admin@" + default_host,"/interface/veth/print")
    lines = result.splitlines()
    lastline = lines[-1]
    print(lastline)

def getconfig(hostname):
    config=executecmd("admin@" + hostname,"/export show-sensitive\n")
    return(config)

def backup_config():
    theconfig = getconfig(default_host)
    now = datetime.datetime.now()
    unique_filename_datetime = now.strftime("configs/config_%Y%m%d_%H%M%S.txt")
    print(unique_filename_datetime)
    with open(unique_filename_datetime,"w") as f:
         f.write(theconfig)

def set_direct_registry():
    result = executecmd("admin@" + default_host,"/container/config/set registry-url=https://registry-1.docker.io tmpdir=sata1/tmp")
    return(result)

def add_direct_pod(image,interface,rootdir,thename):
    backup_config()
    cmd = "/container/add remote-image=" + image + " interface=" + interface + " root-dir=" + cbase +  rootdir + " name=" + thename + " start-on-boot=yes logging=yes"
    result = executecmd("admin@" + default_host,cmd)
    time.sleep(5)
    cmd = "/container/start [find where name=\"" + thename + '"]'
    result = executecmd("admin@" + default_host,cmd)
    return(result)

def delete_pod(thename):
     # [admin@MikroTik] > /container/stop [find where name="registry.gw.lo"]
     # [admin@MikroTik] > /container/remove [find where name="registry.gw.lo"]    
    cmd = "/container/stop [find where name=\"" + thename + '"]'
    result = executecmd("admin@" + default_host,cmd)
    time.sleep(5)
    cmd = "/container/remove [find where name=\"" + thename + '"]'
    result = executecmd("admin@" + default_host,cmd)
    time.sleep(5)

#result = set_direct_registry()
#result = delete_pod("registry.gw.lo")
#result = add_direct_pod("distribution/distribution","veth1", "registry", "registry.gw.lo")
#print(result)

#result = delete_pod("alpine.gw.lo")
#result = add_direct_pod("shahr773/alpine-sshd-arm64:1.0","veth1", "alpine.gw.lo", "alpine.gw.lo")

interface = findnextveth()
print(interface)

