# This code is for mini project 2 and it is written by Melih Keskin(melih) and Victor Smith(vwsmith)

from pymongo import MongoClient
import json
import string
import random
import datetime
import sys
import pprint


def get_random_string():
    """
    Gets a random string of 6 chars
    """ 
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(6))
    
    return result_str


def is_number(s):
    """
    Checks if the input string is a number
    """
 
    for i in range(len(s)):
        if s[i].isdigit() != True:
            return False
 
    return True


def get_uid():
    """
    Gets uid from the user. None if user is anonymous
    """

    uid = input("Enter your uid (a if anonymous) : ")

    if uid.lower() == "a": # If user is anonymous
        uid = None # Uid will be None if user uses the program anonymously

    return uid


def show_main_menu():
    """
    Shows the main menu
    """

    print("-------------------")
    print("---- MAIN MENU ----")
    print("-------------------\n")

    print("To post a question, press p,")
    print("To search for questions, press s,")
    print("To quit the program, press q")

    choice = input("I want to : ").lower()

    return choice


def show_action_menu():
    """
    Shows the action menu after the user selects a post
    """

    print("-----------------------")
    print("----- ACTION MENU -----")
    print("-----------------------\n")

    print("To answer the question, press a,")
    print("To list answers, press l,")
    print("To vote, press v,")
    print('To go back to the main menu, type main,')
    print("To quit the program, press q")
    choice = input("I want to : ").lower()

    return choice


def post_question(db, uid):
    """
    User posts a question
    """ 

    title = input("Enter the title of the question : ")
    body = input("Enter the body of the question : ")

    Id = get_random_string()
    pdate = datetime.datetime.today()

    if_tag = input("Do you want to add tags? (y/n) : ").lower()

    num_tags = "a"

    tags = [] # We are going to store tags here.
    if if_tag == "y":  
        while not num_tags.isdigit(): # Checks if the input is correct
            num_tags = input("How many tags do you want to add? : ")
            if not num_tags.isdigit():
                print("Input was not a number! Please enter a number")
        
        for _ in range(int(num_tags)):
            tag = input("Enter a tag : ")
            tags.append(tag)

    if len(tags) != 0: # If the post has tags
        if uid != None: # If post has tags and uid
            post_info = {
                "Id" : Id,
                "Title" : title,
                "Body" : body,
                "Tags" : tags,
                "Date" : pdate,
                "PostTypeId" : 1,
                "OwnerUserId" : uid,
                "Score" : 0,
                "ViewCount" : 0,
                "AnswerCount" : 0,
                "CommentCount" : 0,
                "FavoriteCount" : 0,
                "ContentLicense" : "CC BY-SA 2.5"
            }

        else:
            post_info = {
                "Id" : Id,
                "Title" : title,
                "Body" : body,
                "Tags" : tags,
                "Date" : pdate,
                "PostTypeId" : 1,
                "Score" : 0,
                "ViewCount" : 0,
                "AnswerCount" : 0,
                "CommentCount" : 0,
                "FavoriteCount" : 0,
                "ContentLicense" : "CC BY-SA 2.5"
            }

        for tag in tags: # Add tags to tags_collection
            tag_coll = db["Tags"]
            #results = tag_coll.find({"TagName" : tag})
            #if results.count_documents(True) > 0: # If tag is in tags table
            if tag_coll.count_documents({"TagName" : tag}, limit = 1) != 0:
                try:
                    tag_coll.update_one({"TagName" : tag}, {"$inc" : {"Count" : 1}})
                    #posts_coll.update_one({"Id" : qid}, {"$inc" : {"AnswerCount" : 1}})
                    print("Tag has been added! 123 ")
                except:
                    print("Update can't be made!")

            else: # If tag does not exist in collection
                tid = get_random_string()
                t_count = 1
                print("tag not in collection")
                tag_info = {
                    "Id" : tid,
                    "TagName" : tag,
                    "Count" : t_count,
                    "ExcerptPostId" : Id
                }

                try:
                    tag_coll.insert_one(tag_info)
                    print("Tag has been added!")

                except:
                    print("Error! Tag cannot be added.")


    else: # If it does not have any tags
        if uid != None: # If post does not have tags but it does have an owner
            post_info = {
                "Id" : Id,
                "Title" : title,
                "Body" : body,
                "Date" : pdate,
                "PostTypeId" : 1,
                "OwnerUserId" : uid,
                "Score" : 0,
                "ViewCount" : 0,
                "AnswerCount" : 0,
                "CommentCount" : 0,
                "FavoriteCount" : 0,
                "ContentLicense" : "CC BY-SA 2.5"
            }
        else:
            post_info = {
                "Id" : Id,
                "Title" : title,
                "Body" : body,
                "Date" : pdate,
                "PostTypeId" : 1,
                "Score" : 0,
                "ViewCount" : 0,
                "AnswerCount" : 0,
                "CommentCount" : 0,
                "FavoriteCount" : 0,
                "ContentLicense" : "CC BY-SA 2.5"
            }
    
    ########### END OF THE POST_INFO

    try:
        db["Posts"].insert_one(post_info)
        print("Question posted!")

    except:
        print("Error! Question can not be posted.")


