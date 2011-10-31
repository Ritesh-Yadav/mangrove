#!/bin/bash
echo 'start code transfer service...'
echo 'access by:'
ip0=`ifconfig en0|egrep -o '([0-9]{1,3}\.){3}[0-9]{1,3}'|sed -n '1p'`
ip1=`ifconfig en1|egrep -o '([0-9]{1,3}\.){3}[0-9]{1,3}'|sed -n '1p'`
echo '    git pull --rebase git://'$ip0'/'
echo 'or  git pull --rebase git://'$ip1'/'
echo 'ctrl+c to stop.'
git daemon --base-path=. --export-all
