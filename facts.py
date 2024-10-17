import random

halloween_facts = [
    "The first Jack-O'-Lanterns were made from turnips.",
    "Halloween is the second most commercial holiday in the US after Christmas.",
    "In some parts of Ireland, people used to play pranks like hiding children's toys on Halloween.",
    "Samhainophobia is the fear of Halloween.",
    "Skeletons symbolize death and the afterlife in many cultures.",
    "The word 'witch' comes from the Old English 'wicce', meaning wise woman.",
    "The origins of Halloween began over 2,000 years ago.",
    "Over 90% of parents supposedly steal their children’s Halloween sweets!",
    "Halloween used to be called All Hallows’ Eve.",
    "Black cats were once believed to be witches' familiars or witches in disguise.",
    "The tradition of dressing up for Halloween comes from the ancient Celtic festival of Samhain.",
    "More than 35 million pounds of candy corn are produced each year.",
    "The most popular Halloween candy is chocolate, especially Reese's Peanut Butter Cups.",
    "In the US, about 48 million children go trick-or-treating every year.",
    "Mummies were once thought to have magical powers in ancient Egypt.",
    "Pumpkins are fruits, not vegetables, and are part of the gourd family.",
    "The concept of a vampire as we know it today was popularized by Bram Stoker's 1897 novel 'Dracula'.",
    "The average American spends around $75 on Halloween each year.",
    "Cemeteries often see a spike in visitors around Halloween, with many people leaving flowers and decorations on graves."
]
def get_random_fact():
    return random.choice(halloween_facts)
