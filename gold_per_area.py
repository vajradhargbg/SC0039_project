"""
This script is intended to read an imod logfile for immunoEM images modelled with IMOD and calculate gold/area.
Please install latest version of IMOD through this link:https://bio3d.colorado.edu/imod/
Follow istructions in readme.txt for modelling structures.
Email in case of questions or issues. Cheers! -Vaj

Author:  vajradhar acharya        vajradhar.shripad.acharya@gu.se
"""

#Before running this script, use areas.com to create areas.log file from your .mod file (see readme.txt for instructions)
#This script will create a directory called "temporary", which can be deleted afterwards
#If you wish to run the script again, delete the temporary folder and rename the .csv file or it will be overwritten
#Output is a csv called "gold_per_area.csv"

#name of the .log file generated by areas.com, in quotation marks: e.g. "areas.log"
log_file = "areas.log"

#Name of the structure of interest in the .mod file, in quotation.  e.g. "multivesicular bodies"
structure_name = "flagellum_area"

#Name of the scattered points object in .mod file used to model gold
gold_model_name = "Gold"

#Name of a second inner structure, that you wish to subtract from area of structure of interest
#e.g. if structure_name = "mitochondria", subtraction_structure_name may be "cristae"
#If you do not wish to subtract a structure, enter False (no quotations)
subtraction_structure_name = False

#If you wish to convert units from nm to um, nm_to_um = True (no quotations)
#ONLY do this if units in model header are in nm
#If you wish to retain units (such as um or pixels), nm_to_um = False .Output will be in whatever units the imod header are in
nm_to_um = True

#####################################################################################################################
### Do not edit below here                                                                                        ###
#####################################################################################################################
import os
import tempfile
import csv

def read_object(text):
    """
Parses the data in info file for a single object.
Input "text" is a list of strings, each string is a line in the original imod info file.  The list as a whole represents data
for 1 object.
Returns a dictionary containing info for that object.  Within the dictionary is a list of dictionaries,
containing information for each contour.

Currently I don't work with open objects so it is not super compatible with them.
"""
    
    ####Note to self: work on scattered points
    object_info = {}
    object_info["contours"] = []
    
    #FCombine all lines to make it easier to search for object type
    combined = '\n'.join(text)
   
    #Check if object is open or closed.  4th line will contain this info.
    if "closed" in combined:
        object_type = "closed"
    elif "open" in combined:
        object_type = "open"
    elif "scattered" in combined:
        object_type = "scattered_points"
    object_info["type"] = object_type
    
    #Import generic data
    for index in range(len(text)):
            if "NAME" in text[index]:
                split_name = text[index].split()
                name = ""
                for word in split_name[1:-1]:
                    name += word + " "
                name += split_name[-1]
                object_info["name"] = name
    
    #Import data for closed object
    if object_type == "closed":
        for index in range(len(text)):
            if "Total cylinder surface area" in text[index]:
                equal_index = text[index].find("=")
                total_area = float(text[index][equal_index + 2:-1])
                object_info["total cylinder surface area"] = total_area
        #import contour information
            if "CONTOUR" in text[index]:
                contour = {}
                hash_index = text[index].find("#")
                contour["contour number"] = text[index][hash_index + 1]
                #then split length, area, etc info
                split_list = text[index].split()
                split_index = tuple(enumerate(split_list))
                #add info for this contour
                for index, item in split_index:
                    if item == "points,":
                        contour["points"] = int(split_index[index - 1][1])
                    if item == "length":
                        contour["length"] = float(split_index[index + 2][1][:-1])
                    if item == "area":
                        contour["area"] = float(split_index[index + 2][1])
                        
                object_info["contours"].append(contour)

                
                
    #Import data for scattered point object
    if object_type == "scattered_points":
        for index in range(len(text)):
            if "CONTOUR" in text[index]:
                contour = {}
                hash_index = text[index].find("#")
                contour["contour number"] = text[index][hash_index + 1]
                #then split length, area, etc info
                split_list = text[index].split()
                split_index = tuple(enumerate(split_list))
                #add info for this contour
                for index, item in split_index:
                    if item == "points":
                        contour["points"] = int(split_index[index - 1][1])
                object_info["contours"].append(contour)
                
    return object_info

