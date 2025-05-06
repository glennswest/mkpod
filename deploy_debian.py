import mkpod

cbase="sata1/images/"
mbase="sata1/volumes"

image_name = mkpod.use_container_tar("debian:latest")
print(image_name)

result = mkpod.delete_pod("debian.gw.lo")
result =  mkpod.add_mount("debian.gw.lo.0",mbase + "/debian.gw.lo.0", "/home")
result =  mkpod.direct_pod("debian.latest.tar","debian.gw.lo","debian.gw.lo",["debian.gw.lo.0"],podcmd="sleep infinity")



#result =  mkpod.direct_pod("fedora.latest.tar" ,"fedora.gw.lo","fedora.gw.lo",['fedora.gw.lo.0'],podcmd="sleep infinity")
