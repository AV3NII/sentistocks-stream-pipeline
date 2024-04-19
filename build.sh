#!/bin/sh

# -- Building the Images

docker build \
  -f dashboard.Dockerfile \
  -t mage .

docker build \
  -f mage.Dockerfile \
  -t mage .

