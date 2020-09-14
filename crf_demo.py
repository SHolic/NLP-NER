from xner.models.crf import train, Predictor

import xner

xner.set_option("label_type", "bmeso")  # 默认就是"bmeso"
# xner.set_option("labels", ["KEYWORDS", "BUSINESS", "ADDR", "BRANCH", "O"])

# # biso标签，CRF字级别
# xner.set_option("label_type", "biso")
# train(train_data_path="./data/addr_train_data.txt",
#       model_path="./data/addr_char_crf_biso_model.pkl",
#       model_params=None,
#       mode="char")

# biso标签，CRF词级别
# xner.set_option("label_type", "biso")
# train(train_data_path="./data/addr_train_data.txt",
#       model_path="./data/addr_word_crf_biso_model.pkl",
#       model_params=None,
#       mode="word")

# bmeso标签，CRF字级别
xner.set_option("label_type", "bmeso")
train(train_data_path="./data/addr_train_data.txt",
      model_path="./data/addr_char_crf_bmeso_model.pkl",
      model_params={
          "all_possible_transitions": True,
          "max_iterations": 50
      },
      mode="char")

"""
         PRV    CTY   CNTY    TWN   CMNT     RD     NO    POI  Total
train  1.000  1.000  0.999  1.000  0.999  1.000  1.000  0.999  1.000
test   0.995  0.985  0.976  0.956  0.906  0.923  0.941  0.826  0.947
"""

# bmeso标签，CRF词级别
# xner.set_option("label_type", "bmeso")
# train(train_data_path="./data/addr_train_data.txt",
#       model_path="./data/addr_word_crf_bmeso_model.pkl",
#       model_params=None,
#       mode="word")

"""
         PRV   CTY   CNTY    TWN   CMNT     RD     NO    POI  Total
train  1.000  1.00  0.999  0.999  0.999  0.998  0.999  0.999  0.999
test   0.996  0.99  0.973  0.959  0.920  0.904  0.930  0.778  0.937
"""

# pred = predict(test_data=["上海航发机电"],
#                model_path="./data/comp_char_crf_bmeso_model.pkl",
#                return_type="merge",
#                mode="char")
# print(pred)
#
# pred = predict(test_data="中国平安保险",
#                model_path="./data/comp_char_crf_bmeso_model.pkl",
#                return_type="merge",
#                mode="char")
# print(pred)
#
predictor = Predictor(model_path="./data/addr_char_crf_bmeso_model.pkl", )
pred = predictor.predict(data=["中学门口", "南通中学门口", "重庆市大渡口区凤祥路123号", "宁波市江东区解放军113医院血液透析室",
                               "浙江省绍兴市柯桥区湖塘街道岭下村岭岗25号", "被征地__民最低生活基本保障资金", "顺河乡吕庄村", "南洋村", "城北村3组"],
                         return_type="dict",
                         mode="char")
print(pred)

# pred = predict(test_data_path="./data/test_data.txt",
#                model_path="./data/char_crf_model.pkl",
#                return_type="dict",
#                mode="char")
# print(pred)
