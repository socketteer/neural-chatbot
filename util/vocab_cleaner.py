import re

def filter_non_ascii(string):
    string = re.sub('‘', '\'', string)
    string = re.sub('’', '\'', string)
    string = re.sub('“', '\"', string)
    string = re.sub('”', '\"', string)
    string = re.sub('…', '...', string)
    string = re.sub('–', '-', string)
    string = re.sub('☻', ':)', string)
    string = re.sub('😞', ':(', string)
    string = re.sub('😊', ':)', string)
    string = re.sub('❤', '<3', string)
    string = re.sub('😢', ':\'(', string)
    string = re.sub(r'[^\x00-\x7F]+', ' ', string) #replaces any other non-ascii characters with space
    return string
