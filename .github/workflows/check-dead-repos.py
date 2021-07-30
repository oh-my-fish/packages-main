#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A Python script to check repositories statuses
# This file is part of Oh My Fish's packages-main
# https://github.com/oh-my-fish/packages-main

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021, Fabian Homborg <FHomborg@gmail.com>
# Copyright (c) 2021, Pablo S. Blum de Aguiar <scorphus@gmail.com>


import json
import logging
import os
import sys

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'warning').upper())

data = sys.stdin.read()
try:
    repo = json.loads(data)
    logging.debug("repo: %s", repo)
except:
    logging.exception("error parsing response")
    repo = None
if not repo:
    logging.error("%s could not be read ❌", sys.argv[1])
elif "documentation_url" in repo:
    logging.critical("rate limit exceeded when reading %s", sys.argv[1])
elif repo.get("message", "") == "Moved Permanently":
    logging.error("%s has moved permanently ❌", sys.argv[1])
elif repo.get("message", "") == "Not Found":
    logging.error("%s does not exist ❌", sys.argv[1])
elif repo.get("archived", False):
    logging.error("%s has been archived ❌", sys.argv[1])
elif repo.get("has_issues") is False:
    logging.error("%s has issues disabled ❌", sys.argv[1])
else:
    logging.info("%s is okay ✅", sys.argv[1])
    sys.exit(0)

sys.exit(1)
