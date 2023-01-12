#!/usr/bin/python3

from __future__ import division
from http.cookiejar import CookieJar
from urllib.request import Request, build_opener, HTTPCookieProcessor, HTTPHandler, urlopen
from urllib.parse import urlencode
from argparse import RawTextHelpFormatter
from pyhunter import PyHunter
from bs4 import BeautifulSoup
import time, json, math, argparse, re, sys, os, urllib3, requests, cloudscraper, getpass, random, unidecode, httpimport, yaml
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with httpimport.remote_repo('https://raw.githubusercontent.com/IntelligenceX/SDK/master/Python/'):
	from intelxapi import intelx

banner = """
  _   _                      ____        _ 
 | \ | | __ _ _ __ ___   ___/ ___| _ __ (_) 
 |  \| |/ _` | '_ ` _ \ / _ \___ \| '_ \| | 
 | |\  | (_| | | | | | |  __/___) | |_) | | 
 |_| \_|\__,_|_| |_| |_|\___|____/| .__/|_| 
                                  |_| v1.1 
             Author: #Waffl3ss \n\n"""
print(banner)

# Parse user arguments
parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument('-li', dest='linkedingen', default=False, required=False, help="Run the LinkedIn module", action='store_true')
parser.add_argument('-zi', dest='zipull', required=False, default=False, help="Pull ZoomInfo Employee Names", action='store_true')
parser.add_argument('-hio', dest='hunterIO', required=False, default=False, help="Pull Emails from Hunter.io", action='store_true')
parser.add_argument('-uss', dest='usstaff', required=False, default=False, help="Pull Names from USStaff (https://bearsofficialsstore.com/) Special Thanks: #bigb0sss", action='store_true')
parser.add_argument('-pb', dest='phonebookCZ', required=False, default=False, help="Pull Names from Phonebook.CZ", action='store_true')
parser.add_argument('-sl', dest='statlikely', required=False, default=False, help="Use Statistically Likely Usernames in output (CAUTION: Creates a VERY long list) Special Thanks: AchocolatechipPancake", action='store_true')
parser.add_argument('-pbdom', dest='phonebookTargetDomain', required=False, help="Domain to query Phonebook")
parser.add_argument('-iapi', dest='intelAPIKey', required=False, help="IntelX API Key")
parser.add_argument('-o', dest='outputfile', required=False, default='', help="Write output to file")
parser.add_argument('-pn', dest='printnames', required=False, default=False, help="Print found names to screen", action='store_true')
parser.add_argument('-c', dest='company', default='', required=False, help="Company to search for")
parser.add_argument('-id', dest='companyid', required=False, help="Company ID to search for")
parser.add_argument('-s', dest='sleep', default=5, required=False, help="Time to sleep between requests")
parser.add_argument('-t', dest='timeout', required=False, default=5, help="HTTP Request timeout")
parser.add_argument('-user', dest='linkedin_username', required=False, help="LinkedIn.com Authenticated Username")
parser.add_argument('-pass', dest='linkedin_password', required=False, help="LinkedIn.com Authenticated Password")
parser.add_argument('-zilink', dest='zilink', required=False, help="ZoomInfo Company Employee Link\n  (eg: https://www.zoominfo.com/pic/google-inc/16400573")
parser.add_argument('-hapi', dest='hunterApiKey', required=False, help="Hunter.io API Key")
parser.add_argument('-hdom', dest='hunterDomain', required=False, help="Domain to query in Hunter.io")
parser.add_argument('-uc', dest='usstaffcompany', default='', required=False, help="Exact company name on USStaff")
parser.add_argument('-proxy', dest='singleproxy', default='None', required=False, help="Use with [TYPE]://[IP]:[PORT]")
parser.add_argument('-proxyfile' , dest='proxylist', default='None', required=False, help="File with newline seperate proxies. Each proxy must have the type\n  i.e. socks5://127.0.0.1:1080")
parser.add_argument('-m', dest='mangleMode', required=False, default=0, help="Mangle Mode (use '-mo' to list mangle options). Only works with an output file (-o)")
parser.add_argument('-mo', dest='mangleOptions', required=False, default=False, help="List Mangle Mode Options", action="store_true")
parser.add_argument('-yaml', dest='useyamlfile', required=False, default='', help="Use YAML input file with options")
args = parser.parse_args()

