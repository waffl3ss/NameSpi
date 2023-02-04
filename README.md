# NameSpi - v1.1
### PLEASE report any recommendations, issues, etc to me. Best way to reach me is keybase @waffless ...

### Please make sure to read the README before using NameSpi. 

This tool is designed to create a list of employees for the company of your choice. It pulls from your choices of LinkedIn, USStaff, Hunter.io, and Phonebook.cz. Also has the ability to pull and mangle a list of 250k statistically likely names.
- The LinkedIn functionality pulls employees from the company LinkedIn page based on your connections. The more connections you have the better.
- The Hunter.io functionality pulls employees names based on your subscription level. The Free version only allows 10. This will also identify the email format if you plan on mangeling names for password guessing.
- The USStaff functionality pulls employee names from https://bearsofficialsstore.com/ (Thanks to #bigb0sss for this one)
- The phonebook functionality pulls emails from Phonebook.cz using your Developer API key. This is limited to 10 requests a day on the free version. 
- The statistically likely functionality pulls 250k statiscially like names. (CAUTION: Long List) (Thanks to #AchocolatechipPancake for this one)
- The script also cleans up the names, removes duplicates, removes accents, changes capitalization for uniformity, and can mangle to the output you want (10 options built in).

- **NEW!** NameSpi can take a YAML file as input! I recommend against putting your linkedin password in a YAML file, therefore if you leave that blank, the script will ask for it after its ran.

**HINT:** You do not need to supply EVERY option in the command itself. If you supply any of the collection methods after that (-li, -hio -uss -pb) and nothing else, the script will ask for the information it requires to complete the function. This is also mentioned below in the **Scraping Options** header.

------------------------------------------------------------------------------------
# Usage

```
$ ./NameSpi.py -h

  _   _                      ____        _ 
 | \ | | __ _ _ __ ___   ___/ ___| _ __ (_) 
 |  \| |/ _` | '_ ` _ \ / _ \___ \| '_ \| | 
 | |\  | (_| | | | | | |  __/___) | |_) | | 
 |_| \_|\__,_|_| |_| |_|\___|____/| .__/|_| 
                                  |_| v1.2 
             Author: #Waffl3ss 


usage: NameSpi_v1.py [-h] [-li] [-hio] [-uss] [-pb] [-pbdom PHONEBOOKTARGETDOMAIN] [-iapi INTELAPIKEY] [-o OUTPUTFILE] [-pn] [-c COMPANY] [-id COMPANYID] [-s SLEEP] [-t TIMEOUT] [-user LINKEDIN_USERNAME]
                     [-pass LINKEDIN_PASSWORD] [-hapi HUNTERAPIKEY] [-hdom HUNTERDOMAIN] [-uc USSTAFFCOMPANY] [-m MANGLEMODE] [-mo] [-yaml USEYAMLFILE]

options:
  -h, --help            show this help message and exit
  -li                   Run the LinkedIn module
  -hio                  Pull Emails from Hunter.io
  -uss                  Pull Names from USStaff (https://bearsofficialsstore.com/) Special Thanks: #bigb0sss
  -pb                   Pull Names from Phonebook.CZ
  -sl                   Use Statistically Likely Usernames in output (CAUTION: Creates a VERY long list) Special Thanks: #AchocolatechipPancake
  -pbdom PHONEBOOKTARGETDOMAIN
                        Domain to query Phonebook
  -iapi INTELAPIKEY     IntelX API Key
  -o OUTPUTFILE         Write output to file
  -pn                   Print found names to screen
  -c COMPANY            Company to search for
  -id COMPANYID         Company ID to search for
  -s SLEEP              Time to sleep between requests
  -t TIMEOUT            HTTP Request timeout
  -user LINKEDIN_USERNAME
                        LinkedIn.com Authenticated Username
  -pass LINKEDIN_PASSWORD
                        LinkedIn.com Authenticated Password
  -hapi HUNTERAPIKEY    Hunter.io API Key
  -hdom HUNTERDOMAIN    Domain to query in Hunter.io
  -uc USSTAFFCOMPANY    Exact company name on USStaff
  -m MANGLEMODE         Mangle Mode (use '-mo' to list mangle options). Only works with an output file (-o)
  -mo                   List Mangle Mode Options
  -yaml USEYAMLFILE     Use YAML input file with options

```
### Examples

```
./NameSpi.py -o MyOutput -li
./NameSpi.py -o MyOutput -li -hio
./NameSpi.py -o MyOutput -li -hio -pn
./NameSpi.py -o MyOutput -li -hio -uss -pb
./NameSpi.py -o MyOutput -li -hio -uss -pb -sl
./NameSpi.py -pn -li -uss
```

------------------------------------------------------------------------------------
# Scraping Options

Options like the LinkedIn credentials, Hunter.io API Key, Hunter.io Domain Name, USStaff name, Phonebook Target Domain, Phonebook API Key, and Company name do not need to be in the command itself, the script will ask for those if you have selected the options to run those modules. These can also be thrown into the YAML file. I dont recommend putting your LinkedIn password in the file, and therefore if you leave it blank in the YAML file, the script will ask for it during execution.

Example:
```
$ ./NameSpi.py -li -hio -uss -pb

  _   _                      ____        _ 
 | \ | | __ _ _ __ ___   ___/ ___| _ __ (_) 
 |  \| |/ _` | '_ ` _ \ / _ \___ \| '_ \| | 
 | |\  | (_| | | | | | |  __/___) | |_) | | 
 |_| \_|\__,_|_| |_| |_|\___|____/| .__/|_| 
                                  |_| v1.2
             Author: #Waffl3ss


Company Name: 
LinkedIn Username: 
LinkedIn Password: 
Hunter.io Domain to Query: 
Hunter.io API Key: 
Phonebook Target Domain: 
Phonebook API Key: 
```

------------------------------------------------------------------------------------
# Mangle Modes

If you want something else, use mode 0 and mangle it yourself.  
Mangle Modes included:
```
     0 = <First> <LAST>    (Default)
     1 = <FIRST>.<LAST>
     2 = <F>.<LAST>
     3 = <FIRST>.<L>
     4 = <FIRST><LAST>
     5 = <F><LAST>
     6 = <FIRST><L>
     7 = <LAST><F>
     8 = <FIRST>_<LAST>
     9 = <LAST>_<FIRST>
     10 = <LAST>.<F>
```
