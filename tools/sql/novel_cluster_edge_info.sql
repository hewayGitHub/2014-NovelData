drop table if exists novel_cluster_edge_info;
create table `novel_cluster_edge_info` (
    `id` bigint(20) unsigned not null auto_increment,
    `gid_x` bigint(20) unsigned not null,
    `gid_y` bigint(20) unsigned not null,
    `similarity` int(10) not null,
    `update_time` timestamp not null default current_timestamp on update current_timestamp,
    primary key (`id`),
    unique key `gid_x` (`gid_x`, `gid_y`),
    key `gid_y` (`gid_y`, `gid_x`),
    key `similarity` (`similarity`)
) engine=InnoDB default charset=gbk;
