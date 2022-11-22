# antiAI
antiAI can be used to protect images/audios/vidoes from AI recognition by multiple algorithms. It only supports fawkes for now and will support more algorithms soon.

# requirements
opencv-python>=4.6.0.66

numpy>=1.15.4

python_version>=3.8

Click>=7.0

numpy>=1.19.5

tensorflow==2.4.1

keras==2.4.3

mtcnn

pillow>=7.0.0

bleach>=2.1.0

Fawkes

stego-lsb

cryptography>=37.0.1

# usage
For the first time use, you can test it by:

    git clone https://github.com/antiAIbyTsinghua/antiAI
    cd antiAI
    python main.py --test --clean

When it finished, it will print test finished.

To generate a new key:

    python main.py --genkey

We strongly recommend you keep the key carefully!

To protect files with a certain key:

    python main.py --protect -d images -m fawkes -k key

To recover files from decrypted files with a certain key:

    python main.py --recover -d images -m fawkes -k key

If none of test, genkey, protect, recover is announced, both protection and recovery will be performed using an existing key. For example:

    python main.py -d images -m fawkes -k key

You will get 3 new kinds of images. The images ended by _cloaked are the original files produced by antiAI algorithms. They seem similar to the original images but are difficult for AI to recognize. The images ended by _sealed are visually the same as the cloaked images, while the original images have been hiden in them. The images ended by _recovered are recovered images from the images ended by _sealed.

antiAI can help users protect their pravicy against AI recognitions. Users can save images ended by _sealed in their devices and can recover the original images whenever they want. An unauthorized visitor can only reach the cloaked images and will never reach the original images.
