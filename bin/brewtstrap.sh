#!/bin/bash -ex

ls -la
ls -la ~
ls -la ~/.local
mkdir -p ~/.local/bin
pushd ~/.local
git clone https://github.com/Homebrew/brew
pushd bin
ln -s ../brew/bin/brew brew
echo 'if [ -d "$HOME/.local/bin" ]; then export PATH="$PATH:$HOME/.local/bin"; fi' >> ~/.bash_profile
bash -c 'brew install stow'
#brew install stow
