#!/usr/bin/env python
# coding=utf-8

import json
from bson import ObjectId
import sys

from crawler.tools.db import conn

def setup_crawler(_fp):
	with open(_fp) as json_file:
		data = json.load(json_file)
		for dat in data:
			dat["_id"] = str(ObjectId())
			conn.project.save(dat)

def main():
	cmd = sys.argv[1:]
	print cmd
	if not cmd:
		print "usage: ./create_crawler.py path_to_file_name"
		sys.exit(1)
	else:
		file_path = cmd[0]
		setup_crawler(file_path)
		print file_path, "was created"


if __name__ == "__main__":
	main()

