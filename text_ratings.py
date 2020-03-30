# This codes loops through rows of texts files and rates the text based on Flesch Kincaid Readability Index, Coleman Liau Index etc. 
# It also provides other metrics such as number of complex words used etc. 

import textstat
import pandas as pd
import readability

twg_full = pd.read_csv('twg1.csv')
twg = pd.Series(twg_full['body'])

# clean text in twg

# Remove NaNs from dataset
twg = twg.dropna()

def readability_stats(text):
    stats = readability.getmeasures(text, lang='en')
    a = stats['sentence info']['words']
    b = stats['sentence info']['syll_per_word']
    c = stats['sentence info']['syllables']
    d = stats['sentence info']['long_words']
    e = stats['sentence info']['complex_words']
    return a, b, c, d, e

read_stats = twg.apply(readability_stats)
read_stats_list = []
for i in read_stats:
    read_stats_list.append(i)


read_stats_df = pd.DataFrame(read_stats_list)
# Add columns to the df
read_stats_df.columns = ['Wordcount', 'Syllable per word', 'Syllables', 'Long words', 'Complex words']

# Define scoring function
def score(text):
    a = textstat.flesch_reading_ease(text)
    b = textstat.flesch_kincaid_grade(text)
    c = textstat.gunning_fog(text)
    d = textstat.smog_index(text)
    e = textstat.coleman_liau_index(text)
    f = textstat.automated_readability_index(text)
    return a, b, c, d, e, f

# The score() function will return a Series (98, 92..) etc. 
# Note the scores need to be added to a list, and then to a DataFrame to split them
# into columns (otherwise, the scores will just exist in one column in the DataFrame)

scores = twg.apply(score)
scores_list = []
for i in scores:
  scores_list.append(i)

scores_df = pd.DataFrame(scores_list)
# Add columns to the to the df
scores_df.columns = ['Flesch Kincaid Reading Ease', 'Flesch Kincaid Grade Level',
             'Gunning Fog Score', 'SMOG Index', 'Coleman Liau Index',
             'Automated Readability Index']

# Add titles
# Get titles from raw file
titles = twg_full['title']
# titles_list = [] 
# for i in titles:
#   titles_list.append(i)

titles = pd.DataFrame(titles)
titles.columns = ['Title']
final_score = pd.concat([titles, read_stats_df, scores_df], axis = 1 )
final_score

# merge df_cd = pd.merge(df_SN7577i_c, df_SN7577i_d, how='inner', left_on = 'Id', right_on = 'Id')

