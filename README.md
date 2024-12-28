**AI个人传记**
================

**注意事项**
------------

*   **zhipu web_search_pro**: 内容质量差，JSON 格式混乱复杂，不建议使用。--2024-12-20
*   **tongyi-workflow**：模型多模态，但是速度较慢，之后等到用户体验再说。先简化步骤MVP --2024-12-23

**项目目标**
------------

*   使用 LLM OpenAI API 统一模型，集成 QWEN 和 OpenAI-4o-Mini 。
*   实现流程更清晰的个人传记编写系统，分为两大部分：(解除耦合，先保存采集数据，再进行编写)
    *   **收集资料**：采集音频与文字稿，整理并数字化保存。
    *   **传记编写内容**：完全体，包括 Agent Writer、Critic、Scorer 等等。


**TODO**
------

*   实现数据收集部分的数字化保存功能。
*   集成 LLM OpenAI API 统一模型，实现传记编写内容部分的自动化。
*   完善项目结构，确保代码清晰易读。

**项目日志**
------
- [x] 12/26，在图书馆四楼两人将项目上线营销 体验：http://150.109.118.248:5000/
- [x] 12/26，修改提示词，让AI传记的文风更优美，采用林语堂或者归拢的风格。 
- [x] 12/28，谢苹果使用cursor修改了代码，增加了加载动画，优化了用户体验。

**产品挑刺**
------
- [ ] 谢苹果在手机端使用，发现对于app用户上传音频文件极度不友好，彷佛故意不想要让用户上传音频文件一样。
- [x] 生成的文本内容呈现要么裸文本要么渲染后的富文本，不要任何markdown
- [ ] 提示词可以修改，支持生成多种文风譬如说文言文的个人传记
- [ ] 服务器后续升级，响应速度更快一些
- [ ] 【佐洛天痕】老哥的建议1：在右边增加几个预设场景方便用户快速上手。甚至可以不走api直接设置好方便上手
- [ ] 【佐洛天痕】老哥的建议2：网页加个反馈渠道
- [ ] 【佐洛天痕】老哥的建议3：后续可以加校验机制
- [ ] 【医生建议】生成的内容更多同时可以支持精美打印成册子

**贡献者**
----------

*   [bbbfishhh]：v1
   

**许可证**
----------

*   本项目使用 [MIT 许可证](https://opensource.org/licenses/MIT)。
