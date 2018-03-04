

if __name__ == "__main__":
	import MangaCMSOld.lib.logSetup
	MangaCMSOld.lib.logSetup.initLogging()

import MangaCMSOld.ScrapePlugins.M.BuMonitor.Run
import MangaCMSOld.ScrapePlugins.M.BuMonitor.Rescan


import MangaCMSOld.ScrapePlugins.H.ASMHentaiLoader.Run
import MangaCMSOld.ScrapePlugins.H.DjMoeLoader.Run
import MangaCMSOld.ScrapePlugins.H.DoujinOnlineLoader.Run
import MangaCMSOld.ScrapePlugins.H.Hentai2Read.Run
import MangaCMSOld.ScrapePlugins.H.HitomiLoader.Run
import MangaCMSOld.ScrapePlugins.H.PururinLoader.Run
import MangaCMSOld.ScrapePlugins.H.SadPandaLoader.Run
import MangaCMSOld.ScrapePlugins.H.TsuminoLoader.Run

import MangaCMSOld.ScrapePlugins.M.Crunchyroll.Run
import MangaCMSOld.ScrapePlugins.M.CxLoader.Run
import MangaCMSOld.ScrapePlugins.M.DynastyLoader.Run
import MangaCMSOld.ScrapePlugins.M.GameOfScanlationLoader.Run
import MangaCMSOld.ScrapePlugins.M.IrcGrabber.BotRunner
import MangaCMSOld.ScrapePlugins.M.IrcGrabber.IrcEnqueueRun
import MangaCMSOld.ScrapePlugins.M.Kawaii.Run
import MangaCMSOld.ScrapePlugins.M.KissLoader.Run
import MangaCMSOld.ScrapePlugins.M.MangaBox.Run
import MangaCMSOld.ScrapePlugins.M.MangaDex.Run
import MangaCMSOld.ScrapePlugins.M.MangaHere.Run
import MangaCMSOld.ScrapePlugins.M.MangaStreamLoader.Run
import MangaCMSOld.ScrapePlugins.M.McLoader.Run
import MangaCMSOld.ScrapePlugins.M.MerakiScans.Run
import MangaCMSOld.ScrapePlugins.M.MangaZuki.Run
import MangaCMSOld.ScrapePlugins.M.WebtoonLoader.Run            # Yeah. There is webtoon.com. and WebtoonsReader.com. Confusing much?
import MangaCMSOld.ScrapePlugins.M.YoMangaLoader.Run
import MangaCMSOld.ScrapePlugins.M.ZenonLoader.Run

import MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.CanisMajorRun
import MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.ChibiMangaRun
import MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.DokiRun
import MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.GoMangaCoRun
import MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.IlluminatiMangaRun
import MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.JaptemMangaRun
import MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.MangatopiaRun
import MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.RoseliaRun
import MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.S2Run
import MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.SenseRun
import MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.ShoujoSenseRun
import MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.TripleSevenRun
import MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.TwistedHelRun
import MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.VortexRun


import MangaCMS.ScrapePlugins.H.HBrowseLoader.Run
import MangaCMS.ScrapePlugins.H.NHentaiLoader.Run
import MangaCMS.ScrapePlugins.M.MangaMadokami.Run
# import MangaCMSOld.ScrapePlugins.M.BooksMadokami.Run

# Convenience functions to make intervals clearer.
def days(num):
	return 60*60*24*num
def hours(num):
	return 60*60*num
def minutes(num):
	return 60*num

