#!/bin/zsh
# env
source ~/.zshrc
repoDir=$4
packageName=$1
commit=$2
date=$3
cd $repoDir
git stash push --include-untracked #This line...
git stash drop #... and this line are to overwrite any changes that might happen...
git checkout -q $commit #checkout next commit from log...
argon -j . > ../${packageName}Argon/${date}_${commit}.json
