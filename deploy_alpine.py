import mkpod

cbase="sata1/images/"
mbase="sata1/volumes"


#result = mkpod.delete_pod("alpine.gw.lo")
result =  mkpod.add_mount("alpine.gw.lo.0",mbase + "/alpine.gw.lo.0", "/var/lib/data")
result =  mkpod.add_mount("alpine.gw.lo.1",mbase + "/alpine.gw.lo.1", "/root")
result =  mkpod.direct_pod("shahr773/alpine-sshd-arm64:1.0","alpine.gw.lo", "alpine.gw.lo",["alpine.gw.lo.0","alpine.gw.lo.1"])


