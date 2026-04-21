from fastmcp import FastMCP  
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

wordLists = [
    "endfield_words.txt",
    "wordlist.txt"
]
charLists = [
    "single_char.txt"
]

charList = []
for f in charLists:
    with open(f, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        charList.extend(lines)

wordList = []
for f in wordLists:
    with open(f, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        wordList.extend(lines)

def convertCharsToSKZ(chars):
    result = ""
    for char in chars:
        result += "gkamztlbdqiyfucxbhsjoprnweygtjmevchdxsanqolkrvwiypjzquhe"[ord(char)%56]
    return result

def searchWord(letters):
    result = []
    for item in wordList:
        if convertCharsToSKZ(item) == letters:
            result.append(item)
    return result


# Initialize the server with a name  
mcp = FastMCP("Sarkaz_tools")  

# Define a tool using the @mcp.tool decorator  
@mcp.tool
def search_exact(chars: str) -> str:  
    """搜索指定萨卡兹字符串对应的中文词汇（精确匹配，字符数量也须匹配）。会同时搜索汉语常用词以及添加进收藏列表的词。"""
    result_general = searchWord(chars)
    result_favorite = []
    try:
        with open("favorite_words.txt", 'r', encoding='utf-8') as f:
            lines = [line for line in f.read().splitlines() if line]
    except FileNotFoundError:
        lines = []
    for item in lines:
        if convertCharsToSKZ(item) == chars:
            result_favorite.append(item)
    result_char = ""
    if result_favorite:
        result_char += "收藏词列表的搜索结果：" + " ".join(result_favorite) + "\n"
    result_char += "常用词的搜索结果：" + " ".join(result_general)
    return result_char

@mcp.tool
def search_general_in_favorite(chars: str) -> str:  
    """模糊搜索收藏词列表，若词汇对应的萨卡兹字符串在提供的萨卡兹字符串中，则返回该词汇。"""
    result_favorite = []
    with open("favorite_words.txt", 'r', encoding='utf-8') as f:
        lines = f.read().split("\n")
    for item in lines:
        if convertCharsToSKZ(item) in chars:
            result_favorite.append(item)
    if len(result_favorite) > 0:
        return "搜索结果："+" ".join(result_favorite) + "\n"
    else:
        return ""

@mcp.tool
def search_single_chinese_character(char: str) -> str:  
    """搜索单个中文字，按出现频率排序。"""
    if len(char) != 1:
        return "仅支持单个中文字"
    result = []
    for item in charList:
        if convertCharsToSKZ(item) in char:
            result.append(item)
    if len(result) > 0:
        return "常用词的搜索结果："+" ".join(result) + "\n"
    else:
        return ""

@mcp.tool
def convert(chars: str) -> str:  
    """将字符串转换为萨卡兹文字"""  
    return convertCharsToSKZ(chars)

@mcp.tool
def bulkConvert(chars: list) -> dict:  
    """将多个字符串转换为萨卡兹文字"""  
    result = {}
    for char in chars:
        result[char] = convertCharsToSKZ(char)
    return result

@mcp.tool
def writeWordIntoFavorite(word: str) -> None:
    """将词汇写入收藏列表文件。写入时仅需提供词汇，无需转换为萨卡兹文字。"""
    with open("favorite_words.txt", 'r', encoding='utf-8') as f:
        lines = f.read().split("\n")
    if word in lines:
        return
    lines.append(word)
    with open("favorite_words.txt", 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

@mcp.tool
def bulkWriteWordsIntoFavorite(words: list) -> None:
    """将多个词汇写入收藏列表文件。写入时仅需提供词汇，无需转换为萨卡兹文字。"""
    with open("favorite_words.txt", 'r', encoding='utf-8') as f:
        lines = f.read().split("\n")
    for word in words:
        if word in lines:
            continue
        lines.append(word)
    with open("favorite_words.txt", 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

@mcp.tool
def readFavoriteWords() -> list:
    """读取收藏列表文件，返回所有词汇（包含转换后的萨卡兹文字）"""
    with open("favorite_words.txt", 'r', encoding='utf-8') as f:
        lines = f.read().split("\n")
    result = []
    for item in lines:
        result.append(item + ": " + convertCharsToSKZ(item))
    return result
if __name__ == "__main__":  
     mcp.run(transport="stdio")
