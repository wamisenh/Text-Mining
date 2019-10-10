# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 13:23:48 2019

@author: USER
"""

'''
CURRENT ISSUES:

1. The program currently only queries for the first BillBoard 100 chart of 2008. 
The first idea I had in mind was hard coding a list of dates (i.e. Jan 1 2008, Jan 1 2009, Jan 1 2010, etc.)
but we can explore alternatives. Additionally, we can increase or decrease the frequency of queries between 2008-2018 
based on our preferences.

2. For songs with lyrics that are hyphenated (for example low-low-low-low-low-low-low in Apple Bottom Jeans T-Pain), the 
program as is concatenates the individual words together (lowlowlowlowlow). This happens in Healey's code, but I believe 
this could be resolved through a conditional statement and regular expressions.I'm in the process of figuring it out.

3. The resulting dataframe is not exactly transposed the same way as how Healey shows it in his site. 

4. I have yet to figure out how to apply any actual analytics to any of this.
 
'''
#import needed packages and software
import os
import billboard
import lyricsgenius
import nltk
from nltk import sent_tokenize, word_tokenize

'''Run these statements once if your program does not work and punkt or stopwords are in the error message:
#nltk.download('punkt')
#nltk.download('stopwords')'''

import gensim
import re
import string
import pandas as pd

#Getting the top 100 chart from Billboard for Jan 5th 2008 
#it's coded as Jan 1 2008, but the program finds the first chart available
chart = billboard.ChartData('hot-100', date= "2008-01-01")
#print(chart)

#Creating the Top-40 chart from the Billboard 100 chart of 2008
top_40 = chart[0:40]

#Creating a song object from the first entry on the top 100: song
song = top_40[0]

#Checking the title and artist attributes of the song object to make sure BillBoard api was correctly queried
print(song.title)
print(song.artist)

#Using the lyricgenius.Genius function from genius api to create a genius object in my environment: genius
#Use your own API Client key (the other thing that isn't the secret key and account number)
genius = lyricsgenius.Genius("BfyQYrtpFTv-Vof75MWQ1Uq8QK8zhQvtA-2OQubQYI5sTolrBcNSC64oTbYYIlkC")

#Use these statements to verify that your genius api stuff works in conjunction with the BillBoard query
song = genius.search_song(song.title, song.artist)
song.lyrics

#Initializing an empty list to store all of the lyrics from this top-40: list_o_lyrics
list_o_lyrics = []

#Getting all of the top 40 song lyrics and squishing them into list_o_lyrics list together: list_o_lyrics
for i in range(len(top_40)):
    song_frmchrt = top_40[i]
    song = genius.search_song(song_frmchrt.title, song_frmchrt.artist)
    list_o_lyrics.append(song.lyrics)
 
#Defining the punctuation elmininator and stuff
#Currently struggling with the fact that this doesn't correctly handle hyphenated strings
punc = re.compile( '[%s]' % re.escape( string.punctuation ) )
term_vec = [ ]

#Tokenize the words by subbing any punctuation with a null
for d in list_o_lyrics:
    d = d.lower()
    d = punc.sub( '', d )
    term_vec.append( word_tokenize( d ) )
    

# Remove stop words from individual songs (term_list) then store them back into term_vec
stop_words = nltk.corpus.stopwords.words( 'english' )

for i in range( 0, len( term_vec ) ):
    term_list = [ ]

    for term in term_vec[ i ]:
        if term not in stop_words:
            term_list.append( term )

    term_vec[ i ] = term_list
    

# Porter stem remaining terms
porter = nltk.stem.porter.PorterStemmer()

for i in range( 0, len( term_vec ) ):
    for j in range( 0, len( term_vec[ i ] ) ):
        term_vec[ i ][ j ] = porter.stem( term_vec[ i ][ j ] )

        
        
#Making a rudimentary chart to look at the frequencies for the first song (should be Apple Bottom Jeans): counted_terms_df
counted_terms = [[x,term_vec[0].count(x)] for x in set(term_vec[0])]
counted_terms_df = pd.DataFrame(counted_terms)
counted_terms_df = counted_terms_df.sort_values(by = 1,ascending=False)
print(counted_terms_df)

'''
If the code runs successfully, you should get this output: a rudimentary dataframe containing stop word cleaned and porter 
stemmed data frame for Apple Bottom Jeans by T-Pain ft. Flo-Rida

                            0   1
26                        flo  20
30                        hit  16
45                     shawti  14
73                        got  12
62                       know   9
34                        fur   8
1    lowlowlowlowlowlowlowlow   8
131                      next   8
117                     strap   8
169                     thing   8
129                     tpain   5
141                      like   5
101                        im   5
39                       gave   5
70                       jean   5
53                        let   5
126                       big   4
82                      booti   4
143                     sweat   4
134                     stack   4
29                       boot   4
71                       appl   4
54                        ayi   4
114                    lookin   4
31                       pant   4
125                    around   4
144                     smack   4
87                       rida   4
167                      aint   4
98                       turn   4
..                        ...  ..
97                     sexual   1
96                        fli   1
94                       told   1
92                    problem   1
91                pornographi   1
90                      woman   1
88                       cake   1
85                    wouldnt   1
84                       yeah   1
81                       rock   1
80                      threw   1
79                     showin   1
77                       band   1
75                       full   1
51                    toaster   1
74                     rubber   1
72                       bank   1
68                      rosay   1
67                     poster   1
66                       babi   1
65                    maybach   1
64                    control   1
63                       moan   1
61                        leg   1
60                       girl   1
58                        pop   1
56                       mama   1
55                      sorri   1
52                       took   1
86                   birthday   1

[173 rows x 2 columns]

'''