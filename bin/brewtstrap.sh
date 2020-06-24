#!/bin/bash

set -e -u -x

function setup-ssh-key() {
  local keyfile=$HOME/.ssh/id_rsa.github.key
  # -B           - display bubblebabble digest
  # -b 2048.     - key bits (2048 recommended for RSA)
  # -E sha256    - key fingerprint algo
  # -f keyfile.  - private keyfile (public will be keyfile.pub)
  # -N ""        - no password
  # -t rsa       - private/public key type
  #
  ssh-keygen -B -b 2048 -E sha256 -f $keyfile -N "" -t rsa
  ssh-add $keyfile
  echo
  echo "please add this ssh key to github"
  echo
  cat $keyfile.pub
  echo
  python3 -mwebbrowser -n https://github.com/settings/ssh/new
  read -p "Please hit ENTER once you've added your key to github"
}

if [ $(uname -s) = "Darwin"]; then
  xcode-select --install > /dev/null 2>&1 || echo "command line tools already installed"
else
  sudo apt install -y git
fi

setup-ssh-key

curl -fLo /tmp/yadm https://github.com/TheLocehiliosan/yadm/raw/master/yadm                                                                                                       
bash /tmp/yadm clone --bootstrap git@github.com:$USER/dotfiles-public.git 
