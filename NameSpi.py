#!/usr/bin/python3

from __future__ import division
from http.cookiejar import CookieJar
from urllib.request import Request, build_opener, HTTPCookieProcessor, HTTPHandler, HTTPSHandler, urlopen
from urllib.parse import urlencode
from argparse import RawTextHelpFormatter
from pyhunter import PyHunter
import time, json, math, ssl, argparse, re, sys, os, codecs, hashlib, hmac, base64, urllib, requests, pyfiglet, cloudscraper, getpass

prebanner = pyfiglet.figlet_format("NameSpi")
banner = "\n" + prebanner + "\tv0.7\t#Waffl3ss\n"
print(banner)

# Parse user arguments
parser = argparse.ArgumentParser(description='Company Linkedin user enumeration and cleanup.', formatter_class=RawTextHelpFormatter)
parser.add_argument('-li', dest='linkedingen', default=False, required=False, help="Run the LinkedIn module", action='store_true')
parser.add_argument('-zi', dest='zipull', required=False, default=False, help="Pull ZoomInfo Employee Names", action='store_true')
parser.add_argument('-hio', dest='hunterIO', required=False, default=False, help="Pull Emails from Hunter.io", action='store_true')
parser.add_argument('-o', dest='outputfile', required=False, default='', help="Write output to file")
parser.add_argument('-pn', dest='printnames', required=False, default=False, help="Print found names to screen", action='store_true')
parser.add_argument('-c', dest='company', default='', required=False, help="Company to search for")
parser.add_argument('-id', dest='companyid', required=False, help="Company ID to search for")
parser.add_argument('-s', dest='sleep', default=5, required=False, help="Time to sleep between requests")
parser.add_argument('-mr', dest='max_requests', default=200, required=False, help="Max number of requests per title while searching, use 0 for unlimited")
parser.add_argument('-t', dest='timeout', required=False, default=5, help="HTTP Request timeout")
parser.add_argument('-user', dest='linkedin_username', required=False, help="LinkedIn.com Authenticated Username")
parser.add_argument('-pass', dest='linkedin_password', required=False, help="LinkedIn.com Authenticated Password")
parser.add_argument('-zilink', dest='zilink', required=False, help="ZoomInfo Company Employee Link\n  (eg: https://www.zoominfo.com/pic/google-inc/16400573")
parser.add_argument('-hapi', dest='hunterApiKey', required=False, help="Hunter.io API Key")
parser.add_argument('-hdom', dest='hunterDomain', required=False, help="Domain to query in Hunter.io") 
parser.add_argument('-m', dest='mangleMode', required=False, default=0, help="Mangle Mode (use '-mo' to list mangle options)")
parser.add_argument('-mo', dest='mangleOptions', required=False, default=False, help="List Mangle Mode Options", action="store_true")
args = parser.parse_args()

# Assign user arguments to variables we can use
company = str(args.company) # String
companyid = args.companyid # Int
sleep = int(args.sleep) # Int
max_requests = int(args.max_requests) # Int
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

if mangleOptions:
	print('  Available Mangle Modes:')
	print('     0 = <First> <LAST>    (Default)')
	print('     1 = <FIRST>.<LAST>')
	print('     2 = <F>.<LAST>')
	print('     3 = <FIRST>.<L>')
	print('     4 = <FIRST><LAST>')
	print('     5 = <F><LAST>')
	print('     6 = <FIRST><L>\n')
	sys.exit()

if outputfile == '':
	print('[-] Output file name required (-o)')
	sys.exit()

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

if "/c/" in zilink:
	zilink = zilink.replace("/c/", "/pic/")

outputfiletemp = outputfile + '_temp'
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3'

# Colors for terminal output because Waffles likes pretty things
class bcolors:
	OKGREEN = '\033[92m'
	BOLD = '\033[1m'
	NONERED = '\033[91m'
	ENDLINE = '\033[0m'
	UNDERLINE = '\033[4m'

# If output file is selected, display output file name
if outputfile != '':
	print(bcolors.OKGREEN + '[+] Output File name: ' + outputfile + bcolors.ENDLINE)

# Check if output files exist, prompt to delete if they do. 
if os.path.exists(outputfile):
	del_outputfile = input(bcolors.NONERED + '\n[!] Output File exists, do you want to overwrite it? [Y/n] ' + bcolors.ENDLINE)
	if del_outputfile == 'y' or 'Y' or '':
		os.remove(outputfile)
	elif del_outputfile == 'n' or 'N':
		print('Stoping script')
		sys.exit()
	else:
		print('Not a valid option, please try again.....')
		main_generator()

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
	try:
		zoomInfoGetPage = zoomInfoSessionFirefox.get(getURL, allow_redirects=True)
	except cloudscraper.exceptions.CloudflareChallengeError as e:
		time.sleep(3)
		try:
			zoomInfoGetPage = zoomInfoSessionFirefox.get(getURL, allow_redirects=True)
		except:
			time.sleep(5)
			try:
				zoomInfoGetPage = zoomInfoSessionFirefox.get(getURL, allow_redirects=True)
			except Exception as e:
				pass
	if zoomInfoGetPage != '':
		return zoomInfoGetPage

