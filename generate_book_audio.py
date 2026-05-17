"""Generate book quiz audio using Microsoft Edge neural TTS."""
import asyncio, os, time
import edge_tts

EN_VOICE = "en-US-JennyNeural"
ZH_VOICE = "zh-CN-XiaoxiaoNeural"

# Each book: list of {q_en, q_zh, opts:[{en, zh},...]}
# IDs assigned per book: alice→q*, caterpillar→c*, wildthings→w*

BOOKS = {
  "alice": [
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
  ],

  "caterpillar": [
    { "q_en":"What did the caterpillar hatch from?",
      "q_zh":"毛毛虫是从什么里孵出来的？",
      "opts":[
        {"en":"An egg",    "zh":"一颗卵"},
        {"en":"A flower",  "zh":"一朵花"},
        {"en":"A cocoon",  "zh":"一个茧"},
        {"en":"A seed",    "zh":"一粒种子"},
      ]},
    { "q_en":"Where was the egg at the start of the story?",
      "q_zh":"故事开始时，卵在哪里？",
      "opts":[
        {"en":"On a leaf",    "zh":"在一片叶子上"},
        {"en":"On a flower",  "zh":"在一朵花上"},
        {"en":"In the grass", "zh":"在草地上"},
        {"en":"Under a tree", "zh":"在树下"},
      ]},
    { "q_en":"What warmed the egg and woke the caterpillar?",
      "q_zh":"什么温暖了卵，唤醒了毛毛虫？",
      "opts":[
        {"en":"The warm sun", "zh":"温暖的太阳"},
        {"en":"The rain",     "zh":"雨水"},
        {"en":"The wind",     "zh":"风"},
        {"en":"A bird",       "zh":"一只鸟"},
      ]},
    { "q_en":"On Monday, what did the caterpillar eat through?",
      "q_zh":"星期一，毛毛虫吃了什么？",
      "opts":[
        {"en":"One apple",  "zh":"一个苹果"},
        {"en":"One pear",   "zh":"一个梨"},
        {"en":"One plum",   "zh":"一个李子"},
        {"en":"One orange", "zh":"一个橙子"},
      ]},
    { "q_en":"On Tuesday, what did the caterpillar eat through?",
      "q_zh":"星期二，毛毛虫吃了什么？",
      "opts":[
        {"en":"Two pears",   "zh":"两个梨"},
        {"en":"Two apples",  "zh":"两个苹果"},
        {"en":"Two plums",   "zh":"两个李子"},
        {"en":"Two bananas", "zh":"两根香蕉"},
      ]},
    { "q_en":"On Wednesday, what did the caterpillar eat through?",
      "q_zh":"星期三，毛毛虫吃了什么？",
      "opts":[
        {"en":"Three plums",   "zh":"三个李子"},
        {"en":"Three apples",  "zh":"三个苹果"},
        {"en":"Three pears",   "zh":"三个梨"},
        {"en":"Three oranges", "zh":"三个橙子"},
      ]},
    { "q_en":"On Thursday, what did the caterpillar eat through?",
      "q_zh":"星期四，毛毛虫吃了什么？",
      "opts":[
        {"en":"Four strawberries", "zh":"四颗草莓"},
        {"en":"Four cherries",     "zh":"四颗樱桃"},
        {"en":"Four grapes",       "zh":"四颗葡萄"},
        {"en":"Four oranges",      "zh":"四个橙子"},
      ]},
    { "q_en":"On Friday, what did the caterpillar eat through?",
      "q_zh":"星期五，毛毛虫吃了什么？",
      "opts":[
        {"en":"Five oranges", "zh":"五个橙子"},
        {"en":"Five apples",  "zh":"五个苹果"},
        {"en":"Five pears",   "zh":"五个梨"},
        {"en":"Five lemons",  "zh":"五个柠檬"},
      ]},
    { "q_en":"How did the caterpillar feel after eating so much on Saturday?",
      "q_zh":"星期六吃了那么多之后，毛毛虫感觉怎么样？",
      "opts":[
        {"en":"He had a stomach ache",  "zh":"他肚子疼"},
        {"en":"He felt very happy",     "zh":"他感到非常开心"},
        {"en":"He fell asleep",         "zh":"他睡着了"},
        {"en":"He felt very strong",    "zh":"他感到非常强壮"},
      ]},
    { "q_en":"What did the caterpillar eat on Sunday to feel better?",
      "q_zh":"星期天，毛毛虫吃了什么让自己好受一些？",
      "opts":[
        {"en":"One nice green leaf",    "zh":"一片嫩绿的叶子"},
        {"en":"One apple",              "zh":"一个苹果"},
        {"en":"Nothing at all",         "zh":"什么都没吃"},
        {"en":"A small piece of cake",  "zh":"一小块蛋糕"},
      ]},
    { "q_en":"How many things did the caterpillar eat on Saturday?",
      "q_zh":"星期六毛毛虫共吃了多少种食物？",
      "opts":[
        {"en":"Ten",    "zh":"十种"},
        {"en":"Eight",  "zh":"八种"},
        {"en":"Five",   "zh":"五种"},
        {"en":"Twelve", "zh":"十二种"},
      ]},
    { "q_en":"Which of these did the caterpillar eat on Saturday?",
      "q_zh":"下列哪种食物是毛毛虫在星期六吃的？",
      "opts":[
        {"en":"A slice of chocolate cake", "zh":"一块巧克力蛋糕"},
        {"en":"A bowl of soup",            "zh":"一碗汤"},
        {"en":"A sandwich",                "zh":"一个三明治"},
        {"en":"A pizza",                   "zh":"一个披萨"},
      ]},
    { "q_en":"What did the caterpillar build around itself?",
      "q_zh":"毛毛虫在自己周围建造了什么？",
      "opts":[
        {"en":"A cocoon", "zh":"一个茧"},
        {"en":"A nest",   "zh":"一个巢"},
        {"en":"A web",    "zh":"一张网"},
        {"en":"A shell",  "zh":"一个壳"},
      ]},
    { "q_en":"How long did the caterpillar stay inside the cocoon?",
      "q_zh":"毛毛虫在茧里待了多久？",
      "opts":[
        {"en":"More than two weeks", "zh":"两周多"},
        {"en":"One week",            "zh":"一周"},
        {"en":"One day",             "zh":"一天"},
        {"en":"One month",           "zh":"一个月"},
      ]},
    { "q_en":"What did the caterpillar become after leaving the cocoon?",
      "q_zh":"毛毛虫从茧里出来后变成了什么？",
      "opts":[
        {"en":"A beautiful butterfly",   "zh":"一只美丽的蝴蝶"},
        {"en":"A moth",                  "zh":"一只飞蛾"},
        {"en":"A bigger caterpillar",    "zh":"一条更大的毛毛虫"},
        {"en":"A dragonfly",             "zh":"一只蜻蜓"},
      ]},
    { "q_en":"How would you describe the caterpillar at the very beginning?",
      "q_zh":"你如何描述故事开始时的毛毛虫？",
      "opts":[
        {"en":"Tiny and hungry",  "zh":"又小又饿"},
        {"en":"Big and strong",   "zh":"又大又壮"},
        {"en":"Sleepy and slow",  "zh":"又困又慢"},
        {"en":"Happy and full",   "zh":"又快乐又饱"},
      ]},
    { "q_en":"On which day did the caterpillar eat the most food?",
      "q_zh":"毛毛虫在哪天吃的东西最多？",
      "opts":[
        {"en":"Saturday",  "zh":"星期六"},
        {"en":"Friday",    "zh":"星期五"},
        {"en":"Sunday",    "zh":"星期天"},
        {"en":"Thursday",  "zh":"星期四"},
      ]},
    { "q_en":"On which day did the caterpillar start eating?",
      "q_zh":"毛毛虫从哪天开始吃东西？",
      "opts":[
        {"en":"Monday",    "zh":"星期一"},
        {"en":"Sunday",    "zh":"星期天"},
        {"en":"Tuesday",   "zh":"星期二"},
        {"en":"Wednesday", "zh":"星期三"},
      ]},
    { "q_en":"After eating the green leaf, how did the caterpillar feel?",
      "q_zh":"吃了绿叶之后，毛毛虫感觉怎么样？",
      "opts":[
        {"en":"Much better",   "zh":"好多了"},
        {"en":"Still hungry",  "zh":"还是很饿"},
        {"en":"Very tired",    "zh":"非常疲倦"},
        {"en":"Very sad",      "zh":"非常伤心"},
      ]},
    { "q_en":"Which of these was NOT something the caterpillar ate on Saturday?",
      "q_zh":"下列哪样东西不是毛毛虫在星期六吃的？",
      "opts":[
        {"en":"A bowl of soup",   "zh":"一碗汤"},
        {"en":"A pickle",         "zh":"一根腌黄瓜"},
        {"en":"A cupcake",        "zh":"一个小蛋糕"},
        {"en":"A sausage",        "zh":"一根香肠"},
      ]},
  ],

  "wildthings": [
    { "q_en":"What was Max wearing when the story began?",
      "q_zh":"故事开始时，麦克斯穿着什么？",
      "opts":[
        {"en":"A wolf suit",        "zh":"狼的服装"},
        {"en":"A monster costume",  "zh":"怪兽服装"},
        {"en":"His pajamas",        "zh":"他的睡衣"},
        {"en":"A superhero cape",   "zh":"超级英雄斗篷"},
      ]},
    { "q_en":"What mischief did Max make?",
      "q_zh":"麦克斯做了什么恶作剧？",
      "opts":[
        {"en":"He chased the dog with a fork", "zh":"他用叉子追狗"},
        {"en":"He broke a window",             "zh":"他打破了窗户"},
        {"en":"He spilled his dinner",         "zh":"他打翻了晚餐"},
        {"en":"He drew on the walls",          "zh":"他在墙上乱画"},
      ]},
    { "q_en":"What did Max's mother call him?",
      "q_zh":"麦克斯的妈妈叫他什么？",
      "opts":[
        {"en":"Wild thing",    "zh":"野兽"},
        {"en":"Naughty boy",   "zh":"淘气包"},
        {"en":"Little monster","zh":"小怪兽"},
        {"en":"Bad wolf",      "zh":"坏狼"},
      ]},
    { "q_en":"What did Max shout back at his mother?",
      "q_zh":"麦克斯对妈妈大喊了什么？",
      "opts":[
        {"en":"I'll eat you up!", "zh":"我要把你吃掉！"},
        {"en":"Go away!",         "zh":"走开！"},
        {"en":"I don't care!",    "zh":"我不在乎！"},
        {"en":"You're mean!",     "zh":"你太坏了！"},
      ]},
    { "q_en":"What punishment did Max receive?",
      "q_zh":"麦克斯受到了什么惩罚？",
      "opts":[
        {"en":"Sent to bed without supper",   "zh":"没吃晚饭就上床睡觉"},
        {"en":"He lost his toys",             "zh":"没收了他的玩具"},
        {"en":"He was not allowed outside",   "zh":"不让他出门"},
        {"en":"He had to clean his room",     "zh":"让他打扫房间"},
      ]},
    { "q_en":"What grew in Max's bedroom?",
      "q_zh":"麦克斯的卧室里长出了什么？",
      "opts":[
        {"en":"A forest",  "zh":"一片森林"},
        {"en":"A garden",  "zh":"一个花园"},
        {"en":"An ocean",  "zh":"一片海洋"},
        {"en":"A jungle",  "zh":"一片丛林"},
      ]},
    { "q_en":"How did Max travel to where the wild things are?",
      "q_zh":"麦克斯是怎么到达野兽国的？",
      "opts":[
        {"en":"In a private boat",      "zh":"乘坐一艘船"},
        {"en":"By flying",              "zh":"飞翔"},
        {"en":"Through a magic door",   "zh":"穿过一扇魔法门"},
        {"en":"Riding a wild thing",    "zh":"骑着一只野兽"},
      ]},
    { "q_en":"How long did Max sail to reach the wild things?",
      "q_zh":"麦克斯航行了多久才到达野兽国？",
      "opts":[
        {"en":"Almost a year", "zh":"将近一年"},
        {"en":"One night",     "zh":"一个晚上"},
        {"en":"One week",      "zh":"一个星期"},
        {"en":"Three days",    "zh":"三天"},
      ]},
    { "q_en":"How did Max tame the wild things?",
      "q_zh":"麦克斯是怎么驯服野兽的？",
      "opts":[
        {"en":"He stared into their yellow eyes without blinking","zh":"他盯着它们的黄色眼睛一动不动"},
        {"en":"He roared very loudly",                           "zh":"他大声咆哮"},
        {"en":"He gave them food",                               "zh":"他给它们食物"},
        {"en":"He danced with them",                             "zh":"他和它们一起跳舞"},
      ]},
    { "q_en":"What colour were the wild things' eyes?",
      "q_zh":"野兽的眼睛是什么颜色的？",
      "opts":[
        {"en":"Yellow","zh":"黄色"},
        {"en":"Red",   "zh":"红色"},
        {"en":"Green", "zh":"绿色"},
        {"en":"Blue",  "zh":"蓝色"},
      ]},
    { "q_en":"What title did the wild things give Max?",
      "q_zh":"野兽们给了麦克斯什么称号？",
      "opts":[
        {"en":"King of All Wild Things", "zh":"所有野兽的王"},
        {"en":"Master of the Forest",    "zh":"森林之主"},
        {"en":"Lord of the Monsters",    "zh":"怪兽领主"},
        {"en":"Chief of the Wild",       "zh":"野兽酋长"},
      ]},
    { "q_en":"What did the wild things do during the wild rumpus?",
      "q_zh":"在野性狂欢中，野兽们做了什么？",
      "opts":[
        {"en":"They roared and danced through the forest","zh":"它们在森林里嚎叫跳舞"},
        {"en":"They ate a big feast",                    "zh":"它们大吃一顿"},
        {"en":"They swam in the sea",                    "zh":"它们在海里游泳"},
        {"en":"They built a castle",                     "zh":"它们建造了城堡"},
      ]},
    { "q_en":"Who stopped the wild rumpus?",
      "q_zh":"是谁终止了野性狂欢？",
      "opts":[
        {"en":"Max",                  "zh":"麦克斯"},
        {"en":"The wild things",      "zh":"野兽们自己"},
        {"en":"The sun rising",       "zh":"太阳升起"},
        {"en":"Max's mother",         "zh":"麦克斯的妈妈"},
      ]},
    { "q_en":"How did Max punish the wild things?",
      "q_zh":"麦克斯是怎么惩罚野兽的？",
      "opts":[
        {"en":"Sent them to bed without supper","zh":"不让它们吃晚饭就去睡觉"},
        {"en":"Locked them away",               "zh":"把它们关了起来"},
        {"en":"Took their crowns",              "zh":"摘走了它们的皇冠"},
        {"en":"Sailed away immediately",        "zh":"立刻扬帆离去"},
      ]},
    { "q_en":"Why did Max decide to leave the wild things?",
      "q_zh":"麦克斯为什么决定离开野兽国？",
      "opts":[
        {"en":"He wanted to be where someone loved him most","zh":"他想去一个最爱他的人身边"},
        {"en":"He was bored",                               "zh":"他感到无聊了"},
        {"en":"He was scared",                              "zh":"他感到害怕"},
        {"en":"He was very hungry",                         "zh":"他非常饿"},
      ]},
    { "q_en":"What did Max smell that made him want to go home?",
      "q_zh":"麦克斯闻到了什么让他想回家？",
      "opts":[
        {"en":"Good things to eat",  "zh":"美食的香味"},
        {"en":"His mother's perfume","zh":"妈妈的香水"},
        {"en":"Fresh sea air",       "zh":"新鲜的海风"},
        {"en":"Flowers",             "zh":"花香"},
      ]},
    { "q_en":"What did the wild things shout when Max wanted to leave?",
      "q_zh":"麦克斯要离开时，野兽们喊了什么？",
      "opts":[
        {"en":"Oh please don't go, we love you so!", "zh":"哦，请不要走，我们爱你！"},
        {"en":"Goodbye King Max!",                   "zh":"再见，麦克斯国王！"},
        {"en":"Come back soon!",                     "zh":"快点回来！"},
        {"en":"We will miss you!",                   "zh":"我们会想念你的！"},
      ]},
    { "q_en":"How long did Max sail on the way home?",
      "q_zh":"麦克斯回家路上航行了多久？",
      "opts":[
        {"en":"Over a year", "zh":"一年多"},
        {"en":"One night",   "zh":"一个晚上"},
        {"en":"One week",    "zh":"一个星期"},
        {"en":"One day",     "zh":"一天"},
      ]},
    { "q_en":"What was waiting for Max when he got home?",
      "q_zh":"麦克斯回家后，什么在等着他？",
      "opts":[
        {"en":"His supper",   "zh":"他的晚饭"},
        {"en":"His mother",   "zh":"他的妈妈"},
        {"en":"His toys",     "zh":"他的玩具"},
        {"en":"An apology",   "zh":"一个道歉"},
      ]},
    { "q_en":"How was Max's supper when he arrived home?",
      "q_zh":"麦克斯到家时，他的晚饭是什么状态？",
      "opts":[
        {"en":"Still hot",       "zh":"还是热的"},
        {"en":"Cold",            "zh":"冷掉了"},
        {"en":"Already eaten",   "zh":"已经被吃掉了"},
        {"en":"Left on the floor","zh":"留在地板上"},
      ]},
  ],
}

# ID prefixes per book
PREFIXES = {"alice": "q", "caterpillar": "c", "wildthings": "w"}

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
    for book_id, questions in BOOKS.items():
        prefix = PREFIXES[book_id]
        print(f"\n=== {book_id} ===")
        for i, q in enumerate(questions):
            qid = f"{prefix}{i}"
            print(f"  Q{i}: {q['q_en'][:50]}...")
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
                oid = f"{prefix}{i}_{j}"
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
