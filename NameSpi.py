#!/usr/bin/python3

from __future__ import division
from argparse import RawTextHelpFormatter
from pyhunter import PyHunter
from bs4 import BeautifulSoup
import json, math, argparse, re, sys, os, urllib3, requests, getpass, unidecode, httpimport, yaml, yaspin, time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with httpimport.remote_repo('https://raw.githubusercontent.com/IntelligenceX/SDK/master/Python/'):
	from intelxapi import intelx

banner = """
  _   _                      ____        _ 
 | \ | | __ _ _ __ ___   ___/ ___| _ __ (_) 
 |  \| |/ _` | '_ ` _ \ / _ \___ \| '_ \| | 
 | |\  | (_| | | | | | |  __/___) | |_) | | 
 |_| \_|\__,_|_| |_| |_|\___|____/| .__/|_| 
                                  |_| v1.5 
             Author: #Waffl3ss \n\n"""
print(banner)

# Parse user arguments
parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument('-li', dest='linkedingen', default=False, required=False, help="Run the LinkedIn module", action='store_true')
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
parser.add_argument('-hapi', dest='hunterApiKey', required=False, help="Hunter.io API Key")
parser.add_argument('-hdom', dest='hunterDomain', required=False, help="Domain to query in Hunter.io")
parser.add_argument('-uc', dest='usstaffcompany', default='', required=False, help="Exact company name on USStaff")
parser.add_argument('-m', dest='mangleMode', required=False, default=0, help="Mangle Mode (use '-mo' to list mangle options). Only works with an output file (-o)")
parser.add_argument('-mo', dest='mangleOptions', required=False, default=False, help="List Mangle Mode Options", action="store_true")
parser.add_argument('-yaml', dest='useyamlfile', required=False, default='', help="Use YAML input file with options")
parser.add_argument('-debug', dest='debugMode', required=False, default=False, help="Turn on debug mode for error output", action="store_true")
args = parser.parse_args()

# Assign user arguments to variables we can use (old habit of mine)
company = str(args.company) # String
companyid = args.companyid # Int
sleep = int(args.sleep) # Int
timeout = int(args.timeout) # Int
outputfile = str(args.outputfile) # String
linkedingen = args.linkedingen # Bool
printnames = args.printnames # Bool
hunterIO = args.hunterIO # Bool
hunterApiKey = args.hunterApiKey # String
hunterDomain = args.hunterDomain # String
linkedin_username = str(args.linkedin_username) # String
linkedin_password = str(args.linkedin_password) # String
mangleMode = int(args.mangleMode) # Int
mangleOptions = args.mangleOptions # Bool
usstaff = args.usstaff # Bool
usstaffcompany = str(args.usstaffcompany) # String
phonebookCZ = args.phonebookCZ # Bool
phonebookTargetDomain = str(args.phonebookTargetDomain) # String
intelAPIKey = str(args.intelAPIKey) # String
useyamlfile = str(args.useyamlfile) # Bool
statlikely = args.statlikely # Bool
debugMode = args.debugMode # Bool

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
			try:
				yamlcontents = yaml.safe_load(yamlfile)
			except Exception as yamlexception:
				if debugMode:
					print(bcolors.NONERED + "[DEBUG] YAML module exception: " + yamlexception + bcolors.ENDLINE)
					sys.exit()
				else: 
					print(bcolors.NONERED + "[!] YAML File Error... Exiting... "+ bcolors.ENDLINE)
					sys.exit()

		if linkedingen:
			if linkedingen and yamlcontents["CompanyID"] == '' and yamlcontents["CompanyName"] != '':
					company = yamlcontents["CompanyName"]
			elif linkedingen and args.companyid is None and args.company == '' and yamlcontents["CompanyID"] == '' and yamlcontents["CompanyName"] != '':
					company = input("Company Name: ")
			elif linkedingen and yamlcontents["CompanyID"] != '':
					companyid = yamlcontents["CompanyID"]
			else:
					print(bcolors.NONERED + '[!] YAML Error getting Company Name... ' + bcolors.ENDLINE)

			if linkedingen and yamlcontents["CompanyID"] != '':
					companyid = yamlcontents["CompanyID"]

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

		if hunterIO:
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

		if usstaff:
			if usstaff and yamlcontents["USStaffCompanyName"] != '':
				usstaffcompany = yamlcontents["USStaffCompanyName"]
			elif usstaff and args.usstaffcompany == '':
				usstaffcompany = input("USStaff Name: ")
			else:
				print(bcolors.NONERED + '[!] YAML Error with USStaff Company... ' + bcolors.ENDLINE)

		if phonebookCZ:
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

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0'

