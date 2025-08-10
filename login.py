users={
    "user1": "pass1",
    "user2": "pass2",
    "user3": "pass3"
}
i=""
entered_username=input("enter your username: ")
entered_password=input("enter your password: ")


######tozih: chon ke fek mikardam users[yekchizi ke dar users nist] hamishe khata mide codehaye zir ro neveshtam:

# while i!="loggedin":
#     print("wrong username or password")
#     entered_username=input("enter your username: ")
#     entered_password=input("enter your password: ")
#     if entered_username in users: #check mikone ke entered_username dar users hast ha na
#         if entered_password==users[entered_username]:
#             i="loggedin"
# else:
#     print("logged in successfully")

######vali badan fahmidam ke codehayi ke (be natije giri khodam) codehayi ke khata midan age mohasebashoon ejbari nabashe kolle code khata nemide mesle in code:


while entered_username not in users or users[entered_username]!=entered_password: #inja age username tooye user nabashe sharte avval true mishe va choon or gozashtim baghiye shart ha check nemishan chon baghiye true ya false bashan roo kolliyat tasiri nadare (che jaleb!!)
    print("you username or password is wrong")
    entered_username=input("enter your username: ")
    entered_password=input("enter your password: ")
else:
    print("logged in successfully")