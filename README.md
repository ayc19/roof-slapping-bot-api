# Roof Slapping Bot API

This is the roof slapping bot (RSB) api. It makes use of the conceptNet api and Flask. Given an input word, conceptNet will grab all other words/phrases that relate to the input word and their relationships. For example, 'dog' has a few possibilities. some words/phrases that could pop up are 'bark' with the relationship 'CapableOf' or 'companionship' with the relationship 'Desires'. 

For this project, I aim to imitate and add on to the Roof slapping twitter bot found [here](https://twitter.com/roofslappingbot?lang=en). Currently the Twitter RSB has a predefined list of hundreds of words and phrases that model the "AtLocation" relationship. This model allows for easy use of the roof slapping car salesman meme which takes the form of

**Slaps roof of ___* *  "This bad boy can fit so many ___"

The twitter bot then randomly selects a line from the predetermined list and then generates a tweet for it.

To improve on this, I wanted to make a website where a use could type in a word and then get a randomly generated roof slapping text. In addition, I added the relationship of "CapableOf" in addition to "AtLocation" since it seemed appropriate for the theme of a car salesman. 

# To use
Currently the API is up and running via heroku at this link:

[https://roof-slapping-bot.herokuapp.com/](https://roof-slapping-bot.herokuapp.com/)

for whatever noun you want, just type in the link above followed by word/\<your word\>

and you'll get a json object with two fields: 'text' and 'word'. Word is the word you typed in and text is a randomly selected text that follows the roof slapping meme. For example if you typed in 'dog' you may get this

```
{
  "text": "*Slaps roof of park* This bad boy can fit so many dogs in it.", 
  "word": "dog"
}

```

If no text is found you'll get a message saying "No results: try again"




# To run locally

```
source .env/bin/activate

pip3 install requirements.txt

export FLASK_APP=app.py

export FLASK_DEBUG=1 

flask run

# When done deactivate the virtual environment
deactivate

```
