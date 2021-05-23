import jieba
from imageio import imread
from wordcloud import WordCloud

with open('qq_word.txt', encoding='utf-8')as f:
    comment_txt=f.read()
    wordlist=jieba.cut(comment_txt,cut_all=True)
    wl=" ".join(wordlist)

# 个性化词云图
# mk=imread("wujioaxing.png")
# wc=WordCloud(font_path='simhei.ttf',background_color='white',mask=mk).generate(wl)

# 默认输出一个长宽2000的词云图
wc=WordCloud(font_path='simhei.ttf',background_color='white',height=2000,width=2000).generate(wl)
wc.to_file('111.jpg')
