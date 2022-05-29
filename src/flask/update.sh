df() {
    date

    git fetch
    git reset --hard HEAD
    git merge origin/$CURRENT_BRANCH

    git pull origin master

    echo ""
}

df >> updated.txt
