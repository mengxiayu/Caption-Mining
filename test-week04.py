courseno = '410'
tidset = set()
fr = open('transcriptions2courses-2021-09-24.csv','r')
fr.readline()
for line in fr:
    arr = line.strip('\r\n').split('\t')
    if arr[7] == courseno:
        tidset.add(arr[0])
        tidset.add(arr[1])
fr.close()
print(len(tidset))
fw = open('corpus_corrected_'+courseno+'.txt','w')
fr = open('week01/corpus_corrected.txt','r')
for line in fr:
    arr = line.strip('\r\n').split('\t')
    tid = arr[0]
    if tid in tidset:
        fw.write(courseno+'\t'+arr[0]+'\t'+arr[1]+'\n')
fr.close()
fw.close()
tids = []
tid2lines = {}
fr = open('week01/nounchunks.txt','r')
for line in fr:
    if not line.startswith('#'):
        arr = line.strip('\r\n').split('\t')
        tid = arr[0]
        tids.append(tid)
        tid2lines[tid] = []
    tid2lines[tid].append(line.strip('\r\n'))
fr.close()
fw = open('nounchunks_'+courseno+'.txt','w')
for tid in tids:
    if tid in tidset:
        line = tid2lines[tid][0]
        fw.write(courseno+'\t'+line+'\n')
        for i in range(1,len(tid2lines[tid])):
            fw.write(tid2lines[tid][i]+'\n')
fw.close()

courseno2word2count = {}
fr = open('corpus_corrected_410.txt','r')
for line in fr:
    arr = line.strip('\r\n').split('\t')
    courseno = arr[0]
    text = ' '+arr[2]+' '
    text = text.replace('.',' . ').replace(',',' , ').replace(';',' ; ').replace("'"," '")
    text = text.replace('?',' ? ').replace('!',' ! ').replace('(',' ( ').replace(')',' ) ')
    while '  ' in text:
        text = text.replace('  ',' ')
    text = text[1:-1].lower()
    for word in text.split(' '):
        if not courseno in courseno2word2count:
            courseno2word2count[courseno] = {}
        if not word in courseno2word2count[courseno]:
            courseno2word2count[courseno][word] = 0
        courseno2word2count[courseno][word] += 1
fr.close()
for courseno,word2count in courseno2word2count.items():
    fw = open('vocabulary_'+courseno+'.txt','w')
    for word,count in sorted(word2count.items(),key=lambda x:-x[1]):
        fw.write(word+'\t'+str(count)+'\n')
    fw.close()

coursenos = [courseno]
import spacy
nlp = spacy.load('en_core_web_sm')
stopwords = nlp.Defaults.stop_words
fw0 = open('stop_stats.txt','w')
for courseno in coursenos:
    words,counts = [],[]
    wordsStop,countsStop = [],[]
    fw = open('vocabulary_'+courseno+'-nonstop.txt','w')
    fr = open('vocabulary_'+courseno+'.txt','r')
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        word,count = arr[0],int(arr[1])
        words.append(word)
        counts.append(count)
        if word in stopwords or len(word) < 2:
            wordsStop.append(word)
            countsStop.append(count)
        else:
            fw.write(word+'\t'+str(count)+'\n')
    fr.close()
    fw.close()
    n = len(words)
    m = sum(counts)
    nStop = len(wordsStop)
    mStop = sum(countsStop)
    fw0.write(courseno+'\t'+str(n)+'\t'+str(nStop)+'\t'+str(100.*nStop/n)
            +'\t'+str(m)+'\t'+str(mStop)+'\t'+str(100.*mStop/m)+'\n')
fw0.close()

courseno2nums = {}
fr = open('nounchunks_'+courseno+'.txt','r')
for line in fr:
    if not line.startswith('#'):
        arr = line.strip('\r\n').split('\t')
        courseno = arr[0]
        if not courseno in courseno2nums:
            courseno2nums[courseno] = []
        courseno2nums[courseno].append(int(arr[2]))
fr.close()
fw = open('courseno-num.txt','w')
for courseno,nums in sorted(courseno2nums.items(),key=lambda x:x[0]):
    fw.write(courseno+'\t'+str(len(nums))+'\n')
fw.close()
for courseno,nums in courseno2nums.items():
    fw = open('numsentences_'+courseno+'.txt','w')
    for num in sorted(nums,key=lambda x:-x):
        fw.write(str(num)+'\n')
    fw.close()

import spacy
nlp = spacy.load('en_core_web_sm')
stopwords = nlp.Defaults.stop_words
courseno2chunk2count = {}
fr = open('nounchunks_'+courseno+'.txt','r')
for line in fr:
    if not line.startswith('#'):
        arr = line.strip('\r\n').split('\t')
        courseno = arr[0]
    if line.startswith('#c'):
        arr = line.strip('\r\n').split('\t')
        chunks = arr[1]
        for chunk in chunks.split(';'):
            words = chunk.split(' ')
            if len(words) > 0:
                while words[0].lower() in stopwords:
                    words.pop(0)
                    if len(words) == 0: break
            if len(words) > 0:
                while words[-1].lower() in stopwords:
                    words.pop(-1)
                    if len(words) == 0: break
            if len(words) > 0:
                _chunk_ = ''
                for word in words:
                    _chunk_ += ' '+word
                _chunk_ = _chunk_[1:]
                if not courseno in courseno2chunk2count:
                    courseno2chunk2count[courseno] = {}
                if not _chunk_ in courseno2chunk2count[courseno]:
                    courseno2chunk2count[courseno][_chunk_] = 0
                courseno2chunk2count[courseno][_chunk_] += 1
fr.close()
for courseno,chunk2count in courseno2chunk2count.items():
    fw1 = open('word2count_'+courseno+'.txt','w')
    fw2 = open('phrase2count_'+courseno+'.txt','w')
    for chunk,count in sorted(chunk2count.items(),key=lambda x:-x[1]):
        if ' ' in chunk:
            fw2.write(chunk+'\t'+str(count)+'\n')
        else:
            fw1.write(chunk+'\t'+str(count)+'\n')        
    fw2.close()
    fw1.close()

