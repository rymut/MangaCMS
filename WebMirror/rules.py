
import json
import os
import os.path
import yaml
import traceback
import urllib.parse

class ValidationError(Exception):
	pass

def getStartURLs(ruleset):
	if not 'baseUrl' in ruleset:
		raise ValidationError("No 'baseUrl' values in ruleset!")
	ret = []
	if not isinstance(ruleset['baseUrl'], list):
		raise ValidationError("'baseUrl' is not a list!")
	ret += ruleset['baseUrl']

	if 'extraStartUrls' in ruleset:
		if not isinstance(ruleset['extraStartUrls'], list):
			raise ValidationError("'extraStartUrls' is not a list!")
		ret += ruleset['extraStartUrls']
	ret.sort()
	return ret

def getFeedUrls(ruleset):
	if 'feedPostfix' in ruleset:
		assert 'feeds' not in ruleset
		assert isinstance(ruleset['feedPostfix'], str)
		feeds = [url+ruleset['feedPostfix'] for url in ruleset['baseUrl']]
		return feeds

	if 'feeds' in ruleset:
		assert 'feedPostfix' not in ruleset
		assert isinstance(ruleset['feeds'], list)
		return ruleset['feeds']

	return []

def getUrlBadWords(ruleset):
	assert 'badwords' in ruleset
	assert isinstance(ruleset['badwords'], list)
	return ruleset['badwords']

def getStripTitle(ruleset):
	if not 'stripTitle' in ruleset:
		return []
	assert isinstance(ruleset['stripTitle'], list)
	return ruleset['stripTitle']

def getDecomposeBefore(ruleset):
	if not 'decomposeBefore' in ruleset:
		return []
	assert isinstance(ruleset['decomposeBefore'], list)
	for item in ruleset['decomposeBefore']:
		assert isinstance(item, dict)
	return ruleset['decomposeBefore']

def getDecomposeAfter(ruleset):
	assert 'decompose' in ruleset
	assert isinstance(ruleset['decompose'], list)
	for item in ruleset['decompose']:
		assert isinstance(item, dict)
	return ruleset['decompose']

def getFileDomains(ruleset):
	if not 'fileDomains' in ruleset:
		return []
	assert isinstance(ruleset['fileDomains'], list)
	for item in ruleset['fileDomains']:
		assert isinstance(item, str)
	return ruleset['fileDomains']


def checkBadValues(ruleset):
	assert 'wg' not in ruleset
	assert 'threads' not in ruleset
	assert 'startUrl' not in ruleset
	assert 'tableKey' not in ruleset
	assert 'pluginName' not in ruleset
	assert 'loggerPath' not in ruleset


def getPossibleNetLocs(ruleset):
	'''
	Given the set of start URLs, and (if present) a set of
	allowed TLDs, generate a comprehensive set of possible allowable
	TLDs that the scrape can walk to.
	'''

	inTlds = set()
	if 'tld' in ruleset and ruleset['tld']:
		assert isinstance(ruleset['tld'], list)
		inTlds = set(ruleset['tld'])


	inList = set()
	for url in ruleset['baseUrl']:
		inList.add(url)

	TLDs = set([urllib.parse.urlsplit(url.lower()).netloc.rsplit(".")[-1] for url in inList])
	TLDs = TLDs | inTlds


	def genBaseUrlPermutations(url):
		netloc = urllib.parse.urlsplit(url.lower()).netloc
		if not netloc:
			raise ValueError("One of the scanned domains collapsed down to an empty string: '%s'!" % url)
		ret = set()
		# Generate the possible wordpress netloc values.
		if 'wordpress.com' in netloc:
			subdomain, mainDomain, tld = netloc.rsplit(".")[-3:]

			ret.add("www.{sub}.{main}.{tld}".format(sub=subdomain, main=mainDomain, tld=tld))
			ret.add("{sub}.{main}.{tld}".format(sub=subdomain, main=mainDomain, tld=tld))
			ret.add("www.{sub}.files.{main}.{tld}".format(sub=subdomain, main=mainDomain, tld=tld))
			ret.add("{sub}.files.{main}.{tld}".format(sub=subdomain, main=mainDomain, tld=tld))

		# Blogspot is annoying and sometimes a single site is spread over several tlds. *.com, *.sg, etc...
		if 'blogspot.' in netloc:
			subdomain, mainDomain, dummy_tld = netloc.rsplit(".")[-3:]
			for tld in TLDs:
				ret.add("www.{sub}.{main}.{tld}".format(sub=subdomain, main=mainDomain, tld=tld))
				ret.add("{sub}.{main}.{tld}".format(sub=subdomain, main=mainDomain, tld=tld))


		elif 'google.' in netloc:
			pass

		else:

			base, dummy_tld = netloc.rsplit(".", 1)
			for tld in TLDs:
				ret.add("{main}.{tld}".format(main=base, tld=tld))
				# print(ret)
		return ret

	retSet = set()
	for url in inList:
		items = genBaseUrlPermutations(url)
		retSet.update(items)

	if 'FOLLOW_GOOGLE_LINKS' in ruleset and ruleset['FOLLOW_GOOGLE_LINKS']:
		retSet.add('https://docs.google.com/document/')
		retSet.add('https://docs.google.com/spreadsheets/')
		retSet.add('https://drive.google.com/folderview')
		retSet.add('https://drive.google.com/open')

	# Filter out spurious 'blogspot.com.{TLD}' entries that are getting in somehow
	ret = [item for item in retSet if not item.startswith('blogspot.com')]

	return ret

