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

First, you will need to train a bot using your Facebook or Skype data (you can skip this section if you want to use the generic pre-trained bot). 

#### Getting Facebook data

#### Getting Skype data

#### Using char-rnn

### Running bots on messenger
