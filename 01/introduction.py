#!/usr/bin/python
from __future__ import division
from collections import Counter
from pprint import pprint
from collections import defaultdict
from matplotlib import pyplot as plt

# 用户列表
users = [
    { "id": 0, "name": "Hero" },
    { "id": 1, "name": "Dunn" },
    { "id": 2, "name": "Sue" },
    { "id": 3, "name": "Chi" },
    { "id": 4, "name": "Thor" },
    { "id": 5, "name": "Clive" },
    { "id": 6, "name": "Hicks" },
    { "id": 7, "name": "Devin" },
    { "id": 8, "name": "Kate" },
    { "id": 9, "name": "Klein" },
    { "id": 10, "name": "Jen" }
]

# 用户好友列表
friendships = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
               (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]

# 用户兴趣列表
interests = [
    (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"), (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"), (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
    (2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3, "Python"),
    (3, "statistics"), (3, "regression"), (3, "probability"),
    (4, "machine learning"), (4, "regression"), (4, "decision trees"), (4, "libsvm"), 
    (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"), (5, "Haskell"), (5, "programming languages"), 
    (6, "statistics"), (6, "probability"), (6, "mathematics"), (6, "theory"),
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"), (7, "neural networks"), (8, "neural networks"), 
    (8, "deep learning"), (8, "Big Data"), (8, "artificial intelligence"), 
    (9, "Hadoop"), (9, "Java"), (9, "MapReduce"), (9, "Big Data")
]

##### 1.3.1 寻找关键联系人
# first give each user an empty list
for user in users:
    user["friends"] = []

# and then populate the lists with friendships
for i, j in friendships:
    # this works because users[i] is the user whose id is i
    users[i]["friends"].append(users[j]) # add i as a friend of j
    users[j]["friends"].append(users[i]) # add j as a friend of i

# get length of friend_ids list
def number_of_friends(user):
    return len(user["friends"]) 

# 总的连接数
total_connections = sum(number_of_friends(user) for user in users)

# 平均每个用户的连接数
num_users = len(users)
avg_connections = total_connections / num_users

##### 1.3.2 寻找某人朋友的朋友，即某人有可能想认识的人
def not_the_same(user, other_user):
    return user["id"] != other_user["id"]

# other_user is not a friend if he's not in user["friends"];
# that is, if he's not_the_same as all the people in user["friends"]"""
def not_friends(user, other_user):
    return all(not_the_same(friend, other_user) for friend in user["friends"])

def friends_of_friend_ids(user):
    return Counter(foaf["id"]
                   for friend in user["friends"]  # for each of my friends
                   for foaf in friend["friends"]  # count *their* friends
                   if not_the_same(user, foaf)    # who aren't me
                   and not_friends(user, foaf))   # and aren't my friends

# 计算对某个领域感兴趣的科学家
def data_scientists_who_like(target_interest):
    return [user_id
            for user_id, user_interest in interests
            if user_interest == target_interest]

# keys are interests, values are lists of user_ids with that interest
user_ids_by_interest = defaultdict(list)

for user_id, interest in interests:
    user_ids_by_interest[interest].append(user_id)

# keys are user_ids, values are lists of interests for that user_id
interests_by_user_id = defaultdict(list)

for user_id, interest in interests:
    interests_by_user_id[user_id].append(interest)

# 和指定用户兴趣最相似的用户
def most_common_interests_with(user_id):
    return Counter(interested_user_id
        for interest in interests_by_user_id[user_id]
        for interested_user_id in user_ids_by_interest[interest]
        if interested_user_id != user_id)

##### 1.3.3 工资与工作年限
salaries_and_tenures = [(83000, 8.7), (88000, 8.1),
                        (48000, 0.7), (76000, 6),
                        (69000, 6.5), (76000, 7.5),
                        (60000, 2.5), (83000, 10),
                        (48000, 1.9), (63000, 4.2)]

def make_chart_salaries_by_tenure():
    tenures = [tenure for salary, tenure in salaries_and_tenures]
    salaries = [salary for salary, tenure in salaries_and_tenures]
    plt.scatter(tenures, salaries)
    plt.xlabel("Years Experience")
    plt.ylabel("Salary")
    plt.show()

# keys are years, values are the salaries for each tenure
salary_by_tenure = defaultdict(list)

for salary, tenure in salaries_and_tenures:
    salary_by_tenure[tenure].append(salary)

average_salary_by_tenure = {
    tenure : sum(salaries) / len(salaries)
    for tenure, salaries in salary_by_tenure.items()
}

def tenure_bucket(tenure):
    if tenure < 2: return "less than two"
    elif tenure < 5: return "between two and five"
    else: return "more than five"

salary_by_tenure_bucket = defaultdict(list)

for salary, tenure in salaries_and_tenures:
    bucket = tenure_bucket(tenure)
    salary_by_tenure_bucket[bucket].append(salary)

average_salary_by_bucket = {
    tenure_bucket : sum(salaries) / len(salaries)
    for tenure_bucket, salaries in salary_by_tenure_bucket.items()
}

##### 1.3.4 付费用户预测
def predict_paid_or_unpaid(years_experience):
    if years_experience < 3.0: return "paid"
    elif years_experience < 8.5: return "unpaid"
    else: return "paid"

##### 1.3.5 用户感兴趣的topic统计
words_and_counts = Counter(word
                           for user, interest in interests
                           for word in interest.lower().split())

##### 测试
if __name__ == "__main__":
    """
    print("######################")
    print("#")
    print("# 1.3.1 寻找关键用户")
    print("#")
    print("######################")
    print()

    print("total connections  : ", total_connections)
    print("number of users    : ", num_users)
    print("average connections: ", total_connections / num_users)
    print()

    # 统计每个用户的连接数，并按连接数的多少排序输出
    num_friends_by_id = [(user["id"], number_of_friends(user)) for user in users]

    print("users sorted by number of friends:")
    print(sorted(num_friends_by_id, key=lambda pair: pair[1], reverse=True))  

    print()
    print("######################")
    print("#")
    print("# 1.3.2 你可能认识的数据科学家")
    print("#")
    print("######################")
    print()

    print("friends of friends for user 3:", friends_of_friend_ids(users[3]))
    """

    print()
    print("######################")
    print("#")
    print("# 1.3.3 工资与工作年限")
    print("#")
    print("######################")
    print()

    # print("average salary by tenure", average_salary_by_tenure)
    print("average salary by tenure bucket", average_salary_by_bucket)

    # make_chart_salaries_by_tenure()

    print()
    print("######################")
    print("#")
    print("# 1.3.5 用户感兴趣的topic ")
    print("#")
    print("######################")
    print()

    for word, count in words_and_counts.most_common():
        if count > 1:
            print(word, count)


