#!/usr/bin/python
# coding=utf-8
#-*-encoding utf-8 -*-
from __future__ import unicode_literals
from os import path, makedirs
import os
import codecs
import urllib2
import bs4
from bs4 import BeautifulSoup
import re
import treetaggerwrapper
import nltk
from nltk.corpus.reader import CategorizedTaggedCorpusReader
import random
from nltk import precision
from nltk.classify import NaiveBayesClassifier
import collections


#########Variables constantes
#Répertoires de sortie
outDir = "output/article"
outDirTag = "corpus/treetagger"

#Gamme de la liste des catégories
rangeFrom = 0
rangeTo = 1

#Nom du site
domain = "http://www.lemonde.fr"

#Catégories
#listeCat = ["politique","culture","economie","sport","sciences"]
listeCat = ["culture","sport"]

stop_words=['à','allô','aucuns','auriez','auxdits','aviez','ayons','bof','çà  ','certaines','chez','comment','da','desquels','deviez','devras','doit','dues','dût','es','êtes','eurêka','excepté','fouchtra','fûmes','ho','hurrah','laquelle','leur','mazette','mâtin','ne','nulle','or','outre','pas','plein','pourraient','pourvu','pouviez','puis','pussent','que','quoi','saperlipopette','serait','sien','sommes','ta','telles','touchant','une','veuillez','voilà','voudrez','voulante','voulue','vôtre	afin','alors','auquel','aurions','auxquelles','avions','aïe','boum','car','certains','chic','concernant','dans','devaient','devions','devrez','doive','duquel','eh','et','étiez','eus','eûmes','furent','fût','holà','hé','le','leurs','me','miséricorde','ni','nulles','ôté','palsambleu','patatras','plouf','pourrais','pouvaient','pouvions','puisque','put','quel','quoique','sapristi','seras','sienne','son','tandis','tels','tous','unième','veuillons','vos','voudriez','voulantes','voulues','vôtres	ah','apr.','aura','aurons','auxquels','avoir','bah','bravissimo','ce','ces','chiche','contre','de','devais','devoir','devriez','doivent','durant','elle','étaient','étions','eusse','eût','fus','fûtes','hop','il','ledit','lorsque','merci','moi','nonobstant','nuls','ou','pan','pechère','plus','pourrait','pouvais','pouvoir','puisse','pécaïre','quelle','rataplan','sauf','serez','siennes','sont','tant','tes','tout','unièmes','veulent','votre','voudrions','voulants','voulurent','zut	ai','as','aurai','auront','avaient','avons','basta','bravo','ceci','cet','chouette','corbleu','debout','devait','devons','devrions','doives','durent','elles','étais','être','eussent','eûtes','fusse','grâce','hormis','ils','lequel','lui','merde','moins','nos','ô','où','par','pendant','plusieurs','pourras','pouvait','pouvons','puissent','pût','quelles','revoici','se','seriez','siens','sous','taratata','tien','toute','v','lan','veut','voudra','voudrons','voulez','voulus',' aie','attendu','auraient','autant','avais','ayant','beaucoup','ç','a','cela','cette','chut','coucou','depuis','devant','devra','devrons','donc','dus','en','était','eu','eusses','évohé','fussent','ha','hors','jarnicoton','les','là','mes','mon','notre','oh','ouais','parbleu','peu','pouah','pourrez','pouvant','psitt','puisses','qq.','quelqu','un','revoilà','selon','serions','sinon','soyez','tayaut','tienne','toutes','va','veux','voudrai','voudront','vouliez','voulussent',' aient','au','aurais','autre','avait','ayante','bernique','ç','aura ','celle','ceux','ciao','couic','des','devante','devrai','devront','dont','dussent','encontre','étant','eue','eussiez','évoé','fusses','hein','hou','je','lesdites','ma','mien','morbleu','nôtre','ohé','ouf','parce','peuchère','pour','pourriez','pouvante','pst','puissiez','qqch.','quelqu','une','rien','sera','serons','soi','soyons','taïaut','tiennes','tu','vers','via','voudraient','voulaient','voulions','voulut', 'aies','aucun','aurait','autres','avant','ayantes','bien','ç','aurait','celles','chacun','clic','crac','desdites','devantes','devraient','dia','du','dut','endéans','étante','eues','eussions','fi','fussiez','hem','hourra','jusque','lesdits','made','mienne','motus','nôtres','olé','ouille','pardi','peut','pourquoi','pourrions','pouvantes','pu','puissions','qqn','quels','sa','serai','seront','soient','stop','te','tiens','tudieu','veuille','vivement','voudrais','voulais','vouloir','voulût',' ait','aucune','auras','aux','avec','ayants','bigre','ç','avait ','celui','chacune','clac','cric','desdits','devants','devrais','diantre','dudit','dès','entre','étantes','euh','eut','fichtre','fussions','hep','hue','la','lesquelles','mais','miennes','moyennant','nous','on','oust','pardieu','peuvent','pourra','pourrons','pouvants','pue','purent','quand','qui','sacristi','seraient','ses','sois','suis','tel','toi','turlututu','veuillent','vlan','voudrait','voulait','voulons','vous',' 	al.','aucunes','aurez ','auxdites','avez','ayez','bis','ça ','cependant','chaque','comme','crénom','desquelles','devez','devrait','dois','due','dû','envers','étants','eurent','eux','fors','fut','heu','hum','ladite','lesquels','malgré','miens','na','nul','ont','ouste','parmi','peux','pourrai','pourront','pouvez','pues','pus','quant','quiconque','sans','serais','si','soit','sur','telle','ton','un','veuilles','voici','voudras','voulant','voulu','vu']



