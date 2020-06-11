The Enron Sent Corpus v1.0
http://www.verbs.colorado.edu/enronsent
Compiled by Will Styler at the University of Colorado
Based on data from the Enron Email Dataset: http://www.cs.cmu.edu/~enron/ as of April, 2006


I. Introduction
***********************
This is a special preparation of a subset of the Enron Email Dataset designed specifically for use in Corpus Linguistics.  It contains 96,107 messages from the "Sent Mail" directories of all the users in the corpus.  Divided across 45 files, the Enron Sent corpus contains 2,205,910 lines and 13,810,266 words.  

II. Privacy Concerns
***********************
All messages in the Enron corpus were made public domain in 2003 by the United States Federal Energy Regulatory Commission during their investigation of Enron. The messages in the source data represent all of the email in the Enron Corporation's database, and not just those of the investigated individuals.  

Although many of the concerned individuals have already had their messages removed from the source data, it is important to remember that the vast majority of the people whose messages are in this corpus were likely not directly involved in the scandals. Please keep the privacy of these individuals in mind as you work with this corpus and the data it contains.

III. Contents
***********************
This file, README.txt
enronsent[0-44], the actual corpus data

IV. Corpus Preparation
***********************
In order to get the corpus in the the form you see it today, a number of steps were taken, some of which require explanation

The data in this corpus is a subset of the data from the Enron Data Set, as posted on http://www.cs.cmu.edu/~enron/ as of April 2006.  

When selecting a subset of the data, I elected to use the messages in the  /(username)/sent and /(username)/sent_items directories.  The goal for the project was to get a large corpus of human produced email, and I found that the sent and sent_items directory seemed to have the highest ratio of human produced text to automated mailings and junk mail ("spam").  In addition, these folders contained enough messages to form a sizable and sufficient corpus.  

Once the various messages were concatenated, I used an automated python script to clean the corpus.  This script searched for and removed as many of the following items as feasible:

* Message Headers and subject lines (please see the EnronSubjects file for the stripped subject lines)
* Quoted messages and Forwarded messages (I found that many messages were duplicated when replies and forwards were left in, due to the high frequency of messages sent within the corporation)
* HTML Messages (Frequently, they are tagged so heavily that they become unreadable and cause undue clutter in the corpus)
* "Subscribe to ____ Mail Service today!" messages
* Enron Specific formulaic signatures and letterheads

Over 2,500,000 lines of text were removed in this process.  Because of the sheer amount of data in the corpus, I chose to make the script more aggressive, and err to the side of losing human generated data.  

Note also that the corpus is not completely "clean".  There is no shortage of forwarded articles, automated messages, and probably errant headers that escaped the scrubber, and no attempt has been made to strip e-mail addresses, websites, phone numbers, and other personal information.

Finally, I split the file into 45 files containing approximately 50,000 lines of text each.


V. Statistics
***********************
The EnronSent corpus contains:
	96106 messages
	220,500 lines
	13,810,266 words
	88,171,505 characters

VI. Distribution
***********************
This preparation and all corpus data is in the public domain.  Feel free to use and redistribute as you see fit, although I ask that you include this README whenever distributing this preparation in full.

VII. Acknowledgments
***********************

Thanks to Martha Palmer, Mark Dredze, Travis Millburn, and the FERC for making this corpus preparation possible!
