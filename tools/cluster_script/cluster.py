#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-24 18:43'

from novel.cluster.ClusterDB import *
from novel.cluster.ClusterEdgeModule import *
from novel.cluster.NovelSimilarityModule import *
from novel.cluster.NovelCleanModule import *

def here():
   print('PrimeMusic')


def init_log(name):
   """
   """
   logger = logging.getLogger(name)
   logger.setLevel(logging.DEBUG)
   fh = logging.FileHandler('./log/{0}.log'.format(name))
   fh.setLevel(logging.DEBUG)
   formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   fh.setFormatter(formatter)
   logger.addHandler(fh)
   logger.info('{0} log init successful!'.format(name))


def get_rid(gid, table_name):
   """
       根据一个gid查询对应的rid
   """
   cluster_db = ClusterDBModule()

   cursor = cluster_db.get_cursor(table_name)
   sql = 'SELECT rid FROM {0} WHERE gid = {1}'.format(table_name, gid)
   cursor.execute(sql)
   rid_list = {}.fromkeys([row[0] for row in cursor.fetchall()]).keys()
   cursor.close()
   if len(rid_list) > 1 or len(rid_list) < 1:
       return False

   return rid_list[0]


def get_gid_list(rid, table_name):
   """
       跟进一个rid查询对应的gid list
   """
   cluster_db = ClusterDBModule()

   cursor = cluster_db.get_cursor(table_name)
   sql = 'SELECT gid FROM {0} WHERE rid = {1}'.format(table_name, rid)
   cursor.execute(sql)
   gid_list = {}.fromkeys([row[0] for row in cursor.fetchall()]).keys()
   cursor.close()
   return gid_list

#--------------------------------------------------------------------------------------------------




#--------------------------------------------------------------------------------------------------

def show_cluster_node(gid):
   """
       检查一个gid对应的虚拟节点的特征目录
   """
   cluster_db = ClusterDBModule()

   cluster_edge = ClusterEdgeModule()
   cluster_similarity = NovelSimilarityModule()

   cluster_node = cluster_edge.cluster_node_collection(gid)
   if not cluster_node:
       return False
   virtual_novel_node = cluster_similarity.virtual_novel_node_generate(cluster_node)
   book_name = cluster_node.book_name.encode('GBK', 'ignore')
   pen_name = cluster_node.pen_name.encode('GBK', 'ignore')
   print('gid: {0}, book_name: {1}, pen_name: {2}'.format(gid, book_name, pen_name))
   print(', '.join('%s: %d' % (chapter.chapter_title.encode('GBK', 'ignore'), chapter.rank) for chapter in virtual_novel_node.chapter_list))
   return virtual_novel_node

#--------------------------------------------------------------------------------------------------

def show_cluster(gid, table_name = 'novel_cluster_dir_info_offline'):
   """
       检查一个gid对应的簇的所有虚拟节点的特征目录
   """
   rid = get_rid(gid, table_name)
   print(rid)
   gid_list = get_gid_list(rid, table_name)
   print(gid_list)
   for gid in gid_list:
       show_cluster_node(gid)

#--------------------------------------------------------------------------------------------------

def show_similarity(gid_x, gid_y):
   """
       检查两个gid的相似性
   """
   novel_node_x = show_cluster_node(gid_x)
   novel_node_y = show_cluster_node(gid_y)

   cluster_similarity = NovelSimilarityModule()
   similarity, match_list = cluster_similarity.novel_node_similarity_calculation(novel_node_x, novel_node_y)
   print(similarity)
   print(match_list)

#--------------------------------------------------------------------------------------------------

