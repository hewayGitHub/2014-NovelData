drop table if exists novel_cluster_dir_rid_info;
create table `novel_cluster_rid_dir_info` (
    `id` bigint(20) unsigned not null auto_increment,
    `dir_id` bigint(20) unsigned not null,
    `rid` bigint(20) unsigned not null,
    `update_time` timestamp(12) not null default current_timestamp on update current_timestamp,
    primary key (`id`),
    unique key `dir_id` (`dir_id`),
) engine=InnoDB default charset=gbk;
