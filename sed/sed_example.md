# Sed example

Assume I have in my repo api `v1alpha1` and wants to deliver api `v1`.
Here is how we could perform the replacement.

## Source

- https://stackoverflow.com/questions/1583219/how-to-do-a-recursive-find-replace-of-a-string-with-awk-or-sed
- https://en.wikipedia.org/wiki/Xargs

## Prerequisite 

### Clone a fresh repo

If want to use sed, and use a windows machine, you can use a linux VM.
If you use `rsync` for directory synchronisation see: https://github.com/scoulomb/myk8s/blob/master/Setup/ArchDevVM/known-issues.md#workaround-4-use-rsync-instead-of-nfs
As it is a one way sync, we will clone a fresh repo on user directory which is not part of the synced folder (`~/dev`) (otherwise `.git` would be overridden`)

````shell script
vagrant ssh
mkdir -p ~/tmp-dns
git clone https://rndwww.nce.amadeus.net/git/scm/~scoulombel/dns-automation.git ~/tmp-dns
````

### Give permissions

In some circumstances you may have permission issue as it is a temp folder we will give all rights.
But do not want to commit it. 

````shell script
sudo chmod -R 777 ~/tmp-dns
cd ~/tmp-dns
vim .git/config # change file mode to false: https://stackoverflow.com/questions/1580596/how-do-i-make-git-ignore-file-mode-chmod-changes
````

### As it is a fresh repo you may have to replace credentials


````shell script
find ~/tmp-dns -name karate-config.js -print0 | xargs -0 sed -i 's/<username>/adminuser/g'
find ~/tmp-dns -name karate-config.js -print0 | xargs -0 sed -i 's/<password>/adminpassword/g'
````

### You should check prior to any modifications that everything is working correct

For instanxce in some project you can you build and non regression via

````shell script
docker build .
docker-compose up 
```` 

See here if you have some issues:
https://github.com/scoulomb/myk8s/blob/master/Setup/ArchDevVM/known-issues.md#issue-b

## Core: perform the replacement


<!-- find ~/dev/dns-automation \( -type d -name .git -prune \) -o -type f | xargs -0 sed -i 's/v1alpha1/v1/g' => not working -->

### see file to replace

````shell script
git grep v1alpha1 | cut -f1 -d ':' 
git grep v1alpha1 | cut -f1 -d ':' |  xargs cat
````

### If any issue on path fix it 

Such as space rater than _ 

````shell script
git mv  "non_regression/src/test/java/dns/add host record_error_case_domain_exclusion.feature" non_regression/src/test/java/dns/add_host_record_error_case_domain_exclusion.feature
````

### Do the replacement 

````shell script
git grep v1alpha1 | cut -f1 -d ':' |  xargs  sed -i 's/v1alpha1/v1/g'
````

## Post check

````shell script
docker-compose up # check build success
git add -p # do not ci pwd
git co <br> ; git ci -m "blah"; git push
````

<!-- see DNS PR#90 -->