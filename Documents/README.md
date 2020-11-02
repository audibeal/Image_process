# Execution
**[WARNING]**: These scripts have been created and tested on GNU/LINUX. I cannot guarantee that they will work flawlessly on Windows or Mac.

To run these two scripts you need to have Python 3 installed on your system.
Then you just open a terminal, go where these script are located and write ```python RocheDB.py``` or ```python3 CsvLEANER.py``` depending on your system.

# CsvLEANER.py

CsvLEANER.py ask for the path of a directory containing CSV files and then proceed to remove all unneeded data from these files.
(Columns XcoinHG1, YcoinHG1, XcoinHD2... As well as all the columns after the objects' coordinates).

## Requirement and comments
Your CSV files' names **must follow** this pattern (the name of the file is used to identify the modifications to do):
*numberObjectThrown_objectName_orderedOrNot_slopeMaterial_arrivalMaterial_angleOfTheSlope*

Your CSV files must have the same organisation as the ones in ```DATA/sorted_raw_data```.

If the number of objects thrown in your CSV is not in the following list: 14, 28, 40, 42; You will need to add a condition in CsvLEANER.py and define an array of columns to ignore and the number of the last column to accept in your CSV files.
Even if you have no experience with Python this should be fairly easy, you can try to understand better by looking at the already existing conditions and their related CSV files.

The clean CSV files will be saved in the directory in which you execute the script.

# RocheDB.py
RocheDB.py creates or updates the two tables in the database.
* The table **data**: This is the table that contains all the coordinates of the different objects as well as all the information relative to the setups, you can create this table by choosing the option *0*. 
The .CSV files you will feed to the script *must* have been cleaned by ```CsvLEANER.py``` beforehand.
Same thing if you want to update the table of an existing database, except you will need to choose the option *1*.
* The table **stat**: This table contains a lot of already computed statistical information, the .CSV files required to create this table can be created by launching the following script ```statistical_analysis/4_stat_table_data.R```.
To be able to launch this script you need to have already created a database with the data table.
To create the table you will need to choose the option *2* and to update it the option *3*.

## Requirement and comments
Your CSV files' names **must follow** this pattern (the name of the file is used to identify the modifications to do):
*numberObjectThrown_objectName_orderedOrNot_slopeMaterial_arrivalMaterial_angleOfTheSlope*

If your data as been collected using new objects, new materials for the slope, new materials for the arrival, a number of objects or an angle that has not been used before you must input these new information in ```filenameSyntax.json```. 
This JSON file is used to make sure that there are no mistakes in the CSV files' names, but also to associate a number to each kind of objects and material in the DB.

It is important to understand that you can always give path to the script, for example, if you execute the script from ```DB_Creator``` and your database is located at ```DATA/data_base```, when the script asks you for the *name* of the database you are expected to give: ```../DATA/data_base/chute_de_bloc.sqlite```.

The script will also create (or update if you have already created a DB) a file called ```context.txt```, where you can see which filename is linked to which setup number.

The SQLite DB and the context.txt file will be saved in the directory in which you execute the script.
For the most part the script should guide you through its use.