def post_answer(db, uid, qid):
    """
    Users can answer posts
    """

    title = input("Enter the title of the answer : ")
    body = input("Enter the body of the answer : ")

    Id = get_random_string() # Post id
    pdate = datetime.datetime.today() # Post date

    if uid != None: # if poster exists
        post_info = {
                    "Id" : Id,
                    "Title" : title,
                    "Body" : body,
                    "Date" : pdate,
                    "PostTypeId" : 2,
                    "OwnerUserId" : uid,
                    "ParentId" : qid,
                    "Score" : 0,
                    "CommentCount" : 0,
                    "ContentLicense" : "CC BY-SA 2.5"
                }
    else:
        post_info = {
                    "Id" : Id,
                    "Title" : title,
                    "Body" : body,
                    "Date" : pdate,
                    "PostTypeId" : 2,
                    "ParentId" : qid,
                    "Score" : 0,
                    "CommentCount" : 0,
                    "ContentLicense" : "CC BY-SA 2.5"
                }

    try:
        db["Posts"].insert_one(post_info) # Adds answer to the post collection
        print("Answer posted!")
    except:
        print("Error! Answer can not be posted.")


    # INCREMENTING AnswerCount for the question that has been answered

    posts_coll = db["Posts"]
     
    try:
        posts_coll.update_one({"Id" : qid}, {"$inc" : {"AnswerCount" : 1}})
    except:
        print("Update can't be made!")


def vote(db, uid, pid):
    """
    Users can vote questions
    """

    Id = get_random_string() # Vote id
    vdate = datetime.datetime.today() # Vote date

    if uid != None: # uid exists -- CONSTRAINT -> A USER CANNOT VOTE MORE THAN ONCE ON A POST
        # Let's check if the user already voted before

        votes_coll = db["Votes"]
        #results = votes_col.find({"PostId" : pid, "VoterId" : uid})
        if votes_coll.count_documents({"PostId" : pid, "VoterId" : uid}, limit = 1) != 0: # If user already voted
            print("You can't vote! You already voted for this post")
            return

        vote_info = {
            "Id" : Id,
            "PostId" : pid,
            "VoteTypeId" : 2,
            "CreationDate" : vdate,
            "VoterId" : uid
        }

    else: # User is anonymous
        vote_info = {
            "Id" : Id,
            "PostId" : pid,
            "VoteTypeId" : 2,
            "CreationDate" : vdate
        }

    try:
        db["Votes"].insert_one(vote_info)
        print("Voting is successful!")
        
    except:
        print("Error! Can not vote.")
        return

    try:
        db["Posts"].update_one({"Id" : pid}, {"$inc" : {"Score" : 1}})

    except:
        print("Score can't be updated.")


