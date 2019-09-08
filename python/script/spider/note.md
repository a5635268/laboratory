# 基于scrapy的爬虫项目

## 链接

手册地址： https://docs.scrapy.org/en/latest/

## 基础命令

```
scrapy startproject 项目名 # 创建爬虫项目
scrapy list # 列出当前项目的所有爬虫名
scrapy genspider 爬虫名字 爬虫的网址 # 创建爬虫
scrapy crawl 爬虫名字  #启动爬虫

# 参数
--nolog # 不打印日志
-s LOG_FILE=spider.log # 日志输出
```

## 配置

```python
LOG_LEVEL = 'ERROR'

# 每个链接之间延迟多少秒再请求，支持小数点
DOWNLOAD_DELAY = 0.35 


# 配置下载图片路径（一定要配置，否则不会执行管道操作）
IMAGES_URLS_FIELD = "front_image_url"  # 默认是image_urls，这里做个修改

project_dir = os.path.abspath(os.path.dirname(__file__))
IMAGES_STORE=os.path.join(project_dir,'images')
```

## spider