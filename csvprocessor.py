#####################################################################
## needed to integrate all the subcsv and to select 20 most important words in the csv.
## To get the 20 most important words, we get their weighted frequency
## The algorithm we use contains 2 steps:
## 1) we look the words (by columns) and get the average number of each word,
## which will be used to minus word count of this word in each website
## = freq(this word) - average(freq(this word))
## 2) we calculate the relative frequency of one word occuring in one website,
## =freq(this word)/max(freq in the website)
## Finally, we convert each count into (1) * (2)
#####################################################################


import pandas as pd
import numpy as np
import csv
import re
import nltk

def csv_integrate(file_list):
    csv_list = []
    for file in file_list:
        f = pd.read_csv(file, header=0, names=None).transpose()
        f.rename(columns=f.iloc[0], inplace=True)
        f.drop(f.index[0], inplace=True)
        f.rename({"WC": file}, axis='index', inplace=True)
        csv_list.append(f)
    csv_list = pd.concat(csv_list)
    return csv_list


def freq(csv_list):
    # first we get the inverse of relative frequency of one word among all websites
    # The more websites containing this word, the less important this word is becoming

    csv_list.fillna(float(0), inplace=True)
    num_website = len(csv_list)
    freq_among_web_list = []
    for i in range(len(csv_list)):
        max_freq = np.max(csv_list.iloc[i])
        for j in range(len(csv_list.columns)):
            aver = np.average(csv_list[csv_list.columns[j]])

            # in order to make sure the final relative frequency is similar in scale to our orignial data,
            csv_list.iloc[i, j] = ((csv_list.iloc[i, j] / max_freq) * (csv_list.iloc[i, j] - aver))

    return csv_list


# Here is the function to choose 20 most important / shining words from all the dataset!
# The idea is summing up the weights of each words and make a dictionary
# Sort the dictionary from greatest value to the lowest and get the first 20 items!
# get the 1st element (word) in each tuple in the list to make a new list, and get those columns from the dataset!
def word_choose(csv_file):
    word_list = []
    weight_list = []
    no_use_list = ['endnoindex', 'noindex', 'university', 'ub', 'rochester', 'department', 'vanderbilt',
                   'buffalo', 'stanford', 'hashimoto', 'tatsunori', 'show', 'submenu', 'mit', 'professor', 'faculty',
                   'history', 'physics', 'computer']
    for word in csv_file.columns:
        if (len(str(word)) != 1) and word not in no_use_list:
            word_list.append(word)
            weight_list.append(np.sum(csv_file[word]))
    dictionary = {word_list[i]: weight_list[i] for i in range(len(word_list))}
    dictionary = sorted(dictionary.items(), key=lambda item:item[1], reverse=True)
    dictionary = dictionary[:20]
    word_to_use = [x[0] for x in dictionary]
    csv_file = csv_file[word_to_use]
    return csv_file

def convertCSV(new_D, string):
    header = ["Noun", "WC"]
    with open(string, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)  # write header in first row
        for row in new_D.items():
            writer.writerow(row)  # write each word respectively






