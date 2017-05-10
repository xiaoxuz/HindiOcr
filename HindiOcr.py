'''
梵文图片识别 & 转写英文体
author: xiaoxuz
date:2017/05/10
'''
import pycurl
import urllib.parse 
import re
import sys
from io import StringIO 
from io import BytesIO 

def getOcr(url, refer, crl):
    crl.setopt(pycurl.URL, url)
    crl.setopt(pycurl.COOKIEJAR, "cookietxt")
    crl.setopt(pycurl.COOKIEFILE, "cookie.txt")
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.USERAGENT, "Mozilla/5.0 (X11; U; Linux i586; de; rv:5.0) Gecko/20100101 Firefox/5.0")
    crl.setopt(pycurl.REFERER, refer)
    crl.setopt(pycurl.POST, 0)
    crl.setopt(pycurl.WRITEFUNCTION, BytesIO().write)
    crl.perform()
    #print(crl)

def post(url, refer, post_data, crl, e):
    crl.setopt(pycurl.URL, url)
    crl.setopt(pycurl.COOKIEJAR, "cookietxt")
    crl.setopt(pycurl.COOKIEFILE, "cookie.txt")
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.USERAGENT, "Mozilla/5.0 (X11; U; Linux i586; de; rv:5.0) Gecko/20100101 Firefox/5.0")
    crl.setopt(pycurl.REFERER, refer)
    crl.setopt(pycurl.POST, 1)
    crl.setopt(pycurl.WRITEFUNCTION, e.write)
    crl.setopt(pycurl.POSTFIELDS, urllib.parse.urlencode(post_data))
    crl.perform()
    data = e.getvalue().decode("utf8")
    return data 
    #print(crl)

def runTransfer(data):
    crl = pycurl.Curl()
    e = BytesIO()
    post_data = {"TextToConvert":data}
    ret = post("http://techwelkin.com/tools/hindi-to-english-roman-font-converter/", "http://techwelkin.com/tools/hindi-to-english-roman-font-converter/", post_data, crl, e)
    crl.close()
    e.close()
    data = parseTransferRet(ret)
    if data:
        print(data)
    else:
        print("Not Match Transfer.")

def parseTransferRet(data):
    matchObj = re.search(r'\<textarea name=\"ConvertedText\" id=\"unicode_text\" cols=\"80\" rows=\"8\">(.*?)\<\/textarea\>', data, re.M|re.I|re.DOTALL)
    if matchObj:
        return matchObj.group(1)
    else:
        return False

def parseOcrRet(data):
    matchObj = re.search( r'val\(\"(.*?)\"\)\.show', data, re.M|re.I)
    if matchObj:
        return matchObj.group(1)
    else:
        return False

def runOcr(img):
    crl = pycurl.Curl()
    e = BytesIO()
    getOcr("http://www.i2ocr.com/", "http://www.i2ocr.com/", crl)
    post_data = {"i2ocr_options":"url", "i2ocr_uploadedfile":"", "i2ocr_url":img, "i2ocr_languages":"in,hin"}
    ret = post("http://www.i2ocr.com/process_form", "http://www.i2ocr.com/", post_data, crl, e)
    crl.close()
    e.close()
    data = parseOcrRet(ret)
    if data:
        return data.encode('utf8').decode('unicode_escape')
    else:
        print("Not Match Ocr.")
        return False

if __name__ == "__main__":
    #ocrRet = runOcr("http://59.110.156.232/wspace/Data/Media/170509-122701.png")
    #ocrRet = runOcr("http://www.i2ocr.com/download/opq64ya1849969d3.png_preview.jpg")
    ocrRet = runOcr(sys.argv[1])
    if ocrRet:
        transferRet = runTransfer(ocrRet)
        if transferRet:
            print(transferRet)