def getAllImages(ruleset):
	if not 'allImages' in ruleset:
		return False
	return ruleset['allImages']

def getCloudflare(ruleset):
	if not 'cloudflare' in ruleset:
		return False
	return ruleset['cloudflare']

def getIgnoreMalformed(ruleset):
	if not 'IGNORE_MALFORMED_URLS' in ruleset:
		return False
	return ruleset['IGNORE_MALFORMED_URLS']

def load_validate_rules(fname, dat):

	checkBadValues(dat)

	rules = {}
	rules['starturls']             = getStartURLs(dat)
	rules['feedurls']              = getFeedUrls(dat)

	rules['badwords']              = getUrlBadWords(dat)
	rules['stripTitle']            = getStripTitle(dat)
	rules['decomposeBefore']       = getDecomposeBefore(dat)
	rules['decompose']             = getDecomposeAfter(dat)
	rules['netlocs']               = getPossibleNetLocs(dat)

	rules['allImages']             = getAllImages(dat)
	rules['fileDomains']           = getFileDomains(dat)
	rules['cloudflare']            = getCloudflare(dat)
	rules['IGNORE_MALFORMED_URLS'] = getIgnoreMalformed(dat)

	# itemGenre
	# allowQueryStr
	# changeMasks
	# stripTitle
	# decomposeBefore
	# decompose
	# badwords
	# FOLLOW_GOOGLE_LINKS
	# allImages

	# Start urls are the values of baseurl +
	# extraStartUrls (if present)

	# feeds
	# feedPostfix


	# Block values:
	# wg
	# threads

	return rules

def get_rules():
	cwd = os.path.split(__file__)[0]
	rulepath = os.path.join(cwd, "rules")

	items = os.listdir(rulepath)
	items.sort()
	ret = []
	for item in [os.path.join(rulepath, item) for item in items if item.endswith('.yaml')]:

		with open(item, "r") as fp:
			try:
				text = fp.read()
				# Fuck you YAML, tabs are better then spaces.
				# Also, single-space indentation discontinuity in
				# YAML causes the whole file to load wrong.
				text = text.replace("	", "    ")
				dat = yaml.load(text)
				rules = load_validate_rules(item, dat)
				if rules:
					ret.append(rules)
			except (yaml.scanner.ScannerError, yaml.parser.ParserError):
				print("ERROR!")
				print("Attempting to load file: '{}'".format(item))
				traceback.print_exc()
			except ValidationError:
				print("ERROR!")
				print("Validation error when trying to load file: '{}'".format(item))
				traceback.print_exc()
				print(dat)
			except AssertionError:
				print("ERROR!")
				print("Validation error when trying to load file: '{}'".format(item))
				traceback.print_exc()
				print(dat)

	print()
	print("Loaded rulesets ({}):".format(len(ret)))
	print()
	# for ruleset in ret:
	# 	print(ruleset)
	# 	print()
	return ret


def load_rules():
	rules = get_rules()
	return rules