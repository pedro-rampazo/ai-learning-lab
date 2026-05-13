with open("1_python_ai_applied/files/Resenhas_App_ChatGPT.txt", "r", encoding="utf-8") as file:
    review = file.read()

review_lst = review.split("\n")