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

# usage

    git clone https://github.com/antiAIbyTsinghua/antiAI
    cd antiAI
    python main.py -d images -m fawkes

Alternatively, you can test it by:

    python main.py -d images -m fawkes --clean
