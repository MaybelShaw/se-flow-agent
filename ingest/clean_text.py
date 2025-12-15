import re

def clean_text(text):
    """
    针对技术文档的安全清洗函数。
    核心思想：先保护关键部分（如代码），再清理其余部分。
    现在支持 Python、C/C++ 和 Java 代码，并清理所有特殊字符。
    """
    # 1. 处理所有类型的空白字符和不可打印字符
    text = re.sub(r'[\t\r\f\v]+', ' ', text)  # 合并所有类型的空白字符
    text = re.sub(r'[\x00-\x09\x0B\x0C\x0E-\x1F\x7F\u200b\u200c\u200d\u200e\u200f\ufeff\u00ad]+', '', text)  # 移除不可打印字符，软连字符，零宽字符等

    # 2. 核心改进：在清理特殊字符时，保护代码块和行内代码
    lines = text.split('\n')
    cleaned_lines = []
    
    # 扩展的编程语言判断模式：Python、C/C++、Java
    code_patterns = [
        # Python 代码匹配
        r'^\s*(def |class |import |from |if |for |while |\w+\.\w+|.*[{}[\]=<>].*)',
        # C/C++ 代码匹配
        r'^\s*(#include |int main\(\)|printf\(|void main\(\)|for |while |if |return |\w+\.\w+|.*[{}[\]=<>].*)',
        # Java 代码匹配
        r'^\s*(public |private |protected |class |for |while |if |else |void |new|import |package).*'
    ]
    
    for line in lines:
        # 判断是否为代码行，匹配 Python、C/C++ 或 Java 的语法特征
        if any(re.search(pattern, line) for pattern in code_patterns) and 'http' not in line:
            # 对于疑似代码行，进行极保守的清理：只移除不可打印和软连字符，保留所有符号
            line = re.sub(r'[\x00-\x1F\x7F\u00ad\u200b]', '', line)  # 仅移除不可打印和软连字符
            line = line.rstrip()  # 只去除行尾空白
        else:
            # 对于普通文本行，进行正常的清理
            line = re.sub(r'[^\w\s.,;:!?\'\"()\-@#$%&*+/=<>[\]{}\\|~`]', ' ', line)  # 保留技术文档常见符号
            line = re.sub(r'\s+', ' ', line).strip()  # 清除多余的空格

        # 对于多行注释（如 """ 或 '''， /* */，//）部分，保留内容，避免清理误伤
        if re.search(r'""".*"""|\'\'\'.*\'\'\'|/\*.*\*/|//.*', line):  # 处理 Python、C/C++、Java 中的注释
            cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)

    text = '\n'.join(cleaned_lines)

    # 3. 清理多余空格并整齐化文本
    text = re.sub(r'[ \t]+', ' ', text)  # 合并多个空格
    text = re.sub(r'\n\s*\n+', '\n\n', text)  # 合并多个空行，保留段落间隔

    return text.strip()

if __name__ == "__main__":
    # sample_text = "This is a sample text with some technical content.\n\nHere is a code snippet:\n\n    def example_function(param1, param2):\n        if param1 > param2:\n            return param1 - param2  # Return the difference\n        else:\n            return param2 - param1  # Return the difference\n\nAnd here is some more text with special characters: \xad \u200b \x07 \x1F !!! ### $$$ %%% ^^^ &&& *** ((())) --- === +++ === <<< >>>\n"
    # cleaned = clean_text(sample_text)
    # print("Original Text:\n", sample_text)
    # print("\nCleaned Text:\n", cleaned)
    from load_docs import load_pdf, load_epub

    pdf_path = "/Users/bobo/Developer/se-flow-agent/data/books/AppendixA/Curriculum Guidelines for Graduate Degree Programs in Software Engineering.pdf"  # Replace with your PDF file path
    content = load_pdf(pdf_path)
    print(content[10000:20000])  # Print a snippet of the content
    printed_cleaned_pdf = clean_text(content)
    print(printed_cleaned_pdf[10000:20000])  # Print a snippet