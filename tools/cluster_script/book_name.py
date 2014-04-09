#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-04-09 09:53'


import MySQLdb

def here():
    print('PrimeMusic')


if __name__ == '__main__':
    conn = MySQLdb.connect(
        host = "10.46.7.171",
        port = 4198,
        user = "wise_novelclu_w",
        passwd = "C9l3U4n6M2e1",
        db = "novels_new")
    conn.set_character_set('GBK')
    cursor = conn.cursor()

    sql = 'SELECT rid, book_name, rank FROM novel_authority_info limit 10000'
    result = cursor.execute(sql)

    book_name_dict = {}
    for (rid, book_name, rank) in result:
        book_name_dict[book_name] = 1

    for (rid, book_name, rank) in result:
        if len(book_name) <= 4:
            continue
        if book_name.find("更多") + 4 == len(book_name):
            book_name = book_name[0 : len(book_name) - 4]
            if book_name_dict.has_key(book_name):
                print('book_name: {0}, book_name: {0}更多'.format(book_name))
            else:
                print('book_name: {0}更多'.format(book_name))

    cursor.close()
    conn.close()


    here()    







