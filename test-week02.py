tid2dept = {}
fr = open('transcriptions2courses-2021-09-24.csv','r')
for line in fr:
    arr = line.strip('\r\n').split('\t')
    dept = arr[5]
    if dept[0].isdigit(): continue
    if dept[0] == ' ': dept = dept[1:]
    tid2dept[arr[0]] = dept
    tid2dept[arr[1]] = dept
fr.close()
fw = open('corpus_corrected_dept.txt','w')
fr = open('week01/corpus_corrected.txt','r')
for line in fr:
    arr = line.strip('\r\n').split('\t')
    tid = arr[0]
    if tid in tid2dept:
        dept = tid2dept[tid]
        fw.write(dept+'\t'+arr[0]+'\t'+arr[1]+'\n')
    else:
        print('error:',tid)
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
fw = open('nounchunks_dept.txt','w')
for tid in tids:
    if tid in tid2dept:
        dept = tid2dept[tid]
        line = tid2lines[tid][0]
        fw.write(dept+'\t'+line+'\n')
        for i in range(1,len(tid2lines[tid])):
            fw.write(tid2lines[tid][i]+'\n')
fw.close()

dept2word2count = {}
fr = open('corpus_corrected_dept.txt','r')
for line in fr:
    arr = line.strip('\r\n').split('\t')
    dept = arr[0]
    text = ' '+arr[2]+' '
    text = text.replace('.',' . ').replace(',',' , ').replace(';',' ; ').replace("'"," '")
    text = text.replace('?',' ? ').replace('!',' ! ').replace('(',' ( ').replace(')',' ) ')
    while '  ' in text:
        text = text.replace('  ',' ')
    text = text[1:-1].lower()
    for word in text.split(' '):
        if not dept in dept2word2count:
            dept2word2count[dept] = {}
        if not word in dept2word2count[dept]:
            dept2word2count[dept][word] = 0
        dept2word2count[dept][word] += 1
fr.close()
fw = open('dept.txt','w')
for dept in dept2word2count:
    fw.write(dept+'\n')
fw.close()
for dept,word2count in dept2word2count.items():
    fw = open('vocabulary_'+dept+'.txt','w')
    for word,count in sorted(word2count.items(),key=lambda x:-x[1]):
        fw.write(word+'\t'+str(count)+'\n')
    fw.close()

depts = []
fr = open('dept.txt','r')
for line in fr:
    depts.append(line.strip('\r\n'))
fr.close()
import spacy
nlp = spacy.load('en_core_web_sm')
stopwords = nlp.Defaults.stop_words
fw0 = open('stop_stats.txt','w')
for dept in depts:
    words,counts = [],[]
    wordsStop,countsStop = [],[]
    fw = open('vocabulary_'+dept+'-nonstop.txt','w')
    fr = open('vocabulary_'+dept+'.txt','r')
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
    fw0.write(dept+'\t'+str(n)+'\t'+str(nStop)+'\t'+str(100.*nStop/n)
            +'\t'+str(m)+'\t'+str(mStop)+'\t'+str(100.*mStop/m)+'\n')
fw0.close()

dept2nums = {}
fr = open('nounchunks_dept.txt','r')
for line in fr:
    if not line.startswith('#'):
        arr = line.strip('\r\n').split('\t')
        dept = arr[0]
        if not dept in dept2nums:
            dept2nums[dept] = []
        dept2nums[dept].append(int(arr[2]))
fr.close()
fw = open('dept-num.txt','w')
for dept,nums in sorted(dept2nums.items(),key=lambda x:x[0]):
    fw.write(dept+'\t'+str(len(nums))+'\n')
fw.close()
for dept,nums in dept2nums.items():
    fw = open('numsentences_'+dept+'.txt','w')
    for num in sorted(nums,key=lambda x:-x):
        fw.write(str(num)+'\n')
    fw.close()

import spacy
nlp = spacy.load('en_core_web_sm')
stopwords = nlp.Defaults.stop_words
dept2chunk2count = {}
fr = open('nounchunks_dept.txt','r')
for line in fr:
    if not line.startswith('#'):
        arr = line.strip('\r\n').split('\t')
        dept = arr[0]
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
                if not dept in dept2chunk2count:
                    dept2chunk2count[dept] = {}
                if not _chunk_ in dept2chunk2count[dept]:
                    dept2chunk2count[dept][_chunk_] = 0
                dept2chunk2count[dept][_chunk_] += 1
fr.close()
for dept,chunk2count in dept2chunk2count.items():
    fw1 = open('word2count_'+dept+'.txt','w')
    fw2 = open('phrase2count_'+dept+'.txt','w')
    for chunk,count in sorted(chunk2count.items(),key=lambda x:-x[1]):
        if ' ' in chunk:
            fw2.write(chunk+'\t'+str(count)+'\n')
        else:
            fw1.write(chunk+'\t'+str(count)+'\n')        
    fw2.close()
    fw1.close()

