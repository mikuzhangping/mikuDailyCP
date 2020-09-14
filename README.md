今日校园自动签到脚本  
====  

该项目是AUST的HuangXu,FengXinYang,ZhouYuYang所写的自动签到脚本的HFUT定制版本，简化了使用方法。项目源地址为<https://gitee.com/Finch1/FuckDailyCP>。下面介绍本项目的使用方法。

第一步
-------

右键点fork（红圈标注的）按钮，在新标签打开，你会复制一份我的仓库。另外如果不觉得麻烦，fork前可以给我一个star吗？
![fork](https://github.com/mikuzhangping/mikuDailyCP/raw/master/picture/fork.png)

第二步
-------

复制完成后你会直接看到复制仓库的主页。在项目页的上方你能看到一个导航栏，点击Action。接下来你会看到一个警告，但是不用管，点击绿色按钮确认警告。
![action](https://github.com/mikuzhangping/mikuDailyCP/raw/master/picture/action.png)

第三步
-------

在主页上方导航栏你将找到setting，进入后找到secret选项，在这里新建一个secret。
![secret1](https://github.com/mikuzhangping/mikuDailyCP/raw/master/picture/secret1.png)
新建一个secret后你将看到如上页面，在name一栏中填ACCOUNT，value中填你的账号。接下来点击下面那个绿色按钮。此时你就将你的账号告诉了脚本。同样的步骤你还要告诉脚本你的密码。新建一个secret，在name一栏中填PASSWORD，value中填你的密码。
![secret2](https://github.com/mikuzhangping/mikuDailyCP/raw/master/picture/secret2.png)

第四步
-------

至此，你已经完成了所有的操作。如果一切都没问题，那么脚本会在每天8点自动签到。另外如果不觉得麻烦，可以给我一个star吗？
但是要注意当辅导员更新表单的时候脚本会失效，你可以先删除现有仓库，等我我更新后再次fork一遍我的仓库。也可以不删除仓库，而是将我仓库中formdb文件夹里面的每一个文件都下载下来，然后上传到你仓库里面的formdb文件夹。

补充
-------

ps：本脚本只支持  合肥工业大学 计算机与信息学院学生使用，其他学校请私聊我。
