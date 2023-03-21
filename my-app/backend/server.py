from sanic import Sanic, response
from sanic.response import json
from sanic_cors.extension import CORS
from sanic_ext import Extend
import mysql.connector
import jwt
import datetime
from sanic_jwt import exceptions
from sanic_jwt import initialize

app = Sanic(__name__)
secret = 'secret_key'

CORS_OPTIONS = {"resources": r'/*', "origins": "*", "methods": ["GET", "POST", "HEAD", "OPTIONS"]}
Extend(app, extensions=[CORS], config={"CORS": False, "CORS_OPTIONS": CORS_OPTIONS})

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '2410',
    database = 'svelte_social3'
)

mycursor = mydb.cursor()

# async def authenticate(request, *args, **kwargs):
#     if request.json is None:
#         raise exceptions.AuthenticationFailed("Invalid JSON payload")
#     if mydb is None:
#         raise exceptions.AuthenticationFailed("Invalid database connection")
#     item = request.json
#     login_control = mydb.cursor()
#     login_control.execute("""
#         SELECT username, user_password FROM user_registration WHERE username = %s""", (item.get('user'),))
#     user_list = login_control.fetchall()

#     for users in user_list:
#         if item.get('user') == users[0] and item.get('user_password') == users[1]:
#             return {"user_id": item.get('user')}
#     raise exceptions.AuthenticationFailed("Invalid credentials")

# async def user_id(payload, *args, **kwargs):
#     return payload["user_id"]

# initialize(app, authenticate=authenticate, user_id=user_id)

# @app.route("/user/login", methods=["POST"])
# async def login(request):
#     return json({"msg": "Welcome!"})



@app.route("user/register", methods=['GET', 'POST'])  # methods = ['GET', 'POST', 'OPTIONS']
async def register(request):

    mycursor.execute("""CREATE TABLE IF NOT EXISTS user_registration (
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    e_mail TEXT,
    user_profile_photo TEXT,
    user_password TEXT,
    registration_time TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL)""")
    user = request.json
    username_control = mydb.cursor()
    username_control.execute("SELECT username FROM user_registration WHERE username = %s", (user['user_name'],))
    result = mycursor.fetchall()

    email_control = mydb.cursor()
    email_control.execute("SELECT e_mail FROM user_registration WHERE e_mail = %s", (user['e_mail'],))
    result2 = mycursor.fetchall()

    for item in result2:
        print('item', item)
    for data in result:
        if user['user_name'] == data[0] and user['e_mail'] == item[0]:
            return response.json({'status': 401, 'info': False})
    user_insert = """INSERT INTO user_registration (
        first_name, last_name, username,
        e_mail, user_profile_photo, user_password
    ) VALUES (%s, %s, %s, %s, %s, %s)"""
    user_info = (user['first_name'], user['last_name'], user['user_name'], user['e_mail'], user['user_profile_photo'], user['user_password'])
    mycursor.execute(user_insert, user_info)
    mydb.commit()
    return response.json({'status': 200, 'info': True})


async def authenticate(request, *args, **kwargs):
    item = request.json
    login_control = mydb.cursor()
    login_control.execute("""SELECT username, user_password FROM user_registration WHERE username = %s""", (item['user_name'],))
    user_list = login_control.fetchall()
    if not item['user_name'] or not item['user_password']:
        raise exceptions.AuthenticationFailed("Missing username or password")
    for data in user_list:
        if item['user_name'] == data[0] and item['user_password'] == data[1]:
            return {"user_id": item.get('user_name')}
    raise exceptions.AuthenticationFailed("Invalid credentials")

initialize(app, authenticate=authenticate)

@app.route('/user/login', methods=['POST'])
async def login(request):
    try:
        await authenticate(request)
        return json({"msg": "Welcome!"})
    except exceptions.AuthenticationFailed as e:
        return json({"msg": str(e)}, status=401)
        

# @app.route('user/login/<user>', methods=['GET', 'POST'])
# async def login(request, user):
#     item = request.json
#     user = user
#     login_control = mydb.cursor()
#     login_control.execute("""
#         SELECT username, user_password FROM user_registration WHERE username = %s""", (user,))
#     user_list = mycursor.fetchall()
    
#     for users in user_list:
#         if user == users[0] and item['user_password'] == users[1] and item:
#             # encoded = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
#             jwt_token = jwt.encode({'sub': user, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, secret, algorithm='HS256')
#             return response.json({'status': 200, 'info': True, 'jwt': jwt_token})
#     return response.json({'status': 500, 'info': False})

@app.route('user/sharePost/<user>', methods=['GET', 'POST'])
async def sharePost(request, user):
    posts = request.json
    user = user
    if user:
        mycursor.execute("""CREATE TABLE IF NOT EXISTS users_posts (
            post_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            user TEXT,
            post_category TEXT,
            post_url TEXT,
            post_subject TEXT,
            post_description TEXT,
            post_likes INT NOT NULL DEFAULT 0,
            post_dislikes INT NOT NULL DEFAULT 0,
            post_time TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL)""")
        insert_posts = mydb.cursor()
        insert_posts = """INSERT INTO users_posts (
            user, post_category, post_url, 
            post_subject, post_description) VALUES (%s, %s, %s, %s, %s)"""
        posts_details = (user, posts['post_category'], posts['post_url'], posts['post_subject'], posts['post_description'])
        mycursor.execute(insert_posts, posts_details)
        mydb.commit()
        return response.json({'info': True})

