import textblob as tb
import snownlp as sp
import jieba
from collections.abc import Iterable


class EnglishBlob:
    def __init__(self, sentence_list):
        if not isinstance(sentence_list, Iterable):
            raise TypeError(f"Parameter 'sentence_list' must be iterable, not '{type(sentence_list)}'")
        self.blobs = [tb.TextBlob(blob) for blob in sentence_list]

    def __str__(self):
        return self.blobs

    def Analyse(self, index):
        result = self.blobs[index].sentiment
        if result.subjectivity >= 0.5:
            remark = "Subjective"
        else:
            remark = "Objective"
        if result.polarity > 0.1:
            return self.blobs[index], ("Positive", result.polarity), (remark, result.subjectivity)
        elif 0.1 >= result.polarity >= -0.1:
            return self.blobs[index], ("Middle", result.polarity), (remark, result.subjectivity)
        else:
            return self.blobs[index], ("Negative", result.polarity), (remark, result.subjectivity)

    def cut(self, index, mode):
        """

        :param index: The index of blob that you want to cut
        :param mode: the mode that you want to cut, default 'word', you can choose 'sentence' or 'word' as well.
        :return: the result of cut list
        """
        value = self.blobs[index]
        if mode.lower() == 'sentence':
            return value.sentences
        elif mode.lower() == 'word':
            return value.words
        else:
            return "Invalid mode '" + mode + "'"

    def GetTags(self, index):
        return self.blobs[index].tags


class ChineseBlob:
    def __init__(self, sentence_list):
        if not isinstance(sentence_list, Iterable):
            raise TypeError(f"Parameter 'sentence_list' must be iterable, not '{type(sentence_list)}'")
        self.blobs = [sp.SnowNLP(blob) for blob in sentence_list]

    def __str__(self):
        return self.blobs

    def Analyse(self, index):
        result = self.blobs[index].sentiments
        if result > 0.1:
            return "正面", result
        elif 0.1 >= result >= -0.1:
            return "中性", result
        else:
            return "负面", result

    def cut(self, index, mode='word'):
        if mode == 'word':
            return self.blobs[index].words
        elif mode == 'sentence':
            return self.blobs[index].sentences
    def GetTags(self, index):
        return list(self.blobs[index].tags)
