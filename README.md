# githubip
国内访问github太慢，可以通过修改host的方法加快速度

# 使用方法

1. 克隆项目到本地，安装则需要安装BeautifulSoup4  
`pip install BeautifulSoup`
2. 修改url.text,加入你需要的修改host的url。#注释url，程序将忽略该行。
3. 在本地运行 `getip.py` 
4. 程序将自动清除自动生成成的host,然后增加新解析的host。