@app.route('post_status', methods=['GET', 'POST'])
async def post_stat(request):
    item = request.json
    if item['stat'] == 'like':
        insert_post_stat = "UPDATE users_posts SET post_likes = post_likes + 1 WHERE post_id = %s"
        mycursor.execute(insert_post_stat, (item['id'],))
        mydb.commit()
        insert_post_stat = "UPDATE users_posts SET post_dislikes = post_dislikes - 1 WHERE post_id = %s"
        mycursor.execute(insert_post_stat, (item['id'],))
        mydb.commit()
    elif item['stat'] == 'dislike':
        insert_post_stat = "UPDATE users_posts SET post_dislikes = post_dislikes + 1 WHERE post_id = %s"
        mycursor.execute(insert_post_stat, (item['id'],))
        mydb.commit()
        insert_post_stat = "UPDATE users_posts SET post_likes = post_likes - 1 WHERE post_id = %s"
        mycursor.execute(insert_post_stat, (item['id'],))
        mydb.commit()
    elif item['stat'] == 'delete':
        delete_post = "DELETE FROM users_posts WHERE post_id = %s"
        delete = (item['id'],)
        mycursor.execute(delete_post, delete)
        mydb.commit()
    elif item['stat'] == 'share':
        pass
    return response.json({'info': True})

@app.route('/deleteFriend/<user>', methods=['GET', 'POST'])
async def delete(request, user):
    status = request.json
    delete_friend = mydb.cursor()
    delete_friend = "DELETE FROM friend_users WHERE user = %s AND friend = %s"
    delete = (user, status['msg'],)
    mycursor.execute(delete_friend, delete)
    mydb.commit()
    return response.json({'msg':'Delete friend'}) 

@app.route('user/profileBio/<user>', methods=['GET', 'POST'])
async def userProfileBio(request, user):
    data = request.json
    if user and data['status'] == True:
        userBio = mydb.cursor()
        userBio.execute('SELECT user_id, first_name, last_name, username, e_mail, user_profile_photo, registration_time FROM user_registration WHERE username = %s', (user,))
        bioInfo = userBio.fetchall()
        return response.json({'bio': bioInfo})
    return response.json({'status': 501, 'info': False})

@app.route('/userFollowers/<user>', methods=['GET', 'POST'])
async def numberOfFollowers(request, user):
    item = request.json
    print(item)
    if item['status'] == 201 and item['info'] == True:
        followers = mydb.cursor()
        followers.execute("SELECT friend FROM friend_users WHERE user = %s",(user,))
        result = followers.fetchall()
        return response.json({'msg': result})

@app.route('user/profile/<user>', methods=['GET', 'POST'])
async def profilePosts(request, user):
    item = request.json
    if user and  item['status'] == True:
        user_posts = mydb.cursor()
        user_posts.execute("SELECT post_id, user, post_category, post_url, post_subject, post_description, post_likes, post_dislikes, post_time FROM users_posts WHERE user = %s", (user,))
        fetch = user_posts.fetchall()
        return response.json({'post': fetch})
    else:
        return response.json({'status': 500, 'info': False})

@app.route('/user_account/<user>', methods=['GET', 'POST'])
async def userAccount(request, user):
    info = request.json
    if user and info['status'] == True:
        user_posts = mydb.cursor()
        user_posts.execute("SELECT post_id, user, post_category, post_url, post_subject, post_description, post_likes, post_dislikes, post_time FROM users_posts WHERE user = %s", (user,))
        all_posts = user_posts.fetchall()
        return response.json({'post': all_posts})
    else: 
        return response.json({'status':500, 'info': False})

@app.route('user/discovery/<user>', methods=['GET', 'POST'])
async def discovery(request, user):
    data = request.json
    print(data)
    user = user
    if user and data['info'] == True:
        if data['post_category'] != 'All':
            posts = mydb.cursor()
            posts.execute('SELECT post_id, user, post_category, post_url, post_subject, post_description, post_likes, post_dislikes, post_time FROM users_posts WHERE post_category = %s', (data['post_category'],))
            select_category = posts.fetchall()
            return response.json({'info': select_category})
        elif data['post_category'] == 'All':
            posts = mydb.cursor()
            posts.execute('SELECT * FROM users_posts') 
            all_posts = posts.fetchall()
            return response.json({'info':all_posts})
    return response.json({'status': 500, 'info': False})

