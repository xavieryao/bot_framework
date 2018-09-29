agent：一个bot，`entity`、`intent`和`workflow`的集合，可指定callback

entity：预定义或用户定义的entity，用于 NER。

intent：树形结构定义的 intent

workflow：一个处理流程。当 context 和 intent 都满足时调用。引导用户填充缺失参数，回复预定义的内容或调用 callback。

context：一个 key-value pair，保存当前已识别的各参数，在指定 turn 之后过期。workflow 结束时可创建新 context。

