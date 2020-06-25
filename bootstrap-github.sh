#!/bin/bash

set -e -u -x

KEYFILE=$HOME/.ssh/id_rsa.github.key

function create-ssh-key() {
  # -b 2048.     - key bits (2048 recommended for RSA)
  # -E sha256    - key fingerprint algo
  # -f keyfile.  - private keyfile (public will be keyfile.pub)
  # -N ""        - no password
  # -t rsa       - private/public key type
  #
  ssh-keygen -b 2048 -E sha256 -f $KEYFILE -N "" -t rsa
}

function setup-ssh-key {
  create-ssh-key
  if [ -n "${TESTING:-}" ]; then
    return
  fi
  ssh-add $KEYFILE
  echo
  echo "please add this ssh key to github"
  echo
  cat $KEYFILE.pub
  echo
  python3 -mwebbrowser -n https://github.com/settings/ssh/new
  read -p "Please hit ENTER once you've added your key to github"
}

if [ $(uname -s) = "Darwin" ]; then
  if ! git > /dev/null 2>&1l then
    echo "command line tools need to be installed"
    echo "run $0 again after xcode install is complete"
    exit 1
  else
    echo "command line tools already installed"
  fi
else
  sudo apt install -y git
fi

ssh-add -l | grep github > /dev/null 2>&1 || setup-ssh-key

curl -fLo /tmp/yadm https://github.com/TheLocehiliosan/yadm/raw/master/yadm                                                                                                       
bash /tmp/yadm clone --bootstrap git@github.com:$USER/dotfiles-public.git 
