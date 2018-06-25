import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import codecs
import datetime
from collections import defaultdict


# Code to more efficiently parse the OSM xml and return a list of XML elements
def get_element(osm_file, tags=('node', 'way', 'relation')):
    #Yield element if it is the right type of tag

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

# Get a subsample of the OSM xml, since the OSM file is very large.  Parse and get every k'th element
# (here, k set to 10) and write this to a sample OSM xml file.
def get_sample_osm(file_to_sample):    
    SAMPLE_FILE = "sample11.osm"
    k = 10 # Parameter: take every k-th top level element
    
    with open(SAMPLE_FILE, 'w') as output:
        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<osm>\n  ')
    
        # Write every kth top level element
        for i, element in enumerate(get_element(file_to_sample)):
            if i % k == 0:
                output.write(str(ET.tostring(element), encoding='utf-8'))
        output.write('</osm>')
    
# Dictionary of terms to replace, i.e. "bbq" --> "barbecue"     
cuisine_dict = {
    "bbq": "barbecue",
    "bar&grill": "grill",
    "donuts": "donut",
    "bagels": "bagel",
    "steak": "steak_house",
    "burgers": "burger",
    "salads": "salad",
    "sandwiches": "sandwich",
    "sandwhiches": "sandwich",
    "sandwhich": "sandwich",
    "hot_dogs": "hot_dog",
    "chicago_dogs": "hot_dog",
    "coffee": "coffee_shop",
    "texmex": "tex_mex",
    "roast_beel": "roast_beef",
    "puertorican": "puerto_rican",
    "jewish_deli": "jewish",
    "fish_tacos": "tacos",
    "juice_bar": "juice",
    "mexcian_food": "mexican",
    "mexican_food": "mexican",
    "wrap": "wraps",
    "french_fries": "fries",
    "drive_thru_coffee": "coffee_shop",
    "healthy_cuisine_-_greek": "greek",
    "tailand": "thai",
    "thailand": "thai"
}

# These are cuisine terms we will throw out and not allow, based on the large-ish sample of values seen.
# NOTE the some terms - "vegan", "vegetarian", "drive_through" - should be included in other tags
#   besides cuisine tags, and the code detects them and adds the appropriate sub-tags later.
disallowed = ["", "food", "vegan", "vegetarian", "vegetarian_and_vegan", "mon", "ret",
              "lunch", "diner", "dinner", "bar", "pub", "drive_through"]

# strips the string of whitespace and leading underscore, and converts to lower-case
# i.e. "_pizza" --> "pizza";  "Fries " --> "fries"
def str_space_undersc_lower(string):
    if string == "" or string == None:
        return ""
    string = string.strip()[1:] if string.strip()[0] == '_' else string.strip()
    return string.lower()

# Replaces spaces between cuisine terms with an underscore
# i.e. "coffee shop" --> "coffee_shop"
def repl_space(string):
    return "_".join(string.split())

# splits strings on comma and/or semicolon
def spl(string):
    return re.split("[,;]", string)

# Replace string with its substitute in the cuisine dictionary, if it is in the dict
# If its not in dict and its not in the disallowed list and if it is 3+ characters long,
#   then use it as is.
def dict_lookup(string):
    if string in cuisine_dict:
        return cuisine_dict[string]
    elif string in disallowed:
        return None
    elif len(string) < 3:
        return None
    else:
        return string

# check if have text indicating they are using text for a drive through for a cuisine
def has_drive_through_text(text):
    lower_text = text.lower()
    return ("drive_through" in lower_text) or ("drivethrough" in lower_text)

# check if have text for vegan in cuisine text
def has_vegan_text(text):
    lower_text = text.lower()
    return "vegan" in lower_text

# check if have text for vegetarian in cuisine text
def has_vegetarian_text(text):
    lower_text = text.lower()
    return "vegetarian" in lower_text

# call dict_lookup after cleaning with str_space_undersc_lower and then repl_space
def process(string):
    return dict_lookup(repl_space(str_space_undersc_lower(string)))

# clean up each element after splitting them, and then rejoin
def shape_cuisine_element(cuisine_str):
    return ";".join(filter(None, map(process, re.split('[,;]', cuisine_str))))

# Do the audit.  Parse, clean up and see how many elements of each cuisine type
def do_audit(file):
    
    cuisine_types = defaultdict(int)
    print(str(datetime.datetime.now()))

    with codecs.open(file, 'r', encoding="utf8") as f:
        
        context = ET.iterparse(f, events=('end',))
        _, root = next(context)
        for event, elem in context:            
            if elem.tag == "node" or elem.tag == "way":           
                cuiss = elem.findall("./tag/[@k='cuisine']")
                for cuis in cuiss:                
                    cuisine_val = cuis.get('v')
                    cleaned_val = shape_cuisine_element(cuisine_val)
                    if cleaned_val != None and cleaned_val != "":
                        cuisine_types[cleaned_val] += 1                   
            root.clear()
               
        print("\n\n*** Cuisine types:") 
        for key in cuisine_types:
            print("{}: {}".format(key,cuisine_types[key]))
                 
    print("\n")
    print(str(datetime.datetime.now()))
