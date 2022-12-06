import sys
import os
import json
import copy
from github import Github

BUILDER_CONFIG_FILE = os.getenv("BUILDER_CONFIG_FILE")

new_image_builder_json = []

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

      new_image_builder_json.append(image)
    except:
      new_image_builder_json.append(image)
      continue

with open(BUILDER_CONFIG_FILE, 'w', encoding='utf-8') as f:
  json.dump(new_image_builder_json, f, ensure_ascii=False, indent=2)

sys.stdout.write(json.dumps(images_to_build) + "\n")
