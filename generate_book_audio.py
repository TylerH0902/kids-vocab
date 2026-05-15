"""Generate Alice in Wonderland quiz audio using Microsoft Edge neural TTS."""
import asyncio, os, time
import edge_tts

EN_VOICE = "en-US-JennyNeural"
ZH_VOICE = "zh-CN-XiaoxiaoNeural"

QUESTIONS = [
    { "q_en":"What did the White Rabbit have that first caught Alice's attention?",
      "q_zh":"是什么让爱丽丝第一次注意到白兔？",
      "opts":[
        {"en":"A waistcoat and a pocket watch","zh":"一件背心和一块怀表"},
        {"en":"A big bag of carrots",          "zh":"一大袋胡萝卜"},
        {"en":"A red hat",                     "zh":"一顶红帽子"},
        {"en":"A storybook",                   "zh":"一本故事书"},
      ]},
    { "q_en":"What was written on the bottle Alice found after she shrank?",
      "q_zh":"爱丽丝变小后发现的瓶子上写着什么？",
      "opts":[
        {"en":"DRINK ME",  "zh":"喝我"},
        {"en":"EAT ME",    "zh":"吃我"},
        {"en":"FOLLOW ME", "zh":"跟我来"},
        {"en":"OPEN ME",   "zh":"打开我"},
      ]},
    { "q_en":"What was in the jar Alice noticed while falling down the rabbit hole?",
      "q_zh":"爱丽丝掉进兔子洞时注意到罐子里装的是什么？",
      "opts":[
        {"en":"Orange Marmalade","zh":"橙子果酱"},
        {"en":"Strawberry Jam",  "zh":"草莓果酱"},
        {"en":"Honey",           "zh":"蜂蜜"},
        {"en":"Apple Jelly",     "zh":"苹果冻"},
      ]},
    { "q_en":"What did Alice use to open the tiny door behind the curtain?",
      "q_zh":"爱丽丝用什么打开了帘子后面的小门？",
      "opts":[
        {"en":"A golden key",  "zh":"一把金钥匙"},
        {"en":"A silver key",  "zh":"一把银钥匙"},
        {"en":"Her hairpin",   "zh":"她的发夹"},
        {"en":"A magic spell", "zh":"一句魔咒"},
      ]},
    { "q_en":"What happened to Alice when she ate the cake marked EAT ME in Chapter 1?",
      "q_zh":"爱丽丝在第一章吃了写着《吃我》的蛋糕后发生了什么？",
      "opts":[
        {"en":"She grew very tall",    "zh":"她变得非常高"},
        {"en":"She shrank very small", "zh":"她变得非常小"},
        {"en":"She became invisible",  "zh":"她变得隐形了"},
        {"en":"She fell asleep",       "zh":"她睡着了"},
      ]},
    { "q_en":"How did Alice create a pool in Chapter 2?",
      "q_zh":"爱丽丝在第二章是如何形成水池的？",
      "opts":[
        {"en":"By crying very hard",   "zh":"大哭流泪"},
        {"en":"By spilling her drink", "zh":"打翻了饮料"},
        {"en":"By finding a fountain", "zh":"找到了一个喷泉"},
        {"en":"By using magic",        "zh":"使用了魔法"},
      ]},
    { "q_en":"Which animal did Alice first meet swimming in the pool of tears?",
      "q_zh":"爱丽丝在泪水池里第一个遇到的是什么动物？",
      "opts":[
        {"en":"A Mouse","zh":"一只老鼠"},
        {"en":"A Duck", "zh":"一只鸭子"},
        {"en":"A Frog", "zh":"一只青蛙"},
        {"en":"A Fish", "zh":"一条鱼"},
      ]},
    { "q_en":"Who suggested the Caucus-Race in Chapter 3?",
      "q_zh":"第三章中是谁提议进行全体赛跑？",
      "opts":[
        {"en":"The Dodo",  "zh":"渡渡鸟"},
        {"en":"Alice",     "zh":"爱丽丝"},
        {"en":"The Mouse", "zh":"老鼠"},
        {"en":"The Lory",  "zh":"鹦鹉"},
      ]},
    { "q_en":"What did Alice hand out as prizes after the Caucus-Race?",
      "q_zh":"全体赛跑结束后，爱丽丝分发了什么作为奖品？",
      "opts":[
        {"en":"Sweets from her pocket","zh":"从口袋里拿出的糖果"},
        {"en":"Golden coins",          "zh":"金币"},
        {"en":"Pieces of cake",        "zh":"蛋糕块"},
        {"en":"Flowers",               "zh":"花朵"},
      ]},
    { "q_en":"What was Alice's own prize after the Caucus-Race?",
      "q_zh":"全体赛跑后，爱丽丝自己得到的奖品是什么？",
      "opts":[
        {"en":"Her own thimble", "zh":"她自己的顶针"},
        {"en":"A golden coin",   "zh":"一枚金币"},
        {"en":"A pretty ribbon", "zh":"一条漂亮的丝带"},
        {"en":"A piece of cake", "zh":"一块蛋糕"},
      ]},
    { "q_en":"What is the name of Alice's cat?",
      "q_zh":"爱丽丝的猫叫什么名字？",
      "opts":[
        {"en":"Dinah",    "zh":"黛娜"},
        {"en":"Whiskers", "zh":"胡须"},
        {"en":"Pepper",   "zh":"胡椒"},
        {"en":"Mittens",  "zh":"手套"},
      ]},
    { "q_en":"Who did the White Rabbit mistake Alice for in Chapter 4?",
      "q_zh":"在第四章中，白兔把爱丽丝误认为是谁？",
      "opts":[
        {"en":"His housemaid Mary Ann","zh":"他的女佣玛丽·安"},
        {"en":"His sister",            "zh":"他的妹妹"},
        {"en":"His neighbour",         "zh":"他的邻居"},
        {"en":"His friend Pat",        "zh":"他的朋友帕特"},
      ]},
    { "q_en":"Who did the White Rabbit send down the chimney?",
      "q_zh":"白兔派谁从烟囱里下去？",
      "opts":[
        {"en":"Bill the Lizard",  "zh":"蜥蜴比尔"},
        {"en":"Pat the gardener", "zh":"园丁帕特"},
        {"en":"A small frog",     "zh":"一只小青蛙"},
        {"en":"The Dodo",         "zh":"渡渡鸟"},
      ]},
    { "q_en":"What happened when Alice drank from the bottle inside the Rabbit's house?",
      "q_zh":"爱丽丝在兔子的家里喝了瓶子里的东西后发生了什么？",
      "opts":[
        {"en":"She grew so large she filled the whole room","zh":"她变得太大，把整个房间都塞满了"},
        {"en":"She shrank very small",                      "zh":"她变得非常小"},
        {"en":"She fell fast asleep",                       "zh":"她很快睡着了"},
        {"en":"She turned invisible",                       "zh":"她变得隐形了"},
      ]},
    { "q_en":"What did the pebbles thrown through the window turn into?",
      "q_zh":"从窗户扔进来的鹅卵石变成了什么？",
      "opts":[
        {"en":"Little cakes","zh":"小蛋糕"},
        {"en":"Sweets",      "zh":"糖果"},
        {"en":"Flowers",     "zh":"花朵"},
        {"en":"Coins",       "zh":"硬币"},
      ]},
    { "q_en":"Where was the Caterpillar sitting when Alice first met it in Chapter 5?",
      "q_zh":"爱丽丝在第五章初次见到毛毛虫时，它坐在哪里？",
      "opts":[
        {"en":"On top of a large mushroom","zh":"一个大蘑菇上"},
        {"en":"On a large leaf",           "zh":"一片大叶子上"},
        {"en":"On a flower",               "zh":"一朵花上"},
        {"en":"On the ground",             "zh":"地面上"},
      ]},
    { "q_en":"What was the Caterpillar doing when Alice met it?",
      "q_zh":"爱丽丝遇到毛毛虫时，它在做什么？",
      "opts":[
        {"en":"Smoking a hookah","zh":"抽水烟"},
        {"en":"Reading a book",  "zh":"读书"},
        {"en":"Eating a leaf",   "zh":"吃叶子"},
        {"en":"Sleeping",        "zh":"睡觉"},
      ]},
    { "q_en":"What were the Caterpillar's first words to Alice?",
      "q_zh":"毛毛虫对爱丽丝说的第一句话是什么？",
      "opts":[
        {"en":"Who are you?",         "zh":"你是谁？"},
        {"en":"Good morning!",        "zh":"早上好！"},
        {"en":"What do you want?",    "zh":"你想要什么？"},
        {"en":"Where are you going?", "zh":"你要去哪里？"},
      ]},
    { "q_en":"Which poem did Alice try to recite for the Caterpillar?",
      "q_zh":"爱丽丝为毛毛虫背诵的是哪首诗？",
      "opts":[
        {"en":"You Are Old, Father William",   "zh":"《你老了，威廉父亲》"},
        {"en":"Twinkle Twinkle Little Star",   "zh":"《一闪一闪亮晶晶》"},
        {"en":"Mary Had a Little Lamb",        "zh":"《玛丽有只小羊羔》"},
        {"en":"How Doth the Little Crocodile", "zh":"《小鳄鱼多么勤劳》"},
      ]},
    { "q_en":"What did the Caterpillar tell Alice about the two sides of the mushroom?",
      "q_zh":"毛毛虫告诉爱丽丝蘑菇的两边分别有什么效果？",
      "opts":[
        {"en":"One side makes you grow, the other makes you shrink","zh":"一边让你长大，另一边让你变小"},
        {"en":"One side is sweet, the other is bitter",             "zh":"一边是甜的，另一边是苦的"},
        {"en":"One side makes you invisible",                       "zh":"一边让你隐形"},
        {"en":"One side will take you home",                        "zh":"一边会带你回家"},
      ]},
]

