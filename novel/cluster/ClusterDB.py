#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-02 22:54'

from basic.DBModule import *

def here():
    print('PrimeMusic')

class ClusterDBModule(MySQLModule):
    """
        封装聚类模块中用到的数据库操作
    """

    def get_dirfmtinfo_id_list(self, site_id, update_time):
        """
        """
        conn = self.buid_connection('dir_fmt_info')
        if conn is False:
            return []

        sql = 'SELECT id FROM dir_fmt_info{0} WHERE update_time > {1}'
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('can not get id list [sql: {0}, error: {1}]'.format(sql, e))
            return []

        id_list = []
        for (id, ) in cursor.fetchall():
            id_list.append(id)
        return id_list



if __name__ == '__main__':
    here()    