if outputfile == '' and not printnames:
	print(bcolors.NONERED + '[!] No output option select, choose an output file (-o) or print to screen (-pn)... ' + bcolors.ENDLINE)
	sys.exit()

linkedInNamesList = []
hunterNamesList = []
usStaffNamesList = []
phonebookNamesList = []
printNamesModifierList = []
printNamesFullList = []
mangledNamesList = []
mangledPrintNamesList = []
statlikelyNamesList = []

def hunterPull(hunterApiKey, hunterDomain, hunterNamesList):
	try:
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

		with yaspin.yaspin(text=" - Running Hunter.IO Enumeration"):
			hunterDomainSearchJSONCreate = json.dumps(domainSearchHunterJson)
			hunterDomainSearchJSONObject = json.loads(hunterDomainSearchJSONCreate)
			listJSONObjectEmails = hunterDomainSearchJSONObject['emails']
			print(bcolors.OKGREEN + '\n[+] Hunter.IO ' + hunterPlanname + ' plan identified\n' + bcolors.ENDLINE)

			for emailKey in listJSONObjectEmails:
				firstName = emailKey['first_name']
				lastName = emailKey['last_name']
				if firstName == None or lastName == None:
					continue
				else:
					finalName = firstName.capitalize() + " " + lastName.capitalize()
					hunterNamesList.append(str(finalName))
	except Exception as hunterexception:
		if debugMode:
			print(bcolors.NONERED + "[DEBUG] Hunter module exception: " + hunterexception + bcolors.ENDLINE)
			sys.exit()
		else: 
			pass

def usStaffMama(company): # Special thanks to bigb0sss for the USStaff function
	try:
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
	except Exception as usstaffexception:
		if debugMode:
			print(bcolors.NONERED + "[DEBUG] USStaff module exception: " + usstaffexception + bcolors.ENDLINE)
			sys.exit()
		else: 
			pass

def phonebookCZFunc(phonebookTargetDomain, intelAPIKey):
	try:
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

		with yaspin.yaspin(text=" - Running PhoneBook.CZ Enumeration"):
			PhonebookSearchFunction = ix.phonebooksearch(phonebookTargetDomain, maxresults=100000, buckets=[], timeout=5, datefrom="", dateto="", sort=4, media=0, terminate=[], target=2)
			for block in PhonebookSearchFunction:
				for result in block['selectors']:
					if result['selectortype'] == 1:
						splitEmailAddress = result['selectorvalue'].split("@")
						phonebookNamesList.append(str(splitEmailAddress[0]))

	except Exception as phonebookexception:
		if debugMode:
			print(bcolors.NONERED + "[DEBUG] PhoneBook.cz module exception: " + phonebookexception + bcolors.ENDLINE)
			sys.exit()
		else: 
			pass

def statlikelyCreator(): # Thank you AchocolatechipPancake for the addition
	try:
		statlikelyList = requests.get("https://github.com/insidetrust/statistically-likely-usernames/raw/master/john.smith.txt", allow_redirects=True, verify=False)
		for nameLine in statlikelyList.iter_lines():
			nameLine = nameLine.decode("utf-8")
			statlikelyFirstName = nameLine.split(".")[0]
			statlikelyLastName = nameLine.split(".")[1]
			statlikelyFullName = str(statlikelyFirstName) + " " + str(statlikelyLastName)
			statlikelyNamesList.append(str(statlikelyFullName))
	except Exception as statlikelyexception:
		if debugMode:
			print(bcolors.NONERED + "[DEBUG] Stat Likely module exception: " + statlikelyexception + bcolors.ENDLINE)
			sys.exit()
		else: 
			pass

