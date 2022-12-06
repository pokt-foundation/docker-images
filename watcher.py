import sys
import os
import json
import copy
from github import Github

BUILDER_CONFIG_FILE = os.getenv("BUILDER_CONFIG_FILE")

with open(BUILDER_CONFIG_FILE) as f:
  images = json.load(f)
  images_to_build = []
  g = Github(per_page=100)

  for image in images:
    try:
      if image["autobuild"] is True:
        watch_repo = image["watch_repo"]
        repo = g.get_repo(watch_repo)
        latest_release = repo.get_latest_release().tag_name

        if latest_release != image["tag"]:
          image_copy = copy.deepcopy(image)

          image_copy["old_tag"] = image["tag"]
          image_copy["tag"] = latest_release

          image["tag"] = latest_release

          images_to_build.append(image_copy)
    except:
      continue

sys.stdout.write(json.dumps(images_to_build) + "\n")