# Assign user arguments to variables we can use
company = str(args.company) # String
companyid = args.companyid # Int
sleep = int(args.sleep) # Int
timeout = int(args.timeout) # Int
outputfile = str(args.outputfile) # String
zipull = args.zipull # Bool
linkedingen = args.linkedingen # Bool
printnames = args.printnames # Bool
hunterIO = args.hunterIO # Bool
hunterApiKey = args.hunterApiKey # String
hunterDomain = args.hunterDomain # String
zilink = str(args.zilink) # String
linkedin_username = str(args.linkedin_username) # String
linkedin_password = str(args.linkedin_password) # String
mangleMode = int(args.mangleMode) # Int
mangleOptions = args.mangleOptions # Bool
usstaff = args.usstaff # Bool
usstaffcompany = str(args.usstaffcompany) # String
singleproxy = str(args.singleproxy) # String
proxylist = str(args.proxylist) # String
phonebookCZ = args.phonebookCZ # Bool
phonebookTargetDomain = str(args.phonebookTargetDomain) # String
intelAPIKey = str(args.intelAPIKey) # String
useyamlfile = str(args.useyamlfile) # Bool
statlikely = args.statlikely # Bool

# Colors for terminal output because Waffles likes pretty things
class bcolors:
        OKGREEN = '\033[92m'
        BOLD = '\033[1m'
        NONERED = '\033[91m'
        ENDLINE = '\033[0m'
        UNDERLINE = '\033[4m'

if mangleOptions:
	print('  Available Mangle Modes:')
	print('	  0 = <First> <LAST>	(Default)')
	print('	  1 = <FIRST>.<LAST>')
	print('	  2 = <F>.<LAST>')
	print('	  3 = <FIRST>.<L>')
	print('	  4 = <FIRST><LAST>')
	print('	  5 = <F><LAST>')
	print('	  6 = <FIRST><L>')
	print('	  7 = <LAST><F>')
	print('	  8 = <FIRST>_<LAST>')
	print('	  9 = <LAST>_<FIRST>')
	print('	  10 = <LAST>.<F>\n')
	sys.exit()

if useyamlfile != '':
	if os.path.exists(useyamlfile):
		with open(useyamlfile, 'r') as yamlfile:
			yamlcontents = yaml.safe_load(yamlfile)
			print(yamlcontents)

		if linkedingen and yamlcontents["CompanyID"] == '' and yamlcontents["CompanyName"] != '':
			company = yamlcontents["CompanyName"]
		elif linkedingen and args.companyid is None and args.company == '':
			company = input("Company Name: ")
		elif linkedingen and yamlcontents["CompanyID"] != '':
			companyid = yamlcontents["CompanyID"]
		else:
			print(bcolors.NONERED + '[!] YAML Error getting Company Name... ' + bcolors.ENDLINE)

		if linkedingen and yamlcontents["LinkedInUsername"] != '':
			linkedin_username = yamlcontents["LinkedInUsername"]
		elif linkedingen and args.linkedin_username is None:
			linkedin_username = input("LinkedIn Username: ")
		else:
			print(bcolors.NONERED + '[!] YAML Error with LinkedIn Username... ' + bcolors.ENDLINE)

		if linkedingen and yamlcontents["LinkedInPassword"] != '':
			linkedin_password = yamlcontents["LinkedInPassword"]
		elif linkedingen and args.linkedin_password is None:
			linkedin_password = getpass.getpass("LinkedIn Password: ")
		else:
			print(bcolors.NONERED + '[!] YAML Error with LinkedIn Password... ' + bcolors.ENDLINE)

		if zipull and yamlcontents["ZoomInfoLink"] != '':
			zilink = yamlcontents["ZoomInfoLink"]
		elif zipull and args.zilink is None:
			zilink = input("ZoomInfo Link: ")
		else:
			print(bcolors.NONERED + '[!] YAML Error with Zoominfo Link... ' + bcolors.ENDLINE)

		if hunterIO and yamlcontents["HunterIODomain"] != '':
			hunterDomain = yamlcontents["HunterIODomain"]
		elif hunterIO and args.hunterDomain is None:
			hunterDomain = input("Hunter.io Domain to Query: ")
		else:
			print(bcolors.NONERED + '[!] YAML Error with HunterIO Domain... ' + bcolors.ENDLINE)

		if hunterIO and yamlcontents["HunterIOKey"] != '':
			hunterApiKey = yamlcontents["HunterIOKey"]
		elif hunterIO and args.hunterApiKey is None:
			hunterApiKey = input("Hunter.io API Key: ")
		else:
			print(bcolors.NONERED + '[!] YAML Error with HunterIO API Key... ' + bcolors.ENDLINE)

		if usstaff and yamlcontents["USStaffCompanyName"] != '':
			usstaffcompany = yamlcontents["USStaffCompanyName"]
		elif usstaff and args.usstaffcompany == '':
			usstaffcompany = input("USStaff Name: ")
		else:
			print(bcolors.NONERED + '[!] YAML Error with USStaff Company... ' + bcolors.ENDLINE)

		if phonebookCZ and yamlcontents["PhonebookDomain"] != '':
			phonebookTargetDomain = yamlcontents["PhonebookDomain"]
		elif phonebookCZ and args.phonebookTargetDomain == '':
			phonebookTargetDomain = input("Phonebook Target Domain: ")
		else:
			print(bcolors.NONERED + '[!] YAML Error with Phonebook CZ Domain... ' + bcolors.ENDLINE)

		if phonebookCZ and yamlcontents["intelXAPIKey"] != '':
			intelAPIKey = yamlcontents["intelXAPIKey"]
		elif phonebookCZ and args.intelAPIKey == '':
			intelAPIKey = input("Phonebook API Key: ")
		else:
			print(bcolors.NONERED + '[!] YAML Error with Phonebook CZ API Key... ' + bcolors.ENDLINE)

	else:
		print(bcolors.NONERED + '[!] YAML file does not exist, exiting....' + bcolors.ENDLINE)
		sys.exit()

