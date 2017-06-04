import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt

ivectorFile = "/work/jiacen/spk_ivector"
ivectorFile = "C:\Users\Zhang\Desktop\spk_ivector"

spk2iv = dict()
speakerAvg = []

with open(ivectorFile) as source:
    for line in source:
        contents = line.split()
        index = contents[0]
        features = map(float, contents[2:-1])
        if index in spk2iv:
            spk2iv[index].append(features)
        else:
            spk2iv[index] = [features]
innerSpeaker = []
betweenSpeaker = []

for speaker in spk2iv:
    for i in range(len(spk2iv[speaker])):
        for j in range(i+1, len(spk2iv[speaker])):
            temp = spatial.distance.cosine(spk2iv[speaker][i], spk2iv[speaker][j])

            innerSpeaker.append(temp)

speakers = spk2iv.keys()
"""
for i in range(len(speakers)-1):
    targets = speakers[i+1:]
    left = speakers[i]
    for ivector in spk2iv[left]:
        for target in targets:
            for one in spk2iv[target]:
                temp = spatial.distance.cosine(ivector, one)
                betweenSpeaker.append(temp)
    break
"""
for speaker in speakers:
	wow = np.array(spk2iv[speaker])
	avgArray = np.mean(wow,axis = 0)
	speakerAvg.append(avgArray)

for i in range(len(speakerAvg)-1):
	for j in range(i+1, len(speakerAvg)):
		betweenSpeaker.append(spatial.distance.cosine(speakerAvg[i], speakerAvg[j]))

plt.hist(innerSpeaker)

plt.hist(betweenSpeaker)
