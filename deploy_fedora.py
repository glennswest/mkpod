import mkpod

cbase="sata1/images/"
mbase="sata1/volumes"

#image_name = mkpod.use_container_tar("fedora:latest")
#print(image_name)

result = mkpod.delete_pod("fedora.gw.lo")
result =  mkpod.add_mount("fedora.gw.lo.0",mbase + "/fedora.gw.lo.0", "/home")
result =  mkpod.direct_pod("fedora.latest.tar" ,"fedora.gw.lo","fedora.gw.lo",['fedora.gw.lo.0'],podcmd="sleep infinity")