else:
	if linkedingen and args.companyid is None and args.company == '':
		company = input("Company Name: ")
	if linkedingen and args.linkedin_username is None:
		linkedin_username = input("LinkedIn Username: ")
	if linkedingen and args.linkedin_password is None:
		linkedin_password = getpass.getpass("LinkedIn Password: ")
	if zipull and args.zilink is None:
		zilink = input("ZoomInfo Link: ")
	if hunterIO and args.hunterDomain is None:
		hunterDomain = input("Hunter.io Domain to Query: ")
	if hunterIO and args.hunterApiKey is None:
		hunterApiKey = input("Hunter.io API Key: ")
	if usstaff and args.usstaffcompany is None:
		usstaffcompany = input("USStaff Name: ")
	if phonebookCZ and args.phonebookTargetDomain is None:
		phonebookTargetDomain = input("Phonebook Target Domain: ")
	if phonebookCZ and args.intelAPIKey is None:
		intelAPIKey = input("Phonebook API Key: ")

if singleproxy != 'None' and proxylist != 'None':
	print("[-] Please only use single proxy OR proxy file, not both")
	sys.exit()

if "/c/" in zilink:
	zilink = zilink.replace("/c/", "/pic/")

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3'

if outputfile == '' and not printnames:
	print(bcolors.NONERED + '[!] No output option select, choose an output file (-o) or print to screen (-pn)... ' + bcolors.ENDLINE)
	sys.exit()

zoomInfoNamesList = []
linkedInNamesList = []
hunterNamesList = []
usStaffNamesList = []
phonebookNamesList = []
printNamesModifierList = []
printNamesFullList = []
mangledNamesList = []
mangledPrintNamesList = []
statlikelyNamesList = []

def getcookie(cookiejar):
	c = ""
	for cookie in cookiejar:
		c += cookie.name + "=" + cookie.value + "; "
	return c

def logincsrf(cookiejar):
	for cookie in cookiejar:
		if cookie.name == "bcookie":
			return cookie.value.split('&')[1][:-1]

def ajaxtoken(cookiejar):
	for cookie in cookiejar:
		if cookie.name == "JSESSIONID":
			return cookie.value[1:-1]

def initialReq():
	cookiejar = CookieJar()
	opener = build_opener(HTTPCookieProcessor(cookiejar), HTTPHandler())
	headers = {
		"Host": "www.linkedin.com",
		"Agent": user_agent,
		}
	req = Request("https://www.linkedin.com")
	f = opener.open(req, timeout=timeout)
	return cookiejar

def authReq(cookiejar):
	opener = build_opener(HTTPCookieProcessor(cookiejar), HTTPHandler())
	lcsrf = logincsrf(cookiejar)

	if (lcsrf is None):
		print(bcolors.NONERED + '[-] Failed to pull CSRF token' + bcolors.ENDLINE)
	
	data = urlencode({"session_key": linkedin_username, "session_password": linkedin_password, "isJsEnabled": "false", "loginCsrfParam": lcsrf}).encode("utf-8")
	headers = {
		"Host": "www.linkedin.com",
		"User-Agent": user_agent,
		"Content-type": "application/x-www-form-urlencoded",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Cookie": getcookie(cookiejar),
		"X-IsAJAXForm": "1",
		}
	req = Request("https://www.linkedin.com/uas/login-submit", headers)
	f = opener.open(req, timeout=timeout, data=data)
	return cookiejar

def pullid():
	global company
	global companyid
	cookiejar = initialReq()
	cookiejar = authReq(cookiejar)
	opener = build_opener(HTTPCookieProcessor(cookiejar), HTTPHandler())
	query = "count=10&filters=List(resultType-%3ECOMPANIES)&" + urlencode({"keywords": company})  + "&origin=SWITCH_SEARCH_VERTICAL&q=all&queryContext=List(spellCorrectionEnabled-%3Etrue,relatedSearchesEnabled-%3Efalse)&start=0"
	headers = {
		"Host": "www.linkedin.com",
		"User-Agent": user_agent,
		"Accept": "application/vnd.linkedin.normalized+json+2.1",
		"x-restli-protocol-version": "2.0.0",
		"Cookie": getcookie(cookiejar),
		"Csrf-Token": ajaxtoken(cookiejar),
		}
	req = Request("https://www.linkedin.com/voyager/api/search/blended?" + query, None, headers)
	data = opener.open(req, timeout=timeout).read()
	content = json.loads(data)

	for companyname in content["included"]:
		id = companyname["entityUrn"].split(":")
		print("{:.<40}: {:s}".format(companyname["name"] + " :",id[3]))
	
	companyid = input("\nSelect company ID value: ")

