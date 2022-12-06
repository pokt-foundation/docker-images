import sys
import os
import json

BUILDER_CONFIG_FILE = os.getenv("BUILDER_CONFIG_FILE")

f = open(BUILDER_CONFIG_FILE)

images_to_build = json.load(f)
images_need_build = []

changed_files = sys.stdin.read().splitlines()

for image in images_to_build:
    path_to_dockerfile = image["context"] + "/" + image["dockerfile"]

    if path_to_dockerfile in changed_files:
        images_need_build.append(image)

sys.stdout.write(json.dumps(images_need_build) + "\n")
