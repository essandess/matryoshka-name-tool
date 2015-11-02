# matryoshka-name-tool
A recursive call of OS X's `install_name_tool` for shared library distributions.

## Synopsis

Apple [does not support](https://developer.apple.com/library/mac/qa/qa1118/_index.html) statically linked binaries on Mac OS X. Therefore, it is necessary to distribute shared libraries whose shared library install names have been changed using `install_name_tool`. But `install_name_tool` must be [applied recursively](http://thecourtsofchaos.com/2013/09/16/how-to-copy-and-relink-binaries-on-osx/) down the entire shared library dependency tree, which can [result](https://github.com/essandess/etv-comskip/) in many hundreds of calls to  `install_name_tool`.

`matryoshka_name_tool` calls `install_name_tool` automatically and creates a common shared library directory that may be used to distribute binaries on OS X.

## Usage

`python matryoshka_name_tool.py ./comskip ./comskip-gui`

`python matryoshka_name_tool.py -h`
> usage: matryoshka_name_tool.py [-h] [-d INSTALL_LIBDIR] [-L LIBDIR] [-u]
>                                OBJS [OBJS ...]
> 
> positional arguments:
>   OBJS                  Object file[s]
> 
> optional arguments:
>   -h, --help            show this help message and exit
>   -d INSTALL_LIBDIR, --install-libdir INSTALL_LIBDIR
>                         Shared library install directory
>   -L LIBDIR, --libdir LIBDIR
>                         Shared library source directory
>   -u, --update          Update the install directory

## License

Licensed under the GNU General Public License, version 2.
