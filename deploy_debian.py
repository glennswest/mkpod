import mkpod

cbase="sata1/images/"
mbase="sata1/volumes"


#result = mkpod.delete_pod("debian.gw.lo")
result =  mkpod.add_mount("debian.gw.lo","debian.gw.lo.home",mbase + "/debian.gw.lo.home", "/home")
result =  mkpod.direct_pod("arm64v8/debian:testing","debian.gw.lo","debian.gw.lo",["debian.gw.lo.data"])

