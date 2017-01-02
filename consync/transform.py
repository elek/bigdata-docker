
import os
import re

class Transform:

    def __init__(self, basepath):
        self.basepath = basepath

    def transform_content(self, filepath, content):
       trans = self.find_transformation(filepath, self.basepath)
       if trans:
           content = getattr(self,"to_%s" % trans)(content)
       return content

    def find_transformation(self, filepath, basepath):
       trafofile = os.path.join(basepath, "transformations.txt")
       transfo = ""
       filename = os.path.basename(filepath)
       if os.path.isfile(trafofile):
           with open(trafofile) as f:
               for line in f:
                   line = line.strip()
                   lsep = line.rfind(" ")
                   pattern = line[0:lsep]
                   if re.search(pattern, filename):
                       transfo = line[lsep:].strip()
       if transfo:
           print("Transforming file {} to format {}".format(filepath, transfo))
       return transfo

    def to_xml(self, content):
       result = "<configuration>\n"
       for line in content.split("\n"):
           keyvalue = line.split(":", 1)
           if len(keyvalue) > 1:
               result += "<property><name>{0}</name><value>{1}</value></property>\n".format(keyvalue[0], keyvalue[1].strip())
       result += "</configuration>"
       return result