def recon(title, cookiejar, count, start):
	opener = build_opener(HTTPCookieProcessor(cookiejar), HTTPHandler())

	if (title is None):
		query = "count=" + str(count) + "&filters=List(currentCompany-%3E" + str(companyid) + ",resultType-%3EPEOPLE" + ")&origin=FACETED_SEARCH&q=all&queryContext=List(spellCorrectionEnabled-%3" + "Etrue,relatedSearchesEnabled-%3Etrue,kcardTypes-%3ECOMPANY%7CJOB_TITLE)&start=" + str(start)
	else:
		query = "count=" + str(count) + "&filters=List(currentCompany-%3E" + str(companyid) + ",resultType-%3EPEOPLE,title-%3E" + urlencode({str(title):None}).split("=")[0] + ")&origin=FACETED_SEARCH&q=all&queryContext=List(spellCorrectionEnabled-%3" + "Etrue,relatedSearchesEnabled-%3Etrue,kcardTypes-%3ECOMPANY%7CJOB_TITLE)&start=" + str(start)

	headers = {
		"Host": "www.linkedin.com",
		"User-Agent": user_agent,
		"Accept": "application/vnd.linkedin.normalized+json+2.1",
		"x-restli-protocol-version": "2.0.0",
		"Cookie": getcookie(cookiejar),
		"Csrf-Token": ajaxtoken(cookiejar),
		}
	req = Request("https://www.linkedin.com/voyager/api/search/blended?" + query, None, headers)
	f = opener.open(req, timeout=timeout)
	return f.read()

def getZISession(companyLink, pageNum):
	zoomInfoSessionFirefox = cloudscraper.CloudScraper(browser={'browser': 'firefox', 'mobile': False, 'platform': 'windows'})
	getURL = str(str(companyLink) + '?pageNum=' + str(pageNum))
	# This proxy stuff below could use a clean up
	if singleproxy != 'None' and proxylist != 'None':
		print(bcolors.NONERED + '\n[!] Please select only one proxy option...' + bcolors.ENDLINE)
		sys.exit()
	if singleproxy != 'None':
		proxies = {
			"http": singleproxy,
			"https": singleproxy,
		}
	elif proxylist != 'None':
		proxylistfile = open(proxylist, 'r')
		possproxy = proxylistfile.readlines()
	else:
		proxies = {
			"http": None,
			"https": None,
		}
	try:
		if proxylist != 'None':
			tryprox1 = random.choice(possproxy)
			proxies = {
				"http": tryprox1,
				"https": tryprox1,
			}
			zoomInfoGetPage = zoomInfoSessionFirefox.get(getURL, allow_redirects=True, proxies=proxies)
		else:
			zoomInfoGetPage = zoomInfoSessionFirefox.get(getURL, allow_redirects=True, proxies=proxies)
	except Exception as e:
	#except cloudscraper.exceptions.CloudflareChallengeError as e:
		time.sleep(3)
		try:
			if proxylist != 'None':
				tryprox2 = random.choice(possproxy)
				proxies = {
				"http": tryprox2,
				"https": tryprox2,
				}
				zoomInfoGetPage = zoomInfoSessionFirefox.get(getURL, allow_redirects=True, proxies=proxies)
			else:
				zoomInfoGetPage = zoomInfoSessionFirefox.get(getURL, allow_redirects=True, proxies=proxies)
		except Exception as e:
			time.sleep(5)
			try:
				if proxylist != 'None':
					tryprox3 = random.choice(possproxy)
					proxies = {
					"http": tryprox3,
					"https": tryprox3,
					}
					zoomInfoGetPage = zoomInfoSessionFirefox.get(getURL, allow_redirects=True, proxies=proxies)
				else:
					zoomInfoGetPage = zoomInfoSessionFirefox.get(getURL, allow_redirects=True, proxies=proxies)
			except Exception as e:
				print(bcolors.NONERED + '[!] Error pulling ZoomInfo page ' + str(pageNum) + '\n' + bcolors.ENDLINE)
				pass
	if zoomInfoGetPage != '':
		return zoomInfoGetPage

