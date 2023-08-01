#!/bin/bash

# Built off of a similar script from https://github.com/joshjohanning/github-misc-scripts, but user focused instead of org.
#
# No need to pass an argument here as it'll use the current user's credentials/username.
# Generate a list of repositories that are listed in your repositories.
#
# Usage: ./generate-repositories-list.sh >> repos.txt

gh api graphql --paginate -f query='
  query($endCursor: String) {
    viewer {
      repositories(first: 100, after: $endCursor) {
        nodes { nameWithOwner }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }' --template '{{range .data.viewer.repositories.nodes}}{{printf "%s\n" .nameWithOwner}}{{end}}'
