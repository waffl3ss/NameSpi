# NameSpi
------------------------------------------------------------------------------------
This tool is stil in development. Please read the README before using NameSpi

This tool is designed to create a list of employees for the company of your choice. It pulls from your choices of LinkedIn, ZoomInfo, and Hunter.io.
- The LinkedIn functionality pulls employees from the company LinkedIn page based on your connections. The more connections you have the better.
- The ZoomInfo functionality pulls employees based on the URL provided. Provide the target company's ZoomInfo link and youll get back 125 unique names.
- The Hunter.io functionality pulls employees email addresses based on your subscription level. The Free version only allows 10. This will also identify the email format if you plan on mangeling names for password guessing.
- The script also cleans up the names, removes duplicates, and mangles to the mode that you want.

------------------------------------------------------------------------------------
# Usage
------------------------------------------------------------------------------------
```
$ ./NameSpi.py -h

 _   _                      ____        _
| \ | | __ _ _ __ ___   ___/ ___| _ __ (_)
|  \| |/ _` | '_ ` _ \ / _ \___ \| '_ \| |
| |\  | (_| | | | | | |  __/___) | |_) | |
|_| \_|\__,_|_| |_| |_|\___|____/| .__/|_|
                                 |_|
        v0.7    #Waffl3ss

usage: NameSpi.py [-h] [-li] [-zi] [-hio] [-o OUTPUTFILE] [-pn] [-c COMPANY] [-id COMPANYID] [-s SLEEP]
                  [-mr MAX_REQUESTS] [-t TIMEOUT] [-user LINKEDIN_USERNAME] [-pass LINKEDIN_PASSWORD] [-zilink ZILINK]
                  [-hapi HUNTERAPIKEY] [-hdom HUNTERDOMAIN] [-m MANGLEMODE] [-mo]

Company Linkedin user enumeration and cleanup.

optional arguments:
  -h, --help            show this help message and exit
  -li                   Run the LinkedIn module
  -zi                   Pull ZoomInfo Employee Names
  -hio                  Pull Emails from Hunter.io
  -o OUTPUTFILE         Write output to file
  -pn                   Print found names to screen
  -c COMPANY            Company to search for
  -id COMPANYID         Company ID to search for
  -s SLEEP              Time to sleep between requests
  -mr MAX_REQUESTS      Max number of requests per title while searching, use 0 for unlimited
  -t TIMEOUT            HTTP Request timeout
  -user LINKEDIN_USERNAME
                        LinkedIn.com Authenticated Username
  -pass LINKEDIN_PASSWORD
                        LinkedIn.com Authenticated Password
  -zilink ZILINK        ZoomInfo Company Employee Link
                          (eg: https://www.zoominfo.com/pic/google-inc/16400573
  -hapi HUNTERAPIKEY    Hunter.io API Key
  -hdom HUNTERDOMAIN    Domain to query in Hunter.io
  -m MANGLEMODE         Mangle Mode (use '-mo' to list mangle options)
  -mo                   List Mangle Mode Options
```
## Examples

```
./NameSpi.py -o MyOutput -li
./NameSpi.py -o MyOutput -li -zi
./NameSpi.py -o MyOutput -li -zi -hio
./NameSpi.py -o MyOutput -li -zi -hio -pn
```

------------------------------------------------------------------------------------
# Scraping Options
------------------------------------------------------------------------------------
Options like the LinkedIn Username and Password, ZoomInfo Link, Hunter.io API Key, Hunter.io Domain Name, and Company name do not need to be in the command itself, the script will ask for those if you have selected the options to run those modules.

Example:
```
$ ./NameSpi.py -o MyOutput -li -zi -hio

 _   _                      ____        _
| \ | | __ _ _ __ ___   ___/ ___| _ __ (_)
|  \| |/ _` | '_ ` _ \ / _ \___ \| '_ \| |
| |\  | (_| | | | | | |  __/___) | |_) | |
|_| \_|\__,_|_| |_| |_|\___|____/| .__/|_|
                                 |_|
        v0.7    #Waffl3ss

Company Name:
LinkedIn Username:
LinkedIn Password:
ZoomInfo Link:
Hunter.io Domain to Query:
Hunter.io API Key:
```

------------------------------------------------------------------------------------
# Mangle Modes
------------------------------------------------------------------------------------
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
```

