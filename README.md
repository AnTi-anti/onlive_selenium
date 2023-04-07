## 参数解释

```python
{
    "date": [7],
    "session": [1],
    "ticket_type": [0],
    "ticket_num": 1,
    "driver_path": "C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe",
    "target_url": "https://m.zhengzai.tv/#/ticket/detail?id=2352133014472826880833749",
    "buy_time": "2022 05 18 00 43 00",
    "wait_time": 0.5,
    "phone": "1111"
}
```

* data:表示日期，最左边默认为0，依次往右递增
* session:表示场次，最左边默认为0，依次往右递增
* tickty_type:表示场次， 最左边默认为0，依次往右递增
* ticket_num：票数
* driver_path：chromedriver地址
* target_url：抢票目标地址
* buy_time：下单时间
* wait_time：等待时间
* phone：手机号

## 提前准备

### 步骤一 下载浏览器

* 下载chrome浏览器，下载地址：https://gakkiwife.lanzouw.com/i4T71wvg3qd 

  * 如果已 经下载可以忽略这一步 

#### 步骤二 chrome配置

* 下载完chrome浏览器之后，点击浏览器最右边的三个点，依次点击---》帮助---》关于Google Chrome，查看自己的Chrome版本

  <img src="https://img-blog.csdnimg.cn/26ac31256b5a4049a68b52991fe0b3f7.png#pic_center" alt="在这里插入图片描述" style="zoom:50%;" />

* 下载和Chrome版本对应的ChromeDriver软件 

  * 链接：http://chromedriver.storage.googleapis.com/index.html 

  * 我自己的Chrome版本是110.5481.78，那么就在链接里找到对应chromedriver的版本，并进行下载，这里我下载的是**windows系统**

    可以看到，链接中并没有完全一致的版本，那么就**挑选一个和当前chrome版本日期最近的版本**，因此这里我选择下载104.0.5112.79

    <img src="https://img-blog.csdnimg.cn/631b602ffebe4e1693a12f5caf94d64e.png#pic_center" alt="在这里插入图片描述" style="zoom:67%;" />

    点进去，继续下载

    <img src="https://img-blog.csdnimg.cn/a7a674a4b47746298f3f236bb66a8caa.png#pic_center" alt="在这里插入图片描述" style="zoom: 67%;" />

​              windows系统下载win32位的zip压缩包即可

* 下载之后进行解压，得到**chromedriver.exe**

  * 打开安装chrome浏览器的目录，将 **chromedriver.exe**放入当前目录中

  <img src="https://img-blog.csdnimg.cn/c29caa0656ef4ab190cc96387a63f61b.png#pic_center" alt="在这里插入图片描述" style="zoom:67%;" />
