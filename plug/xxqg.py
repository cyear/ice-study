import requests, re
#import qrcode
import qrcode_terminal

"""
pip:
    requests
    // qrcode
    qrcode_terminal
"""

def main(self):
    if self.beta:
        self.iLog('获取链接中... ', end='')
        res = requests.get('http://www.iceh2o1.top/xxqg/add').text
        # print(res)
        pattern = r'<a href="(\S+)">'
        result = re.search(pattern, res)
        print('[OK]')
        if result:
            self.iLog('转换二维码...')
            link = result.group(1)
            # print(link)
            '''qr = qrcode.QRCode(
                version=5,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(link)
            qr.make(fit=True)
            img = qr.make_image()
            img.print_png()'''
            qrcode_terminal.draw(link)
            if input('扫码完成后输入yes继续: ')=='yes':
                requests.get('http://www.iceh2o1.top/xxqg/study').text
                self.iLog('学习中... [OK]')