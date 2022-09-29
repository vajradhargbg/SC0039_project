# SC0039_project

##Goal
The goal of this project is to calculate distribution of gold beads in an immuno electron microscopy(ImmunoEM) image. The script will interface with a software package called IMOD that is used to model the structures in the immunoEM image and calculate gold per unit area.

##Considerations
The modelling of the structures of interest and the gold have to be done in advance. These models then need to be run through an IMOD com script to calculate the modelled area and number of modelled gold beads. Running the com scipt will output a logfile with the area that this script will read. Make sure that the com script and the logfile are saved in the directory you are working in. This script is designed specifically for the linux environment as IMOD is a linux only software package.

##What the script does
The script reads the IMOD logfile generated that has information about calculated area of interest and the amount of gold beads modeled in said area. It then sorts this data, i.e. calculate gold per unit area for the area of interest and outputs the information in a readable .csv file. This .csv file can then be used to make graphs/plots for publication.
