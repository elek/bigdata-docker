#!/usr/bin/env python
import requests
import os
import json
import argparse

from builtins import print

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import logging
from consync.template import Template
from consync.transform import Transform
from consync.profiles import Profiles


class ConSync:
    def __init__(self, basepath, consul_url, consul_prefix):
        self.consul_url = consul_url
        self.basepath = basepath
        self.consul_prefix = consul_prefix
        self.plugins = []
        self.plugins.append(Profiles(basepath))
        self.plugins.append(Template(basepath))
        self.plugins.append(Transform(basepath))


    def base_consul_url(self):
        return url + self.consul_prefix + "/"

    def listfiles(self):
        for root, dirs, files in os.walk(self.basepath, topdown=True):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for file in files:
                filepath = os.path.join(root, file)
                print(filepath)
                self.upload(filepath)

    def upload(self, path):
        print("Uploading %s" % path)
        content = self.read_content(path)
        for plugin in self.plugins:
            content = plugin.transform_content(path, content)
        keypath = os.path.relpath(path, self.basepath)
        if not requests.put(self.base_consul_url() + keypath, content).ok:
            print("Error on uploading file {} to {}".format(path, keypath))

    def read_content(self, filepath):
        content = ""
        with open(filepath) as in_file:
            content = in_file.read()
        return content

    def clean(self):
        result = requests.get(self.base_consul_url() + "?recurse")
        if result.ok:
            entries = json.loads(result.text)
            for entry in entries:
                relativeKey = os.path.relpath(entry['Key'], self.consul_prefix)
                filepath = os.path.join(self.basepath, relativeKey)
                if not os.path.isfile(filepath):
                    print("Deleting key " + relativeKey)
                    delete_url = self.base_consul_url() + relativeKey
                    if not requests.delete(delete_url).ok:
                        print("Key delete was unsuccessfull: %s" % delete_url)
        else:
            print("Error on getting existing keys ")


class MyEventHandler(FileSystemEventHandler):
    def __init__(self, syncer):
        self.syncer = syncer

    def on_modified(self, event):
        if not event.is_directory:
            print(event.event_type)
            print(event.src_path)
            self.syncer.upload(event.src_path)


locals()
parser = argparse.ArgumentParser()
parser.add_argument("dir", help="directory to upload")
parser.add_argument("prefix", help="prefix path in consul kv")
parser.add_argument("--serve", help="Listening for new changes and upload only the changed files", action="store_true")
parser.add_argument("--url", help="consul server address (protocol, servername, port)")
args = parser.parse_args()

url = "http://localhost:8500/v1/kv/"

if args.url:
    url = args.url + "/v1/kv/"

syncer = ConSync(args.dir, url, args.prefix)

if not args.serve:
    syncer.clean()
    syncer.listfiles()
else:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    event_handler = MyEventHandler(syncer)
    observer = Observer()
    observer.schedule(event_handler, args.dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
