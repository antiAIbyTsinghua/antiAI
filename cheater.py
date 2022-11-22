# -*- coding: utf-8 -*-
import glob
import os
from cryptography.fernet import Fernet
from fawkes.protection import Fawkes
from stego_lsb import LSBSteg
from PIL import Image

def gen_paths(paths,suffix,form=None):
    output=[0 for i in range(len(paths))]
    if form==None:
        for i in range(len(paths)):
            output[i]='{}_{}.{}'.format('.'.join(paths[i].split('.')[:-1]),suffix,'.'.join(paths[i].split('.')[-1:]))
    else:
        for i in range(len(paths)):
            output[i]='{}_{}.{}'.format('.'.join(paths[i].split('.')[:-1]),suffix,form)
    return output

def gen_key():
    key=Fernet.generate_key()
    with open('key','wb+') as f:
        f.write(key)
    return key

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

def hide_files(original_paths,cloaked_files,key=None,output_paths=None):
    if output_paths==None:
        output_paths=gen_paths(original_paths,'sealed','png')
    if key==None:
        n=0
        for i in range(len(original_paths)):
            #LSBSteg.analysis(cloaked_files[i],original_paths[i],2)
            LSBSteg.hide_data(cloaked_files[i],original_paths[i],output_paths[i],2,1)
            n+=1
    else:
        if not os.path.exists(key):
            key=gen_key()
            n,encr=0,Fernet(key)
            for i in range(len(original_paths)):
                #LSBSteg.analysis(cloaked_files[i],original_paths[i],2)
                with open(original_paths[i],'wb+') as f:
                    image=Image.open(cloaked_files[i])
                    encrypt_file=encr.encrypt(f.read())
                    image=LSBSteg.hide_message_in_image(image,encrypt_file,2)
                    is_animated=getattr(image,"is_animated",False)
                    image.save(output_paths[i],compress_level=1,save_all=is_animated)
                n+=1
        else:
            with open(key,'rb+') as f:
                key=f.read()
            n,encr=0,Fernet(key)
            for i in range(len(original_paths)):
                #LSBSteg.analysis(cloaked_files[i],original_paths[i],2)
                with open(original_paths[i],'rb+') as f:
                    image=Image.open(cloaked_files[i])
                    encrypt_file=encr.encrypt(f.read())
                    image=LSBSteg.hide_message_in_image(image,encrypt_file,2)
                    is_animated=getattr(image,"is_animated",False)
                    image.save(output_paths[i],compress_level=1,save_all=is_animated)
                n+=1
    print('Hide {} files susccessfully!'.format(n))
    return output_paths

def recover_files(sealed_paths,key=None,recover_paths=None):
    if recover_paths==None:
        recover_paths=gen_paths(sealed_paths,'recovered','jpeg')
    if key==None:
        n=0
        for i in range(len(sealed_paths)):
            LSBSteg.recover_data(sealed_paths[i],recover_paths[i],2)
            n+=1
    else:
        with open(key,'rb+') as f:
            key=f.read()
        n,encr=0,Fernet(key)
        for i in range(len(sealed_paths)):
            steg_image,output_file=LSBSteg.prepare_recover(sealed_paths[i],recover_paths[i])
            encrypted_file=LSBSteg.recover_message_from_image(sealed_paths[i],2)
            decrypted_file=encr.decrypt(encrypted_file)
            output_file.write(decrypted_file)
            output_file.close()
            n+=1
    print('Recover {} files susccessfully!'.format(n))
    return recover_paths

def test(paths=r'images',method='fawkes',key=r'key',clean=False):
        original_paths,cloaked_paths=proccess_pic(paths,method)
        sealed_paths=hide_files(original_paths,cloaked_paths,key)
        recovered_paths=recover_files(sealed_paths,key)
        if clean:
            cache_files=cloaked_paths+sealed_paths+recovered_paths
            for f in cache_files:
                try:
                    os.remove(f)
                except:
                    print('cannot delete {}'.format(f))
            print('Clean done!')
        print('Test finished!')

if __name__=='__main__':
    test(r'images','fawkes',r'key',True)