def check_diff_rid(gid):
   """
       检查一个gid对应的簇在新老结果中的区别
   """
   old_rid = get_rid(gid, 'novel_cluster_dir_info')
   if old_rid is False:
       return False
   new_rid = get_rid(gid, 'novel_cluster_dir_info_offline')
   if new_rid is False:
       return False

   if old_rid == new_rid:
       return True

   old_gid_list = get_gid_list(old_rid, 'novel_cluster_dir_info')
   new_gid_list = get_gid_list(new_rid, 'novel_cluster_dir_info_offline')
   old_gid_list = sorted(old_gid_list)
   new_gid_list = sorted(new_gid_list)
   if old_gid_list == new_gid_list:
       return True
   print('new_rid: {0}, old_rid: {1}'.format(new_rid, old_rid))

   print('common_gid:')
   for old_gid in old_gid_list:
       if old_gid in new_gid_list:
           show_cluster_node(old_gid)


   print('old_gid_only:')
   for old_gid in old_gid_list:
       if old_gid in new_gid_list:
           continue
       show_cluster_node(old_gid)

   print('new_gid_only:')
   for new_gid in new_gid_list:
       if new_gid in old_gid_list:
           continue
       show_cluster_node(new_gid)

   print('')
   return False

#--------------------------------------------------------------------------------------------------

def check_cluster_diff():
   """
   """
   gid_list = [int(line.strip()) for line in open('./data/rid.txt', 'r').readlines()]
   for index, gid in enumerate(gid_list):
       check_diff_rid(gid)

#--------------------------------------------------------------------------------------------------

def check_cluster_inside_diff():
   """
       检查聚簇结果中是否还有相同gid不同rid的情况
   """
   cluster_db = ClusterDBModule()
   novel_node_list = cluster_db.get_noveldata_all('novel_cluster_dir_info_offline', ['gid', 'rid'])

   gid_rid_dict = {}
   for (gid, rid) in novel_node_list:
       if not gid_rid_dict.has_key(gid):
           gid_rid_dict[gid] = rid
           continue
       if gid_rid_dict[gid] == rid:
           continue
       print('gid: {0}, rid: {1}'.format(gid, rid))

#---------------------------------------------------------------------------------------------------

def novel_cluster_gid_format():
   """
       将novel_cluster_dir_info_offline表中的gid归一化，保证不出现相同gid，rid不同的情况
   """
   cluster_db = ClusterDBModule()
   novel_node_list = cluster_db.get_noveldata_all('novel_cluster_dir_info_offline', ['dir_id', 'gid', 'rid'])

   gid_rid_dict = {}
   gid_list = []
   for index, (dir_id, gid, rid) in enumerate(novel_node_list):
       if not gid_rid_dict.has_key(gid):
           gid_rid_dict[gid] = rid
           continue
       if gid_rid_dict[gid] == rid:
           continue
       gid_list.append(gid)
   gid_list = {}.fromkeys(gid_list).keys()
   print(len(gid_list))

   cursor = cluster_db.get_cursor('novel_cluster_dir_info_offline')
   for index, gid in enumerate(gid_list):
       print('index: {0}, gid: {1}'.format(index, gid))
       sql = 'UPDATE novel_cluster_dir_info_offline SET rid = {0} WHERE gid = {0}'.format(gid)
       cursor.execute(sql)
   cursor.close()

#---------------------------------------------------------------------------------------------------

def check_chapter_title_clean(gid):
    """
        检查一本书的标题过滤 和 虚拟目录效果
    """
    cluster_edge = ClusterEdgeModule()
    cluster_similarity = NovelSimilarityModule()

    novel_clean = NovelCleanModule()

    cluster_node = cluster_edge.cluster_node_collection(gid)
    if cluster_node is False:
        return False
    print('book_name: {0}, pen_name: {1}'.format(cluster_node.book_name, cluster_node.pen_name))

    for novel_node in cluster_node.novel_node_list:
        for chapter in novel_node.chapter_list:
            chapter.chapter_title = chapter.raw_chapter_title
        novel_clean.novel_chapter_clean(novel_node)

        print(novel_node.dir_url)
        print(', '.join('%s' % chapter.chapter_title.encode('GBK', 'ignore') for chapter in novel_node.chapter_list))
        print(', '.join('%s' % chapter.raw_chapter_title.encode('GBK', 'ignore') for chapter in novel_node.chapter_list))

#---------------------------------------------------------------------------------------------------



if __name__ == '__main__':
   init_log('novel')
   init_log('err')

   #check_cluster_inside_diff()
   #novel_cluster_gid_format()

   #check_cluster_diff()
   #check_diff_rid(3559300410)

   #show_similarity(296957707, 1700002725)

   #show_cluster(2495556309)
   #show_cluster_node(3559300410)
   #check_chapter_title_clean()