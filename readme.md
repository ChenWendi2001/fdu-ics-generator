# fdu_ics_generator
## fdu课程表日历导入脚本

## 什么是ics？
.ics可以帮助你快速导入批量事件到系统日历。使用本脚本将对HTML进行解析，生成.ics文件，帮助你将所有课程添加至你的mac/Win系统日历,可进一步与iPhone、安卓手机、PC/mac等终端同步。

## 如何使用?
### Step 0
使用本脚本你需要配置好python3环境，最好使用chrome浏览器。
	
### Step 1
使用chrome或者其他chromium内核浏览器进入 https://my.fudan.edu.cn/list/bks_xx_kcb 。登录，并使用ctrl+s（Win）或者command+s或者右键选择“另存为”，保存页面的html或htm文件。确保其文件名为“课程表.html”，若文件后缀为.htm，请更改至.html。

### Step 2
下载fdu_ics_generator.py脚本，将其放置在学生课表查询.html文件的同一目录中。**请使用任何一款文本编辑器编辑脚本中的学期开始日期一行。**使用命令行（win+R搜索cmd），切换至该目录，执行以下三条命令。按照提示即可完成转换。

	pip3 install bs4
	pip3 install ics
	python3 fdu_ics_generator.py

### Step3
双击fdu.ics文件即可导入日历。