# Plugins in this dictionary are the active plugins. Comment out a plugin to disable it.
# plugin keys specify when plugins will start, and cannot be duplicates.
# All they do is specify the order in which plugins
# are run, initially, starting after 1-minue*{key} intervals
scrapePlugins = {
	0   : (MangaCMSOld.ScrapePlugins.M.MangaDex.Run,                        hours( 1)),
	1   : (MangaCMSOld.ScrapePlugins.M.MangaStreamLoader.Run,               hours( 6)),
	2   : (MangaCMSOld.ScrapePlugins.M.BuMonitor.Run,                       hours( 1)),
	3   : (MangaCMSOld.ScrapePlugins.M.BuMonitor.Rescan,                    days(  7)),

	11  : (MangaCMSOld.ScrapePlugins.M.McLoader.Run,                        hours(12)),  # every 12 hours, it's just a single scanlator site.
	# 13  : (MangaCMSOld.ScrapePlugins.M.CxLoader.Run,                        hours(12)),  # every 12 hours, it's just a single scanlator site.
	# 12  : (MangaCMSOld.ScrapePlugins.M.IrcGrabber.IrcEnqueueRun,            hours(12)),  # Queue up new items from IRC bots.
	# 15  : (MangaCMSOld.ScrapePlugins.M.IrcGrabber.BotRunner,                hours( 1)),  # Irc bot never returns. It runs while the app is live. Rerun interval doesn't matter, as a result.
	16  : (MangaCMSOld.ScrapePlugins.M.MangaHere.Run,                       hours(12)),
	17  : (MangaCMSOld.ScrapePlugins.M.WebtoonLoader.Run,                   hours( 8)),
	18  : (MangaCMSOld.ScrapePlugins.M.DynastyLoader.Run,                   hours( 8)),
	# 19  : (MangaCMSOld.ScrapePlugins.M.KissLoader.Run,                      hours( 1)),
	20  : (MangaCMSOld.ScrapePlugins.M.Crunchyroll.Run,                     hours( 4)),
	22  : (MangaCMSOld.ScrapePlugins.M.Kawaii.Run,                          hours(12)),
	23  : (MangaCMSOld.ScrapePlugins.M.ZenonLoader.Run,                     hours(24)),
	24  : (MangaCMSOld.ScrapePlugins.M.MangaBox.Run,                        hours(12)),
	25  : (MangaCMSOld.ScrapePlugins.M.YoMangaLoader.Run,                   hours(12)),
	26  : (MangaCMSOld.ScrapePlugins.M.GameOfScanlationLoader.Run,          hours(12)),
	27  : (MangaCMSOld.ScrapePlugins.M.MerakiScans.Run,                     hours(12)),
	28  : (MangaCMSOld.ScrapePlugins.M.MangaZuki.Run,                       hours(12)),


	41  : (MangaCMS.ScrapePlugins.H.HBrowseLoader.Run,                   hours( 2)),
	42  : (MangaCMSOld.ScrapePlugins.H.PururinLoader.Run,                   hours( 2)),
	44  : (MangaCMS.ScrapePlugins.H.NHentaiLoader.Run,                   hours( 2)),
	45  : (MangaCMSOld.ScrapePlugins.H.SadPandaLoader.Run,                  hours(12)),
	46  : (MangaCMSOld.ScrapePlugins.H.DjMoeLoader.Run,                     hours( 2)),
	47  : (MangaCMSOld.ScrapePlugins.H.HitomiLoader.Run,                    hours( 2)),
	48  : (MangaCMSOld.ScrapePlugins.H.ASMHentaiLoader.Run,                 hours( 2)),
	49  : (MangaCMSOld.ScrapePlugins.H.Hentai2Read.Run,                     hours( 2)),
	50  : (MangaCMSOld.ScrapePlugins.H.DoujinOnlineLoader.Run,              hours( 2)),
	51  : (MangaCMSOld.ScrapePlugins.H.TsuminoLoader.Run,                   hours( 2)),

	# FoolSlide modules

	61 : (MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.CanisMajorRun,      hours(12)),
	62 : (MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.ChibiMangaRun,      hours(12)),
	63 : (MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.DokiRun,            hours(12)),
	64 : (MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.GoMangaCoRun,       hours(12)),
	65 : (MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.IlluminatiMangaRun, hours(12)),
	# 66 : (MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.JaptemMangaRun,     hours(12)),
	67 : (MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.MangatopiaRun,      hours(12)),
	# 68 : (MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.RoseliaRun,         hours(12)),
	69 : (MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.S2Run,              hours(12)),
	70 : (MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.SenseRun,           hours(12)),
	71 : (MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.ShoujoSenseRun,     hours(12)),
	72 : (MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.TripleSevenRun,     hours(12)),
	73 : (MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.TwistedHelRun,      hours(12)),
	74 : (MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.VortexRun,          hours(12)),

	80 : (MangaCMS.ScrapePlugins.M.MangaMadokami.Run,                    hours(4)),
	# 81 : (MangaCMSOld.ScrapePlugins.M.BooksMadokami.Run,                    hours(4)),

}


