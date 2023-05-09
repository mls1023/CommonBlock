The Common Block Rent Sharing Website is intended to facilitate convenient rent sharing among NYU students. The system will include the following functions:
A repository of apartments displayed on a map
A repository of user profiles
The ability to create groups of interest between students and for certain apartments. 
The ability to create groups dedicated to the buying/selling of second-hand furniture. 
A review system for both students and apartments. 


HOW TO USE:
Download the Common Block repo/folder. 
Initialize your mysql database connection with the settings in config.py file.
Either create the tables manually or uncomment the db.create_all() lines in run.py.
Insert information into the tables using the MYSQL Local ssion file provided(specifically apartments)
Then while in the CommonBlock folder, run 'python run.py'
The Insert apartments block insets 456 apartments into the databse table, but if you wish to create more:
Run the script in the apartment_scripts folder on a json file containing apartment data.
The json file give in the folder was used to create the 456 entries, acts as an example.
You may need to edit mysql settings in the .vscode folder as well.