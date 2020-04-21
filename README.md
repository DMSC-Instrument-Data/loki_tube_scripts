# loki_tube_scripts
LOKI scripts for tubes and includes conversions for GEANT4 outputs

# Procedure for how to add changes to this repo 
## Pull existing changes first
If you are not sure whether or not there are existing changes you can do the following:
* store your changes using `git stash`
* Checkout the master branch `git checkout master`
* Pull changes `git pull`
* return to your branch `git checkout <branch-name>`
* rebase your branch to master `git rebase origin/master`
* restore your changes `git stash pop`

## View current status of repo
* use `git status` to view your changes. You may have added files or modified files.

## Create branch
* `git branch --no-track <branch-name> origin/master`
* `git branch checkout <branch-name>`

## Stage changes for commit
* To add all files which are new at once use `git add -A`
* To add all files which have been modified `git add -u`
* To add specific files use `git add <filepath/filename>` (without the `<>`)

## Commit and push changes
* To commit changes which have been added use `git commit --no-verify -m "<commit-message>"`
* To push changes on a completely new branch you will need to use `git push --set-upstream orgin <branch-name>`
* To push changes on an existing branch just use `git push`

