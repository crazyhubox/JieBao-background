import smtplib
from email.mime.text import MIMEText

def send_erro(erro:list):

    msg_from='@qq.com'            
    passwd=''                                   
    msg_to='@qq.com'


    subject="SHU_ERROR_HANDLER"                                     #主题
    # datas = [
    #     'There are some bugs:',
    # ]
    content="\n".join(erro)#正文

    msg = MIMEText(content)

    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to


    try:
        s = smtplib.SMTP_SSL("smtp.qq.com",465)     #邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
    except (smtplib.SMTPException) as e:
        print(e)
        print ("发送失败")
    else:
        print( "发送成功")
    finally:
        s.quit()


if __name__ == '__main__':
    main()