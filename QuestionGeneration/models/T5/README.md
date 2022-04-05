## T5 pytorch implementation 

## Introduction 
T5 is proposed by Google in Oct. 2019. Full paper is [BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension](https://arxiv.org/abs/1910.10683) in JMLR 2020. Authors: Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, Peter J. Liu

> Transfer learning, where a model is first pre-trained on a data-rich task before being fine-tuned on a downstream task, has emerged as a powerful technique in natural language processing (NLP). The effectiveness of transfer learning has given rise to a diversity of approaches, methodology, and practice. In this paper, we explore the landscape of transfer learning techniques for NLP by introducing a unified framework that converts all text-based language problems into a text-to-text format. Our systematic study compares pre-training objectives, architectures, unlabeled data sets, transfer approaches, and other factors on dozens of language understanding tasks.

## Environment

1. python >= 3.6.0
```
conda create -n bart python=3.6
conda activate bart
```
2. install necessary packages
```
pip install transformers==3.3.1
pip install torch==1.7.0
pip install -r requirements.txt
```

## Run the code 
```
./finetune.sh
```

*Note* that default script is on Wenhao's CRC account, you need to specify your own netID and envs. 
```
#!/bin/bash
#$ -M YOUR_NETID@nd.edu
#$ -m abe
#$ -q gpu@@mjiang2
#$ -pe smp 1
#$ -l gpu=0

CUDA_VISIBLE_DEVICES=DEVICE_NUM(0-3) /afs/crc.nd.edu/user/w/YOUR_NETID/anaconda3/envs/YOUR_ENV/bin/python -u finetune.py 
```

Please specify your `YOUR_NETID`, `DEVICE_NUM(0-3)` (our 2080ti has 4 cards, so number is from 0 to 3), `YOUR_ENV`.

