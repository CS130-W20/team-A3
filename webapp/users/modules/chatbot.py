import random

def chatbot(text):
    print("TODO: we should do something to handle the chat message; a chatbot. currently it is fake.")
    success = 1 # fail: 0
    candidate_answers = ["hi!", "Hummmmm...", "Yes you are right!", "Yes I totally agree with you!", "Pardon me?", "That sounds interesting!", "So maybe you want to learn more about machine learning?"]
    # not using if text.lower().find("name") != -1 anymore
    words_mentioned = set(text.lower().split())
    sentence_content = text.lower()
    if "name" in words_mentioned or "who" in words_mentioned:
        reply_text = "I am Eda (Education AI) from UCLA! Nice to meet you!"
    elif "you" in words_mentioned or "eda" in words_mentioned:
        reply_text = "I am just the first version of a chatbot; let's not talk about me, let's talk more about you!"
    elif "hello" in words_mentioned or "hi" in words_mentioned or "greeting" in words_mentioned:
        reply_text = "How dost thou, sweet lord?"
    elif "ai" in words_mentioned or "ml" in words_mentioned or "dm" in words_mentioned \
        or sentence_content.find("machine learning")!=-1 or sentence_content.find("artificial intelligence")!=-1 in sentence_content.find("data mining")!=-1:
        reply_text = "Yes you got it! I am an expert in the fields you mentioned. But currently I don't know how to organize my words to tell you what I know."
    else:
        reply_text = random.sample(candidate_answers, 1)[0]
    return success, reply_text