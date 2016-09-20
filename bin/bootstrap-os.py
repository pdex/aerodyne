#!/usr/bin/env python

import argparse
import os
import subprocess

class colors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

def shellout(cmd, echo=False, silent=True):
  if silent and not echo:
    cmd += ' > /dev/null 2>&1'
  if echo:
    print colors.WARNING, cmd, colors.ENDC
  return subprocess.call(cmd, shell=True) == 0

class HomebrewBase(object):
  def __init__(self, formula, install):
    self.formula = formula
    self.should_install = install

  def run(self, dry_run):
    if not self.should_install:
      return True

    if self.is_installed():
      print "%s: already installed!" % self.formula
    else:
      print "%s: installing!" % self.formula
      if not dry_run:
        result = self.install()
        if not result:
          print "%s: install failed!" % self.formula
          return False
    return True

  def is_installed(self):
    return false

  def install(self):
    pass

  def __str__(self):
    return "formula=%s install=%s" % (self.formula, self.should_install)

  def __repr__(self):
    return self.__str__()

class HomebrewFormula(HomebrewBase):
  def is_installed(self):
    return shellout('brew list | grep %s' % self.formula)

  def install(self):
    return shellout('brew install %s' % self.formula, echo=True)

class HomebrewCaskFormula(HomebrewBase):
  def is_installed(self):
    return shellout('brew cask list | grep %s' % self.formula)

  def install(self):
    return shellout('brew cask install %s' % self.formula, echo=True)

def build_group(parser, opt, klass, formula, default_yes):
  group = parser.add_mutually_exclusive_group(required=False)
  def build(enable):
    return klass(formula, enable)
  def hmsg(enable):
    if enable:
      return 'default'
    return ''
  group.add_argument('--' + opt, dest=opt, action='store_const', const=build(True), default=build(default_yes), help=hmsg(default_yes))
  group.add_argument('--no-' + opt, dest=opt, action='store_const', const=build(True), default=build(not default_yes), help=hmsg(not default_yes))

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--homebrew-prefix', action='store', default='~/.local', help='default: ~/.local')
  parser.add_argument('-n', '--dry-run', action='store_const', const=True, default=False)
  # cask formulas
  build_group(parser, 'install-alfred', HomebrewCaskFormula, 'alfred', True)
  build_group(parser, 'install-iterm2', HomebrewCaskFormula, 'iterm2', True)
  build_group(parser, 'install-java', HomebrewCaskFormula, 'java', True)
  build_group(parser, 'install-sizeup', HomebrewCaskFormula, 'sizeup', True)
  build_group(parser, 'install-slack', HomebrewCaskFormula, 'slack', True)
  build_group(parser, 'install-vagrant', HomebrewCaskFormula, 'vagrant', True)
  build_group(parser, 'install-virtualbox', HomebrewCaskFormula, 'virtualbox', True)
  # brew formulas
  build_group(parser, 'install-bash-completion', HomebrewFormula, 'bash-completion', True)
  build_group(parser, 'install-emacs', HomebrewFormula, 'emacs', True)
  build_group(parser, 'install-emacs', HomebrewFormula, 'git', True)
  build_group(parser, 'install-maven', HomebrewFormula, 'maven', True)
  build_group(parser, 'install-packer', HomebrewFormula, 'packer', False)

  return parser.parse_args()

def fix_path(args):
  prefix = os.path.expanduser(args.homebrew_prefix)
  path = os.path.join(prefix, 'bin')
  if path in os.environ["PATH"].split(os.pathsep):
    print 'Path already configured'
  else:
    print 'Updating ~/.profile with new path'
    if not args.dry_run:
      print >> open(os.path.expanduser('~/.profile'), 'a'), 'export PATH={path}:$PATH'.format(path=path)
    os.environ["PATH"] = path + os.pathsep + os.environ["PATH"]

def install_homebrew(args):
  if shellout('which brew'):
    print "brew: already installed!"
    return True
  else:
    print "brew: installing!"
    path = os.path.expanduser(args.homebrew_prefix)
    if not args.dry_run:
      return shellout('''ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install | sed -e 's@^HOMEBREW_PREFIX[[:space:]]*=.*$@HOMEBREW_PREFIX = \"'{path}'\"@')"'''.format(path=path), echo=True)
    else:
      return False

def main():
  args = parse_args()
  #print args
  fix_path(args)
  ready = install_homebrew(args)
  if ready:
    for key, formula in vars(args).iteritems():
      if key.startswith('install'):
        #print key, formula
        result = formula.run(args.dry_run)
        #print
        if not result:
          break

if __name__ == '__main__':
  main()
