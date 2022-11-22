# -*- coding: utf-8 -*-
import glob
import os
from fawkes.protection import Fawkes
from stego_lsb import LSBSteg

def gen_paths(paths,suffix,form=None):
    output=[0 for i in range(len(paths))]
    if form==None:
        for i in range(len(paths)):
            output[i]='{}_{}.{}'.format('.'.join(paths[i].split('.')[:-1]),suffix,'.'.join(paths[i].split('.')[-1:]))
    else:
        for i in range(len(paths)):
            output[i]='{}_{}.{}'.format('.'.join(paths[i].split('.')[:-1]),suffix,form)
    return output

def proccess_pic(input_path,method,cloaked_paths=None):
    if method == 'fawkes':
        protector = Fawkes('arcface_extractor_2','0','1',mode='low')
        image_paths = glob.glob(os.path.join(input_path,'*'))
        image_paths = [path for path in image_paths if '_cloaked' not in path.split('/')[-1]]
        image_paths = [path for path in image_paths if '_sealed' not in path.split('/')[-1]]
        if cloaked_paths==None:
            cloaked_paths=gen_paths(image_paths,'cloaked','png')
        protector.run_protection(image_paths,th=0.01,sd=1000000,lr=2,
                                 max_step=1000,batch_size=1,format='png'
                                 ,separate_target=False,debug=False,no_align=False)
        return image_paths,cloaked_paths

def hide_files(original_paths,cloaked_files,output_paths=None):
    if output_paths==None:
        output_paths=gen_paths(original_paths,'sealed','png')
    n=0
    for i in range(len(original_paths)):
        #LSBSteg.analysis(cloaked_files[i],original_paths[i],2)
        LSBSteg.hide_data(cloaked_files[i],original_paths[i],output_paths[i],2,1)
        n+=1
    print('Hide {} files susccessfully!'.format(n))
    return output_paths

def recover_files(sealed_paths,recover_paths=None):
    if recover_paths==None:
        recover_paths=gen_paths(sealed_paths,'recovered','jpeg')
    n=0
    for i in range(len(sealed_paths)):
        LSBSteg.recover_data(sealed_paths[i],recover_paths[i],2)
        n+=1
    print('Recover {} files susccessfully!'.format(n))
    return recover_paths

def test(paths,method='fawkes',clean=False):
        original_paths,cloaked_paths=proccess_pic(paths,method)
        sealed_paths=hide_files(original_paths,cloaked_paths)
        recovered_paths=recover_files(sealed_paths)
        if clean:
            cache_files=cloaked_paths+sealed_paths+recovered_paths
            for f in cache_files:
                try:
                    os.remove(f)
                except:
                    pass
            print('Clean done!')

if __name__=='__main__':
    test(r'D:\Downloads\京东算法\images','fawkes',True)