def extractZINames(companyLink):
	for pageNum in range(1, 6):
		try:
			zoomInfoGetPage = getZISession(companyLink, pageNum)
			zoomInfoResponseSplit = zoomInfoGetPage.text.split('<script id="app-root-state" type="application/json">')
			zoomInfoResponseSplit2 = zoomInfoResponseSplit[1].split('</script>')[0]
			zoomInfoResponseSplit2 = zoomInfoResponseSplit2.replace('&q;','"').replace('&a;','&').replace('&s;','\'').replace('&l;','<').replace('&g;','>')
			zoomInfoJson = json.loads(zoomInfoResponseSplit2)
		except Exception as e:
			time.sleep(2)
			try:
				zoomInfoGetPage = getZISession(companyLink, pageNum)
				zoomInfoResponseSplit = zoomInfoGetPage.text.split('<script id="app-root-state" type="application/json">')
				zoomInfoResponseSplit2 = zoomInfoResponseSplit[1].split('</script>')[0]
				zoomInfoResponseSplit2 = zoomInfoResponseSplit2.replace('&q;','"').replace('&a;','&').replace('&s;','\'').replace('&l;','<').replace('&g;','>')
				zoomInfoJson = json.loads(zoomInfoResponseSplit2)
			except Exception as e:
				time.sleep(2)
				try:
					zoomInfoGetPage = getZISession(companyLink, pageNum)
					zoomInfoResponseSplit = zoomInfoGetPage.text.split('<script id="app-root-state" type="application/json">')
					zoomInfoResponseSplit2 = zoomInfoResponseSplit[1].split('</script>')[0]
					zoomInfoResponseSplit2 = zoomInfoResponseSplit2.replace('&q;','"').replace('&a;','&').replace('&s;','\'').replace('&l;','<').replace('&g;','>')
					zoomInfoJson = json.loads(zoomInfoResponseSplit2)
				except Exception as e:
					print(bcolors.NONERED + '[!] Error scraping ZoomInfo page ' + str(pageNum) + '\n' + bcolors.ENDLINE)
					pass

		for n in range(25):
			try:
				personName = zoomInfoJson["pic-"]["picParsedData"]["table"]["data"][n][1]["fullName"]
				zoomInfoNamesList.append(str(personName))
			except Exception as e:
				pass
		time.sleep(3)

def linkedInGen():
	if (companyid == '' or companyid is None):
		print(bcolors.OKGREEN + '[+] Pulling Company ID for {:s}\n'.format(company) + bcolors.ENDLINE)
		pullid()

	cj = initialReq()
	cj = authReq(cj)

	print(bcolors.OKGREEN + '[+] ...Searching all contacts...' + bcolors.ENDLINE)
	count = 0
	data = recon(None, cj, 1, 0)
	content = json.loads(data)

	count = content["data"]["metadata"]["totalResultCount"]
	print(bcolors.OKGREEN + '[+] Found {} possible employees'.format(count) + bcolors.ENDLINE)
	for i in range(1, int(math.ceil(count/50))+1):
		if i == 1:
			data = recon(None, cj, 49, 0)
		else:
			data = recon(None, cj, 49, i*50)
		content = json.loads(data)

		for user in content["included"]: # Part where the names are created and/or mangled
			if "firstName" in user:
				first_name = re.sub(r'\W+', ' ', user.get("firstName")).split(" ")[0]
				last_name = re.sub(r'\W+', ' ', user.get("lastName")).split(" ")[0]
				full_name = (first_name.capitalize() + " " + last_name.capitalize())

				if full_name.startswith("."):
					pass
				elif len(first_name) <= 1 or len(last_name) <= 1:
					pass
				else:
					linkedInNamesList.append(str(full_name))
		time.sleep(sleep)
  
def hunterPull(hunterApiKey, hunterDomain, hunterNamesList):
	hunter = PyHunter(hunterApiKey)
	hunterAccountInformation = hunter.account_information()
	hunterAvailableSearches = int(hunterAccountInformation["requests"]["searches"]["available"])
	hunterUsedSearches = int(hunterAccountInformation["requests"]["searches"]["used"])
	hunterRemainingSearches = str(hunterAvailableSearches - hunterUsedSearches)
	hunterContinue = input(bcolors.NONERED + '[!] ' + hunterRemainingSearches + ' Searches Remaining, Continue? [Y/n] ' + bcolors.ENDLINE)
	if hunterContinue == "y" or hunterContinue == "Y" or hunterContinue == "":
		hunterContinue = True
	elif hunterContinue == "n" or hunterContinue == "N":
		hunterContinue = False
		print(bcolors.NONERED + '\n[!] Not pulling names from Hunter.IO\n' + bcolors.ENDLINE)
		return
	else:
		print(bcolors.NONERED + '\n[!] Not a valid option, not pulling names from Hunter.IO\n' + bcolors.ENDLINE)
		return

	domainSearchHunterJson = hunter.domain_search(hunterDomain)
	domainHunterPattern = domainSearchHunterJson['pattern']
	hunterPlanname = hunterAccountInformation['plan_name']
	if domainHunterPattern == None:
		domainHunterPattern = 'No pattern identified in Hunter.IO'
	print(bcolors.OKGREEN + '\n[+] Email Pattern Identified: ' + str(domainHunterPattern) + '\n' + bcolors.ENDLINE)

	hunterDomainSearchJSONCreate = json.dumps(domainSearchHunterJson)
	hunterDomainSearchJSONObject = json.loads(hunterDomainSearchJSONCreate)
	listJSONObjectEmails = hunterDomainSearchJSONObject['emails']
	print(bcolors.OKGREEN + '[+] Hunter.IO ' + hunterPlanname + ' plan identified\n' + bcolors.ENDLINE)

	for emailKey in listJSONObjectEmails:
		firstName = emailKey['first_name']
		lastName = emailKey['last_name']
		if firstName == None or lastName == None:
			continue
		else:
			finalName = firstName.capitalize() + " " + lastName.capitalize()
			hunterNamesList.append(str(finalName))

