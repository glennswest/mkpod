from fabric import Connection
from datetime import datetime
import datetime
import time
import json

# mgmt1

# result = Connection('admin@rose1.gw.lo').run('/log/print',hide=True)
# msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
# print(msg.format(result))

default_host="rose1.gw.lo"
cbase="sata1/images/"
mbase="sata1/volumes"

def executecmd(hostname,cmd):
    try:
      result = Connection(hostname).run(cmd,hide=True)
      msg = "{0.stdout}"
      return(msg.format(result))
    except:
      return("")

def getinterfacenumber(thedevice):
    numbers = ""
    for char in thedevice:
        if char.isdigit():
           numbers = numbers + str(char)
    return(int(numbers))

def getname(theline):
    namepos=theline.find("name=\"")+6
    thename=theline[namepos:]
    index = thename.find('"')
    thename = thename[:index]
    return(thename)

def lastveth(lastline):
    theveth=getname(lastline)
    thenumber=getinterfacenumber(theveth)
    thenumber = thenumber + 1
    thename="veth" + str(thenumber)
    return(thename)

def get_veths():
    result=executecmd("admin@" + default_host,"/interface/veth/print")
    lines = result.splitlines()
    names=[]
    for theline in lines[1:-1]:
        thename = getname(theline)
        if (thename != ""):
           names.append(getname(theline))
    return(names)
def wait_for_veth_delete(thename):
    the_veths = get_veths()
    while(thename in the_veths):
        the_veths = get_veths()

def find_missing_veth(lines):
    names=[]
    for theline in lines[1:-1]:
        thename = getname(theline)
        if (thename != ""):
           names.append(getname(theline))
    nextname="veth1"
    for thename in names:
        if (thename != nextname):
           return(nextname)
        thenum = getinterfacenumber(thename)
        thenum = thenum + 1
        nextname = "veth" + str(thenum)
    return("")

def findnextveth():
    #[admin@MikroTik] > /interface/veth/print
    #Flags: X - disabled; R - running 
    #0  R name="veth1" address=192.168.88.2/24 gateway=192.168.88.1 gateway6="" 
    result=executecmd("admin@" + default_host,"/interface/veth/print")
    lines = result.splitlines()
    lastline = lines[-2]
    if (lastline.startswith("Flags")):
       theveth="veth1"
       return(theveth)
    missingveth = find_missing_veth(lines)
    if (missingveth==""):
       thename = lastveth(lastline)
       return(thename)
    return(missingveth)

def createveth(theveth):
    #/interface/veth/add name=veth1 address=192.168.88.2/24 gateway=192.168.88.1
    #/interface/bridge/port add bridge=bridge interface=veth1
    theinterfacenumber = int(getinterfacenumber(theveth))
    theipnumber = theinterfacenumber + 1 
    theip = "192.168.88." + str(theipnumber)
    cmd = "/interface/veth/add name=" + theveth + " address=" + theip + "/24 gateway=192.168.88.1"
    result=executecmd("admin@" + default_host,cmd)
    cmd = "/interface/bridge/port add bridge=bridge interface=" + theveth
    result=executecmd("admin@" + default_host,cmd)

def getconfig(hostname):
    config=executecmd("admin@" + hostname,"/export show-sensitive\n")
    return(config)

def backup_config():
    theconfig = getconfig(default_host)
    now = datetime.datetime.now()
    unique_filename_datetime = now.strftime("configs/config_%Y%m%d_%H%M%S.txt")
    with open(unique_filename_datetime,"w") as f:
         f.write(theconfig)

def set_direct_registry():
    result = executecmd("admin@" + default_host,"/container/config/set registry-url=https://registry-1.docker.io tmpdir=sata1/tmp")
    return(result)

def add_direct_pod(image,interface,rootdir,thename,mounts = []):
    cmd = "/container/add remote-image=" + image + " interface=" + interface + " root-dir=" + cbase +  rootdir + " name=" + thename + " start-on-boot=yes logging=yes"
    if (len(mounts) > 0):
       themounts = ','.join(mounts)
       cmd = cmd + " mounts=" + themounts
    result = executecmd("admin@" + default_host,cmd)
    # After download, it will go to stopped state
    wait_container_state(thename,"stopped")
    cmd = "/container/start [find where name=\"" + thename + '"]'
    result = executecmd("admin@" + default_host,cmd)
    return(result)

