import pandas as pd
import re

# Change here to allow more than one reviewer from the same country on a given paper
max_reviewers_from_same_country = 1

# receives a string with names in the format
# Name1 LastName1 (Institution1); Name2 LastName2 (Institution2); Name3 LastName3 (Institution3)
# and returns a list containing the names [namelastname1, namelastname2, namelastname3]
# the size of the list varies
def get_names(text):
    names = []
    names_insts = text.lower().split(';')
    for name_inst in names_insts:
        # remove institution
        pos = name_inst.find('(')
        name = name_inst[0:pos].strip()
        names.append(name)
    return names

# receives a string with authors names in the format
# Name1 LastName1 (Institution1); Name2 LastName2 (Institution2); Name3 LastName3 (Institution3)
# and returns a list containing the institutions [institution1, institution2, institution3]
# the size of the list varies, depending on how many authors a given paper has
def get_authors_institutions(text):
    institutions = []
    names_insts = text.lower().split(';')
    for name_inst in names_insts:
        # find institution
        pos1 = name_inst.find('(')
        pos2 = name_inst.find(')')
        # remove the parenthesis from the institution
        institution = name_inst[pos1+1:pos2]
        institutions.append(institution)
    return institutions

# receives a string with emails in the format
# email1@domain1; email2@domain2; email3@domain3
# and returns a list containing the domains [domain1, domain2, domain3]
# the size of the list varies
def get_cmt_domains(text):
    domains = []
    emails = text.lower().split(';')
    for email in emails:
        # find domain
        pos1 = email.find('@')
        # get the domain
        domain = email[pos1 + 1:]
        #remove *, if any (corresponding authors have a * at the end of their email address)
        if '*' in domain:
            domain = domain[0:-1]
        domains.append(domain)
    return domains

# receives a list of names, a dataframe df containing details (of reviewers or metareviwers), and the type of names
# returns a list of email domains for those people
# A POSSIBLE CAUSE OF NOT FOUND is double space sparating first and last name.
# In this case, edit the Papers.xlsx spreadsheet to remove those and replace them by a single space
def get_domains(names, df, type):
    domains = []
    for name in names:
        domain = 'NOT FOUND'
        for _, row in df.iterrows():
            n = row['First Name'].strip().lower() + ' ' + row['Last Name'].strip().lower()
            if name == n:
                domain = row['Email Address'].strip().lower()
                pos1 = domain.find('@')
                domain = domain[pos1 + 1:]
                break
        domains.append(domain)
        if domain == 'NOT FOUND':
            print(f'{name} not found on the dataframe of {type} -> domain not retrieved')
    return domains


# receives a list of names, a dataframe df containing details (of reviewers or metareviwers), and the type of names
# returns a list of institutions of those people
# A POSSIBLE CAUSE OF NOT FOUND is double space sparating first and last name.
# In this case, edit the Papers.xlsx spreadsheet to remove those and replace them by a single space
def get_institutions(names, df, type):
    institutions = []
    for name in names:
        institution = 'NOT FOUND'
        for _, row in df.iterrows():
            n = row['First Name'].strip().lower() + ' ' + row['Last Name'].strip().lower()
            if name == n:
                institution = row['Organization'].strip().lower()
                break
        institutions.append(institution)
        if institution == 'NOT FOUND':
            print(f'{name} not found on the dataframe of {type} -> institution not retrieved')
    return institutions

# receives a list of names, a dataframe df df containing details (of reviewers or metareviwers) and the type of names
# returns a list of countries of those people
# A POSSIBLE CAUSE OF NOT FOUND is double space sparating first and last name.
# In this case, edit the Papers.xlsx spreadsheet to remove those and replace them by a single space
def get_countries(names, df, type):
    countries = []
    for name in names:
        country = 'NOT FOUND'
        for _, row in df.iterrows():
            n = row['First Name'].strip().lower() + ' ' + row['Last Name'].strip().lower()
            if name == n:
                country = row['Country'].strip().lower()
                break
        countries.append(country)
        if country == 'NOT FOUND':
            print(f'{name} not found on the dataframe of {type} -> country not retrieved')
    return countries

