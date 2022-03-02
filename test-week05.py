'''
recordset = set()
fr = open('data/transcriptions2courses-2021-09-24.csv','r')
head = fr.readline()
for line in fr:
    record = line.strip('\r\n')
    arr = record.split('\t')
    if arr[7] == '410':
        recordset.add(record)
fr.close()
tid2records = {}
for record in recordset:
    arr = record.split('\t')    
    tid = arr[0]
    if not tid in tid2records:
        tid2records[tid] = []
    tid2records[tid].append(record)
tid2tms = {}
fr = open('data/allcaptions-2021-09-24.csv','r')
fr.readline()
for line in fr:
    arr = line.strip('\r\n').split('\t')
    tid = arr[0]
    if tid in tid2records:
        tm = arr[1]
        if not tid in tid2tms:
            tid2tms[tid] = []
        tid2tms[tid].append(tm)
fr.close()
tid2period = {}
for tid, tms in tid2tms.items():
    tms = sorted(tms)
    tid2period[tid] = [tms[0],tms[-1]]
records = []
for tid, period in sorted(tid2period.items(),key=lambda x:x[1][0]):
    for record in sorted(tid2records[tid]):
        records.append(period[0]+'\t'+period[1]+'\t'+record)
year2lid2records = [{},{}]
for record in records:
    arr = record.split('\t')
    year,lname = int(arr[0][:4]),arr[6]
    lid = -1
    for x in lname.split(' '):
        if len(x) > 0 and x.isdigit():
            lid = int(x)
            break
    if 'UIUC' in lname:
        if not year in year2lid2records[0]:
            year2lid2records[0][year] = {}
        if not lid in year2lid2records[0][year]:
            year2lid2records[0][year][lid] = []
        year2lid2records[0][year][lid].append(record)
    else:
        if not year in year2lid2records[1]:
            year2lid2records[1][year] = {}
        if not lid in year2lid2records[1][year]:
            year2lid2records[1][year][lid] = []
        year2lid2records[1][year][lid].append(record)
fw = open('transcriptions2courses-410.txt','w')
fw.write('starttime\tendtime\t'+head.strip('\r\n')+'\n')
for i in [0,1]:
    for year, lid2records in sorted(year2lid2records[i].items(),key=lambda x:x[0]):
        for lid, records in sorted(lid2records.items(),key=lambda x:x[0]):
            for record in records:
                fw.write(record+'\n')
fw.close()
'''

import spacy
nlp = spacy.load('en_core_web_sm')
stopwords = nlp.Defaults.stop_words
tid2lines = {}
fr = open('week01/nounchunks.txt','r')
for line in fr:
    if not line.startswith('#'):
        arr = line.strip('\r\n').split('\t')
        tid = arr[0]
        tid2lines[tid] = []
    tid2lines[tid].append(line.strip('\r\n'))
fr.close()
tidlst = [[] for i in range(6)]
for i in range(6):
    fr = open('week05/transcriptions2courses-410-c'+str(i)+'.txt','r')
    fr.readline()
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        tid,vname = arr[2],arr[6]
        if tid in tid2lines:
            tidlst[i].append([tid,vname])
    fr.close()
fw = open('week05/data.txt','w')
fw.write('offering\tlecture\tvideoname\tchunks\n')
for i in range(6):
    for j in range(len(tidlst[i])):
        s = ''
        tid,vname = tidlst[i][j]
        for line in tid2lines[tid]:
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
                        s += ';'+_chunk_
        fw.write(str(i)+'\t'+str(j)+'\t'+vname+'\t'+s[1:]+'\n')
fw.close()

oid2lectures = {}
fr = open('week05/data.txt','r')
fr.readline()
for line in fr:
    arr = line.strip('\r\n').split('\t')
    oid,lecture = int(arr[0]),arr[3].split(';')
    if not oid in oid2lectures:
        oid2lectures[oid] = []
    oid2lectures[oid].append(lecture)
