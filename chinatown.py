# -*- coding: utf-8 -*-

from lxml import etree 
import re, sys, csv

drevnii = []
novii = []
translate = []
transkr = []


dd = 0
nn = 0
tt = 0
tr = 0

chinesedict = open("chinesedict.csv", "w", encoding='utf-8')
writerfortranstext = open('transtext.xml', 'w', encoding='utf-8')

def dict_chinese():
	dict1 = open("cedict_ts.u8")
	dictwords = dict1.readlines()
	for o in dictwords:        #древнекитайское слово
		o = o.split(" ", 1)
		drevnii.append(o[0])
	for n in dictwords:        #современное кит слово
		n = n.split(" ", 2)
		novii.append(n[1])
	for t in dictwords:        #транскрипция
		t = t.replace("[","]").split("]", 3)
		translate.append(t[1])
	for tr in dictwords:       #перевод слова
		tr = tr.split("/", 4)
		transkr.append(tr[1])

	dict1.close()				

def creategoodvalue():
	dict_chinese()

	global drevnii1
	global novii1
	global translate1
	global transkr1
	global dd
	global nn
	global tt
	global tr

	drevnii1 = [[i, ] for i in drevnii] #массив массивов
	for item in drevnii1:
		drevnii1[dd] = ",".join(item) #массив строк
		dd = dd + 1		#счетчик
	novii1 = [[i, ] for i in novii]
	for item in novii1:
		novii1[nn] = ",".join(item)
		nn = nn + 1
	translate1 = [[i, ] for i in translate]
	for item in translate1:
		translate1[tt] = ",".join(item)
		tt = tt + 1
	transkr1 = [[i, ] for i in transkr]
	for item in transkr1:
		transkr1[tr] = ",".join(item)
		tr = tr + 1

	return drevnii1, novii1, transkr1, translate1

def writedict(chinesedict):
	creategoodvalue()

	global rowdic

	csvchinese = csv.writer(chinesedict, delimiter='\t', lineterminator='\n')
	header = (["W1 - Old"] + ["W2 - New"] + ["Translate"] + ["Transkription"])
	rows = zip(drevnii1, novii1, transkr1, translate1) #группировка элементов нескольких списков
	csvchinese.writerow(header)
	for row in rows:
		csvchinese.writerow(row)

	with open("cedict_ts.u8", 'r') as file:
			rowdic = {}
			dict1 = file.readlines()
			for each in dict1:
				each = each.split(' ')
				rowdic[each[1]] = ' '.join(each[2:])

def parse_chinese():
	writedict(chinesedict)

	pr = 0
	tree = etree.parse("stal.xml")
	tree2 = tree.xpath("/html/body/se")
	writerfortranstext.write('<?xml version="1.0" encoding="utf-8"?>\n<html>\n<head>\n</head>\n<body>')

	for t in tree2:
		celayastroka = t.text
		strochka = re.sub(r"[，。！？：“”……；]", " ", celayastroka)
		strochkanorm = strochka.lstrip()
		strochkanorm2 = strochkanorm.split(" ")
		strochkanorm3 = list(filter(None, strochkanorm2))
		strochkanorm4 = ''.join(strochkanorm3)
		lenlen = len(strochkanorm4)
		writerfortranstext.write('\n<se>”')
		while lenlen > 0:
			if strochkanorm4[0:lenlen] in rowdic.keys():  #слово в словаре
				findword = strochkanorm4[0:lenlen]
				writeStal = '\n<w>'
				valuefromdict = rowdic[findword].split('/', 1)
				valuefromdict[1] = valuefromdict[1].replace('\n', '')
				writeStal = writeStal + '<ana lex=\"' + findword + '\" transcr=\"' + valuefromdict[0].strip() + '\" sem=\"' + '/'+ valuefromdict[1] + '\"/>' 
				writeStal = writeStal + findword + '</w>'
				writerfortranstext.write(writeStal) #пишем результат
				strochkanorm4 = strochkanorm4[lenlen:]
				lenlen = len(strochkanorm4)
			else:
				lenlen-=1
		writerfortranstext.write('”</se>')
	writerfortranstext.write('</body>\n</html>')

parse_chinese()

sys.exit()