# -*- coding: utf-8 -*-
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

import urllib.request
import urllib.parse
import json
import os


def get_pdf(filePath):
    '''读取pdf内容，并翻译，写入txt文件'''

    # 以二进制读模式打开本地pdf文件
    fp = open(filePath, 'rb')
    # 用文件对象来创建一个pdf文档分析器
    praser_pdf = PDFParser(fp)
    # 创建一个PDF文档
    doc_pdf = PDFDocument()
    # 连接分析器与文档对象
    praser_pdf.set_document(doc_pdf)
    doc_pdf.set_parser(praser_pdf)
    # 提供初始化密码doc.initialize("123456")，如果没有密码 就创建一个空的字符串
    doc_pdf.initialize()

    # 检查文档是否提供txt转换，不提供就无法翻译文档
    if not doc_pdf.is_extractable:
        # Logger().write(self.fileName + '未能提取有效的文本，停止翻译。')
        print("error1")
        return
    else:
        # 创建PDF资源管理器来共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF参数分析器
        laparams = LAParams()
        # 创建聚合器
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF页面解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一页的内容
        for page in doc_pdf.get_pages():
            # 使用页面解释器来读取
            interpreter.process_page(page)
            # 使用聚合器获取内容
            layout = device.get_result()

            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure,
            # LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for out in layout:
                # 判断是否含有get_text()方法，图片之类的就没有
                if isinstance(out, LTTextBoxHorizontal):
                    content = out.get_text()
                    trans = youdao_translate(content)
                    write(content)
                    write(trans)
        # Logger().write(self.fileName + '翻译完成，新文档：' + self.new_fullPath)
        print('error2')


def youdao_translate(content):
    '''实现有道翻译的接口'''
    youdao_url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    data = {}

    data['i'] = content
    data['from'] = 'AUTO'
    data['to'] = 'AUTO'
    data['smartresult'] = 'dict'
    data['client'] = 'fanyideskweb'
    data['salt'] = '1525141473246'
    data['sign'] = '47ee728a4465ef98ac06510bf67f3023'
    data['doctype'] = 'json'
    data['version'] = '2.1'
    data['keyfrom'] = 'fanyi.web'
    data['action'] = 'FY_BY_CLICKBUTTION'
    data['typoResult'] = 'false'
    data = urllib.parse.urlencode(data).encode('utf-8')

    youdao_response = urllib.request.urlopen(youdao_url, data)
    youdao_html = youdao_response.read().decode('utf-8')
    target = json.loads(youdao_html)

    trans = target['translateResult']
    ret = ''
    for i in range(len(trans)):
        line = ''
        for j in range(len(trans[i])):
            line = trans[i][j]['tgt']
        ret += line + '\n'

    return ret


def baidu_translate(content, type=1):
    '''实现百度翻译'''
    baidu_url = 'http://fanyi.baidu.com/basetrans'
    data = {}

    data['from'] = 'en'
    data['to'] = 'zh'
    data['query'] = content
    data['transtype'] = 'translang'
    data['simple_means_flag'] = '3'
    data['sign'] = '94582.365127'
    data['token'] = 'ec980ef090b173ebdff2eea5ffd9a778'
    data = urllib.parse.urlencode(data).encode('utf-8')

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36"}
    baidu_re = urllib.request.Request(baidu_url, data, headers)
    baidu_response = urllib.request.urlopen(baidu_re)
    baidu_html = baidu_response.read().decode('utf-8')
    target2 = json.loads(baidu_html)

    trans = target2['trans']
    ret = ''
    for i in range(len(trans)):
        ret += trans[i]['dst'] + '\n'

    return ret


def write(content):
    with open(r'C:\Users\Lenovo\Desktop\\chap 3.txt', 'a+', encoding='utf-8') as f:
        # 存储文本
        for text in content:
            f.writelines(text)
    f.close()
    print('写入完毕！')


if __name__ == '__main__':
    filename = r'C:\Users\Lenovo\Desktop\chap 3.pdf'
    get_pdf(filename)
    '''该程序需要改变两个路径，安装相关包即可运行'''
