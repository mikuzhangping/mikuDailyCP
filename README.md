
# 今日校园自动签到脚本  

本项目针对的是合肥工业大学在`今日校园`->`我的大学`->`疫情信息收集`中的打卡，其他学校或其他方式打卡暂不支持。如果你的打卡通过`辅导员通知`发布，请在这里<https://gitee.com/Finch1/FuckDailyCP>寻求帮助。如果你的打卡是`今日校园`->`我的大学`->`签到任务`那种带定位的打卡请到ZimoLoveShuang<https://github.com/ZimoLoveShuang/auto-sign/>寻求帮助。<br>
下面介绍本项目的使用方法。

## 使用方法

### 第一步

右键点fork（红圈标注的）按钮，在新标签打开，你会复制一份我的仓库。另外如果不觉得麻烦，fork前可以给我一个star吗？
![fork](https://github.com/mikuzhangping/mikuDailyCP/raw/master/picture/fork.png)

### 第二步

复制完成后你会直接看到复制仓库的主页。在项目页的上方你能看到一个导航栏，点击Action。接下来你会看到一个警告，但是不用管，点击绿色按钮确认警告。
![action](https://github.com/mikuzhangping/mikuDailyCP/raw/master/picture/action.png)

### 第三步

在主页上方导航栏你将找到setting，进入后找到secret选项，在这里新建一个secret。<br>
![secret1](https://github.com/mikuzhangping/mikuDailyCP/raw/master/picture/secret1.png)<br>
新建一个secret后你将看到如上页面，在·name·一栏中填`INFO`，`value`中填你的`账号`和`密码`,以空格隔开。其中账号为学号，密码为身份证后8位。接下来点击下面那个绿色按钮。此时你就将你的账号告诉了脚本。<br>
![secret2](https://github.com/mikuzhangping/mikuDailyCP/raw/master/picture/secret2.png)<br>
当然你也可以将你的朋友账号和密码加进去，只要以空格隔开，格式形如"账号1 密码1 账号2 密码2 ...账号n 密码n"

### 第四步

至此，你已经完成了所有的操作。如果一切都没问题，那么脚本会在每天14：10自动签到。另外如果不觉得麻烦，可以给我一个star吗？

## 补充

### 脚本无法自动运行

检查仓库的setting的action设置  

### 使用脚本打卡时如果我要外出旅行怎么办？  

A1：脚本每天下午2：10自动运行，并重复提交上次打卡的内容。如果你需要修改每天打卡的内容可以按照以下两个方法操作。  

>1、你在X月20日到达啊目的地，在下午2：10前手动打一遍卡即可。直至你下次修改。  

>2、你可以重新编辑X月19日的打卡内容，这样X月20日就会重复19日的内容。直至你下次修改。  

### 将学号和身份证后8位交给别人代打卡安全吗？  

A2：非常不安全！！！你相当于将身份证号和其他关键信息交给别人。有能力的，请自己研究下如何使用本项目。  

### 脚本免费吗？  

A3：完全免费，给个star就行。请各位不要用信息差赚钱。
