NovelData
=========

The python scripts used for processing novel data.

Not updated any more because of regularites of my company

#第二期正文优化

@(02. 行动)

###前期调研：
通过前期调研，发现杂质具有如下特点：

1. 从**杂质的来源**，分为站点级别的杂质和其它杂质。  
    - 站点级别的杂质主要包含由站点添加的广告（宣传站点、推荐其它书），以及站点为了防止小说被爬取再次利用添加的隐藏的重复正文和杂质、将某些汉字转换成拼音或图片等。  
    - 其它杂质，爬取时带入的杂质（比如&quato;被转义的字符、下一章和目录等导航、正文开头的章节标题）以及因为盗版站点输入正文时导致个别字和标点的缺失、错误等。

2. 从**句子的角度**，杂质主要分为整段杂质、整句杂质和句子的一部分是杂质。

说明：作者的话不认为是杂质，是否去除不做强制要求。

###优化目标：
正文去杂需要在不会去除正确正文的前提下，尽可能多地去除杂质：
- **准确性**：保证不会去除章节正确的正文，保证准确率接近100%。
- **覆盖面**：对于固化的小说，一本书（rid）的一个章节（cid）有且只有一份唯一的资源，要保证该资源的杂质含量低，基本不影响用户体验。
- **时效性**：正文去杂对时效性没有特别要求，由于去杂策略较复杂，需保证一定的运行效率。
- **可修复**：如果出现bad case，为了便于恢复，被删除或替换的杂质句实际上只是被添加了隐藏标签`<span style="display:none"></span>`。

###整体设计
- 通过章节选取，尽可能选择包含杂质少、无正文缺失的正文作为最优正文，从而保证正文的完整性和可用性。
- 主要通过段落对齐和句子对齐识别整段杂质和整句杂质，然后利用对齐的结果，并结合分类模型，进行去杂。
- 对于上述策略无法很好去除的杂质，通过正则表达式、字符串匹配等强规则去除。

###排期
排期：具体排期依赖于样本标注杂质的质量，可能需要迭代或延期。
* 第一期，通过规则去除站点级别的杂质，然后优化选取，选择杂质最少的正文。
* 第二期，考虑句子对齐，并通过杂质句的上下文和分类模型，去除其它整句杂质。【已和第一期合并】
* 第三期，结合句子对齐，解决句子的一部分为杂质的情况。

###外包样本说明
按站点标注杂质

**抽样**：【注意，很多正文里面有换行，需要先替换掉】
* 从top10W中抽取1000本书，其中从1W抽取100本，从剩下的9W中抽取900本
* 从每本书中抽取20章，从最后100或20%章抽取10章，其它从前面抽取10章
* 写入不同站点对应的文件。由于pageDB不稳定和某些章节未固化，样本总计15036章，对应124532个候选正文，共191个站点。
* 第一期标注，从1000*20个章节随机抽取10章，将其所有的候选章节都加入样本集，并基本保证每个站点随机抽取章节数不少于15。共2822个候选章节。

**要求**：
* 连续多个句子是可以作为一个杂质标注，但是如果有[分段]，请分开标注。
    * 请记住我们的网址)本书最新免费章节请访问。[分段]残月轩小说网http://www.30txt.org,千万本小说免费阅读请牢记我们的网站残月轩小说网http://www.30txt.org


**样本文件说明**：
以Tab分列，excel导入分隔符文本即可。分别是
rid     align_id     chapter_id     site_id     site_status     chapter_content

在其后添加两列：
杂质所在句子     杂质     是否在段首或段尾 是否是作者添加的杂质

###第一、二阶段评估
**样本说明**：
对外包样本中的15036个章节做候选聚类、章节选取、去杂，其中有8761个章节可能包含杂质，即8761/15036（58.3%）
故本次评估、测试量为可能包含杂质的8761章。