def check_same_institution(paper):
    reviewers_institutions = paper['Reviewers_Institutions']
    metareviewers_institutions = paper['Metareviewers_Institutions']
    authors_institutions = paper['Authors_Institutions']
    for mi in metareviewers_institutions:
        if mi in reviewers_institutions:
            print(f'PAPER #{paper['Paper_ID']}: Reviewer and Metareviewer from the same institution -> {mi}')
        if mi in authors_institutions:
            print(f'PAPER #{paper['Paper_ID']}: Author and Metareviewer from the same institution -> {mi}')
    for ri in reviewers_institutions:
        if ri in authors_institutions:
            print(f'PAPER #{paper['Paper_ID']}: Author and Reviewer from the same institution -> {ri}')

def check_same_domain(paper):
    reviewers_domains = paper['Reviewers_Domains']
    metareviewers_domains = paper['Metareviewers_Domains']
    authors_domains = paper['Authors_Domains']
    for md in metareviewers_domains:
        if md in reviewers_domains:
            print(f'PAPER #{paper['Paper_ID']}: Reviewer and Metareviewer with the same email domain -> {md}')
        if md in authors_domains:
            print(f'PAPER #{paper['Paper_ID']}: Author and Metareviewer with the same email domain -> {md}')
    for rd in reviewers_domains:
        if rd in authors_domains:
            print(f'PAPER #{paper['Paper_ID']}: Author and Reviewer with the same email domain -> {rd}')

def check_same_country(paper):
    reviewers_countries = paper['Reviewers_Countries']
    metareviewers_countries = paper['Metareviewers_Countries']
    for mc in metareviewers_countries:
        if mc in reviewers_countries:
            print(f'PAPER #{paper['Paper_ID']}: Reviewer and Metareviewer from the same country -> {mc}')
    same_country = []
    for rc in reviewers_countries:
        count = reviewers_countries.count(rc)
        if count > max_reviewers_from_same_country:
            if rc not in same_country:
                same_country.append(rc)
    if len(same_country) > 0:
        print(f'PAPER #{paper['Paper_ID']}: more than {max_reviewers_from_same_country} reviewers from -> {same_country}')
        print(f'   + reviewers for this paper are from {reviewers_countries}')

# === Read Input Files ===
papers_df = pd.read_excel('Papers.xlsx')
reviewers = pd.read_excel('Reviewers.xlsx')
metareviewers = pd.read_excel('MetaReviewers.xlsx')

papers = []

for _, row in papers_df.iterrows():
    reviewers_names = get_names(row['Reviewers'])
    metareviewers_names =  get_names(row['MetaReviewers'])
    papers.append({
        'Paper_ID': row['Paper ID'],
        'Authors_Institutions': get_authors_institutions(row['Authors']),
        'Authors_Domains': get_cmt_domains(row['Author Emails']),
        'Reviewers': reviewers_names,
        'Reviewers_Institutions': get_institutions(reviewers_names, reviewers, 'reviewers'),
        # Looks for domains in two spreadsheets: the Papers spreadsheet that was extracted from CMT,
        # and the Reviewers/Metareviewers spreadsheets that were create by the PC Chairs
        'Reviewers_Domains': get_cmt_domains(row['Reviewer Emails']) + get_domains(reviewers_names, reviewers, 'reviewers'),
        'Reviewers_Countries': get_countries(reviewers_names, reviewers, 'reviewers'),
        'Metareviewers': metareviewers_names,
        'Metareviewers_Institutions': get_institutions(metareviewers_names, metareviewers, 'metareviewers'),
        # Looks for domains in two spreadsheets: the Papers spreadsheet that was extracted from CMT,
        # and the Reviewers/Metareviewers spreadsheets that were create by the PC Chairs
        'Metareviewers_Domains': get_cmt_domains(row['MetaReviewer Emails']) + get_domains(metareviewers_names, metareviewers, 'metareviewers'),
        'Metareviewers_Countries': get_countries(metareviewers_names, metareviewers, 'metareviewers'),
    })

# Check conflicts

print('Checking for assignments with:')
print('   + authors, reviewers or metareviewes from the same institution...')
print('   + authors, reviewers or metareviewes with the same email address domain...')
print(f'   + assignments with more than {max_reviewers_from_same_country} reviewer/metareviewer from the same country... \n')

for paper in papers:
    check_same_institution(paper) 
    check_same_domain(paper)
    check_same_country(paper)

#for paper in papers:
#    print(paper)

