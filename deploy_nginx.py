import mkpod

# From  https://www.youtube.com/watch?v=qlcVx-k-02E - Quick and Easy Local SSL Certificates for Home Lab

cbase="sata1/images/"
mbase="sata1/volumes"

#result = mkpod.delete_pod("nginx.gw.lo")
result =  mkpod.add_mount("nginx.gw.lo","nginx.gw.lo.data",mbase + "/nginx.gw.lo.data", "/data")
result =  mkpod.add_mount("nginx.gw.lo","nginx.gw.lo.letsencrypt",mbase + "/nginx.gw.lo.letsencrypt", "/etc/letsencrypt")
result =  mkpod.direct_pod("jc21/nginx-proxy-manager:latest","nginx.gw.lo", "nginx.gw.lo",["nginx.gw.lo.data","nginx.gw.lo.letsencrypt"])

