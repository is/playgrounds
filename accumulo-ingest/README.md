Frequently Used Commands
========================

1. Force fetch & pull from git

    git fetch
    git reset --hard origin/develop


2. Grab dependent libraries

    mvn dependency:copy-dependencies
    mvn dependency:copy

3. Git commit amend with the same message
   Reference from http://blog.blindgaenger.net/advanced_git_aliases.html

    git log -n 1 --pretty=tformat:%s%n%n%b | git commit -F - --amend
