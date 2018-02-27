
import os
import uuid
import datetime
import urllib.parse
import sys
from ipaddress import IPv4Address, IPv4Network
import settings

from flask import Flask
from flask import g
from flask import request
from flask_wtf.csrf import CsrfProtect
from babel.dates import format_datetime

import nameTools as nt


print("App import!")

app = Flask(__name__)

if "debug" in sys.argv:
	print("Flask running in debug mode!")
	app.debug = True
app.config.from_object('MangaCMS.app.config.BaseConfig')

CsrfProtect(app)


if not app.debug:
	import logging
	from logging.handlers import RotatingFileHandler
	os.makedirs("tmp", exist_ok=True)
	file_handler = RotatingFileHandler('tmp/MangaCMS.log', 'a', 1 * 1024 * 1024, 10)
	file_handler.setLevel(logging.INFO)
	file_handler.setFormatter(logging.Formatter(
		'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	app.logger.addHandler(file_handler)
	app.logger.setLevel(logging.INFO)
	app.logger.info('MangaCMS startup')


from MangaCMS.app import all_scrapers_ever
from MangaCMS.app import views


colours = {
	# Download Status
	"failed"          : "000000",
	"no match"        : "FF9999",
	"moved"           : "FFFF99",
	"Done"            : "99FF99",
	"Uploaded"        : "90e0FF",
	"working"         : "9999FF",
	"queued"          : "FF77FF",
	"new dir"         : "FFE4B2",
	"error"           : "FF0000",

	# Categories

	"valid cat"  : "FFFFFF",
	"picked"    : "999999",

	# Download Status
	"hasUnread"       : "FF9999",
	"upToDate"        : "99FF99",
	"notInMT"         : "9999FF",


	"created-dir"     : "FFE4B2",
	"not checked"     : "FFFFFF",

	# Categories

	"valid category"  : "FFFFFF",
	"bad category"    : "999999"
	}


@app.context_processor
def utility_processor():

	def format_date(value, format='medium'):

		return format_datetime(value, "EE yyyy.MM.dd")

	def date_now():
		return format_datetime(datetime.datetime.today(), "yyyy/MM/dd, hh:mm:ss")

	def ago(then):
		if then == None:
			return "Never"
		now = datetime.datetime.now()
		delta = now - then

		d = delta.days
		h, s = divmod(delta.seconds, 3600)
		m, s = divmod(s, 60)
		labels = ['d', 'h', 'm', 's']
		dhms = ['%s %s' % (i, lbl) for i, lbl in zip([d, h, m, s], labels)]
		for start in range(len(dhms)):
			if not dhms[start].startswith('0'):
				break
		for end in range(len(dhms)-1, -1, -1):
			if not dhms[end].startswith('0'):
				break
		return ', '.join(dhms[start:end+1])

	def fixed_width_ago(then):
		if then == None:
			return "Never"
		now = datetime.datetime.now()
		delta = now - then

		d = delta.days
		h, s = divmod(delta.seconds, 3600)
		m, s = divmod(s, 60)
		labels = ['d', 'h', 'm', 's']
		dhms = ['%s %s' % (str(i).zfill(2), lbl) for i, lbl in zip([d, h, m, s], labels)]
		for start in range(len(dhms)):
			if not dhms[start].startswith('0'):
				break
		for end in range(len(dhms)-1, -1, -1):
			if not dhms[end].startswith('0'):
				break
		ret = ', '.join(dhms)
		return ret


	def terse_ago(then):
		if then is None or then is False:
			return "Never"

		# print("Then: ", then)
		now = datetime.datetime.now()
		delta = now - then

		d = delta.days
		h, s = divmod(delta.seconds, 3600)
		m, s = divmod(s, 60)
		labels = ['d', 'h', 'm', 's']
		dhms = ['%s %s' % (i, lbl) for i, lbl in zip([d, h, m, s], labels)]
		for start in range(len(dhms)):
			if not dhms[start].startswith('0'):
				break
		# for end in range(len(dhms)-1, -1, -1):
		# 	if not dhms[end].startswith('0'):
		# 		break
		if d > 0:
			dhms = dhms[:2]
		elif h > 0:
			dhms = dhms[1:3]
		else:
			dhms = dhms[2:]
		return ', '.join(dhms)


	def compact_date_str(dateStr):
		dateStr = dateStr.replace("months", "mo")
		dateStr = dateStr.replace("month", "mo")
		dateStr = dateStr.replace("weeks", "w")
		dateStr = dateStr.replace("week", "w")
		dateStr = dateStr.replace("days", "d")
		dateStr = dateStr.replace("day", "d")
		dateStr = dateStr.replace("hours", "hr")
		dateStr = dateStr.replace("hour", "hr")
		dateStr = dateStr.replace("minutes", "m")
		dateStr = dateStr.replace("seconds", "s")
		dateStr = dateStr.replace("years", "yrs")
		dateStr = dateStr.replace("year", "yr")
		return dateStr


	def ip_in_whitelist():
		user_ip = IPv4Address(request.remote_addr)

		w_ip = IPv4Network(settings.pronWhiteList)
		if user_ip in w_ip:
			return True
		return False


	def f_size_to_str(fSize):
		if fSize == 0:
			return ''

		fStr = fSize/1.0e6
		if fStr < 100:
			fStr = "%0.2f M" % fStr
		else:
			fStr = "%0.1f M" % fStr

		return fStr


	def timeAgo(inTimeStamp):

		if inTimeStamp == None:
			return "NaN"

		deltatime = datetime.datetime.now() - inTimeStamp
		delta = int(deltatime.total_seconds())
		if delta < 0:
			return "Past?"
		elif delta < 60:
			return "{delta} s".format(delta=delta)
		delta = delta // 60
		if delta < 60:
			return "{delta} m".format(delta=delta)
		delta = delta // 60
		if delta < 24:
			return "{delta} h".format(delta=delta)
		delta = delta // 24
		if delta < 999:
			return "{delta} d".format(delta=delta)
		delta = delta // 365
		return "{delta} y".format(delta=delta)


	def timeAhead(inTimeStamp):

		deltatime = inTimeStamp - datetime.datetime.now()
		delta = deltatime.total_seconds()
		if delta < 0:
			return "Future?"
		elif delta < 60:
			return "{delta} s".format(delta=delta)
		delta = delta // 60
		if delta < 60:
			return "{delta} m".format(delta=delta)
		delta = delta // 60
		if delta < 24:
			return "{delta} h".format(delta=delta)
		delta = delta // 24
		if delta < 999:
			return "{delta} d".format(delta=delta)
		delta = delta // 365
		return "{delta} y".format(delta=delta)


	def generate_row_meta(row):
		ret = {}

		filePath = ""
		if row.file:
			filePath = os.path.join(row.file.dirpath, row.file.filename)

		if row.series_name is None:
			sourceSeriesName = "NONE"
			seriesName = "NOT YET DETERMINED"
		else:
			sourceSeriesName = row.series_name
			seriesName = nt.getCanonicalMangaUpdatesName(row.series_name)

		cleanedName = nt.prepFilenameForMatching(sourceSeriesName)
		ret['itemInfo'] = nt.dirNameProxy[cleanedName]
		if ret['itemInfo']["rating"]:
			ret['rating'] = ret['itemInfo']["rating"]
		else:
			ret['rating'] = ""
		ret['ratingNum'] = nt.ratingStrToFloat(ret['rating'])


		if row.state == 'complete':
			ret['statusColour'] = colours["Done"]
		elif row.state == 'upload':
			ret['statusColour'] = colours["Uploaded"]
		elif row.state == 'fetching' or row.state == 'processing':
			ret['statusColour'] = colours["working"]
		elif row.state == 'new':
			ret['statusColour'] = colours["queued"]
		else:
			ret['statusColour'] = colours["error"]


		if filePath:
			if "=0=" in row.file.dirpath:
				if os.path.exists(filePath):
					ret['locationColour'] = colours["no match"]
				else:
					ret['locationColour'] = colours["moved"]
			elif settings.pickedDir in row.file.dirpath:
				ret['locationColour'] = colours["picked"]
			elif row.dirstate == 'created_dir':
				ret['locationColour'] = colours["new dir"]
			else:
				ret['locationColour'] = colours["valid cat"]
		else:
			if row.state == 'new':
				ret['locationColour'] = colours["queued"]
			elif row.state == 'upload':
				ret['locationColour'] = colours["valid cat"]
			elif row.state == 'fetching' or row.state == 'processing':
				ret['locationColour'] = colours["working"]
			else:
				ret['locationColour'] = colours["failed"]
			filePath = "N.A."


		toolTip  = filePath.replace('"', "") + "<br>"
		toolTip += "Original series name: " + sourceSeriesName.replace('"', "") + "<br>"
		toolTip += "Proper MangaUpdates name: " + seriesName.replace('"', "") + "<br>"
		toolTip += "cleanedName: " + ret['itemInfo']["dirKey"] + "<br>"
		toolTip += "itemInfo: " + str(ret['itemInfo']).replace('"', "") + "<br>"
		toolTip += "rowId: " + str(row.id) + "<br>"
		toolTip += "sourceUrl: " + row.source_id + "<br>"
		toolTip += "dlState: " + str(row.state) + "<br>"
		toolTip += "Flags: " + str([row.deleted, row.was_duplicate, row.phash_duplicate, row.uploaded, row.dirstate]) + "<br>"
		toolTip += "item tags: " + str([tag for tag in row.tags]) + "<br>"
		if row.file:
			toolTip += "file manga tags: " + str([tag for tag in row.file.manga_tags]) + "<br>"
		toolTip += "Source: " + str(row.source_site) + "<br>"

		ret['cellId'] = None
		if os.path.exists(filePath):
			toolTip += "File found."
		else:
			toolTip += "File is missing!"
			ret['cellId'] = uuid.uuid1(0).hex

		ret['toolTip'] = toolTip

		ret['shouldBold'] = False
		if row.origin_name:
			chap = nt.extractChapterVol(row.origin_name)[0]
			if isinstance(chap, float):
				if chap < 10:
					ret['shouldBold'] = True
		ret['terseDate'] = row.downloaded_at.strftime('%y-%m-%d %H:%M')
		return ret


	def generate_hentai_meta(row):
		ret = {}

		filePath = ""
		if row.file:
			filePath = os.path.join(row.file.dirpath, row.file.filename)


		category_name = row.series_name if row.series_name else ""


		if row.state == 'complete':
			ret['statusColour'] = colours["Done"]
		elif row.state == 'fetching' or row.state == 'processing':
			ret['statusColour'] = colours["working"]
		elif row.state == 'new':
			ret['statusColour'] = colours["queued"]
		else:
			ret['statusColour'] = colours["error"]


		if filePath:
			if os.path.exists(filePath):
				ret['locationColour'] = colours["no match"]
			else:
				ret['locationColour'] = colours["moved"]
		else:
			if row.state == 'new':
				ret['locationColour'] = colours["queued"]
			elif row.state == 'upload':
				ret['locationColour'] = colours["valid cat"]
			elif row.state == 'fetching' or row.state == 'processing':
				ret['locationColour'] = colours["working"]
			else:
				ret['locationColour'] = colours["failed"]
			filePath = "N.A."

		ret['item-tags'] = [tmp for tmp in row.tags]
		if row.file:
			ret['file-tags'] = [tmp for tmp in row.file.hentai_tags if tmp not in ret['item-tags']]
		else:
			ret['file-tags'] = []

		toolTip  = filePath.replace('"', "") + "<br>"
		toolTip += "Origin Name: " + row.origin_name.replace('"', "") + "<br>"
		toolTip += "Category Name: " + category_name.replace('"', "") + "<br>"
		toolTip += "rowId: " + str(row.id) + "<br>"
		toolTip += "sourceUrl: " + row.source_id + "<br>"
		toolTip += "dlState: " + str(row.state) + "<br>"
		toolTip += "Flags: " + str([row.deleted, row.was_duplicate, row.phash_duplicate, row.uploaded, row.dirstate]) + "<br>"
		toolTip += "item tags: " + str(ret['item-tags']) + "<br>"
		if row.file:
			toolTip += "file hentai tags: " + str(ret['file-tags']) + "<br>"
		toolTip += "Source: " + str(row.source_site) + "<br>"

		ret['cellId'] = None
		if os.path.exists(filePath):
			toolTip += "File found."
			ret['fsize'] = os.path.getsize(filePath)

		else:
			toolTip += "File is missing!"
			ret['cellId'] = uuid.uuid1(0).hex
			ret['fsize'] = -1

		ret['toolTip'] = toolTip

		ret['shouldBold'] = False
		if row.origin_name:
			chap = nt.extractChapterVol(row.origin_name)[0]
			if isinstance(chap, float):
				if chap < 10:
					ret['shouldBold'] = True
		ret['terseDate'] = row.downloaded_at.strftime('%y-%m-%d %H:%M')
		return ret

	return dict(
			generate_row_meta     = generate_row_meta,
			generate_hentai_meta  = generate_hentai_meta,
			compact_date_str      = compact_date_str,
			ip_in_whitelist       = ip_in_whitelist,
			f_size_to_str         = f_size_to_str,
			format_date           = format_date,
			date_now              = date_now,
			ago                   = ago,
			fixed_width_ago       = fixed_width_ago,
			terse_ago             = terse_ago,
			manga_scrapers        = all_scrapers_ever.manga_scrapers,
			hentai_scrapers       = all_scrapers_ever.hentai_scrapers,
			other_scrapers        = all_scrapers_ever.other_scrapers,

			timeAgo               = timeAgo,
			timeAhead             = timeAhead,

			)
