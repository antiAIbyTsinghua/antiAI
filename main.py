# -*- coding: utf-8 -*-
import os
import sys
import argparse
import glob
from cheater import gen_key,proccess_pic,hide_files,recover_files,test

def main(*argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--genkey', help='generate a new key to encrypt or decrypt images',
                        action='store_true')
    parser.add_argument('--test', help='run a test demo',
                        action='store_true')
    parser.add_argument('--protect', help='protect images against AI',
                        action='store_true')
    parser.add_argument('--recover', help='recover images from decrypted images',
                        action='store_true')
    parser.add_argument('--directory', '-d', type=str,
                        help='the directory that contains images', default='images')
    parser.add_argument('--method', '-m', type=str,
                        help='the algorithmn to protect images (only support fawkes for now)', default='fawkes')
    parser.add_argument('--key', '-k', type=str,
                        help='the key used to encrypt or decrypt images', default='key')
    parser.add_argument('--clean', help='the algorithmn to protect images (only support fawkes for now)',
                        action='store_true')
    args = parser.parse_args()
    
    if args.genkey:
        gen_key()
        print('New key generated!')
    elif args.test:
        test(r'images','fawkes',r'key',args.clean)
    elif args.protect:
        original_paths,cloaked_paths=proccess_pic(args.directory,args.method)
        sealed_paths=hide_files(original_paths,cloaked_paths,args.key)
    elif args.recover:
        image_paths=glob.glob(os.path.join(args.directory,'*'))
        image_paths=[path for path in image_paths if '_sealed' in path.split('/')[-1]]
        image_paths=[path for path in image_paths if '_recovered' not in path.split('/')[-1]]
        recovered_paths=recover_files(image_paths,args.key)
    else:
        original_paths,cloaked_paths=proccess_pic(args.directory,args.method)
        sealed_paths=hide_files(original_paths,cloaked_paths,args.key)
        recovered_paths=recover_files(sealed_paths,args.key)
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