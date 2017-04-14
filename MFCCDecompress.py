#!/usr/bin/python
from subprocess import call
import sys
import os
from multiprocessing import Pool
from time import sleep

tmpDire = "/work/jiacen/temp"
resultDire = "/work/jiacen/result"
dire = "/work/jiacen/mfcc"
vadDict = {}

def decompressMFCC(title):
	#give the mfcc features after vad, organized as:
	#name\n
	#floats\n
	#Cautions:
	#featFile is in the full path
	#Vad files and feat files are not in the same order!
	#First, read all vad in memory
	vad_head = "vad_" + title
	vadFiles = []
	for file in os.listdir(dire):
		if file.startswith(vad_head) and file.endswith(".ark"):
			vadFiles.append(os.path.join(dire, file))
	for vad in vadFiles:
		tmpVadFile = os.path.join(tmpDire, vad.replace(".ark", ""))
		commandVad = ["copy-vector", "ark:"+vad, "ark,t:"+tmpVadFile]
		call(commandVad)
		#Vad-file type: filename_(A|B) [ 0 1 ... 0 ] \n
		with open(tmpVadFile) as vadIn:
			for line in vadIn:
				name = (line.split()[0]).strip()
				if name in vadDict:
					print "ERR, duplicated name"
					exit(1)
				content = line[line.find('[')+1:line.find(']')]
				content = [int(one) for one in content.split()]
				vadDict[name] = content

	mfccOutName = featFile[featFile.find("raw_"): featFile.find(".ark")]
	tmpFeatFile = os.path.join(tmpDire, mfccOutName)
	commandFeat = ["copy-feats", "ark:"+featFile, "ark,t:"+tmpFeatFile]
	call(commandFeat)
	#now we got the full mfcc file in readable type
	#then find the vadFile
	vadFile = featFile.replace("raw_mfcc", "vad")
	tmpVadFile = tmpFeatFile.replace("raw_mfcc", "vad")
	commandVad = ["copy-vector", "ark:"+vadFile, "ark,t:"+tmpVadFile]
	call(commandVad)
	#then, read these two file and get the useful feature, store them in the result file
	feat = open(tmpFeatFile)
	vad = open(tmpVadFile)

	resultName = mfccOutName.replace("raw_", "")
	resultFile = os.path.join(resultDire, resultName)
	result = open(resultFile, "w")

	while True:
		"""
		Vad-file type: filename_(A|B) [ 0 1 ... 0 ] \n
		Feat-file type: filename_(A|B) [ \n
						20 floats \n
						20 floats ]\n
		"""
		currentVad = vad.readline()
		if not currentVad:
			break
		currentName = currentVad.split()[0]
		result.write(currentName + "\n")
		vadArray = currentVad[currentVad.find("[")+1:currentVad.find("]")]
		vadArray = vadArray.split()
		vadArray = [int(one) for one in vadArray]
		vadIter = iter(vadArray)
		while True:
			featLine = feat.readline()
			if not featLine:
				break
			if "[" in featLine:
				relatedFile = featLine.split()[0]
				if relatedFile != currentName:
					exit(0)
			else:
				if vadIter.next() == 1:
					#get the frame according to VAD
					if "]" in featLine:
						featLine = featLine[:-2]
					else:
						featLine = featLine[:-1]
					result.write(featLine+'\n')
		result.write('-'*30+'\n')
	for one in [feat, vad, result]:
	#close the files
		one.close()
	sleep(2)
	os.remove(tmpFeatFile)
	os.remove(tmpVadFile)
	return resultFile

if __name__ == "__main__":
	for i in range(1, len(sys.argv)-1):
		try:
			if sys.argv[i] == "-d":
				dire = sys.argv[i+1]
			if sys.argv[i] == "-o":
				resultDire = sys.argv[i+1]
			if sys.argv[i] == "-t":
				tmpDire = sys.argv[i+1]
		except:
			exit(1)

	#dire: kaldi-type feature files
	#resultDire: output directory
	#tmpDire: temp files directory
	os.chdir(dire)
	allFiles = os.listdir(dire)
	titles = set()
	for f in allFiles:
		if f.startswith("raw") and f.endswith(".ark"):
			title = f.split(".")[0]
			title = title.replace("raw_mfcc_","")
			titles.add(title)
	titles = list(titles)
	for title in titles:
		decompressMFCC(title)
	exit(0)
	p = Pool(2)
	tmpFiles = p.map(decompressMFCC, titles)
	print tmpFiles