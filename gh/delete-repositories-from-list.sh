#!/bin/bash

# Built off of a similar script from https://github.com/joshjohanning/github-misc-scripts, but user focused instead of org.

# Deletes repos from a .txt list

# Need to run this to get the repo delete scope: gh auth refresh -h github.com -s delete_repo

# Usage: 
# Step 1: Run ./generate-repositories-list.sh >> repos.txt
# Step 2: ./delete-repos-from-list.sh repos.txt

if [ $# -lt "1" ]; then
    echo "Usage: $0 <reposfilename>"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "File $1 does not exist"
    exit 1
fi

filename="$1"

while read -r repofull ; 
do
    IFS='/' read -ra data <<< "$repofull"

    org=${data[0]}
    repo=${data[1]}

    echo $"Deleting: $org/$repo"
    gh repo delete "$org/$repo" --yes

done < "$filename"
