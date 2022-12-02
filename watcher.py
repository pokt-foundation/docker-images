import sys
import os
import json
from github import Github

BUILDER_CONFIG_FILE = os.getenv("BUILDER_CONFIG_FILE")

with open(BUILDER_CONFIG_FILE) as f:
  images = json.load(f)
  images_to_build = []
  g = Github(per_page=100)
  for image in images:
    try:
      watch_repo = image["watch_repo"]
      repo = g.get_repo(watch_repo)
      latest_release = repo.get_latest_release().tag_name
      if latest_release != image["tag"]:
        image["new_tag"] = latest_release
        images_to_build.append(image)
    except:
      continue

sys.stdout.write(json.dumps(images_to_build) + "\n")