def direct_pod(image,rootdir,thename,mounts = []):
    interface = findnextveth()
    createveth(interface)
    add_direct_pod(image,interface,rootdir,thename,mounts)

def wait_container_state(thename,thestate):
    cstate = "none"
    while(cstate != thestate):
        cons = containers()
        con = cons.get(thename)
        if (con == None):
           cstate = "missing"
           return
        else:
            cstate = con["status"]

def delete_pod(thename):
     # [admin@MikroTik] > /container/stop [find where name="registry.gw.lo"]
     # [admin@MikroTik] > /container/remove [find where name="registry.gw.lo"]    
    cons = containers()
    con = cons[thename]
    interface = con["interface"]
    cmd = "/container/stop [find where name=\"" + thename + '"]'
    result = executecmd("admin@" + default_host,cmd)
    wait_container_state(thename,"stopped")
    cmd = "/container/remove [find where name=\"" + thename + '"]'
    result = executecmd("admin@" + default_host,cmd)
    wait_container_state(thename,"missing")
    delete_interface(interface)

def containers():
    #0 name="registry.gw.lo" repo="registry-1.docker.io/distribution/distribution:latest" os="linux" arch="arm64" interface=veth1 root-dir=sata1/images/registry mounts="" workdir="/" logging=yes start-on-boot=yes status=running 

    cons = {}
    cmd = "/container/print"
    result = executecmd("admin@" + default_host,cmd)
    full_line = ""
    for theline in result.splitlines():
        full_line = full_line + theline
        if ("status=" in full_line):
           values = full_line.split()
           con = {}
           con["id"] = values[0]
           for idx in range(1,len(values)):
               thepair = values[idx].split("=")
               if (len(thepair) == 2):
                  con[thepair[0]] = thepair[1].strip('\"')
           cons[con["name"]] = con
           full_line = ""
    return(cons)

def delete_interface(interface):
    cmd = "/interface bridge remove [/interface find name=\"" + interface + '"]'
    result = executecmd("admin@" + default_host,cmd)
    wait_for_veth_delete(interface)
    return(result)

    
def add_mount(thecontainer,mount_name,src,dst):
    comment = "\"{cname=\'" + thecontainer + "\'}\""
    cmd = "/container/mount/add name=" + mount_name + " src=" + src + " dst=" + dst + " comment=" + comment
    result = executecmd("admin@" + default_host,cmd)
    return(result)


#result = set_direct_registry()
#result = delete_pod("registry.gw.lo")
#result = add_direct_pod("distribution/distribution","veth1", "registry", "registry.gw.lo")
#print(result)

#result = delete_pod("alpine.gw.lo")
#result = add_direct_pod("shahr773/alpine-sshd-arm64:1.0","veth1", "alpine.gw.lo", "alpine.gw.lo")

#result = direct_pod("distribution/distribution","registry", "registry.gw.lo")
#result =  direct_pod("shahr773/alpine-sshd-arm64:1.0","alpine.gw.lo", "alpine.gw.lo")


#cons = containers()
#print(cons)

#result =  direct_pod("shahr773/alpine-sshd-arm64:1.0","alpine.gw.lo", "alpine.gw.lo")
#result = delete_pod("alpine.gw.lo")


result = delete_pod("alpine.gw.lo")
result =  add_mount("alpine.gw.lo","alpine.gw.lo.0",mbase + "/alpine.gw.lo.0", "/var/lib/data")
result =  add_mount("alpine.gw.lo","alpine.gw.lo.1",mbase + "/alpine.gw.lo.1", "/root")
result =  direct_pod("shahr773/alpine-sshd-arm64:1.0","alpine.gw.lo", "alpine.gw.lo",["alpine.gw.lo.0","alpine.gw.lo.1"])

#veths = get_veths()
#print(veths)

