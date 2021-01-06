# How to squash commit

A good practise 1 PR => 1 commit.
Or at least all commit `HAVE TO` build. 

If I comment **`"squash your commit"`**, here is how to do it.


## Prepare demo environment

````shell script
rm -rf ~/tmprepo
mkdir -p ~/tmprepo
cd ~/tmprepo

git init

git st

echo "world 1" >> file
git add --all
git commit -m "ci message 1"

echo "world 2" >> file
git add --all
git commit -m "ci message 2"

echo "world 3" >> file
git add --all
git commit -m "ci message 3"

echo "world 4" >> file
git add --all
git commit -m "ci message 4"

git status

git log
````


## Method 1: use reset trick

````shell script
set commit_1_sha (git log --all --grep='ci message 1' | grep commit | awk {'print $2'})

echo $commit_1_sha
git reset --soft $commit_1_sha

git commit -m "Squashed commit" --amend

git log 
````

## Method 2: do not add commit and amend directy

Note if commit 2 and 3 are not done yet we skip `reset --soft` and amend directly

## Method 3: perform interactive rebase

https://gitbetter.substack.com/p/how-to-squash-git-commits

### Squash 3rd and 4th commit

````shell script
set commit_2_sha (git log --all --grep='ci message 2' | grep commit | awk {'print $2'})

echo $commit_2_sha

git rebase -i -p $commit_2_sha
````

Output is 


````shell script
pick adb7f15 ci message 3
pick b26a5a3 ci message 4

# Rebase 446a63cb8313..b26a5a31ff2f onto 446a63cb8313 (2 commands)
#
# Commands:
# p, pick <commit> = use commit
# r, reword <commit> = use commit, but edit the commit message
# e, edit <commit> = use commit, but stop for amending
# s, squash <commit> = use commit, but meld into previous commit
[...]
````

we will change this line 

````shell script
pick b26a5a3 ci message 4 => s b26a5a3 ci message 4 
````

and log will show

````shell script
➤ git lg
* 3b88691c4e2c - 2021-01-06 16:37:44 +0000  (HEAD -> master)
|           ci message 3 - Sylvain COULOMBEL
* 446a63cb8313 - 2021-01-06 16:37:44 +0000
|           ci message 2 - Sylvain COULOMBEL
* 490863f0541a - 2021-01-06 16:37:44 +0000
            ci message 1 - Sylvain COULOMBEL
➤ cat file
world 1
world 2
world 3
world 4
````

We could have used HEAD~2

````shell script
git rebase -i -p HEAD~2
````

To  be equivalent. 

Note message can be edited otherwise default to original commit.

### Squash commit to the first commit of the repo

This is a particular case

````shell script
set commit_1_sha (git log --all --grep='ci message 1' | grep commit | awk {'print $2'})

echo $commit_1_sha # it outputs 258f7288b28154171cc1951d7ac09711573b4fbd

git rebase -i -p $commit_1_sha
````

it outputs

````shell script
pick 9b71aac ci message 2
pick b46d67c ci message 3
pick cb4b237 ci message 4

# Rebase 258f7288b281..cb4b23759734 onto 258f7288b281 (3 commands)
[...]
````

We need add manually the first commit.
And then squash, so we so

````shell script
p 258f728 ci message 1 
s 9b71aac ci message 2
s b46d67c ci message 3
s cb4b237 ci message 4
````

This will output 


````shell script
[16:51][master]✓ ~/tmprepo
➤ git lg
* cda6a8542124 - 2021-01-06 16:46:51 +0000  (HEAD -> master)
            ci message 1 - Sylvain COULOMBEL
[16:51][master]✓ ~/tmprepo
➤ cat file
world 1
world 2
world 3
world 4
````
This is very similar to https://github.com/scoulomb/myk8s/blob/master/Repo-mgmt/repo-mgmt.md (including fist commit point).

<!-- could add code review practise, cf jm page STOP-->