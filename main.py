from time import sleep
from docxtpl import DocxTemplate

from selenium import webdriver
from selenium.webdriver.common.by import By


from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# отключает открытие браузера
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920x1080')
service = Service()

driver = webdriver.Chrome(service=service, options=chrome_options)

# driver = webdriver.Chrome()

print('Введите номер документа:\n 1) Исковое заявление о взыскании задолженности по договору уступки прав требований \n 2) Исковое заявление о взыскании неустойки в связи с нарушением сроков работ \n 3) Исковое заявление о взыскании задолженности по договору поставки')
id_doc = str(input())
doc = DocxTemplate("template_isk.docx")
title = ""
if id_doc[0] == '1':
    title = 'о взыскании задолженности по договору уступки прав требований'
elif id_doc[0] == '2':
    title = 'о взыскании неустойки в связи с нарушением сроков работ'
else:
    title = 'о взыскании задолженности по договору поставки'


driver.get("https://egrul.nalog.ru/index.html")

INN_ist = str(input('Введите ИНН истца: '))
INN_otv = str(input('Введите ИНН ответчика: '))

input_INN = driver.find_element(By.ID, 'query')
input_INN.clear()
input_INN.send_keys(str(INN_ist))
find_button = driver.find_element(By.ID, 'btnSearch')
find_button.click()
sleep(4)
name1 = driver.find_element(By.CLASS_NAME, 'op-excerpt')
res1 = driver.find_element(By.CLASS_NAME, 'res-text')
txt1 = name1.text
print('Истец: ' + txt1)
information = res1.text.split(', ')
mp = dict()
for inf in information:
    mp[inf.split(':')[0] + '1'] = inf
input_INN = driver.find_element(By.ID, 'query')
input_INN.clear()
input_INN.send_keys(str(INN_otv))
find_button = driver.find_element(By.ID, 'btnSearch')
find_button.click()
sleep(4)
name2 = driver.find_element(By.CLASS_NAME, 'op-excerpt')
res2 = driver.find_element(By.CLASS_NAME, 'res-text')
txt2 = name2.text
print('Ответчик: ' + txt2)
information = res2.text.split(', ')
for inf in information:
    mp[inf.split(':')[0] + '2'] = inf
context = {
    'title': title,
    'name1': txt1,
    'INN1': mp['ИНН1'],
    'KPP1': mp['КПП1'],
    'OGRN1': mp['ОГРН1'],
    'name2': txt2,
    'INN2': mp['ИНН2'],
    'KPP2': mp['КПП2'],
    'OGRN2': mp['ОГРН2']
}
doc.render(context)
doc_name = str(input('Введите название документа: '))
doc.save(doc_name + ".docx")



