# AV_Workflows

These workflows contain the code to: 
Strip XML files from the MVR (My Virtual Rig) container package.

- This allows for the transformation of the text document into formatted CSV or Pandas Dataframe.

- DB creation allows for the initialisation of a SQLite DB in order to join and output lighting data such as wattage, weight.

- The join is based off the Manufacturer Name Column where a regular expression should be used to capture same fixture interations i.e light, light1, light2.


