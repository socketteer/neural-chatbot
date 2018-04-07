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

### Preprocessing data

First, you will need to train a bot using your Facebook or Skype data (you can skip this section if you want to use the generic pre-trained bot). For this, you will need [botfood-parser](https://github.com/socketeer/botfood-parser). You do not need to clone it inside the neural-chatbot directory.

#### Getting Facebook data

On Facebook desktop, click the down arrow at the upper right corner of the screen and go to Settings -> General. Click the link that says "Download a copy of your Facebook data" and then click "Start my archive." It will take anywhere from a few minutes to a few hours for Facebook to compile your data. You should get an email and a notification when it is ready for download.

Download the zip file called facebook-<your_username>.zip. The "messages" folder in the zip file is the only part you will need. 

Create a new folder in botfood-parser/facebook (you may call it your name or your facebook username). Copy all the html files in "messages" to this folder. Run the fb_parser.py script using:

```bash
$ python fb_parser.py <name of new folder> <your facebook display name>
```

Make sure the name argument is exactly the same as your display name for Facebook, otherwise the script will not parse the data correctly! You will get a warning if it seems like you used the wrong name.

You can use the -g or --groupchat flag to enable parsing data from groupchats. This is not recommended unless you are very active in most of the groupchats you're in.

Running the above command will generate a text file in botfood-parser/corpus called facebook-<your_first_name>.txt. This prepared botfood. Follow the instructions under "Training with char-rnn" to train a bot using your data!

#### Getting Skype data

You will need Skype classic on desktop to export your Skype history. Select Tools -> Options and select Privacy, then Export Chat History. Copy the csv file to botfood-parser/skype.

Run the skype_parser.py script using:

```bash
$ python skype_parser.py <skype_username> <csv_file>
```

Running the above command will generate a text file in botfood-parser/corpus called facebook-<skype_username>.txt. This prepared botfood. Follow the instructions under "Training with char-rnn" to train a bot using your data!

### Training with char-rnn

Compile all the data you want to feed the bot in a single file and name it input.txt (it is totally fine to combine parsed Facebook and Skype data). Create a new folder in neural-chatbot/char-rnn/data and copy input.txt into the folder.

#### Method 1 -- training from scratch

This method works better if you have at least 2MB of data, preferably more. Navigate to the char-rnn directory and run

```bash
$ th train.lua -data_dir data/<new folder name>
```

You can play around with flags such a -rnn_size (defaults to 128; if you have more than a couple MB of data I would recommend a size of 300 or more), -num_layers (defaults to 2; you can try 3 or more) and dropout (try 0.5).

If you are running on CPU, training will take at least a few hours. After training terminates, go to char-rnn/cv and copy the checkpoint with the lowest loss to neural-chatbot/saved_policies. The naming scheme for the files is lm_lstm_epoch<epoch>_<loss>.t7. You can delete the rest of the checkpoints as they take up a lot of space.

##### "Loss is exploding!"

Do you have a relatively small dataset (< 2 MB?) Try the train from generic checkpoint method. Otherwise, you may be using too large of an rnn rize. If training goes on for a while hours before loss explodes, the saved checkpoints may be good enough to use. Generally, if the checkpoint loss is under 1.3 or so, the policy is likely decent.

#### Method 2 -- training from generic checkpoint

If you have a small amount of data, there may not be enough material for the bot to develop internal representations of English syntax without becoming overfitted. A more suitable method for small datasets is training a generic bot on a large dataset first, and then initiating a second network with the same weights and training on the small dataset. This way, the bot can retain the representations it developed from the large dataset while honing to behave more like the small dataset.

I have provided a generic bot trained from a 50 MB conversational dataset, located at neural-chatbot/saved_policies/generic.t7 and a bash script to automate the training process. Run the script like:

```bash
$ chmod +x train-from-checkpoint.sh
$ ./train-from-checkpoint.sh <new folder name>
```

After training terminates, go to char-rnn/cv and copy the checkpoint with the lowest loss neural-chatbot/saved_policies. The loss is the number in the filename following the underscore. You can delete the rest of the checkpoints as they take up a lot of space.

##### "Loss is exploding!"

Try altering the training rate. Often, lowering it helps with preventing loss explosion, although sometimes making it higher can solve the problem as well. 

Note: The train from checkpoint method is a lot faster than training from scratch, and it's pretty normal for training to terminate with loss exploding. As long as the best checkpoint loss score is under 1.3 or so, the policy should be decent.

### Running bots on messenger

Once you've copied your .t7 file to neural-chatbot/saved_policies, you are ready to put your bot online! (I would suggest renaming the .t7 file to something meaningful, especially if you are going to train multiple bots)

Run the autoresponder script:

```bash
$ python autoresponder.py <.t7 file name> --delay
```

For example, to use the generic bot:

```bash
$ python autoresponder.py generic.t7 --delay
``` 
You will be prompted for your Facebook username/email and password. When the prompt displays "Listening...", the chatbot is online!

##### Optional arguments:

--verbose: enables verbose logging during chatbot operation

--maxlength [int]: maximum character length of generated responses

--maxmessages [int]: maximum number of generated messages per incoming message

--threadlength [int]: maximum number of messages from each thread saved in in memory

--delay: insert realistic delay before sending messages. (recommended)

#### Blacklists

##### Thread blacklist:

Are there some group chats you're in that won't welcome bot spam every time anyone says anything? To prevent inevitable social ostracisation, add the IDs of any serious-business group chats you're in to neural-chatbot/blacklist/thread_blacklist. You can get the ID of any conversation by going to https://www.facebook.com/messages on desktop and opening the conversation. The format of the url is 

https://www.facebook.com/messages/t/<thread_id>

##### User blacklist:

Unfortunately, even though neural chatbots are trained on your data, they will not necessarily inherit your discretion. So it might be a good idea to blacklist employers, parents, romantic interests, and anyone else you don't want to risk unleashing a predictive text duplicate of yourself upon.

The user blacklist also comes in handy when there are multiple bots in a group chat. By blacklisting the IDs of all bots, you can prevent the bots from responding to each other and creating infinite spam.

Put user IDs you want to blacklist in neural-chatbot/blacklist/user_blacklist.

You can get the ID of any user by going to https://www.facebook.com/messages on desktop and opening your conversation with them. The format of the url will be

https://www.facebook.com/messages/t/<user_id>

If you want to blacklist someone but don't have a conversation with them, go to their page, right click on their profile picture and select "copy link location." The format of the link you will have copied will be 

https://www.facebook.com/profile/picture/view/?profile_id=<user_id>.
