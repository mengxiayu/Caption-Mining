def output(k2gram2c, filename):
    m = 20
    fw = open(filename,'w')
    k_gram2c = sorted(k2gram2c.items(),key=lambda x:x[0])
    for k,gram2c in k_gram2c:
        num = len(gram2c)
        fw.write(str(k)+'-gram'+'\t'+str(num)+'\n')
    for k,gram2c in k_gram2c:
        gram_c = sorted(gram2c.items(),key=lambda x:-x[1])
        for i in range(min(len(gram_c),m)):
            gram,c = gram_c[i]
            fw.write(str(k)+'\t'+str(i+1)+'\t'+str(c)+'\t'+gram+'\n')
    fw.close()

n = 12
k2ngram2count = {}
dept2k2ngram2count = {}
fr = open('week03/corpus_corrected_dept.txt','r')
for line in fr:
    arr = line.strip('\r\n').split('\t')
    dept = arr[0]
    doc = arr[2].lower().replace('? ','. ')
    for sent in doc.split('. '):
        words = []
        for word in sent.split(' '):
            words.append(word)
        if len(words) == 0: continue
        for i in range(min(len(words),n)):
            k = i+1
            ngram = ''
            for j in range(k):
                ngram += ' '+str(words[j])
            ngram = ngram[1:]
            if not k in k2ngram2count:
                k2ngram2count[k] = {}
            if not ngram in k2ngram2count[k]:
                k2ngram2count[k][ngram] = 0
            k2ngram2count[k][ngram] += 1
            if not dept in dept2k2ngram2count:
                dept2k2ngram2count[dept] = {}
            if not k in dept2k2ngram2count[dept]:
                dept2k2ngram2count[dept][k] = {}
            if not ngram in dept2k2ngram2count[dept][k]:
                dept2k2ngram2count[dept][k][ngram] = 0
            dept2k2ngram2count[dept][k][ngram] += 1
fr.close()

output(k2ngram2count,'week05/ngram2count-all.txt')
for dept,k2gram2c in dept2k2ngram2count.items():
    output(k2gram2c,'week05/ngram2count-'+dept+'.txt')

