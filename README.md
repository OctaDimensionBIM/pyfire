# pyfire
1. Pyrevit based Fire fighting calcuations application
2. First of all you need to install pyrevit.
3. then make a folder in C:\Program Files\pyRevit-Master\extensions named pyFire.extension then inside the folder make folder pyFire.tab then inside the folder make folder No Of Sprinklers.panel then inside this folder make two folders ( NOS.pushbutton and PutSprinklers.pushbutton). Inside NOS.pushbutton put NOS_script.py and in the folder PutSprinklers.pushbutton put PutSprinklers_script.py
5. go to revit then pyrevit tab then on extreme left there is a refresh button click on it. you will get two icons in a pyfire tab
6. Now make a shared parameter named HazardType and another shared parameter named NOS. Associate them with MEP spaces. HazardType should be Text and NOS should be intiger.
7. Specify Hazard type of each space as Light Oridnary or Extra.
8. Click on NOS pushbutton. It will give Number of sprinklers in each MEP space.
9. Now click on PutSprinklers push button. It will put required number of sprinklers in each space as mentioned in NOS.
