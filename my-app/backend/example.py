from sanic import Sanic, response
from sanic.response import json
from sanic_cors.extension import CORS
from sanic_ext import Extend
import mysql.connector

app = Sanic(__name__)
CORS_OPTIONS = {"resources": r'/*', "origins": "*", "methods": ["GET", "POST", "HEAD", "OPTIONS"]}
Extend(app, extensions=[CORS], config={"CORS": False, "CORS_OPTIONS": CORS_OPTIONS})

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '2410',
    database = 'user-register'
)

mycursor = mydb.cursor()

mycursor.execute("""CREATE TABLE IF NOT EXISTS user_register (
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    e_mail TEXT,
    password TEXT,
    user_register_time TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL)""")
    
@app.route("/register", methods = ['GET', 'POST', 'OPTIONS'])
async def register(request):
    user = request.json
    print(user) #
    username_control = mydb.cursor()
    username_control.execute("SELECT username FROM user_register WHERE username = %s", (user['username'],))
    result = mycursor.fetchall()
    print('result', result)

    e_mail_control2 = mydb.cursor()
    e_mail_control2.execute("SELECT e_mail FROM user_register WHERE e_mail = %s", (user['e_mail'],))
    execu = mycursor.fetchall()
    print('execu', execu)

    for item in execu:
        print('item', item)
    
    for data in result:
        print(data)
        if user['username'] == data[0] and user['e_mail'] == item[0]:
            return response.json({'status': False})
    user_insert = """INSERT INTO user_register (
        first_name,
        last_name,
        username,
        e_mail,
        password) VALUES (%s, %s, %s, %s, %s)"""
    user_info = (user['firstName'], user['lastName'], user['username'], user['e_mail'], user['password'])
    mycursor.execute(user_insert, user_info)
    mydb.commit()
    return response.json({'status':True})

@app.route('login/<user>', methods = ['GET', 'POST', 'OPTIONS'])
async def login(request, user):
    req = request.json
    user = user
    print(req, user)
    control_login = mydb.cursor()
    control_login.execute("""
    SELECT username, password FROM user_register WHERE username = %s
    """, (user,))
    user_list = mycursor.fetchall()
    for users in user_list:
        if user == users[0] and req['password'] == users[1]:
            return response.json({'status': True})
    return response.json({'status': False})

@app.route('share/<user>', methods = ['GET', 'POST', 'OPTIONS'])
async def share(request, user):
    req = request.json
    user = user # calismazsa .json
    print(req, user)
    if user:
        mycursor.execute("""CREATE TABLE IF NOT EXISTS share_posts (
            post_id INT AUTO_INCREMENT PRIMARY KEY,
            user TEXT,
            post_category TEXT NOT NULL,
            post TEXT NOT NULL,
            commenter_user TEXT,
            post_comment TEXT,
            likes INT NOT NULL DEFAULT 0,
            dislikes INT NOT NULL DEFAULT 0,
            post_time TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL)""")
        insert_post = mydb.cursor()
        insert_post = """INSERT INTO share_posts (
            user, post_category, post) VALUES (%s, %s, %s)"""
        post_details = (user, req['post_category'], req['post'])
        mycursor.execute(insert_post, post_details)
        mydb.commit()
    return response.json({'status': True})

@app.route('profile/<user>', methods = ['GET', 'POST', 'OPTIONS'])
async def profile(req, user):
    print(req, user)
    select_user_posts = mydb.cursor()
    select_user_posts.execute("SELECT post_id, post_category, post, post_time, likes, dislikes FROM share_posts WHERE user = %s", (user,))
    posts = select_user_posts.fetchall()
    print(posts)
    
    return response.json({'post': posts})

@app.route('profileCard/<user>', methods = ['GET', 'POST', 'OPTIONS'])
async def profileCard(request, user):
    data = request.json
    print('profileCard:', data, user)
    select_profileCard = mydb.cursor()
    select_profileCard.execute("SELECT first_name, last_name, username, e_mail, user_register_time FROM user_register WHERE username = %s", (user,))
    card = select_profileCard.fetchall()
    print(card)

    return response.json({'card': card})
    
@app.route("postStat", methods = ['GET', 'POST', 'OPTIONS'])
async def postStat(request):
    item = request.json
    print(item)
    insert_post_stat = mydb.cursor()
    if item['stat'] == 'like':
        insert_post_stat = "UPDATE share_posts SET likes = likes + 1 WHERE post_id = %s"
        mycursor.execute(insert_post_stat, (item['id'],))
        mydb.commit()
        # insert_post_stat = "UPDATE share_posts SET dislikes = dislikes - 1 WHERE post_id = %s"
        # mycursor.execute(insert_post_stat, (item['id'],))
        # mydb.commit()
    elif item['stat'] == 'dislike':
        insert_post_stat = "UPDATE share_posts SET dislikes = dislikes + 1 WHERE post_id = %s"
        mycursor.execute(insert_post_stat, (item['id'],))
        mydb.commit()
        # insert_post_stat = "UPDATE share_posts SET likes = likes - 1 WHERE post_id = %s"
        # mycursor.execute(insert_post_stat, (item['id'],))
        # mydb.commit()
    elif item['stat'] == 'delete':
        delete_post_stat = "DELETE FROM share_posts WHERE post_id = %s"
        delete = (item['id'],)
        mycursor.execute(delete_post_stat, delete)
        mydb.commit()
    return response.json({'status': 200})

@app.route('post_comments', methods = ['GET', 'POST', 'OPTIONS'])
async def comments(request):
    item = request.json
    print(item)
    if item['commenter'] and item['comment']:
        insert_post_comment = mydb.cursor()
        insert_post_comment = "UPDATE share_posts SET commenter_user = %s, post_comment = %s WHERE post_id = %s"
        mycursor.execute(insert_post_comment, (item['commenter'], item['comment'], item['id'],))
        mydb.commit()
    return response.json({'status': True})

@app.route('discovery', methods = ['GET', 'POST', 'OPTIONS'])
async def discovery(request):
    item = request.json
    print(item)
    if item['status'] == True:
        discovery_posts = mydb.cursor()
        discovery_posts.execute("""SELECT post_id, user, post_category, post, post_time, likes, dislikes FROM share_posts""")
        users_posts = discovery_posts.fetchall()
        print(users_posts)

        return response.json({'users_posts': users_posts})

@app.route('user_profile/<user>', methods=['GET', 'POST', 'OPTIONS'])
async def users_profile(request, user):
    data = request.json
    print("userProfile", data, user)
    return response.json({'sa':'sa'})
    
if __name__ == '__main__':
    app.run(port=5173) #host='localhost'