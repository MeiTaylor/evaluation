
import requests
import json
import regex

# gpt4o_mini分析函数
def gpt4o_mini_analysis(prompt):
    api_key = 'sk-VEA93CzU9Fd892f859C8T3BLBKFJ9d70149fe12640739881'
    url = "https://cn2us02.opapi.win/v1/chat/completions"

    payload = json.dumps({
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json',
        "Authorization": 'Bearer ' + api_key,
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    res = response.json()
    res_content = res['choices'][0]['message']['content']
    return res_content







# 提取完整的JSON数据
def extract_complete_json(response_text):
    json_pattern = r'(\{(?:[^{}]|(?1))*\})'
    matches = regex.findall(json_pattern, response_text)
    if matches:
        try:
            for match in matches:
                json_data = json.loads(match)
                return json_data
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
    return None