def list_answers(db, uid, qid):
    """
    Users can see all answers of the question they chose
    """

    posts_coll = db["Posts"]

    answers = [] # We are going to store all of the answers except for the accepted in this array
    accepted = []
    all_answers = []

    accepted_answer = False 

    question = posts_coll.find({"Id" : qid})

    try:
        if (question[0]["PostTypeId"] != 1) and (question[0]["PostTypeId"] != str(1)): # If post is not a question
            print("Post is not a question")
            return
    except:
        print("Post does not exist")
        return

    results = posts_coll.find({"ParentId" : qid}) # Gets all the answers

    #if posts_coll.find_one({"Id" : qid})["AcceptedAnswerId"] is not None:  # If accepted answer exists
     #   accepted_id = posts_coll.find_one({"Id" : qid})["AcceptedAnswerId"]

    try:
        accepted_id = posts_coll.find_one({"Id" : qid})["AcceptedAnswerId"]
    except KeyError:
        accepted_id = None


    if accepted_id != None: # if accepted answer exists
        for answer in results: # For all answers
            answer_id = answer["Id"]
            #print(answer["Id"])
            if answer_id == accepted_id: # If it's the accepted answer
                accepted.append(answer)
                accepted_answer = True # accepted answer exists
            else:
                answers.append(answer)
            

        all_answers = accepted + answers

        #print(all_answers)

    else: # If there is no accepted answer
        #if results[0] != None: # If the questions has at least one answer
        try:
            for answer in results: # For all answers
                all_answers.append(answer)
        except:
            print("Error!")

        if len(all_answers) == 0:
            print("This question has not been answered before.")
            return
    

    ####### PART 2 OF THE FUNCTION

    index = 0
    for answer in all_answers:
        if (accepted_answer == True) and (index == 0): # Printing accepted answer
            print("***" , answer["Body"][0:80], answer["CreationDate"], answer["Score"])
            index += 1
        else:
            print(answer["Body"][0:80], answer["CreationDate"], answer["Score"])


    choice = input("\nSelect a post to see all of it. (0 for first post, 1 for second etc.) : ")
    
    if (is_number(choice)) and (int(choice) >= 0) and (int(choice) < len(all_answers)):
        # if the input is valid
        print("\n", all_answers[int(choice)])

    else:
        print("Error! Please enter an integer in the range")
        choice = input("Select a post to see all of it. (0 for first post, 1 for second etc.) : ")
        if (is_number(choice)) and (int(choice) >= 0) and (int(choice) < len(all_answers)):
            # if the input is valid
            print("\n", all_answers[int(choice)])

    if_vote = input("Would you like to Vote in this answer? (y/n) : ").lower()

    if if_vote == 'y': # If user wants to vote the answer
        ans_id = all_answers[int(choice)]["Id"]
        vote(db, uid, ans_id)
    else:
        print("You didn't vote")


def search(db):    
    print("Search\n=======")
    keyword_string = input("Input space seperated keywords: ")
    keywords = keyword_string.split()

    # client = MongoClient('127.0.0.1', 27017)
    # db = client["db2"]  # need to retrieve db name automatically
    posts = db["Posts"]

    # do we only want questions???q

    for key in keywords:
        found_title = posts.find({"Title": {"$regex" : key, "$options": "i"} , "PostTypeId" : "1"})
        found_body = posts.find({"Body": {"$regex" : key, "$options": "i"}, "PostTypeId" : "1"})
        found_tags = posts.find({"Tags": {"$regex" : key, "$options": "i"}, "PostTypeId" : "1"})

        finds = [found_title, found_body, found_tags]

        # For each matching question, display the title, the creation date, the score, 
        # and the answer count. The user should be able to select a question to see 
        # all fields of the question from Posts. 
        # After a question is selected, the view count of the question should increase 
        # by one (in Posts) and the user should be able to perform a question action (as discussed next).

        full_dict = {}
        
        print("Title || Cr_date || Score || Ans_count " )
        for dictionary in finds:
            for post in dictionary:
                try:
                    title = post["Title"]
                except:
                    title = 'N/A'

                try:
                    cr_date = post['CreationDate']
                except:
                    cr_date = 'N/A'

                try:
                    score = post["Score"]
                except:
                    score = 'N/A'

                try:
                    ans_count = post["AnswerCount"]
                except:
                    ans_count = 'N/A'

                pid = post['Id']
                full_dict[pid] = {pid}
                
                print( str(post["Id"]) + '||' + str(title) + " || " + str(cr_date) + " || " + str(score) + " || " + str(ans_count) )

        print("\n================================\n")
        
        # make dictionary of keys --> calling by key makes selection of posts quick
        
        picked_pid = select_post(full_dict)

        pid = picked_pid.pop()

        results = db["Posts"].find_one({"Id" : pid}) # Get the post

        #print(results[0]) # Prints all attributes of the post

        for key, value in results.items():
            print(str(key)+" : "+str(value) )

        # INCREMENTING BY 1 AFTER POST VIEWED
    
        db["Posts"].update_one({"Id" : pid}, {"$inc" : {"ViewCount" : 1}})
        
        return pid


