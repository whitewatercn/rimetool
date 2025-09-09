import os
import re
import jieba
from pypinyin import lazy_pinyin
from datetime import datetime
from .encoding_test import detect_file_encoding
from .roman_to_chinese import roman_to_chinese

def contains_chinese(text):
	"""检查文本是否包含中文字符"""
	return bool(re.search(r'[\u4e00-\u9fff]', text))



def main(input_file, output_path, is_web=False, jieba_dict=None):
	# 确保文件编码正确读入，并在输出时转为gbk
	encoding = detect_file_encoding(input_file)
	
	# 只根据main参数jieba_dict加载自定义词库
	if jieba_dict and os.path.exists(jieba_dict):
		print(f"加载jieba自定义词典: {jieba_dict}")
		jieba.load_userdict(jieba_dict)
	
	current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	
	# 短句子级别的输出文件
	short_sentence_output_file = os.path.join(output_path, f'simple_chinese_output_{current_time}_short_sentence.dict.yaml')
	# 长句子级别的输出文件
	long_sentence_output_file = os.path.join(output_path, f'simple_chinese_output_{current_time}_long_sentence.dict.yaml')
	# 词语级别的输出文件
	word_output_file = os.path.join(output_path, f'simple_chinese_output_{current_time}_word.dict.yaml')
	# 完整的输出文件（包含句子和词语）
	full_output_file = os.path.join(output_path, f'simple_chinese_output_{current_time}_full.dict.yaml')
	
	# 用于存储分割后的短句内容
	short_segments_content = []
	# 用于存储分割后的长句内容
	long_segments_content = []
	# 用于存储原始行内容，供jieba分词使用
	original_lines = []
	
	with open(input_file, 'r', encoding=encoding) as infile:
		# 遍历输入文件的每一行
		for line in infile:
			content = line
			# 如果line是空白，就删除（跳过）
			if not content.strip():
				continue
			words = content.rstrip('\n').split('\t')
			original_line = words[0]
			
			# 保存原始行内容供jieba分词使用
			if original_line.strip() and contains_chinese(original_line):
				original_lines.append(original_line.strip())
			
			# 通过标点符号分割成短句（short_sentence）
			short_segments = re.split(r'[，。？：]+', original_line)
			for segment in short_segments:
				if segment.strip():
					short_segments_content.append(segment.strip())

			# 只用句号分割成长句（long_sentence）
			long_segments = re.split(r'[。]+', original_line)
			for segment in long_segments:
				if segment.strip():
					long_segments_content.append(segment.strip())
	
	# 生成短句子级别的词典文件（short_sentence）
	with open(short_sentence_output_file, 'w', encoding='utf-8') as outfile:
		outfile.write(
			"# 生成工具 https://github.com/B-Beginner/rimetool\n" +
			"# 生成时间 " + current_time + "\n" +
			"# 类型: 短句子级别词典\n" +
			"---\n" +
			"name: simple_chinese_output_" + current_time + "_short_sentence\n" +
			"version: \"1.0\"\n" +
			"sort: by_weight\n" +
			"...\n"
		)
		# 对分割后的每个部分进行处理
		for segment in short_segments_content:
			new_line = segment  # 原文保留标点
			# 拼音部分去除标点
			no_punct = re.sub(r'[，。！？；：、“”‘’《》（）\[\]{}\-\—\.,!?;:]+', '', new_line)
			pinyin_line = roman_to_chinese(no_punct)
			pinyin = ' '.join(lazy_pinyin(pinyin_line))
			new_line_with_pinyin = new_line + '\t' + pinyin + '\t1\n'
			outfile.write(new_line_with_pinyin)

	# 生成长句子级别的词典文件（long_sentence）
	with open(long_sentence_output_file, 'w', encoding='utf-8') as outfile:
		outfile.write(
			"# 生成工具 https://github.com/B-Beginner/rimetool\n" +
			"# 生成时间 " + current_time + "\n" +
			"# 类型: 长句子级别词典\n" +
			"---\n" +
			"name: simple_chinese_output_" + current_time + "_long_sentence\n" +
			"version: \"1.0\"\n" +
			"sort: by_weight\n" +
			"...\n"
		)
		# 对分割后的每个部分进行处理
		for segment in long_segments_content:
			new_line = segment  # 原文保留标点
			# 拼音部分去除标点
			no_punct = re.sub(r'[，。！？；：、“”‘’《》（）\[\]{}\-\—\.,!?;:]+', '', new_line)
			pinyin_line = roman_to_chinese(no_punct)
			pinyin = ' '.join(lazy_pinyin(pinyin_line))
			new_line_with_pinyin = new_line + '\t' + pinyin + '\t1\n'
			outfile.write(new_line_with_pinyin)
	
	# 生成词语级别的词典文件
	with open(word_output_file, 'w', encoding='utf-8') as outfile:
		outfile.write(
			"# 生成工具 https://github.com/B-Beginner/rimetool\n" +
			"# 生成时间 " + current_time + "\n" +
			"# 类型: 词语级别词典 (jieba分词)\n" +
			"---\n" +
			"name: simple_chinese_output_" + current_time + "_word\n" +
			"version: \"1.0\"\n" +
			"sort: by_weight\n" +
			"...\n"
		)
		
		# 用jieba对每个原始行进行分词
		word_count = {}  # 用字典统计词语出现次数
		for line in original_lines:
			# 使用jieba分词
			words = jieba.cut(line)
			for word in words:
				word = word.strip()
				# 只保留长度大于1的词，且不是全数字的词，且包含中文字符
				if word and len(word) > 1 and not word.isdigit() and contains_chinese(word):
					if word in word_count:
						word_count[word] += 1
					else:
						word_count[word] = 1
		
		# 输出所有词语及其出现次数，按出现次数从高到低排序
		for word, count in sorted(word_count.items(), key=lambda x: x[1], reverse=True):
			pinyin_line = roman_to_chinese(word) # 将罗马转换为中文
			pinyin = ' '.join(lazy_pinyin(pinyin_line))
			word_with_pinyin = word + '\t' + pinyin + '\t' + str(count) + '\n'
			outfile.write(word_with_pinyin)
	
	# 生成完整的词典文件（拼接短句、长句和词语文件）
	with open(full_output_file, 'w', encoding='utf-8') as outfile:
		outfile.write(
			"# 生成工具 https://github.com/B-Beginner/rimetool\n" +
			"# 生成时间 " + current_time + "\n" +
			"# 类型: 完整词典 (短句+长句+词语拼接)\n" +
			"---\n" +
			"name: simple_chinese_output_" + current_time + "_full\n" +
			"version: \"1.0\"\n" +
			"sort: by_weight\n" +
			"...\n"
		)
		# 先写入短句子级别的内容
		with open(short_sentence_output_file, 'r', encoding='utf-8') as short_file:
			lines = short_file.readlines()
			skip_yaml_config = False
			for line in lines:
				if line.strip() == '---':
					skip_yaml_config = True
					continue
				if line.strip() == '...':
					skip_yaml_config = False
					continue
				if not line.startswith('#') and not skip_yaml_config and line.strip():
					if not (line.startswith('name:') or line.startswith('version:') or line.startswith('sort:')):
						outfile.write(line)
		# 再写入长句子级别的内容
		with open(long_sentence_output_file, 'r', encoding='utf-8') as long_file:
			lines = long_file.readlines()
			skip_yaml_config = False
			for line in lines:
				if line.strip() == '---':
					skip_yaml_config = True
					continue
				if line.strip() == '...':
					skip_yaml_config = False
					continue
				if not line.startswith('#') and not skip_yaml_config and line.strip():
					if not (line.startswith('name:') or line.startswith('version:') or line.startswith('sort:')):
						outfile.write(line)
		# 最后写入词语级别的内容
		with open(word_output_file, 'r', encoding='utf-8') as word_file:
			lines = word_file.readlines()
			# 跳过头部注释、分隔符和YAML配置，只写入词条内容
			skip_yaml_config = False
			for line in lines:
				if line.strip() == '---':
					skip_yaml_config = True
					continue
				if line.strip() == '...':
					skip_yaml_config = False
					continue
				if not line.startswith('#') and not skip_yaml_config and line.strip():
					# 跳过name、version、sort等配置行
					if not (line.startswith('name:') or line.startswith('version:') or line.startswith('sort:')):
						outfile.write(line)
	
	print(f"已生成短句子级别文件 {os.path.abspath(short_sentence_output_file)}")
	print(f"已生成长句子级别文件 {os.path.abspath(long_sentence_output_file)}")
	print(f"已生成词语级别文件 {os.path.abspath(word_output_file)}")
	print(f"已生成完整词典文件 {os.path.abspath(full_output_file)}")
	
	# 返回文件名，用于web下载
	if is_web:
		return [short_sentence_output_file, long_sentence_output_file, word_output_file, full_output_file]
	return [os.path.basename(short_sentence_output_file), os.path.basename(long_sentence_output_file), os.path.basename(word_output_file), os.path.basename(full_output_file)]

if __name__ == "__main__":
    main()