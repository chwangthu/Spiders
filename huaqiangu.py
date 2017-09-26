import urllib, urllib2
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
	url = 'http://www.136book.com/huaqiangu/'
	head = {}
	ua = UserAgent()
	head['User-Agent'] = ua.safari
	req = urllib2.Request(url, headers = head)
	res = urllib2.urlopen(req)
	html = res.read()

	soup = BeautifulSoup(html, 'lxml')
	content = soup.find('div', id = 'book_detail', class_ = 'box1').find_next('div')

	f = open('HuaQianGu.txt', 'w')
	for link in content.ol.children:
		if link != '\n':
			download_url = link.a.get('href')
			print download_url
			download_req = urllib2.Request(download_url, headers = head)
			download_res = urllib2.urlopen(download_req)
			download_html = download_res.read()
			#print download_html
			download_soup = BeautifulSoup(download_html, 'lxml')
			download_content = download_soup.find('div', id = 'content')
			print download_content
			para = download_content.find_all('p', recursive=False)
			f.write(link.text + '\n')
			for item in para:
				#print item.text
				f.write(item.text)
				f.write('\n')
			f.write('\n\n')

	f.close()
