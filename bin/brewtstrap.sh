#!/bin/bash

set -e -x

mkdir -p ~/.local/bin
pushd ~/.local
git clone https://github.com/Homebrew/brew
pushd bin
ln -s ../brew/bin/brew brew
echo 'if [ -d "$HOME/.local/bin" ]; then export PATH="$PATH:$HOME/.local/bin"; fi' >> ~/.bash_profile
bash -c 'brew install stow'
#brew install stow
popd
popd
mkdir .emacs.d
touch .emacs.d/init.el
bash -c 'stow --verbose=3 -t $HOME -S .emacs.d'
test -d $HOME/.emacs.d
test -r $HOME/.emacs.d/init.el