def extractZINames(companyLink, outputFileName):
	for pageNum in range(1, 6):
		zoomInfoGetPage = getZISession(companyLink, pageNum)
		zoomInfoResponseSplit = zoomInfoGetPage.text.split('<script id="app-root-state" type="application/json">')
		zoomInfoResponseSplit2 = zoomInfoResponseSplit[1].split('</script>')[0]
		zoomInfoResponseSplit2 = zoomInfoResponseSplit2.replace('&q;','"').replace('&a;','&').replace('&s;','\'').replace('&l;','<').replace('&g;','>')
		zoomInfoJson = json.loads(zoomInfoResponseSplit2)
		for n in range(25):
			personName = zoomInfoJson["pic-"]["picParsedData"]["table"]["data"][n][1]["fullName"]
			if printnames:
				print(str(personName))
			if outputFileName != '':
				file = open(outputfiletemp,"a+")
				print(personName, file = file)
				file.close()
		time.sleep(3)

def linkedInGen():
	if (companyid == '' or companyid is None):
		print("Pulling Company ID for {:s}\n".format(company))
		pullid()

	cj = initialReq()
	cj = authReq(cj)

	print(bcolors.OKGREEN + '[+] ...Searching all contacts...' + bcolors.ENDLINE)
	count = 0
	total_found = 0
	title_found = 0
	data = recon(None, cj, 1, 0)
	content = json.loads(data)

	# Pull count of identified users
	count = content["data"]["metadata"]["totalResultCount"]
	print(bcolors.OKGREEN + '[+] Found {} users'.format(count) + bcolors.ENDLINE)
	for i in range(1, int(math.ceil(count/50))+1):
		if i == 1:
			data = recon(None, cj, 49, 0)

		# Even though this is less accurate for user counting, we might as well add as many as we got for the requests.
		elif (max_requests != 0 and title_found >= max_requests):
			title_found = 0
			break
		else:
			data = recon(None, cj, 49, i*50)
		content = json.loads(data)

		# Part where the names are created and/or mangled
		for user in content["included"]:
			if "firstName" in user:
				first_name = re.sub(r'\W+', ' ', user.get("firstName")).split(" ")[0]
				last_name = re.sub(r'\W+', ' ', user.get("lastName")).split(" ")[0]
				full_name = (first_name.capitalize() + " " + last_name.capitalize())

				if full_name.startswith("."):
					pass
				elif len(first_name) <= 1 or len(last_name) <= 1:
					pass
				else:
					file = open(outputfiletemp,"a+")
					print(full_name, file = file)
					total_found += 1
					title_found += 1
		time.sleep(sleep)
		file.close()

