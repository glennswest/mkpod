import mkpod

cbase="sata1/images/"
mbase="sata1/volumes"

image_name = mkpod.use_container_tar("ghcr.io/project-zot/zot-linux-arm64:latest")
print(image_name)

result = mkpod.delete_pod("zot.gw.lo")
#result =  mkpod.add_mount("alpine.gw.lo.0",mbase + "/alpine.gw.lo.0", "/var/lib/data")
#result =  mkpod.add_mount("alpine.gw.lo.1",mbase + "/alpine.gw.lo.1", "/root")
result =  mkpod.direct_pod("zot-linux-arm64.tar","zot.gw.lo","zot.gw.lo")

