# neural-chatbot
Train a neural chatbot to imitate your personality using your messaging history! Never be obligated to respond to your friends on Messenger again; your bot will do it for you and say exactly what you would say! Responses are generated from a char-level language model, implemented with a recurrent neural network policy.

## Getting neural-chatbot

Clone neural-chatbot using:
```bash
$ git clone https://github.com/socketteer/neural-chatbot.git
```

## Requirements

Currently, this code has only been tested on Ubuntu. This code is written in Python 3. 

Training chatbots requires [char-rnn](https://github.com/karpathy/char-rnn). Install the requirements for char-rnn as directed. Then clone char-rnn inside the neural-chatbot folder:

```bash
$ cd neural-chatbot
$ git clone https://github.com/karpathy/char-rnn.git
```

Running the autoresponder script requires python module [fbchat](http://fbchat.readthedocs.io/en/master/install.html). You can get it using:

```bash
$ pip install fbchat
```

## Usage

### Training bots

First, you will need to train a bot using your Facebook or Skype data (you can skip this section if you want to use the generic pre-trained bot). For this, you will need [botfood-parser](https://github.com/socketeer/botfood-parser). You do not need to clone it inside the neural-chatbot directory.

#### Getting Facebook data

On Facebook desktop, click the down arrow at the upper right corner of the screen and go to Settings -> General. Click the link that says "Download a copy of your Facebook data" and then click "Start my archive." It will take anywhere from a few minutes to a few hours for Facebook to compile your data. You should get an email and a notification when it is ready for download.

Download the zip file called facebook-<your_username>.zip. 

Create a new folder in neural-chatbot/facebook (you may call it your name or your facebook username). Copy all the html files in Messages to this folder. Run the fb_parser.py script using:

```bash
$ python fb_parser.py <name of new folder> <your facebook display name>
```

Make sure the name argument is exactly the same as your display name for Facebook, otherwise the script will not parse the data correctly! You will get a warning if it seems like you used the wrong name.

You can use the -g or --groupchat flag to enable parsing data from groupchats. This is not recommended unless you are very active in most of the groupchats you're in.

Running the above command will generate a text file in neural-chatbot/corpus called facebook-<your_first_name>.txt. This prepared botfood. Follow the instructions under "Training with char-rnn" to train a bot using your data!

#### Getting Skype data

You will need Skype classic on desktop to download your Skype history. 

#### Training with char-rnn

### Running bots on messenger
