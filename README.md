## Overview

通过关键字抓取百度知道的问题，最多1000条。程序运行后会在当前目录生成一个result.csv的文件

## Installation

	git clone git@github.com:popomore/fzhidao.git
	cd fzhidao
	sudo python setup.py install

## Usage

输入关键字

	fzhidao "akb48"

输入有效时间，最终只会输出有效时间之后的内容
	
	fzhidao "akb48" 2011-1-1
	

