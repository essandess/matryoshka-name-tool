#!/opt/local/bin/python
#coding: utf-8
__author__ = 'stsmith'

# matryoshka_name_tool: recursive copy and apply install_name_tool to .dylib's

# Copyright 2015 Steven T. Smith <steve dot t dot smith at gmail dot com>, GPL

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import argparse, errno, os, re, shutil, subprocess as sp

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

class InstalllName:
    args = None

    def run(self):
        self.args = self.parseArgs()
        self.libdir_pattern = re.compile(r'^\s+' + self.args.libdir)
        self.dylib_pattern = re.compile(r'^\s+(%s.+?) .+' % self.args.libdir)
        if not self.args.update:
            shutil.rmtree(self.args.install_libdir)
            make_sure_path_exists(self.args.install_libdir)
        self.dylibs_copied = set()
        self.dylibs_recursed = set()
        for object in self.args.objects: self.install_name_tool(object)

    def parseArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('objects', metavar='OBJS', type=str, nargs='+',
                            help='Object file[s]')
        parser.add_argument('-d', '--install-libdir', help="Shared library install directory", type=str, default='../lib/')
        parser.add_argument('-L', '--libdir', help="Shared library source directory", type=str, default='/opt/local/lib/')
        parser.add_argument('-u', '--update', help="Update the install directory", action='store_false')
        return parser.parse_args()

    def install_name_tool(self,object):
        p = sp.Popen(['otool', '-L', object], stdout=sp.PIPE)
        out, err = p.communicate()
        lines = out.splitlines()
        for line in lines[1:]:
            if self.libdir_pattern.match(line):
                dylib = self.dylib_pattern.sub(r'\1',line)
                if dylib not in self.dylibs_copied:
                    if not self.args.update and not os.path.isfile(self.args.install_libdir + os.path.basename(dylib)):
                        shutil.copy(dylib, self.args.install_libdir)
                    self.dylibs_copied.add(dylib)
                target = self.args.install_libdir + os.path.basename(object) \
                    if (os.path.splitext(os.path.basename(object))[1] == '.dylib') \
                    else object
                cmd = [ 'install_name_tool', '-change', dylib,
                         '@executable_path/' + self.args.install_libdir + os.path.basename(dylib),
                         target ]
                sp.call(cmd)
                print "\t" + ' '.join(cmd)
                if dylib not in self.dylibs_recursed and dylib != object: # recurse
                    self.install_name_tool(dylib)
                    self.dylibs_recursed.add(dylib)

if __name__ == "__main__":
    install_name = InstalllName()
    install_name.run()
