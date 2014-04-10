#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-04-09 09:53'


import MySQLdb

def here():
    print('PrimeMusic')

def update_book_name(cursor, rid, book_name):
    """
    """
    sql = "UPDATE novel_authority_info SET book_name = '%s' WHERE rid = '%d'" % (book_name, rid)
    try:
        cursor.execute(sql)
    except Exception, e:
        print('error: {0}'.format(e))

    return True


if __name__ == '__main__':
    conn = MySQLdb.connect(
        host = "10.46.7.171",
        port = 4198,
        user = "wise_novelclu_w",
        passwd = "C9l3U4n6M2e1",
        db = "novels_new")
    conn.autocommit(True)
    conn.set_character_set('GBK')
    cursor = conn.cursor()

    sql = 'SELECT rid, book_name, rank FROM novel_authority_info limit 10000'
    result = cursor.execute(sql)

    book_name_list = ['成长让我们懂得了更多', '失去的比拥有的更多', '我爱你比你爱我更多']
    for (rid, book_name, rank) in result:
        if len(book_name) <= 4:
            continue
        if book_name.find("更多") + 4 == len(book_name):
            if book_name in book_name_list:
                continue
            print('book_name: {0}'.format(book_name))
            book_name = book_name[0 : len(book_name) - 4]
            print('book_name: {0}'.format(book_name))
            #update_book_name(cursor, rid, book_name)


    cursor.close()
    conn.close()
    here()







