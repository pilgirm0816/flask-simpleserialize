## flask_simpleserialize

* 一个适用于flask框架(轻型的、简单的)序列化工具

### 使用介绍

```python
pip install flask-simpleserialize
```

当前版本为0.0.1（^_^）,以后还会继续更新(有时间就写)

它不需要你在你的model层实例上面再继承啊什么的，完全不需要，接下来看操作不废话



**个人觉得不管使用什么框架，序列化这一步都应该单独提出来。用作一层**



model.py

```python
from sqlalchemy import orm, BIGINT, Column, TIMESTAMP, BOOLEAN, VARCHAR, TEXT, Integer, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# model类必须要继承declarative_base()
class AppletUser(Base):
    __tablename__ = "applet_user"

    id = Column(BIGINT,primary_key=True,info='用户主键id')
    wx_unique_identification = Column(VARCHAR(256),info='wx端传入的唯一标识',default='')
    wx_user_nickname = Column(VARCHAR(256),info='wx用户的昵称',default="")
    # wx_user_nickname = Column(VARCHAR(256),info='wx用户的昵称',default="dw{}".format(client.get_guid()))
    wx_user_avatar = Column(VARCHAR(256),info='wx用户的头像url',default='')
    wx_user_phone = Column(VARCHAR(256),info='用户电话号码',default='')
    wx_user_country = Column(VARCHAR(256),info='用户所在国家',default='中国')
    wx_user_province = Column(VARCHAR(256),info='用户所在省份/州',default='北京')
    wx_user_city = Column(VARCHAR(256),info='用户所在城市',default='北京')
    wx_user_gender = Column(TINYINT,info='0为未知,1为男性,2为女性',default=0)
    user_memberorder = Column(TINYINT,info='0为普通用户,1为白银会员,2为黄金会员,3为铂金会员,4为钻石会员,5为超级会员',default=0)
    user_integral = Column(BIGINT, info='用户积分', default=0)
    user_balance = Column(BIGINT,info='用户余额',default=0)
    is_activate = Column(BOOLEAN,info='是否激活,默认为激活状态',default=False)
    soft_delete = Column(BOOLEAN, info='后台系统是否软删除删除,True为删除,False为未删除',default=False)
    create_time = Column(DateTime, server_default= func.now(), info='用户创建时间')
    update_time = Column(DateTime, server_default= func.now(), onupdate=func.now(), info='用户更新时间')

    # TODO 由于wx官方不会对用户以前的头像url进行清除，一旦wx用户更改头像就会造成wx用户头像更改小程序端不会更改的问题，
    #  所以当用户换头像的时候小程序也要跟着换，特定义此字段用以存储用户以前的头像
    user_previous_avatar_text = Column(TEXT,info='存储用户以前头像URL')
	
    

    def __repr__(self):
        return "<AppletUser(id='%s',wx_user_nickname='%s')>"%(self.id,self.wx_user_nickname)
```



serialize.py

```python
from flask_simpleserialize import ModelSerialize
class UserSerialize(ModelSerialize):
    class Meta:
        model = AppletUser
        serialize_fields = ['id','wx_unique_identification']
        deserialization_fields = ['create_time']

    def get(self):
        Users = SessionFactory.session().query(AppletUser).all()
        data = self.data(Users)
        return data

```

你只需要自己写一个类导入`ModelSerialize`模块然后继承，再其内部定义一个Meta类(必须要定义的呦)，Meta类里面写入model属性，属性值就是你model实例名称(也是必需要写的)，还有再写入你需要序列化/反序列化的字段值。`serialize_fields`与`deserialization_fields`名称是不能更改的。然后你需要定义一个方法，方法内部执行查询语句，将结果丢给`data`方法.剩下的就不用管了，`ModelSerialize`会全部帮你处理好的



router.py

```python
from serialize import UserSerialize
from flask import Blueprint,request,jsonify
from flasgger import swag_from

user = Blueprint('user',__name__)
@hello_rbp.route('/user',methods=["GET"])
@swag_from('../docs/doc/user.yaml')
def get_user():
    """获取用户信息
    """
    user_serialize = UserSerialize()
    result = user_serialize.get()

    return jsonify(result)
```

请看结果

![image-20220127195443704](img/result1.png)







**当然了它也支持对序列化的字段进行更改，但是你必须要在你定义的model类中加入`cnme`方法并用`@property`装饰器将其装饰成`属性`**

代码如下所示

```python
from sqlalchemy import orm, BIGINT, Column, TIMESTAMP, BOOLEAN, VARCHAR, TEXT, Integer, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# 看到没它还是像以前一样
class AppletUser(Base):
    __tablename__ = "applet_user"

    id = Column(BIGINT,primary_key=True,info='用户主键id')
    wx_unique_identification = Column(VARCHAR(256),info='wx端传入的唯一标识',default='')
    wx_user_nickname = Column(VARCHAR(256),info='wx用户的昵称',default="")
    # wx_user_nickname = Column(VARCHAR(256),info='wx用户的昵称',default="dw{}".format(client.get_guid()))
    wx_user_avatar = Column(VARCHAR(256),info='wx用户的头像url',default='')
    wx_user_phone = Column(VARCHAR(256),info='用户电话号码',default='')
    wx_user_country = Column(VARCHAR(256),info='用户所在国家',default='中国')
    wx_user_province = Column(VARCHAR(256),info='用户所在省份/州',default='北京')
    wx_user_city = Column(VARCHAR(256),info='用户所在城市',default='北京')
    wx_user_gender = Column(TINYINT,info='0为未知,1为男性,2为女性',default=0)
    user_memberorder = Column(TINYINT,info='0为普通用户,1为白银会员,2为黄金会员,3为铂金会员,4为钻石会员,5为超级会员',default=0)
    user_integral = Column(BIGINT, info='用户积分', default=0)
    user_balance = Column(BIGINT,info='用户余额',default=0)
    is_activate = Column(BOOLEAN,info='是否激活,默认为激活状态',default=False)
    soft_delete = Column(BOOLEAN, info='后台系统是否软删除删除,True为删除,False为未删除',default=False)
    create_time = Column(DateTime, server_default= func.now(), info='用户创建时间')
    update_time = Column(DateTime, server_default= func.now(), onupdate=func.now(), info='用户更新时间')

    # TODO 由于wx官方不会对用户以前的头像url进行清除，一旦wx用户更改头像就会造成wx用户头像更改小程序端不会更改的问题，
    #  所以当用户换头像的时候小程序也要跟着换，特定义此字段用以存储用户以前的头像
    user_previous_avatar_text = Column(TEXT,info='存储用户以前头像URL')
	
    ########差异之处##############
    @property
    def cname(self):
        return {'wx_unique_identification':'unique_identification'}

    def __repr__(self):
        return "<AppletUser(id='%s',wx_user_nickname='%s')>"%(self.id,self.wx_user_nickname)
```



**`cname`属性内部直接返回一个字典，字典的key为原始字段名，value则为序列化之后的名字**

如图所示

![image-20220127200040550](img/result2.png)



^_^  以后会继续更新滴
