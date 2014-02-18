drop table if exists novel_cluster_rid_dir;
create table `novel_cluster_rid_dir` (
    `id` bigint(20) unsigned not null auto_increment,
    `rid` bigint(20) unsigned not null,
    `dir_id` bigint(20) unsigned not null,
    `update_time` timestamp(12) not null default current_timestamp on update current_timestamp,
    primary key (`id`),
    unique key `rid` (`rid`, `dir_id`),
) engine=InnoDB default charset=gbk;