def hunterPull(hunterApiKey, hunterDomain, outputFileName):
	hunter = PyHunter(hunterApiKey)
	hunterAccountInformation = hunter.account_information()
	hunterAvailableSearches = int(hunterAccountInformation["requests"]["searches"]["available"])
	hunterUsedSearches = int(hunterAccountInformation["requests"]["searches"]["used"])
	hunterRemainingSearches = str(hunterAvailableSearches - hunterUsedSearches)
	hunterContinue = input(bcolors.NONERED + '[!] ' + hunterRemainingSearches + ' Searches Remaining, Continue? [Y/n] ' + bcolors.ENDLINE)
	if hunterContinue == 'y' or 'Y' or '':
		hunterContinue = True
	if hunterContinue == 'n' or 'N':
		hunterContinue = False
	else:
		print('Not a valid option, please try again.....')
		hunterPull(hunterApiKey, hunterDomain, outputFileName)

	domainSearchHunterJson = hunter.domain_search(hunterDomain)
	domainHunterPattern = domainSearchHunterJson['pattern']
	hunterPlanname = hunterAccountInformation['plan_name']
	print(bcolors.OKGREEN + '\n[+] Email Pattern: ' + domainHunterPattern + '\n' + bcolors.ENDLINE)

	addToMainList = False
	hunterOutputFile = "Hunter_" + outputfile
	if domainSearchHunterJson['pattern'] == '{first}.{last}':
		addToMainList = input(bcolors.NONERED + '[!] Email Pattern matches FIRST.LAST, Add to main output file? [Y/n] \n' + bcolors.ENDLINE)
		if addToMainList == 'y' or 'Y' or '':
			addToMainList = True
			hunterOutputFile = outputFileName
		elif addToMainList == 'n' or 'N':
			addToMainList = False
			print(bcolors.OKGREEN + "[+] Hunter.io Output saving to %s" + bcolors.ENDLINE % hunterOutputFile)
			hunterOutputFile = "Hunter_" + outputfile
		else:
			print(bcolors.NONERED + '\n[!] INVALID SELECTION, EXITING...\n' + bcolors.ENDLINE)
			sys.exit()

	hunterDomainSearchJSONCreate = json.dumps(domainSearchHunterJson)
	hunterDomainSearchJSONObject = json.loads(hunterDomainSearchJSONCreate)
	listJSONObjectEmails = hunterDomainSearchJSONObject['emails']

	print(bcolors.OKGREEN + '[+] ' + hunterPlanname + ' Plan Pulled ' + str(len(listJSONObjectEmails)) + ' Emails From Hunter.io\n' + bcolors.ENDLINE)

	for emailKey in listJSONObjectEmails:
		if addToMainList:
			fullName = emailKey['value'].split('@')[0]
			firstName = fullName.split('.')[0]
			lastName = fullName.split('.')[1]
			finalName = firstName.capitalize() + " " + lastName.capitalize()
			file = open(hunterOutputFile, "a+")
			print(finalName, file = file)
		else:
			file = open(hunterOutputFile,"a+")
			print(emailKey['value'], file = file)
	file.close()

def capDedup(outputfiletemp):
	# Remove Duplicates from outputfile
	if os.path.exists(outputfiletemp):
		lines_seen = set()
		dedupefile = open(outputfile, "a+")
		for line in open(outputfiletemp, "r"):
			if line not in lines_seen:
				lines_seen.add(line.title())
		dedupefile.writelines(sorted(lines_seen))
		dedupefile.close()
		if os.path.exists(outputfiletemp):
			os.remove(outputfiletemp)

def mangler(mangleMode, outputfile):
	inputFileName = outputfile
	mangleFileName = outputfile + "_Mangled"

	if os.path.exists(mangleFileName):
		del_mangleFile = input(bcolors.NONERED + '[!] Mangle File exists, overwrite it? [Y/n] ' + bcolors.ENDLINE)
		if del_mangleFile == 'y' or 'Y' or '':
			os.remove(mangleFileName)
		elif del_mangleFile == 'n' or 'N':
			print('[-] Not mangling names')
			pass
		else:
			print('[!] Not a valid option, please try again.....')
			mangler(mangleMode, outputfile)

	if not os.path.exists(inputFileName) and not hunterIO and not linkedingen and not zipull:
		print(bcolors.NONERED + '[-] No scrape options selected, please select at least 1 scrape option. Exiting.... \n' + bcolors.ENDLINE)
		sys.exit()

	fileInput = open(inputFileName, 'r')
	if mangleMode > 0:
		fileOutput = open(mangleFileName, 'a+')
	fileLines = fileInput.readlines()

	for name in fileLines:
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

		if printnames and mangleMode == 0:
			print(name.strip())
		elif printnames and mangleMode > 0:
			print(name.strip() + " : " + mangledName.strip())
			print(mangledName, file = fileOutput)
		elif not printnames and mangleMode > 0:
			print(mangledName, file = fileOutput)

def main_generator():
	global outputfile
	global mangleMode

	if linkedingen:
		try:
			print(bcolors.OKGREEN + '\n[+] Pulling Company LinkedIn Employee Names\n' + bcolors.ENDLINE)
			linkedInGen()
		except:
			print(bcolors.NONERED + "[!] Errors Pulling LinkedIn Names" + bcolors.ENDLINE)
			pass

	if zipull:
		print(bcolors.OKGREEN + '\n[+] Pulling ZoomInfo Company Employee Names\n' + bcolors.ENDLINE)
		try:
			extractZINames(zilink, outputfiletemp)
		except:
			print(bcolors.NONERED + "[!] Errors Pulling ZoomInfo Names" + bcolors.ENDLINE)
			pass

	if hunterIO:
		try:
			print(bcolors.OKGREEN + '[+] Pulling emails from Hunter.io\n' + bcolors.ENDLINE)
			hunterPull(hunterApiKey, hunterDomain, outputfiletemp)
		except:
			print(bcolors.NONERED + "[!] Errors Pulling Hunter.io Emails" + bcolors.ENDLINE)
			pass

	capDedup(outputfiletemp)
	mangler(mangleMode, outputfile)

if __name__ == "__main__":
	main_generator()
