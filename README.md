# X-NER

**本项目用于<u>实体</u>识别场景，目前包括：**

- 地址信息抽取
- 公司名称抽取

**当前可供选择的模型：**
- crf（字级别/词级别）
- bilstm_crf

(下个版本会加入bert等算法)

# 更新
使用Predictor， 弃用predict(速度慢)， 比如：
```python
from xner.models.crf import Predictor
predictor = Predictor(model_path)
ret = predictor.predict(data=[...])
```

# 1. 使用方法
## 1.1. 项目配置

下载网盘数据，打标训练集`data`数据放根目录，地址`sources`数据放xner下

 1. **把`xner`文件夹移动到工作目录下**
 2. `import` 这个模块
## 1.2. 参数配置

模块`xner` 的基本参数目前有三个:
1. `labels` : 当前数据的标签名称，list形态
2. `label_type` : 当前数据的标签类型，string形态，目前只有"bmeso"和"biso"两种
3. `crf_features` : crf模型所需要的特征名称，list形态，目前已开发的特征包括**BasicFeature**、**NgramFeature**和**DistrictFeature**

```python
import xner

# 默认是地址标签名称，在做公司名称抽取时，则需要修改相应的标签名
xner.set_option("labels", ["PRV", "CTY", ...])

# 默认是"bmeso"
xner.set_option("label_type", "bmeso")

# 默认是三个特征，在做公司名称抽取时，DistrictFeature则不需要
xner.set_option("crf_features", ["BasicFeature", "NgramFeature", "DistrictFeature"])
```

也可以在`ner/__init__.py`里直接修改
```python
# xner/__init__.py
SETTINGS = {
    'labels': ["PRV", "CTY", "CNTY", "TWN", "CMNT", "RD", "NO", "POI", "O"],
    'label_type': "bmeso",  # another is 'biso'
    'crf_features': ["BasicFeature", "NgramFeature", "DistrictFeature"]
}
```


## 1.3. 训练数据格式
一个短语后接一个标签，用tab("\t")隔开。

train_data.txt
```text
安徽省 prv 六安  cty 裕安区 cnty    香樟公寓    poi 二期15#-18#楼101铺  o
安徽  prv 亳州  cty 谯城区 cnty    元化路 rd  小吃一条街   poi 中段御花园东门对面   o
```

## 1.4. 训练与预测
`xner`的各种模型都提供`train`和`predict`接口。

### 1.4.1. CRF模型
```python
from xner.models.crf import train, Predictor

import xner
xner.set_option("label_type", "bmeso")  # 默认就是"bmeso"，如果想使用"bmeso"可不写，另一种为'biso'

train(train_data_path=addr_train_data.txt, # 训练数据的路径
      model_path="./data/model.pkl",           # 模型保存地址，None则不保存
      model_params=None,                       # CRF常用参数，dict格式
      mode="char")                             # 'char'为字级别，'word'为词级别

predictor = Predictor(model_path="./data/char_crf_model.pkl")
pred = predictor.predict(data="四川省成都市龙泉驿区双龙路与转龙路交叉口西北150米", # test_data 可以是string或者list
               return_type="merge",                                  # 返回格式，默认None，仅返回预测标签，"merge"返回合并标签和实体文字，"dict"返回以标签为key的dict，同一个标签有多个实体则以逗号分隔
               mode="char")                                          # 'char'为字级别，'word'为词级别

# return_type=None 
# [['B-PRV', 'M-PRV', 'E-PRV', 'B-CTY', 'M-CTY', 'E-CTY', 'B-CNTY', 'M-CNTY', 'M-CNTY', 'E-CNTY', 'B-RD', 'M-RD', 'E-RD', 'O', 'B-RD', 'M-RD', 'E-RD', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]
# return_type="merged"
# ([['四川省', '成都市', '龙泉驿区', '双龙路', '与', '转龙路', '交叉口西北150米']], [['PRV', 'CTY', 'CNTY', 'RD', 'O', 'RD', 'O']])
# return_type="dict"
# [{'PRV': '四川省', 'CTY': '成都市', 'CNTY': '龙泉驿区', 'RD': '双龙路,转龙路', 'O': '与,交叉口西北150米'}]

```
### 1.4.2. BiLSTM_CRF模型
`train`和`Predictor`接口与crf模型一致，但没有`mode`参数。
```python
from xner.models.bilstm_crf import train, Predictor

train(train_data_path=addr_train_data.txt,
      model_path=bilstm_crf_model.pkl,
      model_params={
          "epoch": 50,
          "embedding_dim": 30,
          "hidden_dim": 20,
          "lr": 0.01,
          "train_test_split_rate": 0.1,
      })


predictor = Predictor(model_path="bilstm_crf_model.pkl")
pred = predictor.predict(data="四川省成都市龙泉驿区双龙路",
                         return_type="merge")
```

## 1.5. 其他API

### 1.5.1. 直接使用模型
可以直接使用封装的模型来自由训练。
```python
from xner.models.crf import CRF
from xner.models.bilstm_crf import BilstmCrf

crf = CRF(**params)
crf.train(x, y) # x为dict的list，每个dict里是crf模型的feature，y是标签list
crf.predict(x)
crf.save(path)
crf.load(path)

bcrf = BilstmCrf(**params)
bcrf.train(x, y) # x为一行文字的字级别的list，y为标签list
bcrf.predict(x)
bcrf.save(path)
bcrf.load(path)
```

### 1.5.2. 四级地址自动补全
（配置中）