if __name__ == "__main__":

	# scrapePlugins = {
		# 0 : (TextScrape.BakaTsuki.Run,                       60*60*24*7),  # Every 7 days, because books is slow to update
		# 1 : (TextScrape.JapTem.Run,                          60*60*24*5),
		# 3 : (TextScrape.Guhehe.Run,                          60*60*24*5),
		# 2 : (TextScrape.ReTranslations.Run,                  60*60*24*1)   # There's not much to actually scrape here, and it's google, so I don't mind hitting their servers a bit.
	# }

	run = [
				MangaCMSOld.ScrapePlugins.M.Crunchyroll.Run,
				MangaCMSOld.ScrapePlugins.M.DynastyLoader.Run,
				MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.CanisMajorRun,
				MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.ChibiMangaRun,
				MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.DokiRun,
				MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.GoMangaCoRun,
				MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.IlluminatiMangaRun,
				MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.MangatopiaRun,
				MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.S2Run,
				MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.SenseRun,
				MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.ShoujoSenseRun,
				MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.TripleSevenRun,
				MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.TwistedHelRun,
				MangaCMSOld.ScrapePlugins.M.FoolSlide.Modules.VortexRun,
				MangaCMSOld.ScrapePlugins.M.GameOfScanlationLoader.Run,
				MangaCMSOld.ScrapePlugins.M.Kawaii.Run,
				MangaCMSOld.ScrapePlugins.M.MangaBox.Run,
				MangaCMSOld.ScrapePlugins.M.MangaDex.Run,
				MangaCMSOld.ScrapePlugins.M.MangaHere.Run,
				# MangaCMS.ScrapePlugins.M.MangaMadokami.Run,
				MangaCMSOld.ScrapePlugins.M.MangaStreamLoader.Run,
				MangaCMSOld.ScrapePlugins.M.MangaZuki.Run,
				MangaCMSOld.ScrapePlugins.M.McLoader.Run,
				MangaCMSOld.ScrapePlugins.M.MerakiScans.Run,
				MangaCMSOld.ScrapePlugins.M.WebtoonLoader.Run,
				MangaCMSOld.ScrapePlugins.M.YoMangaLoader.Run,
				MangaCMSOld.ScrapePlugins.M.ZenonLoader.Run,
				MangaCMSOld.ScrapePlugins.M.BuMonitor.Rescan,
				MangaCMSOld.ScrapePlugins.M.BuMonitor.Run,
				MangaCMSOld.ScrapePlugins.H.ASMHentaiLoader.Run,
				MangaCMSOld.ScrapePlugins.H.DjMoeLoader.Run,
				MangaCMSOld.ScrapePlugins.H.DoujinOnlineLoader.Run,
				MangaCMS.ScrapePlugins.H.HBrowseLoader.Run,
				MangaCMSOld.ScrapePlugins.H.Hentai2Read.Run,
				MangaCMSOld.ScrapePlugins.H.HitomiLoader.Run,
				MangaCMS.ScrapePlugins.H.NHentaiLoader.Run,
				MangaCMSOld.ScrapePlugins.H.PururinLoader.Run,
				MangaCMSOld.ScrapePlugins.H.TsuminoLoader.Run,
				MangaCMSOld.ScrapePlugins.M.BooksMadokami.Run,
				MangaCMSOld.ScrapePlugins.H.SadPandaLoader.Run,
		]

	print("Test run!")
	import nameTools as nt

	def callGoOnClass(passedModule):
		print("Passed module = ", passedModule)
		print("Calling class = ", passedModule.Runner)
		instance = passedModule.Runner()
		instance.go()
		print("Instance:", instance)


	nt.dirNameProxy.startDirObservers()
	import signal
	import runStatus

	def signal_handler(dummy_signal, dummy_frame):
		if runStatus.run:
			runStatus.run = False
			print("Telling threads to stop (activePlugins)")
		else:
			print("Multiple keyboard interrupts. Raising")
			raise KeyboardInterrupt


	signal.signal(signal.SIGINT, signal_handler)
	import sys
	import traceback
	print("Starting")
	try:
		if len(sys.argv) > 1 and int(sys.argv[1]) in scrapePlugins:
			plugin, interval = scrapePlugins[int(sys.argv[1])]
			print(plugin, interval)
			callGoOnClass(plugin)
		else:

			print("Loopin!", scrapePlugins)
			for plugin in run:
				print(plugin)
				try:
					callGoOnClass(plugin)
				except Exception:
					print()
					print("Wat?")
					traceback.print_exc()
					# raise
					print("Continuing on with next source.")

	except:
		traceback.print_exc()


	print("Complete")

	nt.dirNameProxy.stop()
	sys.exit()
