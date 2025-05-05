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


#result = delete_pod("alpine.gw.lo")
#result =  add_mount("alpine.gw.lo","alpine.gw.lo.0",mbase + "/alpine.gw.lo.0", "/var/lib/data")
#result =  add_mount("alpine.gw.lo","alpine.gw.lo.1",mbase + "/alpine.gw.lo.1", "/root")
#result =  direct_pod("shahr773/alpine-sshd-arm64:1.0","alpine.gw.lo", "alpine.gw.lo",["alpine.gw.lo.0","alpine.gw.lo.1"])

#result = delete_pod("registry.gw.lo")
#result =  add_mount("registry.gw.lo","registry.gw.lo.0",mbase + "/registry.gw.lo.0", "/etc/distribution")
#result =  add_mount("registry.gw.lo","registry.gw.lo.1",mbase + "/registry.gw.lo.1", "/var/lib/registry")
#result = direct_pod("distribution/distribution","registry.gw.lo", "registry.gw.lo",["registry.gw.lo.0","registry.gw.lo.1"])

#veths = get_veths()
#print(veths)


