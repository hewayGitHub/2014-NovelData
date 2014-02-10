create table `novel_cluster_chapter_info` (
    `id` bigint(20) unsigned not null auto_increment,
    `dir_id` bigint(20) unsigned not null,
    `chapter_id` bigint(20) unsigned not null,
    `chapter_url` varchar(512) not null,
    `chapter_title` varchar(128) not null,
    `raw_chapter_title` varchar(128) not null,
    `chapter_sort` int(10) not null,
    `chapter_status` tinyint(3) not null,
    `word_sum` int(10) not null,
    `update_time` timestamp(12) not null default current_timestamp on update current_timestamp,
    primary key (`id`),
    unique key `dir_id` (`dir_id`, `chapter_sort`),
    key `chapter_id` (`chapter_id`)
) engine=InnoDB default charset=gbk;
create table novel_cluster_chapter_info0 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info1 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info2 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info3 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info4 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info5 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info6 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info7 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info8 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info9 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info10 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info11 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info12 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info13 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info14 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info15 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info16 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info17 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info18 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info19 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info20 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info21 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info22 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info23 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info24 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info25 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info26 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info27 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info28 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info29 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info30 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info31 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info32 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info33 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info34 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info35 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info36 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info37 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info38 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info39 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info40 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info41 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info42 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info43 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info44 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info45 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info46 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info47 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info48 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info49 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info50 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info51 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info52 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info53 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info54 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info55 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info56 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info57 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info58 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info59 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info60 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info61 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info62 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info63 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info64 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info65 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info66 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info67 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info68 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info69 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info70 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info71 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info72 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info73 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info74 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info75 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info76 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info77 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info78 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info79 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info80 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info81 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info82 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info83 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info84 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info85 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info86 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info87 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info88 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info89 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info90 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info91 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info92 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info93 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info94 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info95 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info96 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info97 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info98 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info99 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info100 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info101 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info102 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info103 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info104 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info105 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info106 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info107 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info108 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info109 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info110 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info111 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info112 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info113 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info114 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info115 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info116 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info117 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info118 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info119 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info120 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info121 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info122 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info123 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info124 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info125 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info126 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info127 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info128 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info129 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info130 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info131 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info132 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info133 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info134 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info135 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info136 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info137 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info138 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info139 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info140 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info141 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info142 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info143 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info144 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info145 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info146 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info147 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info148 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info149 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info150 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info151 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info152 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info153 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info154 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info155 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info156 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info157 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info158 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info159 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info160 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info161 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info162 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info163 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info164 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info165 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info166 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info167 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info168 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info169 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info170 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info171 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info172 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info173 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info174 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info175 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info176 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info177 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info178 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info179 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info180 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info181 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info182 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info183 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info184 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info185 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info186 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info187 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info188 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info189 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info190 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info191 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info192 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info193 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info194 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info195 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info196 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info197 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info198 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info199 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info200 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info201 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info202 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info203 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info204 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info205 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info206 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info207 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info208 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info209 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info210 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info211 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info212 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info213 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info214 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info215 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info216 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info217 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info218 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info219 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info220 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info221 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info222 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info223 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info224 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info225 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info226 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info227 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info228 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info229 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info230 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info231 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info232 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info233 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info234 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info235 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info236 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info237 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info238 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info239 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info240 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info241 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info242 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info243 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info244 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info245 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info246 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info247 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info248 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info249 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info250 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info251 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info252 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info253 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info254 like novel_cluster_chapter_info;
create table novel_cluster_chapter_info255 like novel_cluster_chapter_info;