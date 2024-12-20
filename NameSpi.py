#!/usr/bin/python3

from __future__ import division
from argparse import RawTextHelpFormatter
from pyhunter import PyHunter
import json, math, argparse, sys, os, urllib3, requests, getpass, unidecode, yaml, yaspin, time, logging
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

banner = """
 _   _                      ____        _ 
| \ | | __ _ _ __ ___   ___/ ___| _ __ (_) 
|  \| |/ _` | '_ ` _ \ / _ \___ \| '_ \| | 
| |\  | (_| | | | | | |  __/___) | |_) | | 
|_| \_|\__,_|_| |_| |_|\___|____/| .__/|_| 
                                 |_| v1.7.1 
        Author: #Waffl3ss \n\n"""
print(banner)

# Parse user arguments
parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument('-li', dest='linkedingen', default=False, required=False, help="Run the LinkedIn module", action='store_true')
parser.add_argument('-hio', dest='hunterIO', required=False, default=False, help="Pull Emails from Hunter.io", action='store_true')
parser.add_argument('-sl', dest='statlikely', required=False, default=False, help="Use Statistically Likely Usernames in output (CAUTION: Creates a VERY long list) Special Thanks: AchocolatechipPancake", action='store_true')
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
parser.add_argument('-m', dest='mangleMode', required=False, default=0, help="Mangle Mode (use '-mo' to list mangle options). Only works with an output file (-o)")
parser.add_argument('-mo', dest='mangleOptions', required=False, default=False, help="List Mangle Mode Options", action="store_true")
parser.add_argument('-yaml', dest='useyamlfile', required=False, default='', help="Use YAML input file with options")
parser.add_argument('-debug', dest='debugMode', required=False, default=False, help="Turn on debug mode for error output", action="store_true")
parser.add_argument('-lir', dest='linkedInRetryAmount', required=False, default=10, help="Amount of times to attempt the LinkedIn Security bypass")

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
useyamlfile = str(args.useyamlfile) # Bool
statlikely = args.statlikely # Bool
debugMode = args.debugMode # Bool
linkedInRetryAmount = int(args.linkedInRetryAmount) # Int
retrySecCheck = 1
retryLILogin = 1

