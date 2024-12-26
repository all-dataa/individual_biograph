# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
import os
import json
from typing import Optional

def llmcontent_to_json(data):
    try:
        clean_data = data.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_data) if clean_data else []
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {str(e)}")
        return []
    except Exception as e:
        print(f"处理 JSON 时发生未知错误: {str(e)}")
        return []

def call_llm(
    system_prompt: str,
    user_prompt: str,
    api_key: str = os.getenv("deepseek_api_key"),
    base_url: str = "https://api.deepseek.com",
    model: str = "deepseek-chat",
    temperature: float = 1.5,  # Default temperature
    tools: list = None,        # Default to None, assuming no tools used
    top_p: float = 1.0        # Default top_p value
) -> Optional[str]:
    """
    Simple function to call OpenAI's API using their official client.
    
    Args:
        api_key: Your OpenAI API key
        user_prompt: The prompt to send to the model
        model: The model to use (default: deepseek-chat)
        system_prompt: Optional system prompt to guide model behavior
        temperature: Controls the randomness of the output (default: 0.7)
        tools: A list of tools that can be used by the model (default: None)
        top_p: Controls nucleus sampling, higher value means more randomness (default: 1.0)
    
    Returns:
        The model's response text
    """
    # Initialize the client
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    try:
        # Build the message payload
        message_data = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Add additional parameters if provided
        response = client.chat.completions.create(
            model=model,
            messages=message_data,
            temperature=temperature,   # Pass the temperature to the API
            top_p=top_p,               # Pass the top_p to the API
            tools=tools,               # Pass the tools if provided
            stream=False,
        )

        if not response.choices:
            print("API 返回的响应中没有选项")
            return None
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"调用 LLM API 时出错: {str(e)}")
        return None


def purify(origin_content, character_name):
    """
    Agent: purify 第一步提纯音频
    """
    system_prompt ="""
        你是一名经验丰富的编辑，负责改善文本的清晰度和简洁性。你的目标是通过以下步骤对输入文本进行优化：
        1. 去除冗余的词语和句子。
        2. 简化过于复杂的表达。
        3. 保持核心意思和关键信息。
        4. 改善文本的逻辑结构，使其更加流畅。
        5. 确保文本简洁易懂，适合用作传记内容。
        请专注于提升可读性，减少不必要的冗长，同时保留重要信息。输出应当结构清晰、简洁、符合传记写作的风格。
    """
    
    # user_prompt
    user_prompt = f"""
    以下是从音频记录中提取出的文本，描述了{character_name}的个人经历。请根据以下要求对文本进行优化：
        1. 去除重复和无意义的词语。
        2. 简化冗长复杂的句子。
        3. 保证逻辑结构流畅，内容清晰。
        4. 保留关键事件和重要细节，确保传记的完整性。
        5. 修改模糊或不清晰的表达，提高可读性和清晰度。
        输入文本：
        {origin_content}
        请输出优化后的版本，确保文本简洁、流畅、结构清晰，适合用作传记内容。
    """
        
    try:
        data = call_llm(system_prompt, user_prompt)
        if data is None:
            print("提纯过程失败：LLM 调用返回空结果")
            return None
            
        return data
    except Exception as e:
        print(f"提纯过程发生错误: {str(e)}")
        return None

def outliner(revised_content):
    """
    Agent: outliner 第二部根据文本写大纲
    """
    
    system_prompt = """
    你是一名经验丰富的编辑，擅长根据文本生成逻辑清晰的传记大纲。你的目标是根据输入的文本内容生成一份传记大纲。大纲应包含以下部分：
    1. **引言**：简短介绍人物的背景信息，概括性地说明传记的主题。
    2. **关键生活事件**：列出人物的主要经历和转折点，按时间顺序或主题进行排列。每个事件应简洁明了，突出人物的成长和变化。
    3. **重要成就**：提炼人物的主要成就或重要贡献。
    4. **总结与反思**：概述人物的生活经验，可能包括对人生的总结或未来展望。
    大纲应简洁、逻辑清晰，并且能够为后续的传记撰写提供清晰的框架。请确保每一部分都围绕核心主题展开，并避免冗余和不相关的内容。
    """
    
    user_prompt = f"""
    以下是经过提纯后的文本，描述了人物的生平。请根据这些内容生成一份传记的大纲，要求包含以下部分：
    1. **引言**：简短介绍人物的背景和生平，概括性地说明传记的主题。
    2. **关键生活事件**：列出人物的主要生活事件或转折点，按时间顺序（童年、青年、职业生涯）或主题进行排列。每个事件应简洁明了，突出人物的成长和变化。
    3. **重要成就**：提炼人物的主要成就或贡献。
    4. **总结与反思**：对人物的生活经验进行总结或反思，可能包括人物的人生哲学或未来展望。
    输入文本：
    {revised_content}

    请根据输入文本生成一份传记的大纲。确保内容简洁、条理清晰，能够为后续撰写完整传记提供框架，最后以markdown形式给出。
    """
    
    try:
        biography_outline =  call_llm(system_prompt, user_prompt,temperature=1.5)
        if biography_outline is None:
            print("outline 过程失败：LLM 调用返回空结果")
            return None
        
        biography_outline = biography_outline.replace("```markdown", "").replace("```", "").strip()
        return biography_outline
    except Exception as e:
        print(f"outline 过程发生错误: {str(e)}")
        return None

