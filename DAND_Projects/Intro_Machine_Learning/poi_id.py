#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectFromModel


### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file) 
    

# Remove outliers
possible_outliers = []
for emp, emp_dict in data_dict.items():
    num_parts_of_name = len(emp.split())
    if num_parts_of_name < 2 or num_parts_of_name > 4:
        possible_outliers.append(emp)
        print("# of parts in name: {}, name: {}".format(num_parts_of_name, emp))
    num_nonzero_fields = 0
    for key, val in emp_dict.items():
        if val != 0 and val != 'NaN' and val != False and val != True: # we ignore poi field, as everyone has True or False
            num_nonzero_fields += 1
    if num_nonzero_fields < 2:
        possible_outliers.append(emp)
        print("# of nonzero fields: {}, name: {}".format(num_nonzero_fields, emp))
"""
# of nonzero fields: 0, name: LOCKHART EUGENE E
# of parts in name: 6, name: THE TRAVEL AGENCY IN THE PARK
# of parts in name: 1, name: TOTAL
"""
# after verifying the above candidate outliers above in comments should be removed, we remove them
for outlier in possible_outliers:
    data_dict.pop(outlier)

    
#   Some preprocessing, and adding in and removing a feature
#   We iterate through dict keys to change 'NaN's to 0, to include has_email, a new feature/key in the dict
# which notes whether or not an individual has an email address, we remove the feature/key email_address,
# and we convert the Boolean for poi to integers 0 or 1.
for emp, emp_dict in data_dict.items():    
    has_email = 1
    is_poi = 0
    
    for key, val in emp_dict.items():
        if key == 'email_address' and val == 'NaN':
            has_email = 0
        elif key == 'poi' and val == True:
            is_poi = 1
        elif val == 'NaN':
            emp_dict[key] = 0
        
    emp_dict['has_email'] = has_email
    emp_dict['poi'] = is_poi
    emp_dict.pop('email_address', 0)
 

"""
We ran recursive feature elimination using L1 penalty in TestRunsTuning.ipynb
This was ran using an intial features list of every feature
We used recall for the scoring because:
    1) it worked well in improving scores for recall and precision
    2) using F1 or precision left only a few features
See TestRunsTuning.ipynb for more details, including results using precision and F1 for scoring

CODE IS SHOWN BELOW RATHER THAN RUN IN ORDER TO SAVE RUNNING TIME FOR poi_id.py

selector = RFECV(estimator, step=1, cv=sss(1000), scoring="recall")
selector = selector.fit(features, labels)
l1_penalty_features_list = list(np.array(features_list)[1:][selector.support_])
# this adds all features with rank = 1 from selector.ranking_
l1_penalty_features_list.sort()
l1_penalty_features_list = ["poi"] + l1_penalty_features_list
# append the next feature that would have been selected by RFECV, with rank = 2
# by doing this, tests for recall and precision improved
# adding in feature with rank = 3 did not make improvements in recall or precision
l1_penalty_features_list.append('expenses')  
features_list = l1_penalty_features_list
"""
# NOTE THAT THE NEW FEATURE, has_email, DID NOT MAKE THE CUT from recursive feature elimination
features_list = ['poi', 
                 'director_fees', 
                 'from_messages', 
                 'from_poi_to_this_person', 
                 'from_this_person_to_poi', 
                 'restricted_stock_deferred', 
                 'shared_receipt_with_poi', 
                 'to_messages', 
                 'expenses']


#   Showing a few overview stats
#   Note that the number of POIs without email is 0, hence the reason we made a feature for this
# since this should have some predictive value
pois = [ indiv for indiv in data_dict.keys() if data_dict[indiv]['poi'] == 1 ]
pois_without_email = [ indiv for indiv in data_dict.keys() if data_dict[indiv]['poi'] == 1 and 
                   data_dict[indiv]['has_email'] == 0 ]
num_features = len(data_dict['LAY KENNETH L'].keys())
print("Dataset has {} individuals".format(len(data_dict)))
print("Number of POIs: {}".format(len(pois)))
print("Number of POIs without email: {}".format(len(pois_without_email)))
# we added a feature, has_email, and removed a feature, email_address, so we have same # features as before
print("Number of features: {}".format(num_features)) # we added a feature and removed a feature
 
   
my_dataset = data_dict
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)


#   For the multipe runs and grid searches tuning algorithms and trying different feature selection techniques,
# see TestRunsTuning.ipynb
#   We used AdaBoost algorithm as the classifier with SelectFromModel using logistic regression
# with L1 penalty for feature selection in pipeline, to get optimal precision and recall levels.
adab_clf = AdaBoostClassifier(learning_rate=0.45, n_estimators=18, random_state=42)
select = SelectFromModel(estimator=
                                  LogisticRegression(class_weight='balanced', penalty='l1', random_state=42, tol=0.0001))
clf = Pipeline([('select', select), ('clf', adab_clf)])

dump_classifier_and_data(clf, my_dataset, features_list)