fr.close()
fw = open('week05/heatmap-bigram.txt','w')
for oid,lecture in oid2lectures.items():
    n = len(lecture)
    chunksets = [set(lecture[i]) for i in range(n)]
    chunk2count = {}
    for chunkset in chunksets:
        for chunk in chunkset:
            if not chunk in chunk2count:
                chunk2count[chunk] = 0
            chunk2count[chunk] += 1
    chunkselected = set()
    for chunk,count in chunk2count.items():
        if ' ' in chunk and count > 1:
            chunkselected.add(chunk)
    fw0 = open('week05/bigram-'+str(oid)+'.txt','w')
    for chunk,count in sorted(chunk2count.items(),key=lambda x:-x[1]):
        if chunk in chunkselected:
            fw0.write(chunk+'\t'+str(count)+'\n')
    fw0.close()
    for i in range(n):
        chunksets[i] = chunksets[i] & chunkselected
    chunk2vid = {}
    for i in range(n):
        for chunk in chunksets[i]:
            if not chunk in chunk2vid:
                chunk2vid[chunk] = i
    m = len(chunk2vid)
    fw.write('offering'+'\t'+str(oid)+'\t'+'noun chunks'+'\t'+str(m)+'\n')
    s = ''
    for i in range(n):
        s += '\t'+'video '+str(i)
    fw.write(s+'\n')
    for i in range(n):
        vid2count = {}
        for chunk in chunksets[i]:
            vid = chunk2vid[chunk]
            if not vid in vid2count:
                vid2count[vid] = 0
            vid2count[vid] += 1
        s = 'video '+str(i)
        for vid in range(i+1):
            count = 0
            if vid in vid2count:
                count = vid2count[vid]
            s += '\t'+str(count)
        fw.write(s+'\n')
    fw.write('\n')
fw.close()

oid2lectures = {}
fr = open('week05/data.txt','r')
fr.readline()
for line in fr:
    arr = line.strip('\r\n').split('\t')
    oid,lecture = int(arr[0]),arr[3].split(';')
    if not oid in oid2lectures:
        oid2lectures[oid] = []
    oid2lectures[oid].append(lecture)
fr.close()
fw = open('week05/heatmap-unigram.txt','w')
for oid,lecture in oid2lectures.items():
    n = len(lecture)
    chunksets = [set(lecture[i]) for i in range(n)]
    chunk2count = {}
    for chunkset in chunksets:
        for chunk in chunkset:
            if not chunk in chunk2count:
                chunk2count[chunk] = 0
            chunk2count[chunk] += 1
    chunkselected = set()
    for chunk,count in chunk2count.items():
        if count > 1:
            chunkselected.add(chunk)
    fw0 = open('week05/unigram-'+str(oid)+'.txt','w')
    for chunk,count in sorted(chunk2count.items(),key=lambda x:-x[1]):
        if chunk in chunkselected:
            fw0.write(chunk+'\t'+str(count)+'\n')
    fw0.close()
    for i in range(n):
        chunksets[i] = chunksets[i] & chunkselected
    chunk2vid = {}
    for i in range(n):
        for chunk in chunksets[i]:
            if not chunk in chunk2vid:
                chunk2vid[chunk] = i
    m = len(chunk2vid)
    fw.write('offering'+'\t'+str(oid)+'\t'+'noun chunks'+'\t'+str(m)+'\n')
    s = ''
    for i in range(n):
        s += '\t'+'video '+str(i)
    fw.write(s+'\n')
    for i in range(n):
        vid2count = {}
        for chunk in chunksets[i]:
            vid = chunk2vid[chunk]
            if not vid in vid2count:
                vid2count[vid] = 0
            vid2count[vid] += 1
        s = 'video '+str(i)
        for vid in range(i+1):
            count = 0
            if vid in vid2count:
                count = vid2count[vid]
            s += '\t'+str(count)
        fw.write(s+'\n')
    fw.write('\n')
fw.close()

