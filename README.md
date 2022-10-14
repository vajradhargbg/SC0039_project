# SC0039_project

## Considerations
Read the readme.txt file for instructions on modelling the data.
In this case, for the project, the script is already modified for the test dataset that I have included. Please run the script as is with the log file in the directory in which the log file is saved for the output.
The image stack can be found here: https://gunet-my.sharepoint.com/:u:/g/personal/vajradhar_shripad_acharya_gu_se/ESWs9BLAARtKsTzTDIZ9ZuoBBk2gYd-KX2D-EKEU6intww?e=K5ORh2
The model file is in this repo with the extension .mod
If you wish to look at the images and the model, you can download the IMOD package here:https://bio3d.colorado.edu/imod/
Open the .mrc stack with the images using the command: imod filename.mrc from the command line.
To open the model, go to File-Open and select the .mod file

## Goal
The goal of this project is to calculate distribution of gold beads in an immuno electron microscopy(ImmunoEM) image. The script will interface with a log file from the software package called IMOD that is used to model the structures in the immunoEM image and calculate gold per unit area.

## Prerequisites
The modelling of the structures of interest and the gold have to be done in advance. These models then need to be run through an IMOD com script to calculate the modelled area and number of modelled gold beads. Running the com scipt will output a logfile with the area that this script will read. Make sure that the com script and the logfile are saved in the directory you are working in. This script is tested with imod in Linux and MacOS/ Mileage with Windows may vary.

## What the script does
The script reads the IMOD logfile generated that has information about calculated area of interest and the amount of gold beads modeled in said area. It then sorts this data, i.e. calculate gold per unit area for the area of interest and outputs the information in a readable .csv file. This .csv file can then be used to make graphs/plots for publication.
