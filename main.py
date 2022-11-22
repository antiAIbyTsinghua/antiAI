# -*- coding: utf-8 -*-
import os
import sys
import argparse
from cheater import proccess_pic,hide_files,recover_files

def main(*argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', '-d', type=str,
                        help='the directory that contains images to run protection', default='images/')
    parser.add_argument('--method', '-m', type=str,
                        help='the algorithmn to protect images (only support fawkes for now)', default='fawkes')
    parser.add_argument('--clean', help='the algorithmn to protect images (only support fawkes for now)',
                        action='store_true')
    args = parser.parse_args()
    
    original_paths,cloaked_paths=proccess_pic(args.directory,args.method)
    sealed_paths=hide_files(original_paths,cloaked_paths)
    recovered_paths=recover_files(sealed_paths)
    if args.clean:
        cache_files=cloaked_paths+sealed_paths+recovered_paths
        for f in cache_files:
            try:
                os.remove(f)
            except:
                print('cannot delete {}'.format(f))
        print('Clean done!')

if __name__=='__main__':
    main(*sys.argv)