import chardet


def detect_file_encoding(input_file: str) -> str:
    """简化版自动识别：
    - 检测到 GBK/GB2312/GB18030 时，统一返回 'gb18030'
    - 检测到 UTF-8 BOM 时返回 'utf-8-sig'
    - 其它编码原样返回；若无法判定则返回 'utf-8'
    """
    try:
        with open(input_file, 'rb') as f:
            raw = f.read()
    except FileNotFoundError:
        print(f'文件未找到，请检查文件路径: {input_file}')
        raise

    # 简单 BOM 检测（UTF-8）
    if raw.startswith(b"\xef\xbb\xbf"):
        print('检测到 UTF-8 BOM，使用 utf-8-sig')
        return 'utf-8-sig'

    # chardet 检测
    result = chardet.detect(raw)
    enc = (result.get('encoding') or '').strip()
    confidence = result.get('confidence')
    norm = enc.upper()

    if norm in {'GBK', 'GB2312', 'GB-2312', 'GB18030'}:
        final_enc = 'gb18030'
    elif norm in {'UTF-8', 'UTF8'}:
        final_enc = 'utf-8'
    elif norm in {'UTF-8-SIG', 'UTF8-SIG'}:
        final_enc = 'utf-8-sig'
    else:
        final_enc = enc.lower() or 'utf-8'

    print(f"检测到的编码格式: {final_enc}（原始: {enc}），置信度: {confidence}")
    return final_enc



def replace_roman_with_chinese(text):
    roman_to_chinese = {
    'Ⅰ': '一', 'Ⅱ': '二', 'Ⅲ': '三', 'Ⅳ': '四', 'Ⅴ': '五',
    'Ⅵ': '六', 'Ⅶ': '七', 'Ⅷ': '八', 'Ⅸ': '九', 'Ⅹ': '十', 
	'Ⅺ': '十一', 'Ⅻ': '十二', 'ⅩⅢ': '十三', 'ⅩⅣ': '十四', 'ⅩⅤ': '十五',
	'ⅩⅥ': '十六', 'ⅩⅦ': '十七', 'ⅩⅧ': '十八', 'ⅩⅨ': '十九', 'ⅩⅩ': '二十',
    'α': '阿尔法', 'β': '贝塔', 'γ': '伽玛', 'δ': '德尔塔', 'ε': '艾普西龙',
	'ζ': '泽塔', 'η': '伊塔', 'θ': '西塔', 'ι': '艾欧塔', 'κ': '喀帕',
    'λ': '拉姆达', 'μ': '缪', 'ν': '纽', 'ξ': '克西', 'ο': '欧米克戎',
    'π': '派', 'ρ': '柔', 'σ': '西格玛', 'τ': '陶', 'υ': '宇普西龙',
    'φ': '菲', 'χ': '卡伊', 'ψ': '普赛', 'ω': '欧米伽'
}
    for roman, chinese in roman_to_chinese.items():
        text = text.replace(roman, chinese)
    return text