import subprocess
import re

charset_find = re.compile(r'(\d{3,}?)\\')
re_find = re.compile(r':(.+)')
key_find = re.compile(r'关键内容')

def getDatas():
    charset = getCharSet()
    datas = []
    for each in getWifiName(charset):
        wifi_name = each
        re = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles',wifi_name,'key=clear']).decode(charset).split('\r\n')
        for each in re:
            re_key = key_find.search(each.strip())
            if not re_key:
                continue

            context = each
            key = re_find.search(context).group(1)
            if key:
                print(wifi_name,key)
                datas.append((wifi_name,key))

    return datas


def getWifiName(charset):

    wifis = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode(charset).split('\r\n')
    for each in wifis:
        re = re_find.search(each.strip())
        if not re or re == '':
            continue
        wifi_name = re.group(1).strip()
        yield wifi_name


def getCharSet():
    charsMap = {
        '936': 'gbk',
        '20936': 'gb2312',
        '65001': 'utf-8'
    }
    char_set = subprocess.check_output(['chcp'], shell=True)
    char_set_find = charset_find.search(str(char_set))
    if not char_set_find:
        assert char_set_find is not None
    char_set_code = char_set_find.group(1)
    char_set = charsMap[char_set_code]
    return char_set


if __name__ == '__main__':
   print(getCharSet())

