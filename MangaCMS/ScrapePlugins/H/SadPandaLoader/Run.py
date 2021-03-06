

from .DbLoader import DbLoader
from .ContentLoader import ContentLoader

import runStatus

import MangaCMS.ScrapePlugins.RunBase

class Runner(MangaCMS.ScrapePlugins.RunBase.ScraperBase):


	loggerPath = "Main.Manga.SadPanda.Run"
	pluginName = "SadPanda"


	sourceName = "SadPanda"
	feedLoader = DbLoader
	contentLoader = ContentLoader


def test():
	import utilities.testBase as tb

	with tb.testSetup():
		run = Runner()
		run.go()

if __name__ == "__main__":
	test()