**样本样式说明**：
据集包括9个字段，分别是
rid	align_id	site_id	候选正文数	最大簇正文数	用于去杂的候选正文数	去杂后的正文内容	之前固化的正文内容	去杂之前的正文内容【未做html的过滤和处理，便于发现问题】

去杂后的正文中包含用【】标记起来的句子，其中，
* 【段落杂质】：整段都是杂质
* 【整句杂质】：整句都是杂质
* 【未处理杂质】：可能是句子的一部分是杂质。
* 【数字】和没有方括号标记的：就是其它情况。

**标注要求**：
如下情况需要标注：
* 对于标记为【整句杂质】和【整段杂质】的，如果不是杂质
* 对于标记为【未处理杂质】的，如果包含杂质
* 对于其它没有标记和【数字】的句子，如果是杂质，将整句标出

具体要求为：
* 标注时，句子前面的方括号部分也要拷贝进去
* 对于连续的几句都是bad case的情况，将它们作为一个bad case
* 作者添加的话，不认为是杂质，如果被作为杂质去除也不作为bad case

**测试、评估点**：
* 去掉的【段落杂质】和【整句杂质】是否有bad case
* 【未处理杂质】中是否包含杂质，具体包含哪些杂质？
* 是否有其它杂质没有去除？
* 挑选的最优正文是否有问题？

###RD自测和自评
通过分析log，统计边界情况，即最大簇候选章节过少、大部分段落无法对齐等
1. 最大簇候选章节的个数
1. 段落过滤的情况
1. 最优正文无法对齐段落数
1. 统计最优正文段落各个频数的情况，以及未对齐的段落比例等
1. 统计最优正文句子各个频数的情况，以及未对齐的段落比例等
1. 统计用我们的方法，有多少句子需要进一步用其它策略进行去杂
1. 去掉的整句杂质和整段杂质，用于补充样本，同时记录未处理杂质的情况，以及出现在少于1/2个候选中的句子

**评估结果**：
1. 评估样本中5.03%只有2个候选。考虑到取样来自于top 10W，所以必须针对无法利用段落对齐和句子对齐处理的正文制订站点级杂质过滤、正则表达式、和字符串匹配过滤等。
2. 生成评估集时，共过滤掉402章，过滤掉主要是如下三种情况。【将下界改为0.7和1/4分位点的较小值，将上界改为3/4分位点和1.2的较大值，可以保重过滤掉的段落少于1/2，如果过滤后少于3个候选，放弃过滤】
    - 候选正文只有一段
    - 候选正文中包含较多段落杂质，或分段错误
    - 候选正文中段落稍少，是正确正文
3. 段落对齐，大部分只有少量未对齐的段落，不修改段落对齐策略。
4. 
    

###具体步骤
先通过html过滤和处理，将所有候选正文处理为统一的格式，并过滤掉一些杂质。同时，通过正则表达式、字符串匹配等强规则过滤掉一些杂质。

章节选取从最大簇中选取最优正文后，通过段落对齐发现可能包含杂质的段落，然后针对这些段落，进行句子的对齐，从而判断是整句杂质或句子的一部分是杂质。

####初步去除杂质
这部分主要通过过滤和处理候选正文中的html标签来过滤一部分杂质，同时，通过正则表达式、字符串匹配等强规则过滤掉一些杂质。
- 处理正文，保证处理后所有正文格式一致，只包含<p>标签，即只有段落概念，用于后面进一步去除杂质。【此处返回的是一个段落的列表】
- 过滤掉候选正文中的隐藏内容，<script></script>标签之间的内容，去除超链接。
- 同时，通过正则表达式和字符串匹配等去除一些特殊杂质。

####初步过滤候选
正文去杂的需要做段落和句子的对齐，为了方面后文对齐，提高效率，需要先对最大簇中的所有候选进行初步的过滤【下文中最大簇的所有候选正文已经过该过滤】。
- 先根据汉字数，过滤汉字特别少的。汉字数少于平均80%的候选被过滤掉。
- 然后过滤段落数特别少或特别多的候选。按照段落少从小到大排序，然后取中间的1/2求平均数，过滤小于平均数80%和大于平均数120%的候选。

