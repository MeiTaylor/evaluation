

import logging

import json
import os


from Comprehensiveness import evaluate_comprehensiveness
from conciseness import evaluate_conciseness
from currency import evaluate_currency
from Fact_Hallucination import evaluate_fact_hallucination
from faithfulness import evaluate_faithfulness
from logical_consistency import evaluate_logical_consistency
from strength_of_evidence import evaluate_strength_of_evidence

from Reasons_Evidence_Omission import evaluate_Omission_of_Reasons_and_Evidence


json_path = r'E:\aim\AAAI\AAAI25\Experiment\evaluate_metrics\evaluation\test_example\2022905\2022905_CV_result.json'

# Load the JSON data from the file
# 使用UTF-8编码读取JSON文件
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 提取需要的内容
document_content = {
    "Claim": data['Claim'],
    "Video_information": {
        "video_date": data['Video_information']['video_date'],
        "platform": data['Video_information']['platform'],
        "video_headline": data['Video_information']['video_headline'],
        "video_transcript": data['Video_information']['video_transcript']
    },
    "Final_Judgement": {
        "Answer": data['Final_Judgement']['Answer'],
        "Reasons": data['Final_Judgement']['Reasons']
    }
}

# 提取Evidences
all_evidences_content = {
    "Evidences": data['Evidences']
}




# 生成 content_credibility
content_credibility = {
    "comprehensiveness": evaluate_comprehensiveness(document_content),
    "conciseness": evaluate_conciseness(document_content),
    "currency": evaluate_currency(document_content,all_evidences_content),
    "fact_hallucination": evaluate_fact_hallucination(document_content, all_evidences_content),
    "faithfulness": evaluate_faithfulness(document_content, all_evidences_content),
    "logical_consistency": evaluate_logical_consistency(document_content),
    "strength_of_evidence": evaluate_strength_of_evidence(document_content, all_evidences_content)
}

# 将 content_credibility 添加到原始数据中
data['content_credibility'] = content_credibility

# 将更新后的数据写回到JSON文件中
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Content credibility added successfully.")






# 定义要查找的目录路径
target_gt_path = r'E:\aim\AAAI\AAAI25\Experiment\evaluate_metrics\evaluation\data'

# 目标 Claim，假设从已加载的数据中获取
target_claim = data['Claim']

# 初始化一个变量用于存储找到的结果
ground_truth_content = None

# 遍历目录中的所有 JSON 文件
for filename in os.listdir(target_gt_path):
    if filename.endswith('.json'):
        file_path = os.path.join(target_gt_path, filename)
        
        # 读取 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            
            # 检查 Claim 是否匹配
            if json_data.get('claim') == target_claim:
                # 提取所需的内容
                ground_truth_content = {
                    "original_rationales": json_data.get('original_rationales', {}),
                    "summary_rationales": json_data.get('summary_rationales', {}),
                    "evidences": json_data.get('evidences', {}),
                    "relationship_with_evidence": json_data.get('relationship_with_evidence', [])
                }
                # 如果找到匹配的文件，就跳出循环
                break

# 如果找到匹配的内容，则将其添加到原始数据的 'GroundTruth' 键下
if ground_truth_content:
    # data['GroundTruth'] = ground_truth_content
    # # 将更新后的数据写回到文件
    # with open(json_path, 'w', encoding='utf-8') as file:
    #     json.dump(data, file, ensure_ascii=False, indent=4)

    comparison_with_gt_score = evaluate_Omission_of_Reasons_and_Evidence(document_content, all_evidences_content, ground_truth_content)

    # # 将 content_credibility 添加到原始数据中
    data['comparison_with_gt_score'] = comparison_with_gt_score

    # 将更新后的数据写回到JSON文件中
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("GroundTruth content added successfully.")
else:
    print("No matching claim found in the specified directory.")












# json_comprehensiveness_answer = evaluate_comprehensiveness(document_content)
# json_conciseness_answer = evaluate_conciseness(document_content)
# json_currency_answer = evaluate_currency(document_content)
# json_fact_hallucination_answer = evaluate_fact_hallucination(document_content, all_evidences_content)
# json_faithfulness_answer = evaluate_faithfulness(document_content, all_evidences_content)
# json_logical_consistency_answer = evaluate_logical_consistency(document_content, all_evidences_content)
# json_strength_of_evidence_answer = evaluate_strength_of_evidence(document_content, all_evidences_content)


# content_credibility



# json_omission_of_reasons_and_evidence_answer = evaluate_Omission_of_Reasons_and_Evidence(document_content, all_evidences_content)








# logging.info("-"*50)
# logging.info(f"Comprehensiveness evaluation: \n {json_comprehensiveness_answer}")





















# import os
# import json

# def extract_evidence(subfolder_path):
#     # 初始化一个空字典，用于存储最终的Evidence数据
#     evidence_summary = {}

#     # 获取IR_result.json的路径
#     ir_result_path = os.path.join(subfolder_path, 'IR_result.json')

#     # 检查IR_result.json文件是否存在
#     if os.path.exists(ir_result_path):
#         with open(ir_result_path, 'r', encoding='utf-8') as f:
#             ir_result = json.load(f)
            
#             # 提取RelevantEvidence部分
#             relevant_evidence = ir_result.get('RelevantEvidence', {})

#             # 将子文件夹名作为键，将Evidence数据存储在evidence_summary中
#             subfolder_name = os.path.basename(subfolder_path)
#             evidence_summary[subfolder_name] = relevant_evidence
    
#     return evidence_summary

# def save_to_cv_result(json_data, output_file):
#     # 检查目标文件是否存在
#     if os.path.exists(output_file):
#         # 如果文件存在，加载现有数据并追加
#         with open(output_file, 'r', encoding='utf-8') as f:
#             existing_data = json.load(f)
#     else:
#         # 如果文件不存在，初始化为空字典
#         existing_data = {}

#     # 更新现有数据
#     existing_data.update(json_data)

#     # 将更新后的数据保存回文件
#     with open(output_file, 'w', encoding='utf-8') as f:
#         json.dump(existing_data, f, ensure_ascii=False, indent=4)

# def process_subfolders(folder_path):
#     evidence_summary = {}
    
#     # 遍历当前文件夹的所有子文件夹
#     for subfolder_name in os.listdir(folder_path):
#         subfolder_path = os.path.join(folder_path, subfolder_name)
        
#         # 检查是否为子文件夹
#         if os.path.isdir(subfolder_path):
#             # 提取Evidence数据
#             subfolder_evidence = extract_evidence(subfolder_path)
#             evidence_summary.update(subfolder_evidence)
    
#     return {"Evidences": evidence_summary}

# def process_all_folders(base_path):
#     # 遍历主文件夹中的所有子文件夹
#     for folder_name in os.listdir(base_path):
#         folder_path = os.path.join(base_path, folder_name)
        
#         # 检查是否为子文件夹
#         if os.path.isdir(folder_path):
#             # 构建当前子文件夹中CV_result.json的路径
#             output_file = os.path.join(folder_path, f'{folder_name}_CV_result.json')

#             # 对该子文件夹中的所有子文件夹进行处理
#             evidence_data = process_subfolders(folder_path)

#             # 保存到CV_result.json
#             save_to_cv_result(evidence_data, output_file)

#             print(f"Evidence数据已成功保存到 {output_file}")

# if __name__ == "__main__":
#     base_path = r"E:\aim\AAAI\AAAI25\Experiment\评价指标prompt2\test_example"

#     # 对主文件夹中的所有子文件夹进行处理
#     process_all_folders(base_path)
