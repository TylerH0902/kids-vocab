"""Regenerate audio using macOS say + afconvert (AAC/M4A, much higher quality)."""
import os, subprocess, tempfile

WORDS = [
    ("dog","狗"), ("cat","猫"), ("bird","鸟"), ("fish","鱼"),
    ("rabbit","兔子"), ("elephant","大象"), ("lion","狮子"), ("monkey","猴子"),
    ("duck","鸭子"), ("horse","马"), ("cow","奶牛"), ("frog","青蛙"),
    ("apple","苹果"), ("banana","香蕉"), ("rice","米饭"), ("bread","面包"),
    ("milk","牛奶"), ("egg","鸡蛋"), ("orange","橙子"), ("cake","蛋糕"),
    ("carrot","胡萝卜"), ("noodles","面条"),
    ("red","红色"), ("blue","蓝色"), ("green","绿色"), ("yellow","黄色"),
    ("pink","粉色"), ("purple","紫色"), ("white","白色"), ("black","黑色"),
    ("eye","眼睛"), ("ear","耳朵"), ("nose","鼻子"), ("mouth","嘴巴"),
    ("hand","手"), ("foot","脚"), ("head","头"), ("heart","心脏"),
    ("one","一"), ("two","二"), ("three","三"), ("four","四"), ("five","五"),
    ("six","六"), ("seven","七"), ("eight","八"), ("nine","九"), ("ten","十"),
    ("mother","妈妈"), ("father","爸爸"), ("baby","宝宝"), ("sister","姐妹"),
    ("brother","兄弟"), ("grandma","奶奶"), ("grandpa","爷爷"),
    ("shirt","衬衫"), ("pants","裤子"), ("shoes","鞋子"), ("hat","帽子"),
    ("dress","裙子"), ("socks","袜子"), ("jacket","外套"), ("gloves","手套"),
    ("car","汽车"), ("bus","公共汽车"), ("train","火车"), ("plane","飞机"),
    ("bike","自行车"), ("boat","船"), ("rocket","火箭"), ("truck","卡车"),
]

EN_VOICE = "Samantha"
ZH_VOICE = "Tingting"

os.makedirs("audio/en", exist_ok=True)
os.makedirs("audio/zh", exist_ok=True)


def make(text, voice, out_path):
    with tempfile.NamedTemporaryFile(suffix='.aiff', delete=False) as f:
        tmp = f.name
    try:
        subprocess.run(['say', '-v', voice, '-r', '130', '-o', tmp, text], check=True)
        subprocess.run(['afconvert', '-f', 'm4af', '-d', 'aac', tmp, out_path], check=True)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


for en, zh in WORDS:
    en_path = f"audio/en/{en}.m4a"
    zh_path = f"audio/zh/{en}.m4a"
    print(f"  EN: {en}")
    make(en, EN_VOICE, en_path)
    print(f"  ZH: {zh}")
    make(zh, ZH_VOICE, zh_path)

print(f"\nDone — {len(WORDS)*2} files.")
