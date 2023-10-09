#!/bin/bash
apt-get update
apt-get install -y wget
sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)" -- -t gnzh -p https://github.com/zsh-users/zsh-autosuggestions -p https://github.com/zsh-users/zsh-completions -p git
