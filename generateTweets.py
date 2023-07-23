import csv

import openai
import json
import configparser

accountsFile = 'accounts.ini'
csvFile = "tweets.csv"

def writeToCSV(tweets):
    with open(csvFile, mode='a', newline='') as file:
        writer = csv.writer(file)
        for item in tweets:
            writer.writerow([item])

if __name__ == '__main__':
    message = [
        {"role":"system","content":"You are requested to generate tweets for a twitter campaign. The tweets are supposed to "
                                   "be seperated by a #. You should not print or output anything extra. "
                                   "The tweets should not be more than 15 words"}
    ]
    with open('chatGPTKeys.json', 'r') as json_file:
        json_data = json_file.read()

    chatGPTKeys = json.loads(json_data)
    openai.api_key = chatGPTKeys["key"]
    message.append({"role":"user", "content":"I am resident of Odisha. Aam Aadmi Party Odisha is going to run an electricity "
                                             "campaign in Odisha to demand free electricity for upto 200 units like how AAP "
                                             "did in Delhi and Punjab. Unlike Delhi which does not produces electricity "
                                             "(still provides 200 units of free electricity), Odisha is a producer of electricity. "
                                             "This campaign will be on twitter. For this I need nearly 1000 of written "
                                             "texts for posting on twitter. Can you generate just 10 tweets"})
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=message)
    reply = chat.choices[0].message.content
    message.append({"role":"assistant","content":reply})
    tweets = reply.split("\n\n")
    finalTweets = []
    config = configparser.ConfigParser()
    config.read(accountsFile)
    sections = config.sections()
    writeToCSV(tweets)
    tweetsPerSection = 30

    for _ in range(len(sections)):
        totalChats = tweetsPerSection // 10
        for _ in range(totalChats):
            message.append({"role":"user", "content":"please generate 10 more tweets"})
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message)
            reply = chat.choices[0].message.content
            message.append({"role": "assistant", "content": reply})
            tweets = reply.split("\n\n")
            writeToCSV(tweets)