def usStaffMama(company): # Special thanks to bigb0sss for the USStaff function
	usstaff_url = "https://bearsofficialsstore.com/company/%s/page1" % company
	r = requests.get(usstaff_url)

	if r.status_code != 200:
		print("[!] 404 Error! The company name needs to be verified for USStaff. Go to https://bearsofficialsstore.com/ and find the EXACT company name (e.g., t-mobile != t_mobile)")
		pass

	content = (r.text)
	contentSoup = BeautifulSoup(content, 'html.parser')

	for i in contentSoup.find_all('a'):
		page = i.get('href')
		if "page" in page:
			match = re.search('page([0-9]*)', page)
		else:
			match = None
	if match == None:
		lastPage = 1
		lastPageNum = 2
	else:
		lastPage = match.group()[4:]
		lastPage = int(lastPage)
		lastPageNum = lastPage + 1

	for page in range(1, lastPageNum):
		usstaff_url2 = "https://bearsofficialsstore.com/company/%s/page%s" % (company, page)

		r = requests.get(usstaff_url2)
		content = (r.text)
		contentSoup = BeautifulSoup(content, 'html.parser')

		for j in contentSoup.find_all("img"):
			if 'id="imgCompanyLogo"' in str(j):
				continue
			else:
				raw = j.get('alt').lower().split()

				if len(raw) >= 2:
					firstName = raw[0]
					lastName = raw[1:]

					name = firstName + " " + lastName[0]

					fname = ""
					mname = ""
					lname = ""

					if len(lastName) == 1:
						fname = firstName
						mname = '?'
						lname = lastName[0]
					elif len(lastName) == 2:
						fname = firstName
						mname = lastName[0]
						lname = lastName[1]
					else:
						fname = firstName
						lname = lastName[0]

					fname = re.sub('[^A-Za-z]+', '', fname)
					mname = re.sub('[^A-Za-z]+', '', mname)
					lname = re.sub('[^A-Za-z]+', '', lname)

					if len(fname) <= 1 or len(lname) <= 1:
						continue
				else:
					continue

				if mname != "":
					usStaffNamesList.append(str(fname + " " + lname))
					usStaffNamesList.append(str(fname + " " + mname))
				else:
					usStaffNamesList.append(str(fname + " " + lname))

def phonebookCZFunc(phonebookTargetDomain, intelAPIKey):
	ix = intelx(intelAPIKey)

	creditsLeft = ix.GET_CAPABILITIES()["paths"]["/phonebook/search"]["Credit"]
	creditsTotal = ix.GET_CAPABILITIES()["paths"]["/phonebook/search"]["CreditMax"]
	phonebookCredits = str(creditsLeft) + "/" + str(creditsTotal)
	phonebookContinue = input(bcolors.NONERED + '[!] ' + phonebookCredits + ' Phonebook Searches Remaining, Continue? [Y/n] ' + bcolors.ENDLINE)
	if phonebookContinue == "y" or phonebookContinue == "Y" or phonebookContinue == "":
		phonebookContinue = True
	elif phonebookContinue == "n" or phonebookContinue == "N":
		phonebookContinue = False
		print(bcolors.NONERED + '\n[!] Not pulling names from Phonebook\n' + bcolors.ENDLINE)
		return
	else:
		print(bcolors.NONERED + '\n[!] Not a valid option, not pulling names from Phonebook\n' + bcolors.ENDLINE)
		return

	PhonebookSearchFunction = ix.phonebooksearch(phonebookTargetDomain, maxresults=100000, buckets=[], timeout=5, datefrom="", dateto="", sort=4, media=0, terminate=[], target=2)
	for block in PhonebookSearchFunction:
		for result in block['selectors']:
			if result['selectortype'] == 1:
				splitEmailAddress = result['selectorvalue'].split("@")
				phonebookNamesList.append(str(splitEmailAddress[0]))

def statlikelyCreator(): # Thank you AchocolatechipPancake for the addition
	statlikelyList = requests.get("https://github.com/insidetrust/statistically-likely-usernames/raw/master/john.smith.txt", allow_redirects=True, verify=False)
	for nameLine in statlikelyList.iter_lines():
		nameLine = nameLine.decode("utf-8")
		statlikelyFirstName = nameLine.split(".")[0]
		statlikelyLastName = nameLine.split(".")[1]
		statlikelyFullName = str(statlikelyFirstName) + " " + str(statlikelyLastName)
		statlikelyNamesList.append(str(statlikelyFullName))  
		