def writer(part, outline):
    """
    Agent: writer 第三步，根据大纲写传记
    """
    
    system_prompt = """
    你是一名专业的传记作家，专注于根据用户提供的输入生成人物传记的某个具体阶段内容。每次仅处理一个阶段，内容需详细、生动，语言流畅，符合传记风格。
    根据输入，生成与该阶段相关的内容，描述细节、背景、关键事件以及人物的情感与成长，确保故事性与连贯性。文风采用林语堂或古龙写传记的风格，幽默诙谐且生动。
    """
    
    user_prompt = f"""
    请根据以下输入，生成[某阶段]的传记内容，涵盖重要背景、关键事件以及情感变化。语言需生动流畅，注重细节描写。模仿林语堂或者古龙的风格。
    **输入的阶段**：
    {part}

    **具体内容描述**：
    {outline}

    请生成该阶段的传记内容，确保内容详尽、逻辑清晰、生动引人，文采类似林语堂或者古龙，诗意纵横但同时完全符合用户的叙事准确，最后以markdown形式给出。
    """
    try:
        data = call_llm(system_prompt, user_prompt)
        if data is None:
            print("writer 过程失败：LLM 调用返回空结果")
            return None
        data = data.replace("```markdown", "").replace("```", "").strip()
        return data
    except Exception as e:
        print(f"write 过程发生错误: {str(e)}")
        return None


def conclusioner(content):
    """
    Agent: conclusioner
    """
    system_prompt = "你是一个总结大师，善于根据内容提炼总结，用比较少的内容精准且不丢失内容地概括。"
    user_prompt = f"以下是需要总结的历史背景：{content}"
    
    return call_llm(system_prompt, user_prompt)

# 使用示例
if __name__ == "__main__":
    content = "\n\n哦，到那个煤矿去玩呢。\n\n对，徐州很多煤矿，现在矿都挖满，挖挖完了。\n\n对，现在都搞新能源了。\n\n京都，京都多少年来了，是是是呃几个朋友一起去玩去的。\n\n哦。\n\n他们家有个亲戚嘛，那个时候还小嘛，我就骂人，又没结婚没干嘛的，说走就走。\n\n哦，你你你爱说走就走旅行。\n\n嗯，对啊，几个朋友嘛，玩起来，他们是，因为我们家亲戚在那个徐州，我们家就去去玩嘛，那时候我们家在镇上面算有钱的人家。\n\n哦。\n\n只要有钱就OK了呀，凌晨宣布。\n\n哦，再也打不开。\n\n嗯，二十多岁。\n\n会的。\n\n二十出头一点点吧，那时。\n\n我我前两天在家呆着，家里管我太严，我不在家，回去十五天，本来练车嘞，我看在家不能待下去了，必须得离开。\n\n我直接说学校有事，直接直接提着书，背着电脑，直接出发去徐州宾馆住了一晚上，看个电影，第二天我就打车去宿迁，坐高铁，三十分钟，宿迁，去刘强东老家看了看，打出租车去刘强东老家看看，然后呢，送我到高铁，本来想去淮安玩玩，感觉淮安，哎呀，没啥好玩的，直接坐上海，坐地铁，坐高铁来上海了，当天。\n\n我女儿出去玩呢，我跟她走呢，还不大行，她还蛮喜欢跟她老子走的。\n\n她老子走路呢，她老子喜欢历史，跟刘强东。\n\n历史，我也喜欢历史。\n\n我家东西，我老公，我这个通古知今。\n\n我女儿就喜欢跟着她爸走，为什么，一边走两个人，一边讲解给他听。\n\n他就给他讲这个，哦，行行都知道，就像我们上。\n\n我女儿到这个，呃，里面做这个志愿者，夏天的时候。\n\n学校里面问她，你反正出去吧，行，就帮我讲，出去吧。\n\n她后来，哎，她没想到这个出去还有钱呢。\n\n她不是，做了三个朝野斗争会，呃，她来帮我们学他们，真的，我这个里面怎么多了两百多块钱。\n\n这你哪来的，你自己不知道吗？\n\n后来一查，哦，学校发给我的。\n\n后来，恐怕她将会修点坏。\n\n哎，你不是做志愿者吗？\n\n对，哎，你这个都乱好了，做志愿者还有钱呢。\n\n哦，做志愿者还有钱。\n\n哦，把女儿秀他们，那韩国。\n\n嗯，还会发生类似的模仿。\n\n到意大利会去。\n\n意大利会，哦，多少钱，到外面听清楚多少钱。\n\n不要钱。\n\n哦，做志愿者。\n\n哦，我我看了那个，好像有的。\n\n他这个是学校。\n\n哦，我知道，我知道。\n\n我又把他，本来就是跟你讲的嘛，弄的这个出版社出来。\n\n他是一分钱没有。\n\n就是说，他可以给你开个证明，就上面刻上图章，你在外面一样的。\n\n后来进这个，后来老师问了他，呃，就问你出去了没有，他说，哎哟，我们学校这里，就是他，他每年都给学校分派额度的。\n\n多少人，多少人，你做什么的。\n\n他这个，哎哟，你们家靠在那边的挺近的，你没事的吧，去上好。"""
    queries = Content2BackgroundQuery(content)

    print(queries)