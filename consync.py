#!/usr/bin/env python
import requests
import os
import json
import argparse
import re
from os import listdir
from os.path import isfile, join
from builtins import print
from jinja2 import Template
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import logging
from jinja2 import Environment, FileSystemLoader

url = "http://localhost:8500/v1/kv/"

def base_consul_url(prefix):
    return url + prefix + "/"

def listfiles(dir, prefix):
    for root, dirs, files in os.walk(dir, topdown=True):
        dirs[:] = [d for d in dirs if d != ".git"]
        for file in files:
            filepath = os.path.join(root, file)
            upload(filepath, dir, prefix)


def upload(path, basedir, prefix):
    print("Uploading %s" % path)
    content = read_content(path, basedir)
    keypath = os.path.relpath(path, basedir)
    if not requests.put(base_consul_url(prefix) + keypath, content).ok:
        print("Error on uploading file {} to {}".format(path, keypath))

def template_render(filepath, basepath, content):
   t = Environment(loader=FileSystemLoader(os.path.dirname(filepath))).from_string(content)
   return t.render(env = os.environ)

def find_transformation(filepath, basepath):
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


def to_xml(content):
    result = "<configuration>\n"
    for line in content.split("\n"):
        keyvalue = line.split(":", 1)
        if len(keyvalue) > 1:
            result += "<property><name>{0}</name><value>{1}</value></property>\n".format(keyvalue[0], keyvalue[1].strip())
    result += "</configuration>"
    return result


def read_content(filepath, basepath):
    content = ""
    with open(filepath) as in_file:
        content = in_file.read()
    content = template_render(filepath, basepath, content)
    trans = find_transformation(filepath, basepath)
    if trans:
        content = globals()["to_%s" % trans](content)
    return content


def clean(path, prefix):
    result = requests.get(base_consul_url(prefix) + "?recurse")
    if result.ok:
        entries = json.loads(result.text)
        for entry in entries:
            relativeKey = os.path.relpath(entry['Key'], prefix)
            filepath = os.path.join(path, relativeKey)
            if not os.path.isfile(filepath):
                print("Deleting key " + relativeKey)
                delete_url = base_consul_url(prefix) + relativeKey
                if not requests.delete(delete_url).ok:
                    print("Key delete was unsuccessfull: %s" % delete_url)
    else:
        print("Error on getting existing keys ")


class MyEventHandler(FileSystemEventHandler):
     def __init__(self, basedir, prefix):
         self.basedir = basedir
         self.prefix = prefix

     def on_modified(self, event):
         if not event.is_directory:
            print(event.event_type)
            print(event.src_path)
            upload(event.src_path, self.basedir, self.prefix)

locals()
parser = argparse.ArgumentParser()
parser.add_argument("dir", help="directory to upload")
parser.add_argument("prefix", help="prefix path in consul kv")
parser.add_argument("--serve", help="Listening for new changes and upload only the changed files", action="store_true")
parser.add_argument("--url", help="consul server address (protocol, servername, port)")
args = parser.parse_args()

if args.url:
    print(args.url)
    url = args.url + "/v1/kv/"
if not args.serve:
    clean(args.dir, args.prefix)
    listfiles(args.dir, args.prefix)
else:
  logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

  event_handler = MyEventHandler(args.dir, args.prefix)
  observer = Observer()
  observer.schedule(event_handler, args.dir, recursive=True)
  observer.start()
  try:
     while True:
        time.sleep(1)
  except KeyboardInterrupt:
     observer.stop()
  observer.join()
