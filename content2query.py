# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
import os
import json

def Content2BackgroundQuery(content_extracted):
    """
    从对话内容中提取时间线信息并返回JSON格式的结果
    
    Args:
        content_extracted (str): 对话内容文本
    
    Returns:
        list: 包含时间线信息的JSON格式列表
    """
    client = OpenAI(api_key=os.getenv("deepseek_api_key"), base_url="https://api.deepseek.com")
    
    # history_prompt = f"""对话内容：{content_extracted}
    # 请根据以下采访人物传记文本，从中提取出主要关键词以及对应的时间，并返回以 JSON 格式列出的结果，关键词内容为
    # 社会背景和历史事件：("history_background"）和 猜测时间点("timeline")，格式为'history_background':"",'timeline':"" """
    history_prompt = f"""对话内容：{content_extracted}
    请根据上面的采访人物传记文本，从中提取出重要的社会历史事件背景（如政策、经济危机、经济发展、重大事件等），忽略日常生活中的琐事（如旅游、个人生活等），并返回以下格式的结果：
    [
        {{
        "history_background": "",
        "time&location": ""
        }}
    ]"""    
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个采访内容梳理大师,根据所给内容，梳理时间线"},
                {"role": "user", "content": history_prompt},
            ],
            stream=False
        )

        data = response.choices[0].message.content
        clean_data = data.replace("```json", "").replace("```", "").strip()

        if clean_data:
            return json.loads(clean_data)
        else:
            return []
            
    except Exception as e:
        print(f"处理时出现错误: {str(e)}")
        return []

# 使用示例
if __name__ == "__main__":
    content = "\n\n哦，到那个煤矿去玩呢。\n\n对，徐州很多煤矿，现在矿都挖满，挖挖完了。\n\n对，现在都搞新能源了。\n\n京都，京都多少年来了，是是是呃几个朋友一起去玩去的。\n\n哦。\n\n他们家有个亲戚嘛，那个时候还小嘛，我就骂人，又没结婚没干嘛的，说走就走。\n\n哦，你你你爱说走就走旅行。\n\n嗯，对啊，几个朋友嘛，玩起来，他们是，因为我们家亲戚在那个徐州，我们家就去去玩嘛，那时候我们家在镇上面算有钱的人家。\n\n哦。\n\n只要有钱就OK了呀，凌晨宣布。\n\n哦，再也打不开。\n\n嗯，二十多岁。\n\n会的。\n\n二十出头一点点吧，那时��。\n\n我我前两天在家呆着，家里管我太严，我不在家，回去十五天，本来练车嘞，我看在家不能待下去了，必须得离开。\n\n我直接说学校有事，直接直接提着书，背着电脑，直接出发去徐州宾馆住了一晚上，看个电影，第二天我就打车去宿迁，坐高铁，三十分钟，宿迁，去刘强东老家看了看，打出租车去刘强东老家看看，然后呢，送我到高铁，本来想去淮安玩玩，感觉淮安，哎呀，没啥好玩的，直接坐上海，坐地铁，坐高铁来上海了，当天。\n\n我女儿出去玩呢，我跟她走呢，还不大行，她还蛮喜欢跟她老子走的。\n\n她老子走路呢，她老子喜欢历史，跟刘强东。\n\n历史，我也喜欢历史。\n\n我家东西，我老公，我这个通古知今。\n\n我女儿就喜欢跟着她爸走，为什么，一边走两个人，一边讲解给他听。\n\n他就给他讲这个，哦，行行都知道，就像我们上。\n\n我女儿到这个，呃，里面做这个志愿者，夏天的时候。\n\n学校里面问她，你反正出去吧，行，就帮我讲，出去吧。\n\n她后来，哎，她没想到这个出去还有钱呢。\n\n她不是，做了三个朝野斗争会，呃，她来帮我们学他们，真的，我这个里面怎么多了两百多块钱。\n\n这你哪来的，你自己不知道吗？\n\n后来一查，哦，学校发给我的。\n\n后来，恐怕她将会修点坏。\n\n哎，你不是做志愿者吗？\n\n对，哎，你这个都乱好了，做志愿者还有钱呢。\n\n哦，做志愿者还有钱。\n\n哦，把女儿秀他们，那韩国。\n\n嗯，还会发生类似的模仿。\n\n到意大利会去。\n\n意大利会，哦，多少钱，到外面听清楚多少钱。\n\n不要钱。\n\n哦，做志愿者。\n\n哦，我我看了那个，好像有的。\n\n他这个是学校。\n\n哦，我知道，我知道。\n\n我又把他，本来就是跟你讲的嘛，弄的这个出版社出来。\n\n他是一分钱没有。\n\n就是说，他可以给你开个证明，就上面刻上图章，你在外面一样的。\n\n后来进这个，后来老师问了他，呃，就问你出去了没有，他说，哎哟，我们学校这里，就是他，他每年都给学校分派额度的。\n\n多少人，多少人，你做什么的。\n\n他这个，哎哟，你们家靠在那边的挺近的，你没事的吧，去上好。"""
    queries = Content2BackgroundQuery(content)
    print(queries)