#########Créer des répertoires si n'existe pas
if not path.exists(outDir):
	makedirs(outDir)
if not path.exists(outDirTag):
	makedirs(outDirTag)


#########Charge TreeTagger(pack de langue,TreeTagger chemin lib dans la maison). Par exemple ~/TreeTagger
tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR="TreeTagger")


#########Les fonctions
#Fonction regex exacte(Regex,Le texte,Remplacer par)
def replaceContent(regex,text,replace=''):
	#Créer motif
	pattern=re.compile(regex,re.UNICODE)
	#Chercher
	match=re.search(pattern,text)
	#Remplacer si trouvé
	if match:
		#Substring
		text=re.sub(pattern,replace,text)
	return text
#Fonction qui appelle toto(Le texte)
def filterHTML(text):
	#Replacer de Lire aussi
	text = replaceContent(r'<p class="lire.*">\s+Lire aussi :\s+\xa0\s+<a href=".*">\s+.*\s+</a>\s+</p>',text)
	#Replacer de script
	#text = replaceContent(r'<script(\s|.*)+<\/script>',text)
	#Replacer de style
	#text = replaceContent(r'<style(\s|.*)+<\/style>',text,)
	#replacer de \t\n\r\f\v
	text = replaceContent(r'[ \t\n\r\f\v]+',text,' ')
	#
	text = replaceContent(r"(?<!')\s( )+(?=.)",text)
	#Replacer Twitter tag
	text = replaceContent(r'<blockquote class="twitter.*>[\s\S]+<\/blockquote>',text)
	#Replacer de graphique
	text = replaceContent(r'<div class="contenu-portfolio-atome"\s.[\s\S]*<\/a>\s.*\s.+',text)
	return text
#
def get_word_features(all_words, stop_words,n):
	word_features = []
	for w in  all_words.keys()[:n]:
		if(not(w in stop_words)):
			word_features.append(w)
	return word_features
#
def sent_features(sent):
	sent_words=set(sent)
	features={}
	for word in word_features:
		features['contains(%s)'%word]=(word in sent_words)
	return features
#
def precision_recall (classifier, test_set):
	refsets = collections.defaultdict(set)
	testsets = collections.defaultdict(set)
	for i, (sent, category) in enumerate(test_set):
		refsets[category].add(i)
		observed = classifier.classify(sent)
		testsets[observed].add(i)
	prec ={}
	rec ={}
	for category in lemonde.categories():
		prec[category] = nltk.precision(refsets[category], testsets[category])
		rec[category] = nltk.recall(refsets[category], testsets[category])
	return prec, rec
#
def fmesure(category):
	precc=float(PREC[category])
	rapp=float(RAPP[category])
	fm=(2*precc*rapp)/(precc+rapp)
	return category,fm


