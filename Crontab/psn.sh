#!/bin/bash -ex

GITHUB_URL="git@github.com:lidejia/psn-discount.git"

export PATH="${HOME}/.local/bin:$PATH"
CWD=$(cd $(dirname $0)/../ && pwd)

rm -f ${CWD}/games.json
rm -f ${CWD}/games.me
rm -rf ${CWD}/gh-pages

# fetch games
cd ${CWD}/PsnGame && scrapy crawl psn -o ${CWD}/games.json -t json

# generate markdown
cd ${CWD}/PageGenerator && ./generator.py -s ${CWD}/games.json -t ${CWD}/games.md

# push to github
[ -d "${CWD}/gh-pages" ] || git clone "${GITHUB_URL}" -b gh-pages ${CWD}/gh-pages
mv ${CWD}/games.md ${CWD}/gh-pages/README.md
cd ${CWD}/gh-pages
git add README.md
git commit -m "Update for $(date +'%Y%m%d')"
git push origin
