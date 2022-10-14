These scripts are to analyze the data from an immuno-gold experiment that has been modeled in imod and return a csv file that contains gold particles/area of a certain structure.  You will need python 3 installed.

1)
All images must have been taken at the same magnification, and then combined into a stack for modeling of structures in imod.  Create a scattered points object for modeling to gold that labels the structure of interest, and a closed structure for modeling the structure of interest (open structures cannot be analyzed by this script).  If you wish, a third structure (closed) can be used, if you wish to subtract area from within your structure of interest.  More things can be modeled, but to get the gold/area of multiple structures you will have to re run this from step 3 onwards for each one.

2)
Copy areas.com and gold_per_area.py to the folder containing your .mod model file.  
areas.com separates your imod info for each image in the stack.  Edit this as a text file, change the number after range to the number of images in your stack minus 1.  Then change model_file_here.mod to the name of your .mod file (but leave temp.mod as is)
Run areas.com with this command in the terminal:

subm areas.com

Result will be called areas.log.  If this was created, proceed to step 3.

3)
Now edit gold_per_area.py as a text file.  There are instructions in the file on how to do this.  Basically, you are inputing the names of your structures in the .mod file.  Run this with this command in the terminal:

python gold_per_area.py

This will create a temporary folder which can be deleted and a csv file with you output.

4)
If you wish to analyze another structure in your model delete the temporary folder, rename the csv file from the last structure, and repeat step 3 for the new structure.

Cheers,
Vaj