def mangler(mangleMode, nameList):
	for name in nameList:
		if mangleMode == 0:
			firstPart = name.split(" ")[0]
			lastPart = name.split(" ")[1]
			mangledName = str(firstPart.strip()) + " " + str(lastPart.strip())
		elif mangleMode == 1:
			firstPart = name.split(" ")[0]
			lastPart = name.split(" ")[1]
			mangledName = str(firstPart.strip()) + "." + str(lastPart.strip())
		elif mangleMode == 2:
			firstPart = name.split(" ")[0][:1]
			lastPart = name.split(" ")[1]
			mangledName = str(firstPart.strip()) + "." + str(lastPart.strip())
		elif mangleMode == 3:
			firstPart = name.split(" ")[0]
			lastPart = name.split(" ")[1][:1]
			mangledName = str(firstPart.strip()) + "." + str(lastPart.strip())
		elif mangleMode == 4:
			firstPart = name.split(" ")[0]
			lastPart = name.split(" ")[1]
			mangledName = str(firstPart.strip()) + str(lastPart.strip())
		elif mangleMode == 5:
			firstPart = name.split(" ")[0][:1]
			lastPart = name.split(" ")[1]
			mangledName = str(firstPart.strip()) + str(lastPart.strip())
		elif mangleMode == 6:
			firstPart = name.split(" ")[0]
			lastPart = name.split(" ")[1][:1]
			mangledName = str(firstPart.strip()) + str(lastPart.strip())
		elif mangleMode == 7:
			firstPart = name.split(" ")[0][:1]
			lastPart = name.split(" ")[1]
			mangledName = str(lastPart.strip()) + str(firstPart.strip())
		elif mangleMode == 8:
			firstPart = name.split(" ")[0]
			lastPart = name.split(" ")[1]
			mangledName = str(firstPart.strip()) + "_" + str(lastPart.strip())
		elif mangleMode == 9:
			firstPart = name.split(" ")[0]
			lastPart = name.split(" ")[1]
			mangledName = str(lastPart.strip()) + "_" + str(firstPart.strip())
		elif mangleMode == 10:
			firstPart = name.split(" ")[0][:1]
			lastPart = name.split(" ")[1]
			mangledName = str(lastPart.strip()) + "." + str(firstPart.strip())

		mangledNamesList.append(mangledName.strip())
		if printnames:
			mangledPrintNamesList.append(name.strip() + ' : ' + mangledName.strip())

