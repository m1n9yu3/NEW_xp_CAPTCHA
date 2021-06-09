#!/usr/bin/env python
# coding = utf-8
# @Author   : m1n9yu3
# @Time     : 2021/6/9 21:41
# @File     : server2.py
# @Project  : NEW_xp_CAPTCHA


import muggle_ocr
import re,time,base64,os
from flask import Flask,request,abort



host = {'host':'0.0.0.0', "port":8899}
count = 50 #保存多少个验证码及结果

app = Flask(import_name=__name__)


@app.route("/",methods=['GET'])
def do_GET():
    with open('github/temp/log.txt', 'r') as f:
        content = f.read()
    data = '<title>xp_CAPTCHA</title><body style="text-align:center"><h1>验证码识别：xp_CAPTCHA</h1><a href="http://www.nmd5.com">author:算命縖子</a><p><TABLE style="BORDER-RIGHT: #ff6600 2px dotted; BORDER-TOP: #ff6600 2px dotted; BORDER-LEFT: #ff6600 2px dotted; BORDER-BOTTOM: #ff6600 2px dotted; BORDER-COLLAPSE: collapse" borderColor=#ff6600 height=40 cellPadding=1 align=center border=2><tr align=center><td>验证码</td><td>识别结果</td><td>时间</td></tr>%s</body>'%(content)
    return data

@app.route("/base64",methods=['POST'])
def do_POST():
    req_datas = request.data.decode()
    base64_img = re.search('base64=(.*?)$', req_datas)

    # print(base64_img.group(1)) #post base64参数的内容
    img_name = time.time()

    with open("temp/%s.png" % img_name, 'wb') as f:
        f.write(base64.b64decode(base64_img.group(1)))
        f.close()

    # 验证码识别
    sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
    with open(r"temp/%s.png" % img_name, "rb") as f:
        b = f.read()
    text = sdk.predict(image_bytes=b)
    # text = '1'
    print(text)  # 识别的结果

    # 保存最新count个的验证码及识别结果
    with open('github/temp/log.txt', 'r') as f:
        data = ""
        counts = 0
        content = f.read()
        pattern = re.compile(r'.*?\n')
        result1 = pattern.findall(content)
        for i in result1:
            counts += 1
            if counts >= count: break
            data = data + i

    with open('github/temp/log.txt', 'w') as f:
        f.write('<tr align=center><td><img src="data:image/png;base64,%s"/></td><td>%s</td><td>%s</td></tr>\n' % (
        base64_img.group(1), text, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(img_name)))) + data)

    # 删除掉图片文件，以防占用太大的内存
    os.remove("temp/%s.png" % img_name)

    return text


if __name__ == '__main__':
    os.makedirs('github/temp', exist_ok=True)
    with open('github/temp/log.txt', 'w') as f:
        pass
    app.run(debug=False, host=host['host'], port=host['port'])