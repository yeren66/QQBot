import jieba
import mysqlt
import time

# test = "这一期的120的那个大月卡好像挺香的"
# test1 = "我来到北京清华大学"
# list = jieba.cut(test, cut_all=False)
# list1 = pseg.cut(test)

# for word, flag in list1:
#     print('%s %s' % (word, flag))

# print("result: " + " ".join(list))

start = time.time()
jieba.load_userdict("directory.txt")
sql = mysqlt.SQL()
object_ = "黑暗降临_220418"
sql.adjust(object_)

context = sql.process(object_)
# print(context.loc[1, "content"])
length = len(context)

for i in range(length):
    sentence = context.loc[i, "content"]
    words = jieba.cut(sentence, cut_all=False)
    list = []
    for word in words:
        ret = sql.rank_message(word, object_)
        list.append(word)
    if ret:
        print("done: " + str(i) + " / " + str(length) + " | sentence: " + str(sentence) + "\n\t\t\t-->   " + " ".join(list))

print("all works done.")

sql.adjust_punctuation("words_" + object_)

print("adjust punctuation has been done.")

end = time.time()

print("spend time: " + str(end - start))