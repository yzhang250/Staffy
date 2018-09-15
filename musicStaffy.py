# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import urllib
import sys
import os
from fpdf import FPDF

# given a key word and search from the below website, scrap all the staff from the search results
url_basic="http://www.everyonepiano.cn"


#this is the func will be used to get and write the file in dir
def print_staff_from_soup_img(soup_img,name):
	imgList=[]
	for i in range(0,len( soup_img.find_all("img",{"src":re.compile("/pianomusic")}))/2):
		img=url_basic+soup_img.find_all("img",{"src":re.compile("/pianomusic")})[i].get("src")
		f = open(name+str(i+1),'wb')
		img_content=urllib.urlopen(img).read()
		f.write(img_content)
		imgList.append(name+str(i+1))
		f.close()
	pdf = FPDF()
	for image in imgList:
		pdf.add_page()
		pdf.image(image,x = None, y = None, w = 200, h = 265, type = 'PNG', link = '')
	pdf.output(name.encode("utf8")+".pdf", "F")

def main():
	if len(sys.argv)!=2:
		print "We need ONE keyword to search!"
		sys.exists(1)


	#create a new folder and cd to it
	path = r'/Users/yzhang250/Desktop/计算机学习/Staff/'+sys.argv[1]
	if not os.path.exists(path):
		os.makedirs(path)
	os.chdir(path)
	#scrolling the pages in search results
	for page in range(1,200):
    	#start to parse the search result of the key word----sys.argv[1]
		url_kw='http://www.everyonepiano.cn/Music-search/?word='+sys.argv[1]+'&come=web&p='+str(page)
		r_kw=requests.get(url_kw)
		soup_kw=BeautifulSoup(r_kw.content,'lxml')

		if soup_kw.find('span',{"class":"current"}).text!=str(page):
			break
		else:

			#list out all the musics from the key word and put into a list of links
			tags=soup_kw.find_all("a",{"class":"Title"})# this find all the
			links=[]
			for i in range(0,len(tags)):
				links.append(tags[i].get('href'))


			#get and print out the stave from EACH link in links list
			for i in range(0,len(links)):
				#get the soup_music, which is the page for each music
				url_music=url_basic+links[i]
				r_music=requests.get(url_music)
				soup_music=BeautifulSoup(r_music.content,'lxml')
				num_match=re.search("\d+",str(soup_music.find("div",{"class":"EOPRTRight"})))
				if num_match!=None:
					music_num=num_match.group()
					url_img="http://www.everyonepiano.cn/Stave-"+music_num+".html"
					r_img=requests.get(url_img)
					soup_img=BeautifulSoup(r_img.content,'lxml')
					# this is to determine the name of the music
					name=soup_music.h1.text
					if not os.path.exists(path+'/'+name.encode("utf8")):
						os.makedirs(path+"/"+name.encode("utf8"))
						os.chdir(path+"/"+name.encode("utf8"))
						print_staff_from_soup_img(soup_img,name)
					os.chdir(path)
				else:
					continue



if __name__ == '__main__':
	main()
