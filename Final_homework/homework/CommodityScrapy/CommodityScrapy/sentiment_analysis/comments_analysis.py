from snownlp import SnowNLP
import datetime


def sentiment_analysis(text):
    score = SnowNLP(text)
    return score.sentiments


if __name__ == '__main__':
    # test_text = "太难喝，根本没气，别上当了"
    # result = sentiment_analysis(test_text)
    # print(len(str(result)), type(result), result)
    p = [2, 50, 22, 55, 3, 8, 6, 9, 7, 8, 3, 16, 1, 0, 0, 70, 31, 14, 62, 14, 19, 24, 1, 80, 18, 5, 9, 19, 50, 2]
    print(sorted(p)[-10])
