#-*- coding:utf-8 -*-
import urllib
import urllib2
import re
from bs4 import BeautifulSoup

wikiUrl = 'https://en.wikipedia.org'
class Player:
	def __init__(self, baseUrl, max):
		self.allTeams = []
		self.allPlayers = []
		self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		self.headers = { 'User-Agent' : self.user_agent}
		self.baseURL = baseUrl
		self.file = None
		self.number = 0
		self.maxPlayer = max

	def getCategory(self):
		url = 'https://en.wikipedia.org/wiki/Category:National_Basketball_Association_players_by_club'
		response = urllib2.urlopen(url)
		pageCode = response.read().decode('utf-8')
		pattern = re.compile(r'<div class="CategoryTreeItem">.*?wiki/Category:(.*?)">')
		items = re.findall(pattern, pageCode)
		for item in items:
			#print item
			self.allTeams.append(item)
	def getSingleLink(self, baseUrl, category):
		print 'getting single link'
		html = urllib2.urlopen(baseUrl + category)
		#print "finding in " + str(html)
		soup = BeautifulSoup(html, 'html.parser')
		links = soup.find("div", id="mw-pages").find_all('a', href=re.compile("^(/wiki/)((?!;)\S)*$"))
		i = 0
		for item in links:
			#print item.attrs['href']
			i += 1
			if i > 2:
				self.allPlayers.append(item.attrs['href'])
				self.number += 1
		#print self.allPlayers
	def getPage(self, name):
	 	try:
	 		url = wikiUrl + str(name)
	 		request = urllib2.Request(url, headers = self.headers)
	 		response = urllib2.urlopen(request)
	 		pageCode = response.read().decode('utf-8')
	 		return pageCode
	 	except urllib2.URLError, e:
	 		if hasattr(e, "reason"):
	 			print u"没能打开这个运动员的页面，错误原因", e.reason
	 			return None

	#每个球员的姓名 出生日期 国籍
	def getSingleInfo(self, name):
		pageCode = self.getPage(name)
		if not pageCode:
			print u"页面加载失败..."
			return None
		pattern = re.compile(r'<caption class="fn summary">(.*?)</caption>.*?"bday">(.*?)</span>.*?Nationality.*?<td>(.*?)</td>', re.S)
		items = re.findall(pattern, pageCode)
		for item in items:
			return "Name:"+item[0]+"\n" +"Born:"+item[1]+"\n"+"Nationality:"+item[2]+"\n\n"


	def start(self):
		self.getCategory()
		for item in self.allTeams:
			if self.number < self.maxPlayer:
				self.getSingleLink(self.baseURL, item)
			#print self.allPlayers
		print "We will search " + str(len(self.allPlayers)) 
		self.file = open("player.txt", "w+")
		for item in self.allPlayers:
			print item
			content = self.getSingleInfo(item)
			if content == None:
				self.file.write("Cannot get the information of the player\n")
			else:
				self.file.write(content.encode('utf-8'))

		

baseURL = 'https://en.wikipedia.org/wiki/Category:'
player = Player(baseURL, 1000)
#player.getSingleLink(baseURL, 'Baltimore_Bullets_(1944–54)_players')
#player.getPage('/wiki/John_Abramovic')
#player.getSingleInfo('/wiki/Don_Asmonga')
player.start()
