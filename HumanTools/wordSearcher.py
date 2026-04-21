wordLists = [
    "C:/Users/Administrator/PycharmProjects/pythonProject/ZhangHuo/endfield/skzy/wordlist.txt"
    ]

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

if __name__ == "__main__":
    while True:
        letters = input("请输入要搜索的字母：")
        if letters == "":
            break
        print("  ".join(searchWord(letters)))