logger = logging.getLogger(__name__)
logging.basicConfig(filename='namespi.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logger.addHandler(console_handler)

if debugMode:
	logger.setLevel(logging.DEBUG)
	console_handler.setLevel(logging.DEBUG)
	console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

# Colors for terminal output because Waffles likes pretty things
class bcolors:
		OKGREEN = '\033[92m'
		BOLD = '\033[1m'
		NONERED = '\033[91m'
		WARNYELL = '\033[93m'
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
				logger.debug(f"YAML module exception: {yamlexception}")
				logger.error("YAML File Error... Exiting... ")
				sys.exit()

		if linkedingen:
			if linkedingen and yamlcontents["CompanyID"] == '' and yamlcontents["CompanyName"] != '':
					company = yamlcontents["CompanyName"]
			elif linkedingen and args.companyid is None and args.company == '' and yamlcontents["CompanyID"] == '' and yamlcontents["CompanyName"] != '':
					company = input("Company Name: ")
			elif linkedingen and yamlcontents["CompanyID"] != '':
					companyid = yamlcontents["CompanyID"]
			else:
					logger.error("YAML Error getting Company Name... ")

			if linkedingen and yamlcontents["CompanyID"] != '':
					companyid = yamlcontents["CompanyID"]

			if linkedingen and yamlcontents["LinkedInUsername"] != '':
				linkedin_username = yamlcontents["LinkedInUsername"]
			elif linkedingen and args.linkedin_username is None:
				linkedin_username = input("LinkedIn Username: ")
			else:
				logger.error("YAML Error with LinkedIn Username... ")

			if linkedingen and yamlcontents["LinkedInPassword"] != '':
				linkedin_password = yamlcontents["LinkedInPassword"]
			elif linkedingen and args.linkedin_password is None:
				linkedin_password = getpass.getpass("LinkedIn Password: ")
			else:
				logger.error("YAML Error with LinkedIn Password... ")

		if hunterIO:
			if hunterIO and yamlcontents["HunterIODomain"] != '':
				hunterDomain = yamlcontents["HunterIODomain"]
			elif hunterIO and args.hunterDomain is None:
				hunterDomain = input("Hunter.io Domain to Query: ")
			else:
				logger.error("YAML Error with HunterIO Domain... ")

			if hunterIO and yamlcontents["HunterIOKey"] != '':
				hunterApiKey = yamlcontents["HunterIOKey"]
			elif hunterIO and args.hunterApiKey is None:
				hunterApiKey = input("Hunter.io API Key: ")
			else:
				logger.error("YAML Error with HunterIO API Key... ")
	else:
		logger.error("YAML file does not exist, exiting....")
		sys.exit()

else:
	if linkedingen and args.companyid is None and args.company == '':
		company = input("     Company Name: ")
	if linkedingen and args.linkedin_username is None:
		linkedin_username = input("     LinkedIn Username: ")
	if linkedingen and args.linkedin_password is None:
		linkedin_password = getpass.getpass("     LinkedIn Password: ")
	if hunterIO and args.hunterDomain is None:
		hunterDomain = input("     Hunter.io Domain to Query: ")
	if hunterIO and args.hunterApiKey is None:
		hunterApiKey = input("     Hunter.io API Key: ")

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0'

if outputfile == '' and not printnames:
	logger.error("No output option select, choose an output file (-o) or print to screen (-pn)... ")
	sys.exit()

linkedInNamesList = []
hunterNamesList = []
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
		hunterContinue = input(f'\n{hunterRemainingSearches} Searches Remaining, Continue? [Y/n] ')
		print('\n')
		if hunterContinue == "y" or hunterContinue == "Y" or hunterContinue == "":
			hunterContinue = True
		elif hunterContinue == "n" or hunterContinue == "N":
			hunterContinue = False
			logger.error("Not pulling names from Hunter.IO")
			return
		else:
			logger.error("Not a valid option, not pulling names from Hunter.IO")
			return

		domainSearchHunterJson = hunter.domain_search(hunterDomain)
		domainHunterPattern = domainSearchHunterJson['pattern']
		hunterPlanname = hunterAccountInformation['plan_name']
		if domainHunterPattern == None:
			domainHunterPattern = 'No pattern identified in Hunter.IO'
		logger.info(f"Email Pattern Identified: {domainHunterPattern}")

		hunterDomainSearchJSONCreate = json.dumps(domainSearchHunterJson)
		hunterDomainSearchJSONObject = json.loads(hunterDomainSearchJSONCreate)
		listJSONObjectEmails = hunterDomainSearchJSONObject['emails']
		logger.info(f"Hunter.IO {hunterPlanname} plan identified")

		with yaspin.yaspin(text=" - Running Hunter.IO Enumeration"):
			for emailKey in listJSONObjectEmails:
				firstName = emailKey['first_name']
				lastName = emailKey['last_name']
				if firstName == None or lastName == None:
					continue
				else:
					finalName = firstName.capitalize() + " " + lastName.capitalize()
					hunterNamesList.append(str(finalName))
	except Exception as hunterexception:
		logger.debug(f"Hunter module exception: {hunterexception}")
		pass

def statlikelyCreator(): 
	try:
		statlikelyList = requests.get("https://github.com/insidetrust/statistically-likely-usernames/raw/master/john.smith.txt", allow_redirects=True, verify=False)
		for nameLine in statlikelyList.iter_lines():
			nameLine = nameLine.decode("utf-8")
			statlikelyFirstName = nameLine.split(".")[0]
			statlikelyLastName = nameLine.split(".")[1]
			statlikelyFullName = str(statlikelyFirstName) + " " + str(statlikelyLastName)
			statlikelyNamesList.append(str(statlikelyFullName))
	except Exception as statlikelyexception:
		logger.debug(f"Stat Likely module exception: {statlikelyexception}")
		pass

def linkedInGen():
	global retrySecCheck
	global retryLILogin
	if retrySecCheck >= linkedInRetryAmount:
		logger.error(f'LinkedIn Security Check Implemented, {linkedInRetryAmount} retries attemped and failed. Please use the README for more info.')
		sys.exit(0)

	if retryLILogin >= 6:
		logger.error('Attempted to login to LinkedIn 5 times with no success. Please use the README for more info. ')
		sys.exit(0)

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
					logger.error('Failed to pull CSRF token')

		# Conduct Login and Store in Session
		loginData = {"session_key": linkedin_username, "session_password": linkedin_password, "isJsEnabled": "false", "loginCsrfParam": csrfCookie}
		loginRequest = linkedinSession.post("https://www.linkedin.com/checkpoint/lg/login-submit", data=loginData, timeout=timeout, verify=False)

		if "<title>Security Verification | LinkedIn</title>" in loginRequest.content.decode("utf-8"):
			retrySecCheck += 1
			logger.debug(f'LinkedIn Security Check Bypass Attempt #{retrySecCheck}')
			linkedInGen()
		else:
			if 'li_at' in linkedinSession.cookies.get_dict():
				logger.debug('LinkedIn Login Successful')
			else:
				retryLILogin += 1
				logger.debug(f'LinkedIn Login Unsuccessful... Retrying attempt #{retryLILogin}')
				time.sleep(3)
				linkedInGen()
		
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
			logger.info(f'Pulling Company ID for {company.strip()}')
			query = "includeWebMetadata=true&variables=(start:0,origin:SWITCH_SEARCH_VERTICAL,query:(keywords:" + str(company) + ",flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:resultType,value:List(COMPANIES))),includeFiltersInResponse:false))&&queryId=voyagerSearchDashClusters.8456d8ebf04d20b152309b0c7cfabee2"
			req = linkedinSession.get("https://www.linkedin.com/voyager/api/graphql?" + query, verify=False)
			jsonObject = json.loads(req.content.decode())

			for companyObject in jsonObject["included"]:
				try:
					id = companyObject["trackingUrn"].split(":")[3]
					companyname = companyObject["title"]["text"]
					print("   {:.<55}: {:s}".format(companyname + " ",id))
				except:
					pass

			companyid = input("\n   Select company ID value: ")
			print('\n')

		employeeSearchQuery = "/voyager/api/graphql?variables=(start:0,origin:COMPANY_PAGE_CANNED_SEARCH,query:(flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:currentCompany,value:List(" + str(companyid) + ")),(key:resultType,value:List(PEOPLE))),includeFiltersInResponse:false))&&queryId=voyagerSearchDashClusters.c4f33252de52295107ac12f946d34b0d"
		employeeSearchRequest = linkedinSession.get("https://www.linkedin.com" + employeeSearchQuery, verify=False)
		jsonUserListObject = json.loads(employeeSearchRequest.content.decode())

		count = 0
		count = jsonUserListObject["data"]["data"]["searchDashClustersByAll"]["metadata"]["totalResultCount"]
		logger.info(f'Found {count} possible employees\n')

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
					logger.debug(f'LinkedIn user module exception: {linkedinuserexception}')
					pass
	except Exception as linkedinexception:
		logger.debug(f'LinkedIn module exception: {linkedinexception}')
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
			del_outfile = input(bcolors.WARNYELL + 'Output File exists, overwrite? [Y/n] ' + bcolors.ENDLINE)
			print('\n')
			if del_outfile == 'y' or 'Y' or '':
				os.remove(outputfile)
			elif del_outfile == 'n' or 'N':
				logger.error('Not overwriting file, exiting...')
				sys.exit()
			else:
				logger.error('Not a valid option, exiting...')
				sys.exit()

	if linkedingen:
		try:
			logger.info('Pulling Company LinkedIn Employee Names')
			linkedInGen()
			logger.info(f'Pulled {len(linkedInNamesList)} LinkedIn Employees')
		except:
			logger.error('Errors Pulling LinkedIn Names')
			pass

	if hunterIO:
		try:
			logger.info('Pulling emails from Hunter.io')
			hunterPull(hunterApiKey, hunterDomain, hunterNamesList)
			logger.info(f'Pulled {len(hunterNamesList)} Hunter.io Employees')
		except:
			logger.error('Errors Pulling Hunter.io Emails')
			pass

	if statlikely:
		statlikelyContinue = input(bcolors.OKGREEN + '  Statistically Likely Option enabled, this will generate a VERY long list. Continue? [Y/n] ' + bcolors.ENDLINE)
		if statlikelyContinue == "y" or statlikelyContinue == "Y" or statlikelyContinue == "":
			statlikelyContinue = True
		elif statlikelyContinue == "n" or statlikelyContinue == "N":
			statlikelyContinue = False
			logger.error('Not pulling names from Statistically Likely')
			return
		else:
			logger.error('Not a valid option, not pulling names from Statistically Likely')
			return
		if statlikelyContinue:
			try:
				logger.info('Pulling names from Statistically Likely')
				with yaspin.yaspin(text=" - Running StatLikely Enumeration"):
					statlikelyCreator()
				logger.info('Pulled 248,231 Statistically Likely Names')
			except:
				logger.error('Errors pulling Statistically Likely Names')
				pass

	if len(linkedInNamesList) == 0 and len(hunterNamesList) == 0 and len(statlikelyNamesList) == 0:
		logger.error('No names obtained, Exiting...')
		sys.exit()

	printNamesModifierList = linkedInNamesList + hunterNamesList + statlikelyNamesList
	printNamesModifierList = list(set(printNamesModifierList))
	for potentialName in printNamesModifierList:
		finalPotentialName = unidecode.unidecode(potentialName.capitalize())
		printNamesFullList.append(str(finalPotentialName).lower())
	mangler(mangleMode, printNamesFullList)

	totalPotentialUsers = int(len(printNamesFullList))
	totalPotentialUsersMangled = int(len(mangledNamesList))

	if outputfile != '':
		if mangleMode == 0:
			with open(outputfile, mode='wt', encoding='utf-8') as writeOutFile:
				writeOutFile.write('\n'.join(printNamesFullList))
		if mangleMode > 0:
			with open(outputfile, mode='wt', encoding='utf-8') as writeOutFile:
				writeOutFile.write('\n'.join(mangledNamesList))

	if printnames:
		print('\n')
		if mangleMode == 0:
			for i in list(printNamesFullList):
				print(str(i))
		if mangleMode > 0:
			for i in list(mangledPrintNamesList):
				print(str(i))
		print('\n')

	if mangleMode == 0:
		logger.info(f'Found a total of {totalPotentialUsers} potential usernames')
	if mangleMode > 0:
		logger.info(f'Found a total of {totalPotentialUsersMangled} potential usernames')

if __name__ == "__main__":
	main_generator()
