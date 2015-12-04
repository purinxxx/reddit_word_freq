# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import praw
import MeCab
from collections import Counter

def hinsi(sentence):
	global data
	sentence = url.sub('', sentence)	#マークダウンでurlが記述されている部分を削除するよ
	sentence = quote.sub('', sentence)	#マークダウンで引用がされている部分を削除するよ
	sentence = sentence.strip().encode('utf-8')
	tagger = MeCab.Tagger('-Ochasen -d /usr/local/Cellar/mecab/0.996/lib/mecab/dic/mecab-ipadic-neologd')	#固有名詞がたくさん入った辞書使うよ
	node = tagger.parseToNode(sentence)
	while node:
		#if node.surface != '' and node.feature.split(",")[0] != '助詞' and node.feature.split(",")[0] != '助動詞' and node.feature.split(",")[0] != '記号' and node.feature.split(",")[0] != 'BOS/EOS':
		if node.feature.split(",")[0] == '名詞':	#名詞だけ抽出の方が面白い気がする
			data.append(node.surface)
		node = node.next

def analyze():
	global raw, target
	r = praw.Reddit(user_agent='word_freq_jp by /u/purinxxx')

	subreddit = r.get_subreddit(target)
	comments = subreddit.get_comments(limit=1000)

	for i, comment in enumerate(comments, start=1):
		if i%100 == 0:
			print i
		if str(comment.author) != 'TweetsInCommentsBot' or str(comment.author) != 'AutoModerator':
			raw.append(comment.body.replace('\n',' '))
			if isinstance(comment, praw.objects.Comment):	#レス
				hinsi(comment.body.replace('\n',' '))
			else:	#スレ
				hinsi(comment.title)
				if comment.is_self:	#テキスト投稿のコメントだよ
					hinsi(comment.selftext.replace('\n',' '))

#def main():
target = 'newsokurMod'
start = time.time()
data, result, raw = [], [], []
url = re.compile('\[.*\]\(.*\)')
quote = re.compile('^> .*$')
analyze()
counter = Counter(data)
#print counter.most_common()
for word, cnt in counter.most_common():
	result.append(str(word) + '\t' + str(cnt))
f = open(target + '_result.txt','w')
for x in result:
	f.write(str(x) + '\n')
f = open(target + '_raw.txt','w')
for x in raw:
	f.write(str(x) + '\n')
elapsed_time = time.time() - start
print format(elapsed_time) + ' sec'
print os.path.abspath(os.path.dirname(__file__)) + '/' + target + '_result.txt'
print os.path.abspath(os.path.dirname(__file__)) + '/' + target + '_raw.txt'

