# jupyter as wiki

插件控制台
```
pip install jupyter_contrib_nbextensions && jupyter contrib nbextension install 
pip install qgrid
jupyter nbextension enable --py --sys-prefix qgrid
```

配置
```
/usr/local/etc/jupyter/jupyter_nbconvert_config.json
```

run
```
jupyter notebook
```