#########Source principale
#chaque boucle de catégorie
for cat in listeCat:
	#Catégorie sous-répertoire
	sourDir=outDir+"/"+cat
	if not path.exists(sourDir):
		makedirs(sourDir)
	#Nom de l'article Tagged
	mmFichierTag = "article_"+cat+"_tagged.txt"
	#Plage liste boucle
	for i in range(rangeFrom,rangeTo):
		print "Getting /{}/{}.html".format(cat,i)
		#Obtenir article archive à partir url
		fichier=urllib2.urlopen(domain+"/{}/{}.html".format(cat,i))
		#HTML pour le HTML valide
		Soup = BeautifulSoup( fichier,"html5lib")
		#Trouver article urls
		blockURLS = Soup.findAll(href=re.compile(r'\/\S+\/article\/\S+.html'))
		#Nom de l'article de texte
		mmFichier = "article_"+cat+"_"+str(i)+".txt"
		#Si elles existent déjà fichiers texte de l'article
		if not os.path.isfile(os.path.join(sourDir, mmFichier)):
			#Flux d'écriture de fichier ouvert avec UTF8
			with codecs.open(os.path.join(sourDir, mmFichier),"w",encoding="utf-8") as fout:
				#pour cent
				perc=0
				#boucle pour chaque URL
				for e in blockURLS:
					#Obtenir l'article de URL
					fichie=urllib2.urlopen(domain+e["href"])
					#HTML pour le HTML valide
					Sou=BeautifulSoup( fichie,"html5lib")
					#Obtenir l'article par id
					article = unicode(Sou.find(id=re.compile("articleBody")))
					#Appliquer nos filtres
					article = filterHTML(article)
					#HTML pour le HTML valide
					article = BeautifulSoup( article,"html5lib")
					#Obtenir le contenu de l'article
					article = article.get_text()
					#Ecrire dans le fichier
					fout.write(article)
					#Augmenter pour cent
					perc = perc + 1
					#l'état d'impression
					print sourDir+"/"+mmFichier+" "+str(100*perc/len(blockURLS))+"%"
			##Près flux
			fout.close()
		#Si elles existent déjà texte de l'article "tagged" fichiers
		if not os.path.isfile(os.path.join(outDirTag, mmFichierTag)):
			#Flux d'écriture de fichier ouvert avec UTF8
			with codecs.open(os.path.join(outDirTag, mmFichierTag),"w",encoding="utf-8") as fouttag:
				#pour cent
				perc=0;
				#boucle pour chaque URL
				for e in blockURLS:
					#Obtenir l'article de URL
					fichie=urllib2.urlopen(domain+e["href"])
					#HTML pour le HTML valide
					Sou=BeautifulSoup( fichie,"html5lib")
					#Obtenir l'article par id
					article = unicode(Sou.find(id=re.compile("articleBody")))
					#Appliquer nos filtres
					article = filterHTML(article)
					#HTML pour le HTML valide
					article = BeautifulSoup( article,"html5lib")
					#Obtenir le contenu de l'article
					article = article.get_text()

					#Générer des balises et écrire dans le fichier
					tags=tagger.tag_text(article)
					for tag in tags:
						fouttag.write(tag+"\n")
					#Augmenter pour cent
					perc = perc + 1
					#l'état d'impression
					print outDirTag+"/"+mmFichierTag+" "+str(100*perc/len(blockURLS))+"%"
			#Près flux
			fouttag.close()

print "Categorized Tagged Corpus Reader:"
#Lire les fichiers catégorisés
lemonde=CategorizedTaggedCorpusReader(outDirTag,r'\S+_tagged.txt',cat_pattern='article_(\w+)_tagged.txt')

phrases_total=0
#'''
#chaque boucle de catégorie tagué
for category in lemonde.categories():
	#Compter les caractères
	nb_caractero=len(lemonde.raw(categories=category))
	#Compter les mots
	nb_moto= len(lemonde.words(categories=category))
	#Compter les phrases
	nb_phrases=len(lemonde.sents(categories=category))
	#Compter les vocabs
	nb_vocab=len(set([w.lower() for w in lemonde.words(categories=category)]))
	phrases_total=phrases_total+nb_phrases
	#Chiffres d'impression pour chaque catégorie
	print (category+": Caracteres "+unicode(nb_caractero)+", Mots "+unicode(nb_moto)+", Phrases "+unicode(nb_phrases)+", Vocab "+unicode(nb_vocab)+"\n")

#'''


documents=[(sent,category) for category in lemonde.categories() for sent in lemonde.sents(categories=category)]
random.shuffle(documents)
all_words=nltk.FreqDist(w.lower() for w in lemonde.words())

word_features=get_word_features(all_words,stop_words,10)

featuresets=[(sent_features(sent),category) for (sent,category) in documents]

a=int(phrases_total*0.7)
b=phrases_total-a
train_set,test_set=featuresets[a:],featuresets[:b]

classifier=nltk.NaiveBayesClassifier.train(train_set)
PrecisionRappel=precision_recall(classifier,test_set)
PREC=PrecisionRappel[0]
RAPP=PrecisionRappel[1]

print PREC
print RAPP

for category in lemonde.categories():
	try:
		print fmesure(category)
	except:
		print "("+"'"+category+"'"+",pas me valeur)"

#########La fin