def user_report(uid, db):

    print("\nUser Post Stats")
    print("=================")
    posts = db["Posts"]
     # (1) the number of questions owned and the average score for those questions, 
     # (2) the number of answers owned and the average score for those answers, and 
    num_questions = posts.count_documents({"OwnerUserId" : str(uid) , "PostTypeId" : "1"})
    num_answers = posts.count_documents({"OwnerUserId" : str(uid) , "PostTypeId" : "2"})

    questions = posts.find({"OwnerUserId" : str(uid) , "PostTypeId" : "1"})
    answers = posts.find({"OwnerUserId" : str(uid) , "PostTypeId" : "2"})

    score_questions = 0    
    score_answers = 0

    
    for x in questions:
        try:
            score_questions += x["Score"]
        except:
            score_questions += 0
    
    for y in answers:
        try:
            score_answers += y["Score"]
        except:
            score_questions += 0

    # questions

    if (num_questions == 0):
        print("Number of answers: None")
        print("Average Score (answers): None")
    else:
        avg_score_q = score_questions / num_questions
        print("Number of questions: " + str(num_questions))
        print("Average Score (questions): " + str(avg_score_q))

    # answers

    if (num_answers == 0):
        print("Number of answers: None")
        print("Average Score (answers): None")       
    else:
        avg_score_a = score_answers / num_answers
        print("Number of answers: " + str(num_answers))
        print("Average Score (answers): " + str(avg_score_a))   

    total_score = num_answers + num_questions 
    # (3) the number of votes registered for the user. 
    print("Number of votes " + str(total_score))

    # (3) the number of votes registered for the user. 



    # Users may also use the system without providing a user id, in which case no report is displayed.


def select_post(found_dict):
    """
    Selects a post
    """

    done = False

    while done == False:
        desired_key = input("Please enter the post ID of the post you wish to select: ")
        try:
            pid = found_dict[desired_key]
            done = True
        except:
            print("Pid does no exists!")

    return pid
 

def main():
    port_num = input("Port number: ") 
    client = MongoClient('127.0.0.1', int(port_num))
    db = client["291db"] # Creates or opens the database "291db"
    
    uid = get_uid() # Gets uid from the user

    if uid != None: # If user is not anonymous
        user_report(uid, db)

    choice = None

    while (choice != 'p') or (choice != 's') or (choice != 'q'): # While the input is not correct

        choice = show_main_menu() # Displays the following main menu

        if choice == 'p': # User wants to post a question
            post_question(db, uid)
        elif choice == 's': # User wants to search posts
            pid = search(db)
            choice = show_action_menu()
            if choice == 'a': # User wants to answer a question
                post_answer(db, uid, pid)
            elif choice == 'v': # User wants to vote
                vote(db, uid, pid)
            elif choice == 'l': # User wants to see answers
                list_answers(db, uid, pid)
            elif choice == 'q':
                sys.exit()
        elif choice == 'q': # User wants to quit
            sys.exit()


main()