# 2. 场景案例
## 2.1. 地址标准化场景
### 2.1.1. 使用标签
|标签|解释|
|:------|:---|
|PRV|省级行政区，包括省、自治区、直辖市、特别行政区四类|
|CTY|地级行政区，常规的第二级行政区划单位，包括地级市、盟(如内蒙古兴安盟)、自治州(如延边朝鲜族自治州)和地区(如大兴安岭地区)|
|CNTY|县级行政区，包括县、自治县、县级市、旗、自治旗(如内蒙古鄂伦春自治旗)、市辖区(如上海黄浦区)，另有林区(湖北神农架林区)和特区(六盘水市六枝特区)各一个特例|
|TWN|乡级行政区，包括镇、街道办事处、乡、民族乡(如北京怀柔区喇叭沟门满族乡)、苏木(如包头市吉忽伦图苏木)、民族苏木(呼伦贝尔市陈旗鄂温克民族苏木)|
|CMNT|除上述四级行政区划之外的区域，包括社区、村庄、村民组等|
|RD|道路，包括桥、高速路、高架路|
|NO|门牌号码|
|POI|各类重要地点，用做标准化的主要查询词，包括小区、商场、写字楼等|
|O|其他|

### 2.1.2. 训练效果
目前使用2000个训练样本，crf的`train_test_split_rate`为0.2，bilstm_crf为0.1。
训练集在`data/addr_train_data.txt`中。

|模型(bmeso标签)|训练集acc|测试集acc|
|:----|:----|:----|
|CRF（字级别）|0.998|0.896|
|CRF（词级别）|0.999|0.812|
|BILSTM-CRF|0.999|0.870|

|模型(biso标签)|训练集acc|测试集acc|
|:----|:----|:----|
|CRF（字级别）|0.999|0.870|
|CRF（词级别）|0.998|0.808|
|BILSTM-CRF|0.999|0.843|

详细结果
```text
# biso标签，CRF词级别
         PRV    CTY   CNTY    TWN   CMNT     RD     NO    POI  Total
train  0.968  0.960  0.981  0.837  0.733  0.899  0.932  0.917  0.926
test   0.933  0.936  0.845  0.644  0.609  0.778  0.810  0.607  0.808

# biso标签，CRF字级别
         PRV    CTY   CNTY    TWN   CMNT     RD     NO    POI  Total
train  0.998  0.999  0.997  0.998  1.000  1.000  1.000  0.995  0.998
test   0.983  0.978  0.825  0.817  0.789  0.901  0.867  0.602  0.870

# bmeso标签，CRF词级别
         PRV    CTY   CNTY    TWN   CMNT     RD     NO    POI  Total
train  0.968  0.960  0.981  0.837  0.737  0.897  0.934  0.918  0.926
test   0.933  0.929  0.883  0.681  0.580  0.782  0.829  0.605  0.812

# bmeso标签，CRF字级别
         PRV    CTY   CNTY    TWN   CMNT     RD     NO    POI  Total
train  0.999  0.999  0.997  1.000  1.000  0.999  1.000  0.996  0.999
test   0.980  0.981  0.835  0.857  0.899  0.905  0.867  0.711  0.896

# bmeso标签，bilstm
        PRV   CTY   CNTY   TWN   CMNT     RD     NO    POI  Total
train  1.00  1.00  1.000  1.00  1.000  0.999  0.998  0.997  0.999
test   0.99  0.96  0.926  0.82  0.811  0.899  0.860  0.612  0.870 

# biso标签，bilstm
         PRV    CTY   CNTY    TWN   CMNT     RD     NO    POI  Total
train  0.999  0.999  1.000  1.000  0.997  0.998  0.998  0.997  0.999
test   0.990  0.953  0.778  0.852  0.676  0.882  0.837  0.565  0.843
```


## 2.2. 公司名称标准化场景
### 2.2.1. 使用标签
|标签|解释|
|:------|:---|
|ADDR|地址|
|KEYWORDS|公司关键词|
|BUSINESS|公司经营范围|
|BRANCH|分公司信息|
|O|其他|

### 2.2.2. 训练效果
目前使用11331个训练样本，crf的`train_test_split_rate`为0.2，bilstm_crf为0.1。
训练集在`data/comp_train_data.txt`中。

|模型(bmeso标签)|训练集acc|测试集acc|
|:----|:----|:----|
|CRF（字级别）|0.997|0.866|
|CRF（词级别）|1.000|0.842|
|BILSTM-CRF|-|-|

|模型(biso标签)|训练集acc|测试集acc|
|:----|:----|:----|
|CRF（字级别）|0.994|0.870|
|CRF（词级别）|0.999|0.840|
|BILSTM-CRF|-|-|

详细结果
```text
# biso标签，CRF词级别
       KEYWORDS  BUSINESS   ADDR  BRANCH  Total
train     0.953     0.947  0.977   0.974  0.958
test      0.810     0.826  0.916   0.712  0.840

# biso标签，CRF字级别
       KEYWORDS  BUSINESS   ADDR  BRANCH  Total
train     0.999     0.985  0.999   0.998  0.994
test      0.846     0.859  0.935   0.721  0.870

# bmeso标签，CRF词级别
       KEYWORDS  BUSINESS   ADDR  BRANCH  Total
train     0.953     0.948  0.978   0.975  0.959
test      0.812     0.828  0.918   0.694  0.842

# bmeso标签，CRF字级别
       KEYWORDS  BUSINESS   ADDR  BRANCH  Total
train     0.999     0.994  0.999   0.999  0.997
test      0.844     0.850  0.936   0.725  0.866
```

