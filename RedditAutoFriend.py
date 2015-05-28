#!/usr/bin/env python

"""RedditAutoFriend.py: Script to automatically add users from a subreddit to your friends list."""

__author__ = "Ayu"
__license__ = "GPL"

import praw
import tkinter
from tkinter import ttk
from tkinter import messagebox

reddit = praw.Reddit(user_agent='RedditAutoFriend')

root = tkinter.Tk()
root.title("Reddit Auto Friend")
frame = ttk.Frame(root, padding="3 3 12 12")
frame.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)


def start_add():
    reddit.login(user_entry.get(),pass_entry.get())
    friends = reddit.user.get_friends()
    for submission in get_submissions(sub_entry.get().rstrip()):
        user_list = get_users_from_submission(submission)
        for user in user_list:
            if user not in friends:
                user.friend()

    messagebox.showinfo("Sucess", "Sucessfully friended users from "+sub_entry.get())


def get_submissions(sub_name,post_num=1000):
    return reddit.get_subreddit(sub_name).get_hot(limit=post_num)


def get_users_from_submission(submission):
    users_list = []

    try:
        users_list = [submission.author]
    except Exception:
        pass

    comments = praw.helpers.flatten_tree(submission.comments)

    for comment in comments:
        try:
            if comment.score > 1:
                users_list.append(comment.author)
        except Exception:
            pass

    return users_list

user_entry = ttk.Entry(frame, width=7)
user_entry.grid(column=2, row=1, sticky=(tkinter.W, tkinter.E))
pass_entry = ttk.Entry(frame, width=7, show="*")
pass_entry.grid(column=2, row=2, sticky=(tkinter.W, tkinter.E))
sub_entry = ttk.Entry(frame, width=7)
sub_entry.grid(column=2, row=3, sticky=(tkinter.W, tkinter.E))
ttk.Label(frame, text="Username:").grid(column=1, row=1, sticky=tkinter.E)
ttk.Label(frame, text="Password:").grid(column=1, row=2, sticky=tkinter.E)
ttk.Label(frame, text="SubReddit:").grid(column=1, row=3, sticky=tkinter.E)
ttk.Button(frame, text="Start", command=start_add).grid(column=2, row=4, sticky=(tkinter.W, tkinter.E))

for child in frame.winfo_children(): child.grid_configure(padx=5, pady=5)

user_entry.focus()

root.mainloop()
