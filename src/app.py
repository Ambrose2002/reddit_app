import json
from flask import Flask
from flask import jsonify
from flask import request
import random

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"


# your routes here
posts = {
  "posts": [
    {
      "id": 0,
      "upvotes": 1,
      "title": "My cat is the cutest!",
      "link": "https://i.imgur.com/jseZqNK.jpg",
      "username": "alicia98",
    },
    {
      "id": 1,
      "upvotes": 3,
      "title": "Cat loaf",
      "link": "https://i.imgur.com/TJ46wX4.jpg",
      "username": "alicia98",
    },
  ]
}
    


post_current_id = len(posts["posts"]) - 1


comments = {
    0:{
        "comments": [{
            "id": 0, 
            "upvotes": random.randint(1, 10),
            "text": "Wow, my first reddit gold!",
            "username": "alicia98",
        },
            {"id": 1, 
            "upvotes": random.randint(1, 10),
            "text": "Wow, my first reddit gold!",
            "username": "alicia98"},
        ]
    }
}


comment_ids = -1
for key in comments.keys():
    for child in comments[key]:
        comment_ids += len(comments[key][child])
        
        
@app.route("/api/posts/")
def getPosts():
    """Gets all the posts

    Returns a json of all the posts
    """
    if post_current_id == -1:
        return json.dumps({"error": "There are no posts"}), 404
    
    return json.dumps(posts), 200


@app.route("/api/posts/", methods = ["POST"])
def createPost():
    """Creates a new post

    Returns a json of the just created post
    """
    global post_current_id
    post_current_id += 1
    body = json.loads(request.data)
    title = body.get('title')
    link = body.get('link')
    username = body.get('username')
    post = {"id": post_current_id, "upvotes": random.randint(1, 10),"title": title, "link": link, "username": username}
    posts["posts"].append(post)
    return json.dumps(post), 201


@app.route("/api/posts/<int:post_id>/")
def getOnePost(post_id):
    """gets a post by id

    Returns a json of a single post
    """
    for post in posts["posts"]:
        if post["id"] == post_id:
            return json.dumps(post), 200
    return json.dumps({"error": "Post not found"}), 404


@app.route("/api/posts/<int:post_id>/", methods = ["DELETE"])
def deletePost(post_id):
    """deletes a post

    Args:
        post_id (int): the post id of the post to be deleted

    Returns the json of the deleted post
    """
    for post in posts["posts"]:
        if post["id"] == post_id:
            new_post = post
            posts["posts"].remove(post)
            return json.dumps(new_post), 200
    return json.dumps({"error": "Post not found"}), 404


@app.route("/api/posts/<int:post_id>/comments/")
def getOneComment(post_id):
    """gets all the comments from a post

    Args:
        post_id (int): the id of the post whose comments you want to get

    Returns a json of all the comments form a post
    """
    keys = [key for key in comments.keys()]
    if post_id in keys:
        comment = comments.get(post_id)
        return json.dumps(comment), 200
    return json.dumps({"error": "Comment not found"}), 404


@app.route("/api/posts/<int:post_id>/comments/", methods = ["POST"])
def postComment(post_id):
    """to make a comment to a post

    Args:
        post_id (int): the id of the post you want to addd the comment to

    Returns a json of the just created comment
    """
    global comment_ids
    try:
        comment_ids += 1
        body = json.loads(request.data)
        text = body["text"]
        username = body["username"]
        comment = {"id" : comment_ids, "upvotes": random.randint(0, 10), "text" : text, "username" : username}
        comments[post_id]["comments"].append(comment)
        return json.dumps(comment), 201
    
    except:
        for post in posts["posts"]:
            if post["id"] == post_id:
                comments[post_id] = {"comments" : [comment]}
                return json.dumps(comment), 201
    return json.dumps({"error": "Post does not exist hence comment cannot be created"}), 404
        
  
    
@app.route("/api/posts/<int:post_id>/comments/<int:cid>/", methods = ["POST"])
def editComment(post_id, cid):
    """to edit a comment for a post

    Args:
        post_id (int): the id of the post whose comment you want to edit
        cid (int): the id of the comment you want to edit

    Returns the just created comment 
    """
    body = json.loads(request.data)
    text = body.get("text")
    keys = [post["id"] for post in posts["posts"]]
    if post_id not in keys :
        return json.dumps({"error": "Post with id " + str(post_id) +" does not exist"}), 404
    try:
        comments_by_id = comments[post_id]
        for comment in comments_by_id["comments"]:
            if comment["id"] == cid:
                comment["text"] = text
                return json.dumps(comment), 200
    except:
        return json.dumps({"error": "Comment with id " + str(cid) + " does not exist"}), 404
    return json.dumps({"error": "Comment with id " + str(cid) + " does not exist"}), 404
            

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)


