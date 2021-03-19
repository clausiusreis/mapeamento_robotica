# -*- coding: utf-8 -*-

#######################################################################################################
### W_CBIE ############################################################################################
#######################################################################################################

page = 'https://www.br-ie.org/pub/index.php/wcbie/issue/archive'

terms = ['robótica', 
         'robô', 
         'robotic', 
         'robot']

# Import libraries
import requests
from bs4 import BeautifulSoup

# Load the page
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'}

pageRequest = requests.get(page, headers=headers)
soup = BeautifulSoup(pageRequest.content, 'html.parser')

# Find the editions
content = soup.find(id='issues')
auxEditionYear = content.find_all('h3')
auxEditionLink = content.find_all('h4')

aux = 0
editions = []
selectedPapers = []
for e in auxEditionYear:
    if int(auxEditionYear[aux].text) >= 2010:
        print('%s - %s' % ( auxEditionYear[aux].text, auxEditionLink[aux].find('a', href=True)['href']))
        editions.append([auxEditionYear[aux].text, auxEditionLink[aux].find('a', href=True)['href']])
    aux += 1
   
# For each edition, find the links related to papers
for ye in editions:
    print('ANO: %s' % (ye[0]))    
    pageRequest = requests.get(ye[1], headers=headers)
    soup = BeautifulSoup(pageRequest.content, 'html.parser')
    content = soup.find(id='content')

    papers = content.find_all(class_='tocTitle')
    links = []
    for p in papers:
        link = p.find('a', href=True)
        links.append(link['href'])
    
    print('Number of papers in issue %s: %s' % (ye[0], len(links)))
    
    # For each link, look for each term occurrence
    print('')
    print('#############################################')
    print('### ANALYSIS ################################')
    print('#############################################')
    print('')    
    i = 1
    for l in links:
        print('Analisando: %s of %s: %s' % (i, len(links), l))    
        linkReq = requests.get(l, headers=headers)
        soupReq = BeautifulSoup(linkReq.content, 'html.parser')
        title = soupReq.find(id='articleTitle').find('h3').text.strip()
        abstract = soupReq.find(id='articleAbstract').find('div').text.strip()        

        termsFound = ""
        termExist = False
        for t in terms:
            #testar cada um dos termos no title e abstract
            nTitle = title.lower().count(t.lower())
            nAbstract = abstract.lower().count(t.lower())
            if (nTitle > 0) | (nAbstract > 0):
                termExist = True            
                termsFound = termsFound + ", " + t.lower()
        
        # Remove the first comma
        termsFound = termsFound[2:]
    
        if termExist == True:
            # Ano, Link, Termos, Número de artigos da edição, Título
            selectedPapers.append([ye[0], l, termsFound, len(links), title])
            print('   ADD: %s - %s - %s - %s' % (ye[0], l, termsFound, len(links)))
        i += 1
    
    print('#############################################')
    print('### RESULTS #################################')
    print('#############################################')
    print('')

for p in selectedPapers:
    print('%s|%s|%s|%s|%s' % (p[0], p[1], p[2], p[3], p[4]))


# %%

#######################################################################################################
### RENOTE ############################################################################################
#######################################################################################################

page = 'https://seer.ufrgs.br/renote/issue/archive'

terms = ['robótica', 
         'robô', 
         'robotic', 
         'robot']

# Import libraries
import requests
from bs4 import BeautifulSoup

# Load the page
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'}

pageRequest = requests.get(page, headers=headers)
soup = BeautifulSoup(pageRequest.content, 'html.parser')

# Find the editions
content = soup.find(id='issues')
auxEditionYear = content.find_all('h4')
auxEditionLink = content.find_all(class_='issueCoverImage')

aux = 0
editions = []
selectedPapers = []
for e in auxEditionYear:
    print('%s | %s' % ( auxEditionYear[aux].text, auxEditionLink[aux].find('a', href=True)['href']))
    editions.append([auxEditionYear[aux].text, auxEditionLink[aux].find('a', href=True)['href']])
    aux += 1

# Fix the links
aux = 0
for e in editions:    
    print('Fixing link: %s' % (e[1]))    
    pageRequest = requests.get(e[1], headers=headers)
    soup = BeautifulSoup(pageRequest.content, 'html.parser')        
    content = soup.find(id='main')
    eYear = content.find('h2').text[-5:-1]    
    eLink = content.find(id='content').find(id="issueCoverImage").find('a', href=True)['href']    
    if int(eYear) >= 2010:
        editions[aux][0] = eYear #Ano
        editions[aux][1] = eLink #link
    aux += 1

