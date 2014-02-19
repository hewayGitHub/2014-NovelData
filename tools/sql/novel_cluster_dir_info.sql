drop table if exists novel_cluster_dir_info;
create table `novel_cluster_dir_info` (
    `id` bigint(20) unsigned not null auto_increment,
    `site_id` int(10) not null,
    `site` varchar(128) not null,
    `site_status` tinyint(3) not null,
    `dir_id` bigint(20) unsigned not null,
    `dir_url` varchar(512) not null,
    `gid` bigint(20) unsigned not null,
    `rid` bigint(20) unsigned not null,
    `book_name` varchar(128) not null,
    `pen_name` varchar(128) not null,
    `chapter_count` int(10) not null,
    `valid_chapter_count` int(10) not null,
    `chapter_word_sum` int(10) not null,
    `update_time` timestamp(12) not null default current_timestamp on update current_timestamp,
    primary key (`id`),
    unique key `dir_id` (`dir_id`),
    key `gid` (`gid`),
    key `rid` (`rid`),
    key `book_name` (`book_name`),
    key `pen_name` (`pen_name`),
    key `update_time` (`update_time`)
) engine=InnoDB default charset=gbk;
