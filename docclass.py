import re
#regular expression
import yahoosplitter as splitter

import math
import sys

def getwords(doc):
    words =[s for s in splitter.split(doc) if len(s)>1 and len(s) < 20]
    return dict([(w,1) for w in words])
    #ユニークな単語のみ返す

class classifier:
    def __init__(self, getfeatures, filename=None):
        self.feature_category_count = {}
        self.category_count = {}
        self.getfeatures=getfeatures

    def increment_feature_category(self, feature, category):
        self.feature_category_count.setdefault(feature,{})
        self.feature_category_count[feature].setdefault(category,0)
        self.feature_category_count[feature][category]+=1

    def increment_category_counter(self,category):
        self.category_count.setdefault(category,0)
        self.category_count[category] += 1

    def feature_counter(self, feature, category):
        if feature in self.feature_category_count and category in self.feature_category_count[feature]:
            return float(self.feature_category_count[feature][category])
        return 0.0

    def category_counter(self, category):
        if category in self.category_count:
            return float(self.category_count[category])
        return 0.0

    def total_counter(self):
        return sum(self.category_count.values())

    def categories(self):
        return self.category_count.keys()

    def train(self, item, category):
        features = self.getfeatures(item)
        for feature in features:
            self.increment_feature_category(feature, category)
        self.increment_category_counter(category)

    def feature_probability(self, feature, category):
        if self.category_counter(category)==0 : return 0
        return self.feature_counter(feature, category) / self.category_counter(category)

    def weighted_probability(self, feature, category, prf, weight=1.0, average_point=0.5):
        basic_probability = prf(feature, category)
        totals = sum([self.feature_counter(feature, c) for c in self.categories() ])

        weighted_probability = ( (weight * average_point) + (totals*basic_probability) ) / (weight + totals)
        return weighted_probability

    def sample_data_injector(cl):
        cl.train("これはペンです", "good")
        cl.train("高収入！　安心安全なパパ活環境！　初心者でもらくらく稼げる！儲かる！　詳しくはこちら", "bad")
        cl.train("python3は昔昔、何者かのコンピューターに強い人によって開発されました。今では機械学習やデータサイエンスにも役立っています", "good")
        #以下twitterでパパ活と検索した結果
        cl.train("初めてでわからないことだらけですがお声かけお待ちしてます", "bad")
        cl.train("""圧倒的人気NO.1エロかわいい萌え萌えお姫様みらいちゃん！※パパ活コース可
18:00～ご案内できます♪                
色白でスタイル抜群のアニメ声！
このエロい身体に会いに来てください☆
ご予約はお急ぎください！
(link: http://comet.magnum-f.info/top/) 
comet.magnum-f.info/top/
080-4866-9495
#池袋 #パパ活 #派遣 #リフレ""", "bad")
        cl.train("""アラサーですが特に年齢でのやりにくさはあまり感じたことありません。
たぶん、私が会っているPさんは若い子は求めていないのでしょうね。
#ペイターズ 
#パパ活""", "good")

class naivebayes(classifier):
  def doc_probability(self, item, category):
    p=1
    for feature in features: p *= self.weighted_probability(feature, category, self.feature_probability)
    return p