# For each edition, find the links related to papers
for ye in editions:
    print('ANO: %s' % (ye[0]))    
    pageRequest = requests.get(ye[1], headers=headers)
    soup = BeautifulSoup(pageRequest.content, 'html.parser')
    content = soup.find(id='content')

    papers = content.find_all(class_='tocTitle')
    links = []
    for p in papers:
        link = p.find('a', href=True)
        links.append(link['href'])
    
    print('Number of papers in issue %s: %s' % (ye[0], len(links)))
    
    # For each link, look for each term occurrence
    print('')
    print('#############################################')
    print('### ANALYSIS ################################')
    print('#############################################')
    print('')    
    i = 1
    for l in links:
        print('Analisando: %s of %s: %s' % (i, len(links), l))    
        linkReq = requests.get(l, headers=headers)
        soupReq = BeautifulSoup(linkReq.content, 'html.parser')
        
        title1 = soupReq.find(id='articleTitle')                
        abstract1 = soupReq.find(id='articleAbstract')
        if (title1 is not None) & (abstract1 is not None):
            title = soupReq.find(id='articleTitle').find('h3').text.strip()
            abstract = soupReq.find(id='articleAbstract').find('div').text.strip()

            termsFound = ""
            termExist = False
            for t in terms:
                #testar cada um dos termos no title e abstract
                nTitle = title.lower().count(t.lower())
                nAbstract = abstract.lower().count(t.lower())
                if (nTitle > 0) | (nAbstract > 0):
                    termExist = True            
                    termsFound = termsFound + ", " + t.lower()
            
            # Remove the first comma
            termsFound = termsFound[2:]
        
            if termExist == True:
                # Ano, Link, Termos, Número de artigos da edição, Título
                selectedPapers.append([ye[0], l, termsFound, len(links), title])
                print('   ADD: %s | %s | %s | %s | %s' % (ye[0], l, termsFound, len(links), title))
        i += 1
    
    
print('#############################################')
print('### RESULTS #################################')
print('#############################################')
print('')

for p in selectedPapers:
    print('%s|%s|%s|%s|%s' % (p[0], p[1], p[2], p[3], p[4]))


# %%

#######################################################################################################
### SBIE - Rachel #####################################################################################
#######################################################################################################

page = 'https://www.br-ie.org/pub/index.php/sbie/issue/archive'

terms = ['robótica', 
         'robô', 
         'robotic', 
         'robot']

# Import libraries
import requests
from bs4 import BeautifulSoup

# Load the page
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'}

pageRequest = requests.get(page, headers=headers)
soup = BeautifulSoup(pageRequest.content, 'html.parser')

# Find the editions
content = soup.find(id='issues')
auxEditionYear = content.find_all('h3')
auxEditionLink = content.find_all('h4')

aux = 0
editions = []
selectedPapers = []
for e in auxEditionYear:
    if int(auxEditionYear[aux].text) >= 2010:
        print('%s | %s' % ( auxEditionYear[aux].text, auxEditionLink[aux].find('a', href=True)['href']))
        editions.append([auxEditionYear[aux].text, auxEditionLink[aux].find('a', href=True)['href']])
    aux += 1

# Fix the links
# aux = 0
# for e in editions:
#     print('Fixing link: %s' % (e[1]))
#     pageRequest = requests.get(e[1], headers=headers)
#     soup = BeautifulSoup(pageRequest.content, 'html.parser')
#     content = soup.find(id='main')
#     eYear = content.find('h2').text[-5:-1]    
#     eLink = content.find(id='content').find(id="issueCoverImage").find('a', href=True)['href']    
#     editions[aux][0] = eYear #Ano
#     editions[aux][1] = eLink #link
#     aux += 1

# For each edition, find the links related to papers
for ye in editions:
    print('ANO: %s' % (ye[0]))    
    pageRequest = requests.get(ye[1], headers=headers)
    soup = BeautifulSoup(pageRequest.content, 'html.parser')
    content = soup.find(id='content')

    papers = content.find_all(class_='tocTitle')
    links = []
    for p in papers:
        link = p.find('a', href=True)
        links.append(link['href'])
    
    print('Number of papers in issue %s: %s' % (ye[0], len(links)))
    
    # For each link, look for each term occurrence
    print('')
    print('#############################################')
    print('### ANALYSIS ################################')
    print('#############################################')
    print('')    
    i = 1
    for l in links:
        print('Analisando: %s of %s: %s' % (i, len(links), l))    
        linkReq = requests.get(l, headers=headers)
        soupReq = BeautifulSoup(linkReq.content, 'html.parser')
        
        title1 = soupReq.find(id='articleTitle')                
        abstract1 = soupReq.find(id='articleAbstract')
        if (title1 is not None) & (abstract1 is not None):
            title = soupReq.find(id='articleTitle').find('h3').text.strip()
            abstract = soupReq.find(id='articleAbstract').find('div').text.strip()

            termsFound = ""
            termExist = False
            for t in terms:
                #testar cada um dos termos no title e abstract
                nTitle = title.lower().count(t.lower())
                nAbstract = abstract.lower().count(t.lower())
                if (nTitle > 0) | (nAbstract > 0):
                    termExist = True            
                    termsFound = termsFound + ", " + t.lower()
            
            # Remove the first comma
            termsFound = termsFound[2:]
        
            if termExist == True:
                # Ano, Link, Termos, Número de artigos da edição
                selectedPapers.append([ye[0], l, termsFound, len(links), title])
                print('   ADD: %s | %s | %s | %s | %s' % (ye[0], l, termsFound, len(links), title))
        i += 1
    
    
print('#############################################')
print('### RESULTS #################################')
print('#############################################')
print('')

for p in selectedPapers:
    print('%s|%s|%s|%s|%s' % (p[0], p[1], p[2], p[3], p[4]))


## %%







