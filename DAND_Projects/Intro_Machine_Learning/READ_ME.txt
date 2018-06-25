This project was developed using Python 2.7.

Code in poi_id.py instantiates the classifier and features and dumps them, as expected in tester.py. 
It does not run the code doing the grid searches, nor the code for recurvsive feature eliminination, in order to save running time for poi_id.py. 

Changes from first submission:  
poi_id.py: Added in the outlier detection/removal
poi_id.py: Used the features from recursive feature elimination found in the runs on TestRunsTuning.ipynb
<NOTE: the grader said that my 1st submission did not have the feature selection stuff in the poi_id.py, but it absolutely did have it with the SelectFromModel using L1 penalty based feature selection which was used in the pipeline in poi_id.py. I don't understand the reasoning for not saying there was no feature selection in poi_id.py.>
Machine_Learning_QandAs.docx: Updated the final recall and precision scores when using the feature set from recursive feature elimination.

Machine_Learning_QandAs.docx contains the answers to the 6 Enron Submission Free-Response Questions

TestRunsTuning.ipynb has the multiple tests runs with grid search and manual tuning to get optimal algorithm performance.  It is a reference document included mostly for reproducibility purposes, as well as showing some of the trial and error process;  it is referred to several times in Machine_Learning_QandAs.docx answers, but it is by no means necessary to go through the entire .ipynb file in order to understand the logic and decision making going into the project.

EnronEmailSearches.txt shows the text keyword searches (grep commands) through the email text, attempting to find anything interesting in terms of known phrases associated with some Enron fraud schemes; this was done to get a measure of involvement in fraud independent of the already given "poi" tags.  However, nothing interesting was found after searching through every inbox for the key phrases, and so this document can be skipped entirely.


References:

SelectFromModel tips:
http://scikit-learn.org/stable/modules/feature_selection.html
https://datascience.stackexchange.com/questions/14198/feature-selection-with-l1-regularization-on-sklearns-logisticregression
https://stackoverflow.com/questions/35376293/extracting-selected-feature-names-from-scikit-pipeline

Enron notes:
https://web.archive.org/web/20041125110444/http://www.chron.com/content/chronicle/special/01/enron/background/glossary/glossary.html
https://www.nytimes.com/2002/05/08/business/enron-s-many-strands-strategies-enron-got-california-buy-power-it-didn-t-need.html


I hereby confirm that this submission is my work. I have cited above the origins of any parts of the submission that were taken from Websites, books, forums, blog posts, github repositories, etc.




