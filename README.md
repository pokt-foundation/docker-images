## Automated build
- Add your docker image information in the `image-builder.json` file
- When you open a PR the `Build Docker Images` workflow will run and check if it's necessary to build the image (if there's any changes)
- The image will only be published when you merge your PR to `master`