####定位和识别杂质
这部分主要用于定位杂质，即定位可能存在杂质的句子。
- 对于最大簇中所有的候选正文，进行段落的对齐。
- 对于未对齐的段落，进行句子的对齐。
- 对于未对齐的句子，做进一步的判断和识别。

**段落对齐的思路**：
因为一个正文中一个段落重复出现的概率很小，另外，因为是从上到下地对齐，所以段落对齐可以直接统计出现频次即可。
- 初步去除杂质后，每个候选正文对应一个段落列表，统计最优正文段落出现在其它候选中的频次。
- 对于频次为1的段落，即在其它候选中未找到匹配的段落，寻找上下最近的频次超过总候选1/2的段落A和B。
    - 如果其它候选中A和B对应段落之间不存在其它段落，认为A和B之间所有的段落都是整段杂质。
    - 否则，A和B之间的段落可能包含杂质，将它们切分成句子，做句子的对齐。

*注意*：两个段落匹配，表示两个段落的内容完全相同，包括标点符号、字母、数字、汉字等所有字符

**句子对齐的思路**：
由于网络小说中句子重复出现的概率可能比较大，如果按照段落对齐的方法，统计句子出现频次的时候，一方面可能杂质本身的频次并不是1，这样有些杂质就无法去掉，另外一方面，极有可能出现句子错误的对齐，从而无法正确地区分整句杂质和句子一部分是杂质的情况。

所以，考虑先做段落的对齐，然后只对未对齐的段落做句子的对齐，这可以减少句子重复的概率。

按照标点符号和空格切分句子，句子的内容分为两个部分，汉字、字母和数字作为句子的fmt_content，其后所有的标点符号作为句子的after_punctuation。

*具体步骤为*：
- 对于最优正文需要对齐的段落中的每一个句子，统计其在其它候选中出现的频次，在某个候选中重复出现视为一次出现，并检测该句子是否有重复出现的情况。重复出现包括两种情况：
    -  在最优正文需要对齐的段落中，某个句子重复出现。
    -  某个句子在其它某个候选正文中重复出现。
- 统计完全匹配的句子，完全匹配指某个句子在所有的候选中都出现了，并且没有重复。
- 对于没有完全匹配的句子，查找其上下最近的完全匹配的句子A和B，检查A和B之间是否有与之匹配的句子。
    - 如果句子没有重复，并且其在候选中对应的句子在完全匹配的句子之间，认为找到匹配，否则认为无法匹配。
    - 如果句子有重复，并且其在完全匹配的句子之间出现一次，认为找到匹配，否则如果没有出现或者出现多次，认为无法匹配。
- 对于频次为1的句子，即在其它候选中未找到匹配的句子，寻找上下最近的频次大于1的句子，C和D。
    - 如果其它候选中C和D对应的句子之间不存在其它句子，认为C和D之间句子都是整句杂质。
    - 否则，认为句子的一部分是杂质，需要做进一步的检测和处理。

*注意*：不同两个段落的匹配，句子的匹配指比较了句子的fmt_content。所以，如果两个段落只是标点符号等不同，段落对齐时它们无法匹配，句子对齐时，它们确实完全匹配的。

####去除杂质
去除杂质部分主要是整句杂质标点符号的处理。
- 对于整段杂质，直接去除杂质句，用`<span style="display:none"></span>`包裹，并添加对应的class属性，`whole_paragraph_remove`和`whole_sentence_remove`。
- 对于整句杂质，需要处理标点符号，直接用其它候选正文中对应标点符号进行替换。
- 对于句子的一部分是杂质的情况，对于正文缺失、标点缺失等情况，替换正文内容；对于包含杂质，为对应的杂质内容用`<span style="display:none"></span>`包裹，并添加class属性，`part_sentence_remove`，同样利用其它候选做标点的替换。

