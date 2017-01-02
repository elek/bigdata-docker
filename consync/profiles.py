import os


class Profiles:
    def __init__(self, basepath):
        self.basepath = basepath
        profile_file = os.path.join(basepath, "profiles.txt")
        self.profiles = []
        if os.path.isfile(profile_file):
            with open(profile_file) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        self.profiles.append(line)
        print("active profiles: " + " ".join(self.profiles))


    def transform_content(self, filepath, content):
        keypath = os.path.relpath(filepath, self.basepath)
        for profile in self.profiles:
           extension_file = os.path.join(self.basepath, "profiles", profile, keypath)
           if os.path.isfile(extension_file):
               with open(extension_file) as f:
                   print ("Using extension file {}".format(extension_file))
                   content += "\n" + f.read()
        return content

