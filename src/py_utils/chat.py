######## 对话
import requests
import re

MODEL_END_POINT = "http://localhost:11434"

def getAvailableModels():
    try:
        response = requests.get("{MODEL_END_POINT}/api/tags".format(MODEL_END_POINT=MODEL_END_POINT))
        return response.json()
    except Exception as e:
        return None

def hasDeepSeek():
    all_models = getAvailableModels()
    if all_models is None:
        return {"has": False, "model": None}

    for model in all_models['models']:
        if ("deepseek" in model['name']):
            return {"has": True, "model": model['name']}
    return {"has": False, "model": None}

def clear_think(text):
    # 移除<think>标签及其内容
    cleaned_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    # 替换不规则的引号为标准中文引号
    cleaned_text = cleaned_text.replace('“', '「').replace('”', '」')
    # 输出处理后的文本
    return cleaned_text


def chat(prompt):
    try:
        deepSeek = hasDeepSeek()
        if (deepSeek['has']):
            reqobj = {
                "model": deepSeek['model'],
                "prompt": prompt,
                "stream": False
            }
            response = requests.post("{MODEL_END_POINT}/api/generate".format(MODEL_END_POINT=MODEL_END_POINT), json=reqobj)
            respJson = response.json()
            if (respJson.get('response')):
                cleaned_text = clear_think(respJson['response'])
                return cleaned_text
            return "无输出"
        else:
            return {"error": "DeepSeek model not available"}
    except Exception as e:
        return {"error": e}