###句子的一部分是杂质
句子的一部分是杂质的情况比较复杂，需要做更加详尽的设计。因为站点间的正文存在拷贝现象，导致大多数的正文并不一定是正确的正文。
**调研结果**：
1. 错别字问题。比如最优中是'的'，其它是'得'。
2. 拼音问题，个别字被替换成拼音，或者个别字被替换成了某些符号，基本是句子之间相似度很高，然后其中某个不包含拼音，即字母或符号包含个数不同。
1. 字的缺失或者多余，个别的多了一个字或者少了一个字（更常见），但多数的并不一定是正确的正文。与上类似，但是各句的字母个数相同。
1. 多个句子因为缺少标点（也有可能多了标点符号、空格），在某些候选中变成一个句子。
1. 在附件重复出现的句子，被认为无法对齐的，需要进一步检测。
1. 句子的一部分是杂质。
1. 恰好所有候选对应的句子都是杂质。 

因为站点，那些freq大于1的不一定不包含杂质，但是主要是句中杂质，通常影响不是特别大。可暂时不作处理。

**策略**：
- 将需要检测的多个句子的`fmt_content`连接在一起。
- 如果，候选之间内容相等，应该是标点符号、空格等造成一个句子分成多个句子，选取包含标点符号多的句子【经调研发现，基本都是盗版站点输入时漏输入了标点符号】。
- 否则，从前到后比较句子的字。
    - 如果大部分匹配，然后它们的字数相等，认为可能是错别字问题，不做处理。
    - 如果大部分匹配，然后字数不相等，如果句子之间存在包含关系，用分类器检测最长的句子中未匹配的部分是否是杂质，如果是杂质，认为是句子的一部分是杂质，用较短的句子作为最终返回的句子。否则，认为可能是某些字缺失，返回最长的句子。如果句子之间不存在包含关系，比较包含的字母和符号的个数，如果不相同认为是拼音问题。
    - 如果大部分字都无法匹配，用分类器检测所有的句子，如果都是杂质，认为是杂质句，作为整句杂质去除。否则，不做任何处理。

###分类器描述
因为小说正文的内容比较复杂，没有合理的策略能够覆盖需要覆盖的正文。所以，分类器性能不稳定，某些正例或者句子一部分是杂质的情况，都可能造成误判，认为其是杂质。

因此，分类器的目标定义为，作为句子对齐的辅助，阈值设为0.1，即概率小于0.1表示其为杂质，对于杂质的召回率达到100%，即不会将杂质判断为非杂质。

**策略**：【以下策略是在句子未对齐的前提下实施的】
* 对于短句，尤其是一个中文字通常认为是正例。将连续的几个可能包含杂质的句子作为一个整体用分类器判断。如果字数还是小于3，如果全都是数字或者字母，直接作为杂质
* 对于字母和数字和标点符号等容易判断为正例，判断如果不包含中文字符，则直接当做杂质处理。
* 有一些负例训练集中没有，通过整句杂质补充训练集。
* 对于文章的章节标题等，需要更多的训练集，可以人工构造，所有第*章和第*节，作为负例的训练集

###其他说明：
####边界情况
因为段落对齐和句子对齐依赖于最大簇中候选正文的数量，所以对于如下情况，只做`初步去除杂质`。
- 如果最大簇中候选正文少于3个，不做段落对齐和句子对齐的去杂处理
- 如果最优正文中大部分的段落都无法对齐，放弃段落对齐和句子对齐

####逻辑需要注意的地方
- 某些句子的`fmt_content`为空，只有标点符号。比如段首的`“`。未做特殊处理。

####整句杂质的输出
- 获得的整句杂质会被输出，指定所在的site_id和杂质句，以及当前分类器判别的概率和结果等。
