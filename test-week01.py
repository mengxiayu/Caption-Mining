'''
tid2tm2begin2text = {}
tid2begin2text = {}
fr = open('allcaptions-2021-09-24.csv','rb')
fr.readline()
for line in fr:
    arr = line.strip('\r\n').split('\t')
    if not len(arr) == 6: continue
    tid,tm,begin,text = arr[0],arr[1],arr[3],arr[5]
    if not tid in tid2tm2begin2text:
        tid2tm2begin2text[tid] = {}
    if not tm in tid2tm2begin2text[tid]:
        tid2tm2begin2text[tid][tm] = {}
    if not begin in tid2tm2begin2text[tid][tm]:
        tid2tm2begin2text[tid][tm][begin] = []
    tid2tm2begin2text[tid][tm][begin].append(text)
    if not tid in tid2begin2text:
        tid2begin2text[tid] = {}
    tid2begin2text[tid][begin] = text
fr.close()
fw = open('corpus_original.txt','w')
for tid,tm2begin2text in sorted(tid2tm2begin2text.items(),key=lambda x:x[0]):
    s = ' '
    for tm,begin2text in sorted(tm2begin2text.items(),key=lambda x:x[0]):
        for begin,texts in sorted(begin2text.items(),key=lambda x:x[0]):
            for text in texts:
                s += ' '+text
    s += ' '
    s = s.replace('\t',' ').replace('\r',' ')
    while '  ' in s:
        s = s.replace('  ',' ')
    fw.write(tid+'\t'+s[1:-1]+'\n')
fw.close()
fw = open('corpus_corrected.txt','w')
for tid,begin2text in sorted(tid2begin2text.items(),key=lambda x:x[0]):
    s = ' '    
    for begin,text in sorted(begin2text.items(),key=lambda x:x[0]):
        s += ' '+text
    s += ' '
    s = s.replace('\t',' ').replace('\r',' ')
    while '  ' in s:
        s = s.replace('  ',' ')
    fw.write(tid+'\t'+s[1:-1]+'\n')
fw.close()
'''

'''
import spacy
from spacy.pipeline import Sentencizer
nlp = spacy.load('en_core_web_sm')
sentencizer = nlp.add_pipe("sentencizer")
sentencizer = Sentencizer()
fw = open('nounchunks.txt','w')
fr = open('corpus_corrected.txt','r')
for line in fr:
    arr = line.strip('\r\n').split('\t')
    tid = arr[0]
    text = arr[1]
    doc = nlp(text)
    n = len(list(doc.sents))
    fw.write(tid+'\t'+str(n)+'\n')
    sid = 0
    for text in doc.sents:
        _text_ = str(text)
        sid += 1
        fw.write('#s'+str(sid)+'\t'+_text_+'\n')        
        sent = nlp(_text_)
        s = ''
        for chunk in sent.noun_chunks:
            s += ';'+chunk.text
        if not s == '':
            fw.write('#c'+str(sid)+'\t'+s[1:]+'\n')
fr.close()
fw.close()
'''

'''
word2count = {}
fr = open('corpus_corrected.txt','r')
for line in fr:
    arr = line.strip('\r\n').split('\t')
    text = ' '+arr[1]+' '
    text = text.replace('.',' . ').replace(',',' , ').replace(';',' ; ').replace("'"," '")
    text = text.replace('?',' ? ').replace('!',' ! ').replace('(',' ( ').replace(')',' ) ')
    while '  ' in text:
        text = text.replace('  ',' ')
    text = text[1:-1].lower()
    for word in text.split(' '):
        if not word in word2count:
            word2count[word] = 0
        word2count[word] += 1
fr.close()
fw = open('vocabulary.txt','w')
for word,count in sorted(word2count.items(),key=lambda x:-x[1]):
    fw.write(word+'\t'+str(count)+'\n')
fw.close()
'''

'''
import spacy
nlp = spacy.load('en_core_web_sm')
stopwords = nlp.Defaults.stop_words
words,counts = [],[]
wordsStop,countsStop = [],[]
fw = open('vocabulary-nonstop.txt','w')
fr = open('vocabulary.txt','r')
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
print(n,nStop,100.*nStop/n)
print(m,mStop,100.*mStop/m)
'''

'''
nums = []
fr = open('nounchunks.txt','r')
for line in fr:
    if not line.startswith('#'):
        arr = line.strip('\r\n').split('\t')
        nums.append(int(arr[1]))
fr.close()
fw = open('numsentences.txt','w')
for num in sorted(nums,key=lambda x:-x):
    fw.write(str(num)+'\n')
fw.close()
'''

'''
import spacy
nlp = spacy.load('en_core_web_sm')
stopwords = nlp.Defaults.stop_words
chunk2count = {}
fr = open('nounchunks.txt','r')
for line in fr:
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
                if not _chunk_ in chunk2count:
                    chunk2count[_chunk_] = 0
                chunk2count[_chunk_] += 1
fr.close()
fw1 = open('word2count.txt','w')
fw2 = open('phrase2count.txt','w')
for chunk,count in sorted(chunk2count.items(),key=lambda x:-x[1]):
    if ' ' in chunk:
        fw2.write(chunk+'\t'+str(count)+'\n')
    else:
        fw1.write(chunk+'\t'+str(count)+'\n')        
fw2.close()
fw1.close()
'''

