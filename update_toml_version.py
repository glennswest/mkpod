with open(".version_mkpod") as v:
     thefile = v.read()
thelines = thefile.splitlines()
version = thelines[0]

with open("pyproject.toml") as f:
     thedata = f.read()
data = thedata.splitlines()

for idx in range(len(data)):
    if ("version" in data[idx]):
       data[idx] = "version = " + version

with open("pyproject.toml") as f:
     for item in data:
         file.write(item + "\n")

