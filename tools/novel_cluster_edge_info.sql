create table `novel_cluster_edge_info` (
    `id` bigint(20) unsigned not null auto_increment,
    `dir_id_i` bigint(20) unsigned not null,
    `dir_id_j` bigint(20) unsigned not null,
    `similarity` int(10) not null,
    `update_time` timestamp(12) not null default current_timestamp on update current_timestamp,
    primary key (`id`),
    unique key `dir_id` (`dir_id_i`, `dir_id_j`),
    key `similarity` (`similarity`)
) engine=InnoDB default charset=gbk;
create table novel_cluster_edge_info0 like novel_edge_chapter_info;
create table novel_cluster_edge_info1 like novel_edge_chapter_info;
create table novel_cluster_edge_info2 like novel_edge_chapter_info;
create table novel_cluster_edge_info3 like novel_edge_chapter_info;
create table novel_cluster_edge_info4 like novel_edge_chapter_info;
create table novel_cluster_edge_info5 like novel_edge_chapter_info;
create table novel_cluster_edge_info6 like novel_edge_chapter_info;
create table novel_cluster_edge_info7 like novel_edge_chapter_info;
create table novel_cluster_edge_info8 like novel_edge_chapter_info;
create table novel_cluster_edge_info9 like novel_edge_chapter_info;
create table novel_cluster_edge_info10 like novel_edge_chapter_info;
create table novel_cluster_edge_info11 like novel_edge_chapter_info;
create table novel_cluster_edge_info12 like novel_edge_chapter_info;
create table novel_cluster_edge_info13 like novel_edge_chapter_info;
create table novel_cluster_edge_info14 like novel_edge_chapter_info;
create table novel_cluster_edge_info15 like novel_edge_chapter_info;
create table novel_cluster_edge_info16 like novel_edge_chapter_info;
create table novel_cluster_edge_info17 like novel_edge_chapter_info;
create table novel_cluster_edge_info18 like novel_edge_chapter_info;
create table novel_cluster_edge_info19 like novel_edge_chapter_info;
create table novel_cluster_edge_info20 like novel_edge_chapter_info;
create table novel_cluster_edge_info21 like novel_edge_chapter_info;
create table novel_cluster_edge_info22 like novel_edge_chapter_info;
create table novel_cluster_edge_info23 like novel_edge_chapter_info;
create table novel_cluster_edge_info24 like novel_edge_chapter_info;
create table novel_cluster_edge_info25 like novel_edge_chapter_info;
create table novel_cluster_edge_info26 like novel_edge_chapter_info;
create table novel_cluster_edge_info27 like novel_edge_chapter_info;
create table novel_cluster_edge_info28 like novel_edge_chapter_info;
create table novel_cluster_edge_info29 like novel_edge_chapter_info;
create table novel_cluster_edge_info30 like novel_edge_chapter_info;
create table novel_cluster_edge_info31 like novel_edge_chapter_info;
create table novel_cluster_edge_info32 like novel_edge_chapter_info;
create table novel_cluster_edge_info33 like novel_edge_chapter_info;
create table novel_cluster_edge_info34 like novel_edge_chapter_info;
create table novel_cluster_edge_info35 like novel_edge_chapter_info;
create table novel_cluster_edge_info36 like novel_edge_chapter_info;
create table novel_cluster_edge_info37 like novel_edge_chapter_info;
create table novel_cluster_edge_info38 like novel_edge_chapter_info;
create table novel_cluster_edge_info39 like novel_edge_chapter_info;
create table novel_cluster_edge_info40 like novel_edge_chapter_info;
create table novel_cluster_edge_info41 like novel_edge_chapter_info;
create table novel_cluster_edge_info42 like novel_edge_chapter_info;
create table novel_cluster_edge_info43 like novel_edge_chapter_info;
create table novel_cluster_edge_info44 like novel_edge_chapter_info;
create table novel_cluster_edge_info45 like novel_edge_chapter_info;
create table novel_cluster_edge_info46 like novel_edge_chapter_info;
create table novel_cluster_edge_info47 like novel_edge_chapter_info;
create table novel_cluster_edge_info48 like novel_edge_chapter_info;
create table novel_cluster_edge_info49 like novel_edge_chapter_info;
create table novel_cluster_edge_info50 like novel_edge_chapter_info;
create table novel_cluster_edge_info51 like novel_edge_chapter_info;
create table novel_cluster_edge_info52 like novel_edge_chapter_info;
create table novel_cluster_edge_info53 like novel_edge_chapter_info;
create table novel_cluster_edge_info54 like novel_edge_chapter_info;
create table novel_cluster_edge_info55 like novel_edge_chapter_info;
create table novel_cluster_edge_info56 like novel_edge_chapter_info;
create table novel_cluster_edge_info57 like novel_edge_chapter_info;
create table novel_cluster_edge_info58 like novel_edge_chapter_info;
create table novel_cluster_edge_info59 like novel_edge_chapter_info;
create table novel_cluster_edge_info60 like novel_edge_chapter_info;
create table novel_cluster_edge_info61 like novel_edge_chapter_info;
create table novel_cluster_edge_info62 like novel_edge_chapter_info;
create table novel_cluster_edge_info63 like novel_edge_chapter_info;
create table novel_cluster_edge_info64 like novel_edge_chapter_info;
create table novel_cluster_edge_info65 like novel_edge_chapter_info;
create table novel_cluster_edge_info66 like novel_edge_chapter_info;
create table novel_cluster_edge_info67 like novel_edge_chapter_info;
create table novel_cluster_edge_info68 like novel_edge_chapter_info;
create table novel_cluster_edge_info69 like novel_edge_chapter_info;
create table novel_cluster_edge_info70 like novel_edge_chapter_info;
create table novel_cluster_edge_info71 like novel_edge_chapter_info;
create table novel_cluster_edge_info72 like novel_edge_chapter_info;
create table novel_cluster_edge_info73 like novel_edge_chapter_info;
create table novel_cluster_edge_info74 like novel_edge_chapter_info;
create table novel_cluster_edge_info75 like novel_edge_chapter_info;
create table novel_cluster_edge_info76 like novel_edge_chapter_info;
create table novel_cluster_edge_info77 like novel_edge_chapter_info;
create table novel_cluster_edge_info78 like novel_edge_chapter_info;
create table novel_cluster_edge_info79 like novel_edge_chapter_info;
create table novel_cluster_edge_info80 like novel_edge_chapter_info;
create table novel_cluster_edge_info81 like novel_edge_chapter_info;
create table novel_cluster_edge_info82 like novel_edge_chapter_info;
create table novel_cluster_edge_info83 like novel_edge_chapter_info;
create table novel_cluster_edge_info84 like novel_edge_chapter_info;
create table novel_cluster_edge_info85 like novel_edge_chapter_info;
create table novel_cluster_edge_info86 like novel_edge_chapter_info;
create table novel_cluster_edge_info87 like novel_edge_chapter_info;
create table novel_cluster_edge_info88 like novel_edge_chapter_info;
create table novel_cluster_edge_info89 like novel_edge_chapter_info;
create table novel_cluster_edge_info90 like novel_edge_chapter_info;
create table novel_cluster_edge_info91 like novel_edge_chapter_info;
create table novel_cluster_edge_info92 like novel_edge_chapter_info;
create table novel_cluster_edge_info93 like novel_edge_chapter_info;
create table novel_cluster_edge_info94 like novel_edge_chapter_info;
create table novel_cluster_edge_info95 like novel_edge_chapter_info;
create table novel_cluster_edge_info96 like novel_edge_chapter_info;
create table novel_cluster_edge_info97 like novel_edge_chapter_info;
create table novel_cluster_edge_info98 like novel_edge_chapter_info;
create table novel_cluster_edge_info99 like novel_edge_chapter_info;
create table novel_cluster_edge_info100 like novel_edge_chapter_info;
create table novel_cluster_edge_info101 like novel_edge_chapter_info;
create table novel_cluster_edge_info102 like novel_edge_chapter_info;
create table novel_cluster_edge_info103 like novel_edge_chapter_info;
create table novel_cluster_edge_info104 like novel_edge_chapter_info;
create table novel_cluster_edge_info105 like novel_edge_chapter_info;
create table novel_cluster_edge_info106 like novel_edge_chapter_info;
create table novel_cluster_edge_info107 like novel_edge_chapter_info;
create table novel_cluster_edge_info108 like novel_edge_chapter_info;
create table novel_cluster_edge_info109 like novel_edge_chapter_info;
create table novel_cluster_edge_info110 like novel_edge_chapter_info;
create table novel_cluster_edge_info111 like novel_edge_chapter_info;
create table novel_cluster_edge_info112 like novel_edge_chapter_info;
create table novel_cluster_edge_info113 like novel_edge_chapter_info;
create table novel_cluster_edge_info114 like novel_edge_chapter_info;
create table novel_cluster_edge_info115 like novel_edge_chapter_info;
create table novel_cluster_edge_info116 like novel_edge_chapter_info;
create table novel_cluster_edge_info117 like novel_edge_chapter_info;
create table novel_cluster_edge_info118 like novel_edge_chapter_info;
create table novel_cluster_edge_info119 like novel_edge_chapter_info;
create table novel_cluster_edge_info120 like novel_edge_chapter_info;
create table novel_cluster_edge_info121 like novel_edge_chapter_info;
create table novel_cluster_edge_info122 like novel_edge_chapter_info;
create table novel_cluster_edge_info123 like novel_edge_chapter_info;
create table novel_cluster_edge_info124 like novel_edge_chapter_info;
create table novel_cluster_edge_info125 like novel_edge_chapter_info;
create table novel_cluster_edge_info126 like novel_edge_chapter_info;
create table novel_cluster_edge_info127 like novel_edge_chapter_info;
create table novel_cluster_edge_info128 like novel_edge_chapter_info;
create table novel_cluster_edge_info129 like novel_edge_chapter_info;
create table novel_cluster_edge_info130 like novel_edge_chapter_info;
create table novel_cluster_edge_info131 like novel_edge_chapter_info;
create table novel_cluster_edge_info132 like novel_edge_chapter_info;
create table novel_cluster_edge_info133 like novel_edge_chapter_info;
create table novel_cluster_edge_info134 like novel_edge_chapter_info;
create table novel_cluster_edge_info135 like novel_edge_chapter_info;
create table novel_cluster_edge_info136 like novel_edge_chapter_info;
create table novel_cluster_edge_info137 like novel_edge_chapter_info;
create table novel_cluster_edge_info138 like novel_edge_chapter_info;
create table novel_cluster_edge_info139 like novel_edge_chapter_info;
create table novel_cluster_edge_info140 like novel_edge_chapter_info;
create table novel_cluster_edge_info141 like novel_edge_chapter_info;
create table novel_cluster_edge_info142 like novel_edge_chapter_info;
create table novel_cluster_edge_info143 like novel_edge_chapter_info;
create table novel_cluster_edge_info144 like novel_edge_chapter_info;
create table novel_cluster_edge_info145 like novel_edge_chapter_info;
create table novel_cluster_edge_info146 like novel_edge_chapter_info;
create table novel_cluster_edge_info147 like novel_edge_chapter_info;
create table novel_cluster_edge_info148 like novel_edge_chapter_info;
create table novel_cluster_edge_info149 like novel_edge_chapter_info;
create table novel_cluster_edge_info150 like novel_edge_chapter_info;
create table novel_cluster_edge_info151 like novel_edge_chapter_info;
create table novel_cluster_edge_info152 like novel_edge_chapter_info;
create table novel_cluster_edge_info153 like novel_edge_chapter_info;
create table novel_cluster_edge_info154 like novel_edge_chapter_info;
create table novel_cluster_edge_info155 like novel_edge_chapter_info;
create table novel_cluster_edge_info156 like novel_edge_chapter_info;
create table novel_cluster_edge_info157 like novel_edge_chapter_info;
create table novel_cluster_edge_info158 like novel_edge_chapter_info;
create table novel_cluster_edge_info159 like novel_edge_chapter_info;
create table novel_cluster_edge_info160 like novel_edge_chapter_info;
create table novel_cluster_edge_info161 like novel_edge_chapter_info;
create table novel_cluster_edge_info162 like novel_edge_chapter_info;
create table novel_cluster_edge_info163 like novel_edge_chapter_info;
create table novel_cluster_edge_info164 like novel_edge_chapter_info;
create table novel_cluster_edge_info165 like novel_edge_chapter_info;
create table novel_cluster_edge_info166 like novel_edge_chapter_info;
create table novel_cluster_edge_info167 like novel_edge_chapter_info;
create table novel_cluster_edge_info168 like novel_edge_chapter_info;
create table novel_cluster_edge_info169 like novel_edge_chapter_info;
create table novel_cluster_edge_info170 like novel_edge_chapter_info;
create table novel_cluster_edge_info171 like novel_edge_chapter_info;
create table novel_cluster_edge_info172 like novel_edge_chapter_info;
create table novel_cluster_edge_info173 like novel_edge_chapter_info;
create table novel_cluster_edge_info174 like novel_edge_chapter_info;
create table novel_cluster_edge_info175 like novel_edge_chapter_info;
create table novel_cluster_edge_info176 like novel_edge_chapter_info;
create table novel_cluster_edge_info177 like novel_edge_chapter_info;
create table novel_cluster_edge_info178 like novel_edge_chapter_info;
create table novel_cluster_edge_info179 like novel_edge_chapter_info;
create table novel_cluster_edge_info180 like novel_edge_chapter_info;
create table novel_cluster_edge_info181 like novel_edge_chapter_info;
create table novel_cluster_edge_info182 like novel_edge_chapter_info;
create table novel_cluster_edge_info183 like novel_edge_chapter_info;
create table novel_cluster_edge_info184 like novel_edge_chapter_info;
create table novel_cluster_edge_info185 like novel_edge_chapter_info;
create table novel_cluster_edge_info186 like novel_edge_chapter_info;
create table novel_cluster_edge_info187 like novel_edge_chapter_info;
create table novel_cluster_edge_info188 like novel_edge_chapter_info;
create table novel_cluster_edge_info189 like novel_edge_chapter_info;
create table novel_cluster_edge_info190 like novel_edge_chapter_info;
create table novel_cluster_edge_info191 like novel_edge_chapter_info;
create table novel_cluster_edge_info192 like novel_edge_chapter_info;
create table novel_cluster_edge_info193 like novel_edge_chapter_info;
create table novel_cluster_edge_info194 like novel_edge_chapter_info;
create table novel_cluster_edge_info195 like novel_edge_chapter_info;
create table novel_cluster_edge_info196 like novel_edge_chapter_info;
create table novel_cluster_edge_info197 like novel_edge_chapter_info;
create table novel_cluster_edge_info198 like novel_edge_chapter_info;
create table novel_cluster_edge_info199 like novel_edge_chapter_info;
create table novel_cluster_edge_info200 like novel_edge_chapter_info;
create table novel_cluster_edge_info201 like novel_edge_chapter_info;
create table novel_cluster_edge_info202 like novel_edge_chapter_info;
create table novel_cluster_edge_info203 like novel_edge_chapter_info;
create table novel_cluster_edge_info204 like novel_edge_chapter_info;
create table novel_cluster_edge_info205 like novel_edge_chapter_info;
create table novel_cluster_edge_info206 like novel_edge_chapter_info;
create table novel_cluster_edge_info207 like novel_edge_chapter_info;
create table novel_cluster_edge_info208 like novel_edge_chapter_info;
create table novel_cluster_edge_info209 like novel_edge_chapter_info;
create table novel_cluster_edge_info210 like novel_edge_chapter_info;
create table novel_cluster_edge_info211 like novel_edge_chapter_info;
create table novel_cluster_edge_info212 like novel_edge_chapter_info;
create table novel_cluster_edge_info213 like novel_edge_chapter_info;
create table novel_cluster_edge_info214 like novel_edge_chapter_info;
create table novel_cluster_edge_info215 like novel_edge_chapter_info;
create table novel_cluster_edge_info216 like novel_edge_chapter_info;
create table novel_cluster_edge_info217 like novel_edge_chapter_info;
create table novel_cluster_edge_info218 like novel_edge_chapter_info;
create table novel_cluster_edge_info219 like novel_edge_chapter_info;
create table novel_cluster_edge_info220 like novel_edge_chapter_info;
create table novel_cluster_edge_info221 like novel_edge_chapter_info;
create table novel_cluster_edge_info222 like novel_edge_chapter_info;
create table novel_cluster_edge_info223 like novel_edge_chapter_info;
create table novel_cluster_edge_info224 like novel_edge_chapter_info;
create table novel_cluster_edge_info225 like novel_edge_chapter_info;
create table novel_cluster_edge_info226 like novel_edge_chapter_info;
create table novel_cluster_edge_info227 like novel_edge_chapter_info;
create table novel_cluster_edge_info228 like novel_edge_chapter_info;
create table novel_cluster_edge_info229 like novel_edge_chapter_info;
create table novel_cluster_edge_info230 like novel_edge_chapter_info;
create table novel_cluster_edge_info231 like novel_edge_chapter_info;
create table novel_cluster_edge_info232 like novel_edge_chapter_info;
create table novel_cluster_edge_info233 like novel_edge_chapter_info;
create table novel_cluster_edge_info234 like novel_edge_chapter_info;
create table novel_cluster_edge_info235 like novel_edge_chapter_info;
create table novel_cluster_edge_info236 like novel_edge_chapter_info;
create table novel_cluster_edge_info237 like novel_edge_chapter_info;
create table novel_cluster_edge_info238 like novel_edge_chapter_info;
create table novel_cluster_edge_info239 like novel_edge_chapter_info;
create table novel_cluster_edge_info240 like novel_edge_chapter_info;
create table novel_cluster_edge_info241 like novel_edge_chapter_info;
create table novel_cluster_edge_info242 like novel_edge_chapter_info;
create table novel_cluster_edge_info243 like novel_edge_chapter_info;
create table novel_cluster_edge_info244 like novel_edge_chapter_info;
create table novel_cluster_edge_info245 like novel_edge_chapter_info;
create table novel_cluster_edge_info246 like novel_edge_chapter_info;
create table novel_cluster_edge_info247 like novel_edge_chapter_info;
create table novel_cluster_edge_info248 like novel_edge_chapter_info;
create table novel_cluster_edge_info249 like novel_edge_chapter_info;
create table novel_cluster_edge_info250 like novel_edge_chapter_info;
create table novel_cluster_edge_info251 like novel_edge_chapter_info;
create table novel_cluster_edge_info252 like novel_edge_chapter_info;
create table novel_cluster_edge_info253 like novel_edge_chapter_info;
create table novel_cluster_edge_info254 like novel_edge_chapter_info;
create table novel_cluster_edge_info255 like novel_edge_chapter_info;