def read_stack_info(textfile):
    """
Input: text file
Output: returns list of lists, each list is an object in the text file, each element in that list is object_info
generated by read_object
"""
    object_list = []
    through_header = False
    
    with open(textfile, "r") as file:
        lines = file.readlines()
        for line in lines:
            if "OBJECT" in line:
                if through_header == True:
                    object_info = read_object(new_object)
                    object_list.append(object_info)
                new_object = []
                through_header = True
            if through_header == True:
                new_object.append(line)
            #Read the last object without getting to next object
            if line == lines[-1]:
                object_info = read_object(new_object)
                object_list.append(object_info)              
                
    return object_list

def read_areaslog(textfile):
    """
Reads areas.log file generated by areas.mod shell script (which separates imodinfo for each image in stack)
Input: areas.log text file
Output: A set of intermediate files in a scratch directory, each corresponds to a different image in the stack.
Returns the number in name of last file.
"""
    path = os.getcwd()
    new_path = path + "/temporary"
    os.mkdir(new_path)   
    
    #open areas log
    with open(textfile, "r") as read_file:
        count = 0
        lines = read_file.readlines()
        for line in lines:
            if "Entries to program clipmodel" in line:
                count += 1
            name = "temporary/Image{}.txt".format(count)
            #avoid writing blank lines or blank files
            if line.strip() != "":
                with open(name, "a") as new_file:
                    new_file.write(line)
    return count
            
def areaslog_to_stackinfo(textfile):
    """
Reads areas.log file using read_areaslog() to split data into separate files for each image in stack,
reads each of these files using read_stack_info(), returns a dictionary in which each key is "Image #"
and each value is the stackinfo list of lists for that image
"""
    stack_info = {}
    num_images = read_areaslog(textfile)
    for filenum in range(1, num_images + 1):
        name = "temporary/Image{}.txt".format(filenum)
        image = "image {}".format(filenum)
        stack_info[image] = read_stack_info(name)
    
    return stack_info
        
def total_gold_per_area(stack_info, structure_name, gold_name, subtraction_structure = False):
    """
Input:  Stack info from areaslog_to_stackinfo.  Name of the structure of interest in the model (string), Name of the
scattered points object that was used to model gold in the model for that specific structure.  Subtraction structure
is the name of a structure within a structure that you want to subtract from the area of structure_name, defaults to False
Returns:  Total gold in structure over all micrographs / total area of structure in all micrographs
"""
    structure_area = 0
    subtraction_area = 0
    gold_number = 0
    
    ###Note to self: make all of these smaller later so its easier to adapt program to other uses
    #iterate over info for each image
    for image, info in stack_info.items():
        #iterate over objects modeled
        for imod_object in info:
            #add area for structure of interest
            if imod_object["name"] == structure_name:
                #iterate over contours in object
                for contour in imod_object["contours"]:
                    structure_area += contour["area"]
            #add area of subtraction structure
            if subtraction_structure != False:
                if imod_object["name"] == subtraction_structure:
                    #iterate over contours in object
                    for contour in imod_object["contours"]:
                        subtraction_area += contour["area"]
            #count gold
            if imod_object["name"] == gold_name:
                #iterate over contours in object
                for contour in imod_object["contours"]:
                    gold_number += contour["points"]
    #final arithmetic
    gold_per_area = float(gold_number) / (structure_area - subtraction_area)
    return gold_per_area
                    
def gold_per_area_stack(stack_info, structure_name, gold_name, subtraction_structure = False):
    """
Input:  Stack info from areaslog_to_stackinfo.  Name of the structure of interest in the model (string), Name of the
scattered points object that was used to model gold in the model for that specific structure.  Subtraction structure
is the name of a structure within a structure that you want to subtract from the area of structure_name, defaults to False

Returns:  List of tuples.  Each tuple corresponds to data for one micrograph:
first element is micrograph number,
second area of structure of interest,
third number of gold on that structure,
fourth area of subtraction structure (or 0 if none),
fifth is gold divided by the difference of the structure and subtraction structure
"""
    ###Note to self:  check this works properly once you set it up to export csv!
    
    tuple_list = []
    count = 1
    #iterate over info for each image
    for image, info in stack_info.items():
        print("Calculating gold per area for image {}".format(count))
        #initialize values for image
        structure_area = 0
        subtraction_area = 0
        gold_number = 0
        #iterate over objects modeled
        for imod_object in info:
            #add area for structure of interest
            if imod_object["name"] == structure_name:
                #iterate over contours in object
                for contour in imod_object["contours"]:
                    structure_area += contour["area"]
             #add area of subtraction structure
            if subtraction_structure != False:
                if imod_object["name"] == subtraction_structure:
                    #iterate over contours in object
                    for contour in imod_object["contours"]:
                        subtraction_area += contour["area"]
            #count gold
            if imod_object["name"] == gold_name:
                #iterate over contours in object
                for contour in imod_object["contours"]:
                    gold_number += contour["points"]
        #calculate gold / area
        if (structure_area - subtraction_area) != 0:
            gold_per_area = float(gold_number) / (structure_area - subtraction_area)
        else:
            gold_per_area = 0
                
        #create tuple for data for this image
        image_data = (count, structure_area, gold_number, subtraction_area, gold_per_area)
        tuple_list.append(image_data)
        count += 1

    return tuple_list
           
