#!/usr/bin/env fish

# A Fish script to check for "dead" repositories
# This file is part of Oh My Fish's packages-main
# https://github.com/oh-my-fish/packages-main

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021, Fabian Homborg <FHomborg@gmail.com>
# Copyright (c) 2021, Pablo S. Blum de Aguiar <scorphus@gmail.com>


function read_repository -a user_repo
  set -l url https://api.github.com/repos/$user_repo
  test "$USERNAME:$TOKEN" != ":"
    and curl -s -u $USERNAME:$TOKEN $url
    or curl -s $url
end

set -l packages packages/*
set -l python_script (type -p read_repository | sed s/\\.fish\$/\\.py/)
set -l count 0

for package in $packages
  set -l url (string replace -rf 'repository *= *(.*)' '$1' < $package)
  or begin
    echo $package has no repository line ❌
    continue
  end
  set url (string replace -r '.git$' '' -- $url | string trim -c '/')
  set package (string replace -r '.*/' '' $package)
  set -l user_repo (string replace 'https://github.com/' '' $url)
  or begin
    echo $package is not on GitHub -- $url ⚠️
    continue
  end
  read_repository $user_repo | python $python_script $package
  set count (math $count + $status)
end

set -l total (ls $packages | wc -l)

if test $count -gt 0
  echo Found $count/$total repositories with issues 💥
  exit 1
end

echo No issues found in $total repositories 🤘