def main_generator():
	global outputfile
	global mangleMode

	if linkedingen:
		try:
			print(bcolors.OKGREEN + '[+] Pulling Company LinkedIn Employee Names\n' + bcolors.ENDLINE)
			linkedInGen()
			print(bcolors.OKGREEN + '[+] Pulled ' + str(len(linkedInNamesList)) + ' LinkedIn Employees\n' + bcolors.ENDLINE)
		except:
			print(bcolors.NONERED + "[!] Errors Pulling LinkedIn Names" + bcolors.ENDLINE)
			pass

	if zipull:
		print(bcolors.OKGREEN + '[+] Pulling ZoomInfo Company Employee Names\n' + bcolors.ENDLINE)
		if proxylist != 'None':
			print(bcolors.OKGREEN + '[+] Using Proxy File ' + str(proxylist) + '\n' + bcolors.ENDLINE)
		if singleproxy != 'None':
			print(bcolors.OKGREEN + '[+] Using ' + str(singleproxy) + ' as the Proxy\n' + bcolors.ENDLINE)
		try:
			extractZINames(zilink)
			print(bcolors.OKGREEN + '[+] Pulled ' + str(len(zoomInfoNamesList)) + ' ZoomInfo Employees\n' + bcolors.ENDLINE)
		except:
			print(bcolors.NONERED + "[!] Errors Pulling ZoomInfo Names" + bcolors.ENDLINE)
			pass

	if hunterIO:
		try:
			print(bcolors.OKGREEN + '[+] Pulling emails from Hunter.io\n' + bcolors.ENDLINE)
			hunterPull(hunterApiKey, hunterDomain, hunterNamesList)
			print(bcolors.OKGREEN + '[+] Pulled ' + str(len(hunterNamesList)) + ' Hunter.io Employees\n' + bcolors.ENDLINE)
		except:
			print(bcolors.NONERED + "[!] Errors Pulling Hunter.io Emails" + bcolors.ENDLINE)
			pass

	if usstaff:
		try:
			print(bcolors.OKGREEN + '[+] Pulling names from USStaff\n' + bcolors.ENDLINE)
			usStaffMama(usstaffcompany)
			print(bcolors.OKGREEN + '[+] Pulled ' + str(len(usStaffNamesList)) + ' USStaff Employees\n' + bcolors.ENDLINE)
		except:
			print(bcolors.NONERED + "[!] Errors scraping USStaff names" + bcolors.ENDLINE)
			pass

	if phonebookCZ:
		try:
			print(bcolors.OKGREEN + '[+] Pulling names from Phonebook\n' + bcolors.ENDLINE)
			phonebookCZFunc(phonebookTargetDomain, intelAPIKey)
			print(bcolors.OKGREEN + '[+] Pulled ' + str(len(phonebookNamesList)) + ' Employees from Phonebook\n' + bcolors.ENDLINE)
		except:
			print(bcolors.NONERED + "[!] Errors pulling Phonebook names" + bcolors.ENDLINE)
			pass

	if statlikely:
		statlikelyContinue = input(bcolors.OKGREEN + '[+] Statistically Likely Option enabled, this will generate a VERY long list. Continue? [Y/n] ' + bcolors.ENDLINE)
		if statlikelyContinue == "y" or statlikelyContinue == "Y" or statlikelyContinue == "":
			statlikelyContinue = True
		elif statlikelyContinue == "n" or statlikelyContinue == "N":
			statlikelyContinue = False
			print(bcolors.NONERED + '\n[!] Not pulling names from Statistically Likely\n' + bcolors.ENDLINE)
			return
		else:
			print(bcolors.NONERED + '\n[!] Not a valid option, not pulling names from Statistically Likely\n' + bcolors.ENDLINE)
			return
		if statlikelyContinue:
			try:
				print(bcolors.OKGREEN + '[+] Pulling names from Statistically Likely\n' + bcolors.ENDLINE)
				statlikelyCreator()
				print(bcolors.OKGREEN + '[+] Pulled 248,231 Statistically Likely Names\n' + bcolors.ENDLINE)
			except:
				print(bcolors.NONERED + "[!] Errors pulling Statistically Likely Names" + bcolors.ENDLINE)
				pass

	if len(zoomInfoNamesList) == 0 and len(linkedInNamesList) == 0 and len(usStaffNamesList) == 0 and len(hunterNamesList) == 0 and len(phonebookNamesList) == 0 and len(statlikelyNamesList) == 0:
		print(bcolors.NONERED + "[!] No names obtained, Exiting...\n" + bcolors.ENDLINE)
		sys.exit()

	printNamesModifierList = linkedInNamesList + zoomInfoNamesList + hunterNamesList + usStaffNamesList + statlikelyNamesList
	printNamesModifierList = list(set(printNamesModifierList))
	for potentialName in printNamesModifierList:
		finalPotentialName = unidecode.unidecode(potentialName.capitalize())
		printNamesFullList.append(str(finalPotentialName))
	mangler(mangleMode, printNamesFullList)

	totalPotentialUsers = int(len(printNamesFullList)) + int(len(phonebookNamesList))
	totalPotentialUsersMangled = int(len(mangledNamesList)) + int(len(phonebookNamesList))

	if outputfile != '':
		if os.path.exists(outputfile):
			del_outfile = input(bcolors.NONERED + '[!] Output File exists, overwrite? [Y/n] ' + bcolors.ENDLINE)
			print('\n')
			if del_outfile == 'y' or 'Y' or '':
				os.remove(outputfile)
			elif del_outfile == 'n' or 'N':
				print(bcolors.NONERED + '[-] Not overwriting file, exiting...' + bcolors.ENDLINE)
				sys.exit()
			else:
				print(bcolors.NONERED + '[!] Not a valid option, exiting...' + bcolors.ENDLINE)
				sys.exit()

		if mangleMode == 0:
			with open(outputfile, mode='wt', encoding='utf-8') as writeOutFile:
				writeOutFile.write('\n'.join(printNamesFullList))
				if phonebookCZ:
					writeOutFile.write('\n'.join(phonebookNamesList))
		if mangleMode > 0:
			with open(outputfile, mode='wt', encoding='utf-8') as writeOutFile:
				writeOutFile.write('\n'.join(mangledNamesList))
				if phonebookCZ:
					writeOutFile.write('\n'.join(phonebookNamesList))

	if printnames:
		if mangleMode == 0:
			for i in list(printNamesFullList):
				print(str(i))
			if phonebookCZ:
				for n in list(phonebookNamesList):
					print(str(n))
		if mangleMode > 0:
			for i in list(mangledPrintNamesList):
				print(str(i))
			if phonebookCZ:
				for n in list(phonebookNamesList):
					print(str(n))

	if mangleMode == 0:
		print(bcolors.OKGREEN + '\n[+] Found a total of ' + str(totalPotentialUsers) + ' potential usernames\n' + bcolors.ENDLINE)
	if mangleMode > 0:
		print(bcolors.OKGREEN + '\n[+] Found a total of ' + str(totalPotentialUsersMangled) + ' potential usernames\n' + bcolors.ENDLINE)

if __name__ == "__main__":
	main_generator()
