DIALOGUE_1 = [
  {
    "message": "Ah, a new face in Carrotly Town! I'm Sarah, a trader of rare and unusual finds. If you're lucky, I might even show you something... special.",
    "options": [
      {
        "text": "What special item do you have?",
        "next": 1
      },
      {
        "text": "How did you become a trader?",
        "next": 2
      },
      {
        "text": "I don't care about your stories, just show me the goods.",
        "next": 3
      }
    ]
  },
  {
    "message": "Ah, you're interested! It's an ancient amulet said to hold... peculiar properties. But such items aren't cheap. I'm asking 500 Carrotly Coins for it.",
    "options": [
      {
        "text": "500 coins? That's too much!",
        "next": 4
      },
      {
        "text": "Tell me more about its properties.",
        "next": 5
      },
      {
        "text": "I'll think about it.",
        "finish": True
      }
    ]
  },
  {
    "message": "My family were sailors, but I chose the life of a trader. Every trinket I carry has its own tale.",
    "options": [
      {
        "text": "That's fascinating, but what about the amulet?",
        "next": 1
      },
      {
        "text": "Thank you for sharing.",
        "finish": True
      }
    ]
  },
  {
    "message": "Hmm, not much for pleasantries, are you? Very well, but know this—trust is earned, not given freely.",
    "options": [
      {
        "text": "Just show me the amulet.",
        "next": 1
      },
      {
        "text": "Fine, I'll be polite. What's your name?",
        "next": 0
      }
    ]
  },
  {
    "message": "It's a fair price for something so rare! Though... for the right buyer, I might consider 425.",
    "options": [
      {
        "text": "Still too high. Can you go lower?",
        "next": 6
      },
      {
        "text": "Fine, I'll take it.",
        "finish": True
      }
    ]
  },
  {
    "message": "Its origins lie in the Desert of Whispers. Some say it hums when danger is near. But enough talk—it's yours for 500 coins.",
    "options": [
      {
        "text": "That's intriguing. I'll buy it.",
        "finish": True
      },
      {
        "text": "I need more proof it's worth it.",
        "next": 7
      }
    ]
  },
  {
    "message": "The lowest I can go is 350 coins, and not a coin less.",
    "options": [
      {
        "text": "Deal! Here's the money.",
        "finish": True
      },
      {
        "text": "No deal. Find another buyer.",
        "finish": True
      }
    ]
  },
  {
    "message": "If you're unsure, perhaps this isn't the right artifact for you. There are plenty of other stalls here.",
    "options": [
      {
        "text": "You're right, maybe later.",
        "finish": True
      },
      {
        "text": "Wait! I'll buy it.",
        "finish": True
      }
    ]
  }
]

DIALOGUE_2 = [{"message": "(Sarah spits on the ground near the player's feet, her face contorted with rage.)  Get away from me, murderer.  You're not worth the air you breathe.", "options": None, "finish": True}]

DIALOGUE_3 = [{"message": "Ah, my dear friend! It's so good to see you again. You\u2019ve done so much for me and my family\u2014I can never repay you. But let me show my gratitude by offering you first pick of my finest wares.", "options": [{"text": "Tell me more about the wares.", "next": 1, "finish": None}, {"text": "How much are you selling it for?", "next": 2, "finish": None}, {"text": "You\u2019re welcome, Sarah. It was nothing.", "next": 3, "finish": None}], "finish": None}, {"message": "This amulet comes from the Desert of Whispers. Some say it holds strange powers, but I haven\u2019t dared to test them myself. Still, it\u2019s a remarkable piece, isn\u2019t it? Worth quite a fortune if sold to the right person.", "options": [{"text": "Sounds fascinating. What\u2019s your price?", "next": 2, "finish": None}, {"text": "Do you think its powers are real?", "next": 4, "finish": None}], "finish": None}, {"message": "For anyone else, I\u2019d ask 500 Carrotly Coins. But for you, my savior, I\u2019ll part with it for just 300. Does that sound fair?", "options": [{"text": "Deal! Here\u2019s the gold.", "next": None, "finish": True}, {"text": "I\u2019ll think about it. Thanks, Sarah.", "next": None, "finish": True}], "finish": None}, {"message": "Please, don\u2019t dismiss your kindness so lightly. You\u2019ve saved my brother and helped me countless times. If there\u2019s ever anything you need, just ask. Now, shall we talk about the amulet?", "options": [{"text": "Yes, tell me about it.", "next": 1, "finish": None}, {"text": "Let\u2019s discuss the price.", "next": 2, "finish": None}], "finish": None}, {"message": "Who knows? Magic items are rare here in Carrotly Town, and I don\u2019t take chances with something like this. But perhaps you\u2019d know more about it than I do?", "options": [{"text": "I might. Let me take a closer look.", "next": 5, "finish": None}, {"text": "I\u2019m no expert, but I\u2019ll trust your word.", "next": 2, "finish": None}], "finish": None}, {"message": "Be careful\u2014it feels heavy with history. Maybe you\u2019ll sense something I missed.", "options": [{"text": "Hmm, it does feel unusual...", "next": None, "finish": True}, {"text": "I don\u2019t notice anything special.", "next": 2, "finish": None}], "finish": None}]