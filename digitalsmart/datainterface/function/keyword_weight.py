class KeyWordWeight:
    """
    文本关键词以及权重对象
    """
    __slots__ = ['word', 'weight']

    def __init__(self, word, weight):
        self.word = word
        self.weight = weight

    def __str__(self):
        return "关键词：{word}   权重：{weight}".format(word=self.word, weight=self.weight)