def linkedInGen():
	try:
		global companyid
		# Create Login Session and Hold Cookies
		linkedinSession = requests.Session()
		linkedinSession.headers.update({'User-Agent': user_agent})
		linkedinSession.get('https://www.linkedin.com/uas/login?trk=guest_homepage-basic_nav-header-signin', verify=False)

		# Get CSRF cookie
		for cookie in linkedinSession.cookies:
			if cookie.name == "bcookie":
				csrfCookie = str(cookie.value.split('&')[1][:-1])
				if csrfCookie is None:
					print(bcolors.NONERED + '[-] Failed to pull CSRF token' + bcolors.ENDLINE)

		# Condcut Login and Store in Session
		loginData = {"session_key": linkedin_username, "session_password": linkedin_password, "isJsEnabled": "false", "loginCsrfParam": csrfCookie}
		loginRequest = linkedinSession.post("https://www.linkedin.com/checkpoint/lg/login-submit", data=loginData, timeout=timeout, verify=False)

		if "<title>Security Verification | LinkedIn</title>" in loginRequest.content.decode("utf-8"):
			print(bcolors.NONERED + '[-] LinkedIn Security Check Implemented, try again (check README for more information)' + bcolors.ENDLINE)
			sys.exit(0)
		else:
			if 'li_at' in linkedinSession.cookies.get_dict():
				if debugMode:
					print(bcolors.OKGREEN + '[+] LinkedIn Login Successful' + bcolors.ENDLINE)
			else:
				print(bcolors.NONERED + '[-] Login Unsuccessful... Exiting' + bcolors.ENDLINE)
				sys.exit(0)

		specialCookieList = ''
		for cookie in linkedinSession.cookies:
			if cookie.name == "JSESSIONID":
				ajaxcookie = cookie.value[1:-1]
			specialCookieList += cookie.name + "=" + cookie.value + "; "

		linkedinSession.headers.update({
			"Host": "www.linkedin.com",
			"User-Agent": user_agent,
			"Accept": "application/vnd.linkedin.normalized+json+2.1",
			"x-restli-protocol-version": "2.0.0",
			"Cookie": specialCookieList,
			"Csrf-Token": ajaxcookie,
			})

		if (companyid == '' or companyid is None):
			print(bcolors.OKGREEN + '[+] Pulling Company ID for {:s}\n'.format(company.strip()) + bcolors.ENDLINE)

			query = "includeWebMetadata=true&variables=(start:0,origin:SWITCH_SEARCH_VERTICAL,query:(keywords:" + str(company) + ",flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:resultType,value:List(COMPANIES))),includeFiltersInResponse:false))&&queryId=voyagerSearchDashClusters.8456d8ebf04d20b152309b0c7cfabee2"
			req = linkedinSession.get("https://www.linkedin.com/voyager/api/graphql?" + query, verify=False)
			jsonObject = json.loads(req.content.decode())

			for companyObject in jsonObject["included"]:
				try:
					id = companyObject["trackingUrn"].split(":")[3]
					companyname = companyObject["title"]["text"]
					print("{:.<55}: {:s}".format(companyname + " ",id))
				except:
					pass

			companyid = input("\nSelect company ID value: ")  

		employeeSearchQuery = "/voyager/api/graphql?variables=(start:0,origin:COMPANY_PAGE_CANNED_SEARCH,query:(flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:currentCompany,value:List(" + str(companyid) + ")),(key:resultType,value:List(PEOPLE))),includeFiltersInResponse:false))&&queryId=voyagerSearchDashClusters.c4f33252de52295107ac12f946d34b0d"
		employeeSearchRequest = linkedinSession.get("https://www.linkedin.com" + employeeSearchQuery, verify=False)
		jsonUserListObject = json.loads(employeeSearchRequest.content.decode())

		count = 0
		count = jsonUserListObject["data"]["data"]["searchDashClustersByAll"]["metadata"]["totalResultCount"]
		print(bcolors.OKGREEN + '[+] Found {} possible employees'.format(count) + bcolors.ENDLINE)

		with yaspin.yaspin(text=" - Running LinkedIn Enumeration"):
			for countNum in range(0,int((int(math.ceil(count / 10.0)) * 10) / 10)):
				try:
					pageQuery = "/voyager/api/graphql?variables=(start:" + str(countNum * 10) + ",origin:COMPANY_PAGE_CANNED_SEARCH,query:(flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:currentCompany,value:List(" + str(companyid) + ")),(key:resultType,value:List(PEOPLE))),includeFiltersInResponse:false))&&queryId=voyagerSearchDashClusters.c4f33252de52295107ac12f946d34b0d"
					pageRequest = linkedinSession.get("https://www.linkedin.com" + pageQuery, verify=False)
					jsonUserContent = json.loads(pageRequest.content.decode())
					for person in jsonUserContent["included"]:
						if "title" in person:
							nameField = person["title"]["text"]
							if "," in nameField:
								cleanNameField = nameField.split(",")[0]
								first_name = cleanNameField.split(" ")[0]
								last_name = cleanNameField.split(" ")[-1]
							else:
								first_name = nameField.split(" ")[0]
								last_name = nameField.split(" ")[-1]

							if len(first_name) <= 1 or len(last_name) <= 1:
								pass
							elif "LinkedIn" in first_name:
								pass
							elif "." in last_name:
								pass
							elif "." in first_name:
								pass
							else:
								full_name = (first_name.capitalize() + " " + last_name.capitalize())
								if full_name.startswith("."):
									pass
								else:
									linkedInNamesList.append(str(full_name))
					time.sleep(sleep)

				except Exception as linkedinuserexception:
					if debugMode:
						print(bcolors.NONERED + "[DEBUG] LinkedIn user module exception: " + linkedinuserexception + bcolors.ENDLINE)
						sys.exit()
					else:
						pass
	except Exception as linkedinexception:
		if debugMode:
			print(bcolors.NONERED + "[DEBUG] LinkedIn module exception: " + linkedinexception + bcolors.ENDLINE)
			sys.exit()
		else:
			pass

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

	if linkedingen:
		try:
			print(bcolors.OKGREEN + '[+] Pulling Company LinkedIn Employee Names\n' + bcolors.ENDLINE)
			linkedInGen()
			print(bcolors.OKGREEN + '[+] Pulled ' + str(len(linkedInNamesList)) + ' LinkedIn Employees\n' + bcolors.ENDLINE)
		except:
			print(bcolors.NONERED + "[!] Errors Pulling LinkedIn Names" + bcolors.ENDLINE)
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
			with yaspin.yaspin(text=" - Running US Staff Enumeration"):
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
				with yaspin.yaspin(text=" - Running StatLikely Enumeration"):
					statlikelyCreator()
				print(bcolors.OKGREEN + '[+] Pulled 248,231 Statistically Likely Names\n' + bcolors.ENDLINE)
			except:
				print(bcolors.NONERED + "[!] Errors pulling Statistically Likely Names" + bcolors.ENDLINE)
				pass

	if len(linkedInNamesList) == 0 and len(usStaffNamesList) == 0 and len(hunterNamesList) == 0 and len(phonebookNamesList) == 0 and len(statlikelyNamesList) == 0:
		print(bcolors.NONERED + "[!] No names obtained, Exiting...\n" + bcolors.ENDLINE)
		sys.exit()

	printNamesModifierList = linkedInNamesList + hunterNamesList + usStaffNamesList + statlikelyNamesList
	printNamesModifierList = list(set(printNamesModifierList))
	for potentialName in printNamesModifierList:
		finalPotentialName = unidecode.unidecode(potentialName.capitalize())
		printNamesFullList.append(str(finalPotentialName))
	mangler(mangleMode, printNamesFullList)

	totalPotentialUsers = int(len(printNamesFullList)) + int(len(phonebookNamesList))
	totalPotentialUsersMangled = int(len(mangledNamesList)) + int(len(phonebookNamesList))

	if outputfile != '':
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
		print(bcolors.OKGREEN + '[+] Found a total of ' + str(totalPotentialUsers) + ' potential usernames\n' + bcolors.ENDLINE)
	if mangleMode > 0:
		print(bcolors.OKGREEN + '[+] Found a total of ' + str(totalPotentialUsersMangled) + ' potential usernames\n' + bcolors.ENDLINE)

if __name__ == "__main__":
	main_generator()
