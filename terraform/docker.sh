#!/bin/sh

func() {
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
    sudo usermod -aG docker $USER

    sudo docker compose -f ~/src/docker-compose.yml up -d gitlab
    sudo docker compose -f ~/src/docker-compose.yml up -d 
    printf "\n\nSleeping...\n\n" && sleep 60 && \
    sudo cp ~/src/gitlab-backup/1653615066_2022_05_27_14.10.0-ee_gitlab_backup.tar ~/src/gitlab/data/backups/ && \
    printf "\n\nPart 1...\n\n" && sleep 5 && \
    sudo cp ~/src/gitlab-backup/gitlab-secrets.json ~/src/gitlab/config/ && \
    sudo cp ~/src/gitlab-backup/gitlab.rb ~/src/gitlab/config/ && \
    printf "\n\nPart 2...\n\n" && sleep 5 && \
    sudo docker exec -i gitlab_ee chown -v git:git /var/opt/gitlab/backups/1653615066_2022_05_27_14.10.0-ee_gitlab_backup.tar && \
    printf "\n\nPart 3...\n\n" && sleep 5 && \
    sudo docker exec -i gitlab_ee gitlab-ctl reconfigure && \
    printf "\n\nPart 4...\n\n" && sleep 5 && \
    sudo docker exec -i gitlab_ee gitlab-ctl start && \
    printf "\n\nPart 5...\n\n" && sleep 5 && \
    sudo docker exec -i gitlab_ee gitlab-ctl stop unicorn && \
    printf "\n\nPart 6...\n\n" && sleep 5 && \
    sudo docker exec -i gitlab_ee gitlab-ctl stop sidekiq &&  \
    printf "\n\nStarting backup restore...\n\n" && sleep 5 && \
    sudo docker exec -i gitlab_ee bash -c 'yes yes | gitlab-rake gitlab:backup:restore --trace' && \
    printf "\n\nPart 7...\n\n" && sleep 5 && \
    sudo docker exec -i gitlab_ee gitlab-ctl restart && \
    printf "\n\nSanitizing Gitlab...\n\n" && sleep 15 && \
    sudo docker exec -i gitlab_ee bash -c 'yes yes | gitlab-rake gitlab:check SANITIZE=true'
}

func > output.txt