def areas_log_to_gold_per_area_csv(text_file, structure_name, gold_name, subtraction_structure = False, nm_to_um = True):
    """
Takes an areas.log file generated by areas.mod and writes a .csv file with data table containing info about gold/area.
Inputs:
text_file: areas.log file generated by areas.mod
structure name: name of structure of interest in model (.mod file)
gold_name:  name of scattered points object in .mod file used to model gold in structure of interest
subtraction_structure:  if you wish to subtract area of an inner structure from the structure of interest before
calculating gold/area, input sructure of interest name here
nm_to_um:  assumes data is nm/pixel in model, change to false if this is not true
"""
    print("Importing data...")
    stack_info = areaslog_to_stackinfo(text_file)
    print("Calculating total gold per area...")
    total_gpa = total_gold_per_area(stack_info, structure_name, gold_name, subtraction_structure)
    individual_gpa_list = gold_per_area_stack(stack_info, structure_name, gold_name, subtraction_structure)
    
    #convert data from nm squared to um squared
    if nm_to_um == True:
        print("converting units from nm to um...")
        total_gpa = total_gpa * 1e6
        new_gpa_list = []
        for image_tuple in individual_gpa_list:
            new_structure_area = image_tuple[1] / 1e6
            new_subtraction_area = image_tuple[3] / 1e6
            new_gpa = image_tuple[4] * 1e6
            new_gpa_tuple = (image_tuple[0], new_structure_area, image_tuple[2], new_subtraction_area, new_gpa)
            new_gpa_list.append(new_gpa_tuple)
        individual_gpa_list = new_gpa_list
        
    #write file
    print("writing csv file...")
    filename = structure_name + "_gold_per_area.csv"
    with open(filename, "w", newline = '') as csvfile:
        writer = csv.writer(csvfile, delimiter= ",", quotechar= '|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Total gold per area", total_gpa])
        writer.writerow("")
        
        if subtraction_structure == False:
            writer.writerow(["Image number", structure_name, "number gold particles", "gold per area"])
            for image_data in individual_gpa_list:
                writer.writerow([image_data[0], image_data[1], image_data[2], image_data[4]])
        else:
            writer.writerow(["Image number", structure_name, "number gold particles", subtraction_structure, "gold per area"])
            for image_data in individual_gpa_list:
                writer.writerow([image_data[0], image_data[1], image_data[2], image_data[3], image_data[4]])
    print("Success!")
    

######Testing##########

### for read_object
# with open("closed_object.txt", "r") as file:
#     closed = file.readlines()
#     print(read_object(closed))
#     
# with open("scattered_object.txt", "r") as file:
#     scattered = file.readlines()
#     print(read_object(scattered))

###for read_stack_info
# read_stack = read_stack_info("data.txt")
# print(read_stack)
# print(read_stack[3])

###for read_areaslog
#log = read_areaslog("areas.log")
#print(log)

###for areaslog_to_stackinfo
#stackinfo = areaslog_to_stackinfo("areas.log")
#print(stackinfo)

###for total_gold_per_area
# stackinfo = areaslog_to_stackinfo("areas.log")
# #print(stackinfo)
# density = total_gold_per_area(stackinfo, "flagellum", "Gold in flagellum(mitochondria excluded)", "Mitochondria")
# print(density)
    
###for gold_per_area_stack
# stackinfo = areaslog_to_stackinfo("short_areas.log")
# print(stackinfo)
# density = gold_per_area_stack(stackinfo, "flagellum", "Gold in flagellum(mitochondria excluded)", "Mitochondria")
# print(density)

###Implementation
areas_log_to_gold_per_area_csv(log_file, structure_name, gold_model_name, subtraction_structure_name, nm_to_um)
