from xner.models.bilstm_crf import train, Predictor

import xner

xner.set_option("label_type", "biso")  # 默认就是"bmeso"

train(train_data_path="./data/addr_train_data.txt",
      model_path="./data/addr_bilstm_crf_biso_model.pkl",
      model_params={
          "epoch": 1,
          "embedding_dim": 100,
          "hidden_dim": 120,
          "lr": 0.01,
      })

predictor = Predictor(model_path="./data/addr_bilstm_crf_biso_model.pkl")
pred = predictor.predict(data="江苏南通江苏省南通中学",
                         return_type="merge")
print(pred)

# pred = predict(test_data_path="./data/test_data.txt",
#                model_path="./data/bilstm_crf_model140.pkl",
#                return_type="merged")
# print(pred)
