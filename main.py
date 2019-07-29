import requests

from bs4 import BeautifulSoup
from terminaltables import AsciiTable

url = 'http://140.131.110.236/_eportfolio/_portfolio/studentscoreview.jsp'

def check_year(year):
    if year.isdigit() == False or len(year) != 3:
        return False
    else:
        return True

def check_semester(semester):
    if semester != '1' and semester != '2':
        return False
    else:
        return True

def check_std_id(std_id):
    if std_id[1] == 'N' and (len(std_id) == 8 or len(std_id) == 9):
        return True
    elif len(std_id) == 7 or len(std_id) == 8:
        return True
    else:
        return False

def check_class_id(class_id):
    if class_id[1] == 'N' and (len(class_id) == 5 or len(class_id) == 6):
        return True
    elif len(class_id) == 4 or len(class_id) == 5:
        return True
    else:
        return False

def get_score(year, semester, std_id):
    res = requests.get(url,{
        'year': year,
        'str': semester,
        'id': std_id
    })

    if res.status_code != 200:
        print('Http 錯誤 {} !!!'.format(res.status_code))
        print()
        return False

    if '無任何資訊' in res.text:
        print("找不到 {} 的成績!!!".format(std_id))
        print()
        return False

    print(std_id, '{}學年'.format(year), '第{}學期'.format(semester))
    soup = BeautifulSoup(res.text, 'html.parser')
    rows = soup.find_all('table', 'table_boder_style2')

    score = []
    for row in rows[:-3]:
        score.append([i.text for i in row.find_all('td', 'content_word')])
    
    head = ["名稱", "開課別", "學分數", "成績"]
    table = AsciiTable([head, *score])
    print(table.table)

    score = []
    for row in rows[-3:]:
        score.append([i.text for i in row.find_all('td', 'content_word')])

    head = ["名稱", "成績"]
    table = AsciiTable([head, *score])
    print(table.table)
    print()

def main():
    year = input('學年度：')
    if check_year(year) == False:
        print('學年度格式錯誤!!!')
        return

    semester = input('學期 [1 or 2]：')
    if check_semester(semester) == False:
        print('學期格式錯誤!!!')
        return
    
    search_type = input("學號查詢請輸's' 班級查詢請輸入'c'：")
    if search_type == 's':
        std_id = input('學號：')
        if check_std_id(std_id) == False:
            print('學號格式錯誤!!!')
            return
        get_score(year, semester, std_id)
    elif search_type == 'c':
        class_id = input('班級代號：')
        if check_class_id(class_id) == False:
            print('班級代號格式錯誤!!!')
            return

        n = 0
        res_fail = 0
        while True:
            n += 1
            if class_id[0] == 'N':
                std_id = '{}{}'.format(class_id, '%02d' % n)
            else:
                std_id = '{}{}'.format(class_id, '%03d' % n)
            if get_score(year, semester, std_id) == False:
                res_fail += 1
                if res_fail == 5:
                    break
                else:
                    continue

            res_fail = 0

        print('已完成!!!')
    else:
        print('[學號/班級]格式錯誤!!!')

if __name__ == '__main__':
    main()