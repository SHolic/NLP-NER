# Table of contents
- [Table of contents](https://git.creditx.com/baojs/NLP-NER/blob/master/#Table-of-contents)
- [X-NER](https://git.creditx.com/baojs/NLP-NER/blob/master/#X-NER)
- [1. 使用方法](https://git.creditx.com/baojs/NLP-NER/blob/master/#1-使用方法)
    - [1.1. 项目配置](https://git.creditx.com/baojs/NLP-NER/blob/master/#11-项目配置)
    - [1.2. 参数配置](https://git.creditx.com/baojs/NLP-NER/blob/master/#12-参数配置)
    - [1.3. 训练数据格式](https://git.creditx.com/baojs/NLP-NER/blob/master/#13-训练数据格式)
    - [1.4. 训练与预测](https://git.creditx.com/baojs/NLP-NER/blob/master/#14-训练与预测)
        - [1.4.1. CRF模型](https://git.creditx.com/baojs/NLP-NER/blob/master/#141-CRF模型)
        - [1.4.2. BiLSTM_CRF模型](https://git.creditx.com/baojs/NLP-NER/blob/master/#142-BiLSTM_CRF模型)
    - [1.5. 其他API](https://git.creditx.com/baojs/NLP-NER/blob/master/#15-其他API)
        - [1.5.1. 直接使用模型](https://git.creditx.com/baojs/NLP-NER/blob/master/#151-直接使用模型)
        - [1.5.2. 四级地址自动补全](https://git.creditx.com/baojs/NLP-NER/blob/master/#152-四级地址自动补全)
- [2. 场景案例](https://git.creditx.com/baojs/NLP-NER/blob/master/#2-场景案例)
    - [2.1. 地址标准化场景](https://git.creditx.com/baojs/NLP-NER/blob/master/#21-地址标准化场景)
        - [2.1.1. 使用标签](https://git.creditx.com/baojs/NLP-NER/blob/master/#211-使用标签)
        - [2.1.2. 训练效果](https://git.creditx.com/baojs/NLP-NER/blob/master/#212-训练效果)
    - [2.2. 公司名称标准化场景](https://git.creditx.com/baojs/NLP-NER/blob/master/#22-公司名称标准化场景)
        - [2.2.1. 使用标签](https://git.creditx.com/baojs/NLP-NER/blob/master/#221-使用标签)
        - [2.2.2. 训练效果](https://git.creditx.com/baojs/NLP-NER/blob/master/#222-训练效果)
- [3. 训练集打标注意点](https://git.creditx.com/baojs/NLP-NER/blob/master/#3-训练集打标注意点)
    - [3.1. 地址标签](https://git.creditx.com/baojs/NLP-NER/blob/master/#31-地址标签)

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



# 3. 训练集打标注意点

## 3.1. 地址标签
- 北京的"[东西南北]里"，一定要加前缀，前缀可能是路，可能是社区，可能是poi，可能是twn，可能有本身的名字
    - 东城区 cnty 工体北路 rd 幸福一村西里 poi 甲5号 no 渝信川菜 poi 3层 o
    - 北京 prv 望花路西里社区 cmnt 22号楼 o
    - 北京 prv 二七剧场路东里 poi 新16-1-501 o
    - 北京市 prv 石佛营东里 poi 131号院2号楼1003 o
    - 北京市 prv 车公庄大街北里 poi 乙37号 o
    - 北京市 prv 忠实里 poi 南街乙六号 o

- 交叉口打标方法
    - 鲁谷路 rd 与 o 银河大街 rd 交汇十字路口东北角， o 银河财智中心 poi A座B1层139号 o
    - 北京 prv 万丰路 rd 小井桥 rd 东南角 o

- 开发区打成o
    - 北京 prv 顺义天竺开发区 o 林荫路 rd 荣和广场 poi 5号楼 o
    - 北京 prv 经济技术开发区 o 科创11街 rd 18号院1号楼B-1F-01、02 o
    - 亦庄开发区 o 文化园东路 rd 与 o 荣华北路 rd 交叉东侧 o 亦庄生活广场 poi 3层 o
    - 亦庄 o 林肯公园 poi B区10号楼107底商 o

- 村后号码打成o
    - 北京市 prv 泰燕路 rd 十三陵镇 twn 燕子口村 cmnt 26号 o
    - 怀柔 cnty 雁栖镇 twn 范崎路 rd 莲花池村 cmnt 188号 o

- 商业街为poi
    - 江苏省 prv 宿迁 cty 宿城区 cnty 富康大道 rd 楚街北门 poi 向南30米Y23-Y29号 o
    - 山东省 prv 济宁市 cty 凤凰城商业街 poi 北七号楼 o
    - 鄂尔多斯市 cty 金辉商业街 poi 斜对过 o
    - 广东省 prv 广州市 cty 天河区 cnty 黄村 cmnt 怡顺商业街 poi 18号 o

- 弄与号连着打成no，没有号时单独打成no，除非弄有非数字的名字
    - 青浦区 cnty 公园路 rd 666弄 no 桥梓湾商场 poi 内 o
    - 巨鹿路 rd 889弄21号 no
    - 闵行区 cnty 金汇路 rd 463弄28号 no D栋M室 o
    - 松江区 cnty 文涵路 rd 99弄22号 no
    - 张杨路 rd 2389弄 no LCM置汇旭辉广场 poi 3楼04室 o
    - 大学路 rd 88弄90号 no 502室 o
    - 虹桥镇 twn 虹泉路 rd 1101弄 no 2楼 o 新东苑酒店 poi 正门旁 o
    - 浙江省 prv 杭州 cty 下城区 cnty 武林路 rd 桃花河弄 rd 11号 no

- 自治区的一些地区虽然不是真正的cty，但级别属于cty，打成cty，参考pcas.csv
    - 西藏自治区 prv 阿里地区 cty 噶尔县 cnty 德吉路 rd 行署会议中心 poi 东侧 o
    - 黑龙江 prv 大兴安岭地区 cty 漠河县 cnty 西林吉镇 twn 38区 o 乔路小区 poi 6号楼00单元101 o
    - 新疆维吾尔自治区 prv 阿勒泰地区 cty 阿勒泰市 cnty 北 o 屯西北路 rd 明豪 poi 一号楼一层0708号 o
    - 新疆维吾尔自治区 prv 喀什地区 cty 喀什市 cnty 克孜勤都维路 rd 环疆新世界 poi 8楼 o
    - 新疆自治区 prv 和田地区 cty 和田市 cnty 凯旋路 rd 2号 no 川亿住宅区 poi 2楼102号商铺 o
    - 贵州省 prv 毕节地区 cty 河滨路 rd 金城商住小区 poi

- 与路名相关的"段|条"打成o
    - 南充市 cty 南虹路 rd 三段 o 盛世天城 poi
    - 成都市 prv 人民南路 rd 四段 o 45号 no
    - 成都 cty 锦江区 cnty 盐市口街道 twn 人民南路rd 一段 o 122-124号 no 成都城市名人酒店 poi 2楼 o
    - 四川省 prv 成都市 cty 成华区 cnty 二环路 rd 北四段 o 9号 no 高车一路 rd 汇融名城 poi D区 o
    - 吉林省 prv 长春市 cty 二道区 cnty 长石公路 rd 三道段 o 4388号 no 惠泽园 poi 15-3-1210 o
    - 长沙 cty 芙蓉南路 rd 二段 o 中建芙蓉工社 poi 4栋601 o
    - 长沙市 cty 开福区 cnty 金霞路 rd 一段 o 418号 no 极目楚天 poi 七栋208房 o
    - 长沙市 cty 芙蓉中路 rd 三段 o 269号 no
    - 四川 prv 巴中 cty 光雾山大道 rd 朝阳段 o 147号 no
    - 四川省 prv 德阳市 cty 台北路 rd 东二段 o 1号 no

- 某些"桥|街"结尾的地名不是rd，其实是twn，着重注意桥后直接接poi，rd，cmnt的情况
    - 北京市 prv 酒仙桥 twn 三街坊 cmnt 东申公寓 poi 二号楼 o
    - 北京 prv 沙河 cnty 北大桥 twn 超吉特公寓 poi 9号楼402 o
    - 北京市 prv 朝阳区 cnty 四惠桥 twn 南伊莎文心广场 poi B座2号楼 o
    - 重庆市 prv 九龙坡区 cnty 石坪桥 twn 安迪苑 poi 1栋2单元7-4 o
    - 湖北 prv 武汉 cty 汪集街 twn 童畈村 cmnt 程榨湾二组19号 o
    - 天津市 prv 万新街 twn 先锋路 rd 61号 no 恒星世界 poi
    - 广东省 prv 广州市 cty 番禺区 cnty 市桥街 twn 东环路 rd 449 no

- 重复地名重复打
    - 四川省 prv 阿坝藏族羌族自治州 cty 阿坝州 cty 若尔盖县 cnty 达扎寺镇 twn
    - 四川省 prv 成都市 cty 四川 prv 的 o 都江堰市 cty 崇义镇 twn 借牌村 cmnt 九组44号 o

- 内蒙古中的"苏木"打twn，"嘎查"打cmnt 
    - 内蒙古自治区 prv 鄂尔多斯市 cty 鄂托克前旗 cnty 城川镇 twn 糜地梁嘎查 cmnt 四社103 o
    - 内蒙古自治区 prv 锡林郭勒盟 cty 浩勒图高勒镇 twn 查汗淖尔嘎查 cmnt 1组80号 o
    - 内蒙古自治区 prv 呼和浩特市 cty 代力吉苏木 twn 西五井子嘎查 cmnt 035号 o
    - 内蒙古自治区 prv 锡林郭勒盟 cty 东乌珠穆沁 cnty 萨麦苏木 twn 陶森宝拉格嘎查 cmnt 111号
    - 内蒙古自治区 prv 锡林郭勒盟 cty 上都镇 twn 青格勒图嘎查桃山村 cmnt
    - 内蒙古自治区 prv 鄂尔多斯市 cty 苏米图苏木 twn 苏里格嘎查 cmnt 巴音陶勒盖小队046号 o

- 带"畈"的地名大多为cmnt
    - 浙江省 prv 金华市 cty 大水畈 cmnt 2区12栋401室 o
    - 湖北省 prv 武汉市 cty 新市镇 twn 城畈村 cmnt 149户 o
    - 浙江省 prv 金华市 cty 对家畈 cmnt 兰亭街 rd 85号 no
    - 湖北省 prv 襄阳市 cty 冷集镇 twn 龙畈村 cmnt 四组 o

- 城区打o
    - 山西省 prv 晋城市 cty 城区 o 西街办事处 twn 五龙居委 cmnt B区1号楼2单元802室 o
    - 山西省 prv 晋城市 cty 城区 o 白水街 rd 方程国际 poi 8o7室 o
    - 山西省 prv 晋城市 cty 城区 o 凤台西街 rd 338号 no

- 亦庄是开发区，可能会简写，打o
    - 北京市 prv 北京 prv 大兴 cnty 亦庄 o 永昌 rd 8号 no 8301 o
    - 亦庄开发区 o 文化园东路 rd 与 o 荣华北路 rd 交叉东侧 o 亦庄生活广场 poi 3层 o
    - 亦庄 o 林肯公园 poi B区10号楼107底商 o

- 庄的定位很复杂，需具体分析
    - 河北省 prv 唐山市 cty 唐家庄 twn 红北道 rd
    - 北京市 prv 北京 prv 大兴 cnty 亦庄 o 永昌 rd 8号 no 8301 o
    - 石家庄市 cty 河北省 prv 民族路 rd 77号 no 华强广场 poi A座1031 o
    - 广东省 prv 深圳市 cty 金稻田路 rd 比华丽山庄 poi 综合楼三楼309 o
    - 山东省 prv 菏泽市 cty 曹县 cnty 孙老家镇 twn 袁白庄行政村 cmnt 17号 o
    - 河南省 prv 周口市 cty 刘振屯乡 twn 范庄 cmnt 132号 o
    - 四川省 prv 宜宾市 cty 南岸西区 cnty 碧水山庄 poi T栋5楼5B o

- "大道[东西南北]"一起打成rd（大多是广东的），"路[东西南北]"则分开打成rd和no
    - 广东省 prv 东莞市 cty 厚街镇 twn 大道东 rd 50号 no
    - 广西 prv 南宁 cty 那洪大道南 rd 宁奥园雅典 poi 7栋2单元602 o
    - 湖北省 prv 武汉市 cty 五环大道东 rd 西湖大道南 rd 1栋302号 o
    - 广东省 prv 惠州市 cty 黄埠镇 twn 海滨二路 rd 北一号 no 顺福公寓 poi
    - 广东省 prv 河源市 cty 南门路 rd 东1号 no
    - 福建省 prv 漳州市 cty 霞美镇 twn 北江村路 rd 东57号 no
    - 浙江省 prv 宁波市 cty 陆埠镇 twn 干溪村路 rd 东142号 no
    
- "[路街][0-9一二三四五六七八九十]巷"一起打成rd
    - 佛山市	cty	广东省	prv	百西科技园	o	黎家村	cmnt	黎家大街四巷	rd	22号楼整栋207	o
    - 海南省	prv	儋州市	cty	海头镇	twn	南港居委会	cmnt	南街二巷	rd
    - 广东省	prv	广州市	cty	工业大道	rd	中庄头	cmnt	东边街四巷	rd	九号	no	303	o
    
- 重庆的"[一二三四五六七八九十]公里"打成cmnt
    - 重庆市	prv	八公里	cmnt	渝南大道	rd	西站	o	国际汽车城	poi	4213	o
    - 重庆市	prv	重庆市	prv	南岸区	cnty	四公里	cmnt	绿洲龙城	poi	4栋1楼	o
    
- 一般只有一个村，后缀为自然村，湾，坡，坞，村等代表村的，如果前面有cmnt就打o，没有打cmnt
    - 圣泉乡	twn	北城集行政村	cmnt	朱连屯17号	o
    - 浙江省	PRV	湖州市	CTY	长兴县	CNTY	虹星桥镇	TWN	谭家村	CMNT	人文庄自然村20号	O
    - 浙江省	PRV	湖州市	CTY	长兴县	CNTY	泗安镇	TWN	玉泉村	CMNT	西山边自然村32号	O
    - 浙江省	PRV	湖州市	CTY	长兴县	CNTY	虹星桥镇	TWN	人文庄自然村20号	O
    - 圣泉乡	twn	朱连屯 cmnt    17号	o
    
- 一般括号打o，除非公司名称中带括号
    - 台州市	CTY	三门县	CNTY	岭峰石材市场	POI	（屠宰厂旁）	O
    - 台州市	CTY	玉环县	CNTY	经济开发区	O	银湖大道	RD	23号	NO	（	O	雅仕兰家具	POI	）	O
    - 台州	CTY	玉环市	CNTY	楚门文房路	RD	（	O	中心幼儿园	POI	）	O
    - 乐清市	CNTY	柳市镇	TWN	新光工业区160号（	O	振宏电气集团有限公司	POI	）	O
    - 余姚市	CNTY	陆埠镇	TWN	五马工业园区余	O	姚市佳龙软管洁具厂	POI	（普通合伙）	O
    - 温州市	CTY	苍南县	CNTY	钱库镇	TWN	振兴西街	RD	398号	NO	（	O	金梦迪酒店	POI	对面）	O
    - 嘉兴市	CTY	经济开发区	O	岗山路	RD	500号	NO	东海橡塑（嘉兴）有限公司	POI
    - 上海	PRV	徐汇区	CNTY	淮海中路	RD	999	NO	环贸IAPM	POI	二期26楼	O	苹果电脑贸易（上海）有限公司	POI 
    
 ## 3.2. 公司名称标签
 暂无