os.makedirs("audio/book/en", exist_ok=True)
os.makedirs("audio/book/zh", exist_ok=True)


async def make(text, voice, out_path):
    for attempt in range(5):
        try:
            communicate = edge_tts.Communicate(text, voice, rate="-10%")
            await communicate.save(out_path)
            return
        except Exception as e:
            wait = 3 * (attempt + 1)
            print(f"    retry {attempt+1} ({e.__class__.__name__}) — waiting {wait}s")
            await asyncio.sleep(wait)
    raise RuntimeError(f"Failed after 5 attempts: {out_path}")


async def main():
    total = skipped = 0
    for i, q in enumerate(QUESTIONS):
        qid = f"q{i}"
        print(f"Q{i}: {q['q_en'][:50]}...")

        for path, text, voice in [
            (f"audio/book/en/{qid}.mp3", q["q_en"], EN_VOICE),
            (f"audio/book/zh/{qid}.mp3", q["q_zh"], ZH_VOICE),
        ]:
            if os.path.exists(path):
                skipped += 1
            else:
                await make(text, voice, path)
                total += 1
                await asyncio.sleep(0.3)

        for j, opt in enumerate(q["opts"]):
            oid = f"q{i}_{j}"
            for path, text, voice in [
                (f"audio/book/en/{oid}.mp3", opt["en"], EN_VOICE),
                (f"audio/book/zh/{oid}.mp3", opt["zh"], ZH_VOICE),
            ]:
                if os.path.exists(path):
                    skipped += 1
                else:
                    await make(text, voice, path)
                    total += 1
                    await asyncio.sleep(0.3)

    print(f"\nDone — {total} new files, {skipped} skipped.")


asyncio.run(main())
