# NameSpi
### PLEASE report any recommendations, issues, etc to me. Best way to reach me is keybase @waffless ... Im new to the github issues thing but ill get around to it if you post it there

### This tool is stil in development. Please read the README before using NameSpi. If you submit an 'issue' that is labeled in the README, I will call you stupid and close it.

This tool is designed to create a list of employees for the company of your choice. It pulls from your choices of LinkedIn, ZoomInfo, USStaff, and Hunter.io.
- The LinkedIn functionality pulls employees from the company LinkedIn page based on your connections. The more connections you have the better.
- The ZoomInfo functionality pulls employees based on the URL provided. Provide the target company's ZoomInfo link and youll get back up to 125 unique names.
- The Hunter.io functionality pulls employees names based on your subscription level. The Free version only allows 10. This will also identify the email format if you plan on mangeling names for password guessing.
- The USStaff functionality pulls employee names from https://bearsofficialsstore.com/
- The script also cleans up the names, removes duplicates, and can mangle to the output you want.

- ZoomInfo can be picky with how many times an IP can hit the employee names portion. Therefore, the ZoomInfo portion is ProxyAware with the `-proxy` or `-proxyfile` options. Make sure to include the type of proxy (i.e. `socks5://127.0.0.1:1080`)

**HINT:** You do not need to supply EVERY option in the command itself. If you supply any of the collection methods after that (-li, -zi, -hio) and nothing else, the script will ask for the information it required to complete the function. This is also mentioned below in the **Scraping Options** header.

------------------------------------------------------------------------------------
# Usage

```
$ ./NameSpi.py -h
  _   _                      ____        _ 
 | \ | | __ _ _ __ ___   ___/ ___| _ __ (_) 
 |  \| |/ _` | '_ ` _ \ / _ \___ \| '_ \| | 
 | |\  | (_| | | | | | |  __/___) | |_) | | 
 |_| \_|\__,_|_| |_| |_|\___|____/| .__/|_| 
                                  |_| v0.9
             Author: #Waffl3ss
         Special Thanks: #bigb0sss


usage: NameSpi.py [-h] [-li] [-zi] [-hio] [-uss] [-o OUTPUTFILE] [-pn] [-c COMPANY] [-id COMPANYID] [-s SLEEP] [-t TIMEOUT]
                  [-user LINKEDIN_USERNAME] [-pass LINKEDIN_PASSWORD] [-zilink ZILINK] [-hapi HUNTERAPIKEY] [-hdom HUNTERDOMAIN]
                  [-uc USSTAFFCOMPANY] [-proxy SINGLEPROXY] [-proxyfile PROXYLIST] [-m MANGLEMODE] [-mo]

optional arguments:
  -h, --help            show this help message and exit
  -li                   Run the LinkedIn module
  -zi                   Pull ZoomInfo Employee Names
  -hio                  Pull Emails from Hunter.io
  -uss                  Pull Names from USStaff
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
  -zilink ZILINK        ZoomInfo Company Employee Link
                          (eg: https://www.zoominfo.com/pic/google-inc/16400573
  -hapi HUNTERAPIKEY    Hunter.io API Key
  -hdom HUNTERDOMAIN    Domain to query in Hunter.io
  -uc USSTAFFCOMPANY    Exact company name on USStaff (https://bearsofficialsstore.com/)
  -proxy SINGLEPROXY    Use with [TYPE]://[IP]:[PORT]
  -proxyfile PROXYLIST  File with newline seperate proxies. Each proxy must have the type
                          i.e. socks5://127.0.0.1:1080
  -m MANGLEMODE         Mangle Mode (use '-mo' to list mangle options). Only works with an output file (-o)
  -mo                   List Mangle Mode Options

```
### Examples

```
./NameSpi.py -o MyOutput -li
./NameSpi.py -o MyOutput -li -zi
./NameSpi.py -o MyOutput -li -zi -hio
./NameSpi.py -o MyOutput -li -zi -hio -pn
./NameSpi.py -pn -li -zi -uss
./NameSpi.py -pn -zi -proxy socks5://127.0.0.1:1080
```

------------------------------------------------------------------------------------
# Scraping Options

Options like the LinkedIn credentials, ZoomInfo Link, Hunter.io API Key, Hunter.io Domain Name, USStaff name, and Company name do not need to be in the command itself, the script will ask for those if you have selected the options to run those modules.

Example:
```
$ ./NameSpi.py -zi -li -hio -uss

  _   _                      ____        _ 
 | \ | | __ _ _ __ ___   ___/ ___| _ __ (_) 
 |  \| |/ _` | '_ ` _ \ / _ \___ \| '_ \| | 
 | |\  | (_| | | | | | |  __/___) | |_) | | 
 |_| \_|\__,_|_| |_| |_|\___|____/| .__/|_| 
                                  |_| v0.9
             Author: #Waffl3ss
         Special Thanks: #bigb0sss


Company Name: 
LinkedIn Username: 
LinkedIn Password: 
ZoomInfo Link: 
Hunter.io Domain to Query: 
Hunter.io API Key: 
USStaff Name: 
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
```