@app.route('/addFriend/<user>', methods=['GET', 'POST'])
async def friend_add(request, user):
    added_friend = request.json

    main_user = mydb.cursor()
    main_user.execute("""SELECT user, post_category, post_url, 
    post_subject, post_description, post_likes, post_dislikes, 
    post_time FROM users_posts WHERE user = %s""", (user,))
    main = main_user.fetchall()
    for user1 in main:
        print(user1)

    friend = mydb.cursor()
    friend.execute("""SELECT user, post_category, post_url,
    post_subject, post_description, post_likes, post_dislikes,
    post_time FROM users_posts WHERE user = %s""", (added_friend['msg'],))
    added = friend.fetchall()
    for body in added:
        print(body)

    mycursor.execute("""CREATE TABLE IF NOT EXISTS friend_users (
                friends_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                user TEXT,
                friend TEXT,
                added_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)""")

    if user and body[0] == added_friend['msg']:
        if added_friend['info'] == True and added_friend['msg']:
            insert_friends = mydb.cursor()
            insert_friends = """INSERT INTO friend_users (user, friend) VALUES (%s, %s)"""
            info = (user, added_friend['msg'])
            mycursor.execute(insert_friends, info)
            mydb.commit()
            return response.json({'msg':'Added Friend'}, status=201)
    return response.json({'msg': False}, status=401)

# @app.route('/show_Friend?/<user>', methods=['GET', 'POST'])
# async def showFriend(request, user):
#     messages = request.json
#     friends = mydb.cursor()
#     friends.execute("""SELECT friends_id, friend FROM friend_users WHERE user = %s""", (user,))
#     all_friends = friends.fetchall()
#     for friend in all_friends:
#         print(friend)
#     friends_posts = mydb.cursor()
#     friends_posts.execute("""SELECT post_id, user, post_category, post_url, post_subject, post_description, post_likes, post_dislikes, post_time FROM users_posts WHERE user = %s""", (friend[1],))
#     all_posts = friends_posts.fetchall()

#     return response.json({'msg': True, 'info':all_posts}, status=201)
@app.route('/show_Friend?/<user>', methods=['GET', 'POST'])
async def showFriend(request, user):
    messages = request.json
    friends = mydb.cursor()
    friends.execute("""SELECT friends_id, friend FROM friend_users WHERE user = %s""", (user,))
    all_friends = friends.fetchall()
    friend_posts = []
    for friend in all_friends:
        print(friend)
        friends_posts = mydb.cursor()
        friends_posts.execute("""SELECT post_id, user, post_category, post_url, post_subject, post_description, post_likes, post_dislikes, post_time FROM users_posts WHERE user = %s""", (friend[1],))
        all_posts = friends_posts.fetchall()
        friend_posts += all_posts

    return response.json({'msg': True, 'info': friend_posts}, status=201)

@app.route('/shared/posts/<user>', methods=['GET', 'POST'])
async def sharedPosts(request, user):
    posts = request.json
    print(posts, user)
    select_posts = mydb.cursor()
    select_posts.execute("""SELECT post_id, user, post_category, 
    post_url, post_subject, post_description, post_likes, post_dislikes, 
    post_time FROM users_posts WHERE post_id =%s""",(posts['id'],))
    post = select_posts.fetchall()
    for item in post:
        print(item)
    mycursor.execute("""CREATE TABLE IF NOT EXISTS users_shared_posts (
                shared_post_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                user TEXT,
                shared_post_user TEXT,
                post_category TEXT,
                post_url TEXT,
                post_subject TEXT,
                post_description TEXT,
                post_likes TEXT,
                post_dislikes TEXT,
                post_time TEXT)""")
    if user and posts['id']:
        insert_shared_posts = """INSERT INTO users_shared_posts (user, shared_post_user, post_category, post_url, post_subject, post_description, post_likes, post_dislikes, post_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        shared_posts_info = (user, item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8])
        mycursor.execute(insert_shared_posts, shared_posts_info)
        mydb.commit()
        return response.json({'info': True, 'msg': 'Shared Post'}, status=200)
    return response.json({'info': False, 'msg': 'posts not found'}, status=500)

@app.route("/show_shared_posts/<user>", methods=['GET', 'POST'])
async def showPosts(request, user):
    item = request.json
    if item['status'] == 200 and item['info'] == True:
        select = mydb.cursor()
        select.execute("""SELECT shared_post_id, user, shared_post_user, 
        post_category, post_url, post_subject, post_description, 
        post_likes, post_dislikes, post_time FROM users_shared_posts WHERE user = %s""", (user,))
        data = select.fetchall()
        return response.json({'info': True, 'msg': data}, status=200)
    return response.json({'info': False, 'msg': 'Posts Not Found'}, status=400)

# @app.route('number_of_shared', methods=['GET', 'POST'])
# async def number_of_shared(request):
#     post_subject = request.json
#     print(post_subject)
#     if post_subject['subject']:
#         select = mydb.cursor()
#         select.execute("""SELECT shared_post_id, user, shared_post_user, 
#         post_category, post_url, post_subject, post_description, 
#         post_likes, post_dislikes, post_time FROM users_shared_posts WHERE post_subject = %s""", (post_subject['subject'],))
#         item = select.fetchall()
#         return response.json({'info': True, 'msg': item}, status=200)
#     return response.json({'info': False}, status=400)

if __name__ == '__main__':
    app.run(port=5173) #host='localhost'