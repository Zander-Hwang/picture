## <center>Picture Warehouse</center>

```shell
#获取项目依赖包，输出到 requirements.txt 中
pip freeze > ./requirements.txt
```

```shell
#安装依赖包
pip install -r ./requirements.txt
```

```python
# 创建文件信息存储表
from src.utils import DataBase

db = DataBase('./database/picture.db')
columns = f'''
    id INTEGER PRIMARY KEY  NOT NULL,
    type TEXT    NOT NULL,
    path TEXT    NOT NULL,
    path_en TEXT,
    date TEXT    NOT NULL,
    title TEXT    NOT NULL,
    title_en TEXT,
    copyright TEXT,
    copyright_en TEXT
'''
db.create_table('picture_info', columns)
db.close()
```