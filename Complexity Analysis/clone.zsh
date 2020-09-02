#!/bin/zsh
packageName=$1
gitUrl=$2
git clone $gitUrl
cd $packageName
git config core.fileMode false
git log --date=short  --pretty=format:"Commit: %h Date: %ad" > ../${packageName}CommitHistory.log
cd ../
# rm -rf $packageName
# git checkout <commit>
# argon -j . > argon.json
