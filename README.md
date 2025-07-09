# Conflict Checker

Conflict Checker is a Python script that checks for conflicts in paper assignments done via [CMT](https://cmt3.research.microsoft.com/). It checks for: 

-  authors, reviewers, or metareviewes from the same institution
-  authors, reviewers, or metareviewes with the same email address domain
-  assignments with more than *max_reviewers_from_same_country* reviewer/metareviewer from the same country

## Input Files 

As inputs, the script reads 3 spreadsheets: 

- **Papers.xlsx**, which can be obtained directly from [CMT](https://cmt3.research.microsoft.com/) after the reviewer assignment is done. For that, go to the Submissions page, filter for the correct submission track, then filter for papers with status "Awaiting Decision". Go to the Actions button on the top right, select "Export to Excel/Submissions".

- **Reviewers.xlsx** and **Metareviewers.xlsx**, which contain the list of reviewers and metareviewers, respectively. **These are NOT exported from CMT**, as they contain info that is not there. Also, some reviewers/metareviewers use generic email accounts (such as Gmail, Outlook, etc.) on CMT instead of their institutional email addresses, and this hinders checking for domain conflicts. These two files should contain five columns: "First Name", "Last Name", "Email Address", "Organization", "Country". Samples of these files are available in the docs folder.  

## Output 

The script prints out the set of conflicts it finds in the assignments. Once they are manually corrected in CMT, a new assignment spreadsheet can be downloaded and the script can be used to check for new conflicts, as many times as necessary. 

## Instalation 

Create a venv 

```
$ python –m venv conflict
```

Activate the venv 

```
$ source conflict/bin/activate
```

Install pandas 

```
$ (conflict) pip install pandas
```

Install openpyxl 


```
$ (conflict) pip install openpyxl
```

## Execution 

Place the three input files in the same folder as the script. If you want to allow a paper to have more than 1 reviewer from the same country, edit the script and change the value of the **max_reviewers_from_same_country** variable. 

Run: 

```
$ python conflict-checker.py
```

When the script prints a message that it could not find a reviewer or metareviewer, check for extra spaces in their names. **Do all the fixings on the Reviewers.xlsx or Metareviewers.xlsx**. The names on those files must match the names on CMT that were exported to the Papers.xlsx file. Since you, as a PC-chair, do not have permission to change the names of reviewers and metareviewers on CMT, change it on the other two files, so they are an exact match. 
