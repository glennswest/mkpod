with open(".version_mkpod") as v:
     thefile = v.read()
thelines = thefile.splitlines()
version = thelines[0].rstrip("\n")

with open("pyproject.toml") as f:
     thedata = f.read()
data = thedata.splitlines()

for idx in range(len(data)):
    if ("version" in data[idx]):
       data[idx] = "version = \"" + version + "\""

with open("pyproject.toml","w") as f:
     for item in data:
         f.write(item + "\n")

