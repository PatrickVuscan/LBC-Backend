from fastapi import FastAPI, requests
from api.database.db_initialize import SessionLocal, engine
from api.model.table_models import USERS, USER_POSTS, COMMENTS, EMERGENCY_CONTACTS, Base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base.metadata.create_all(bind=engine)
# Creates all tables if not exists, for db based on SQLALCHEMY_DATABASE_URL in api/database/db_initialize.py

"""
Run this file while in team-project-13-lady-ballers-camp-backend directory

Mac: $ python3 -m scripts.db_test
Windows: $ python -m scripts.db_test

Creates a sqlite db in api/database and populates each of the 4 tables with test data
"""

def insert_USERS_test(session_maker):

    orm_session = session_maker()
    # Insert data into USERS table

    # Insert Method 1
    new_user = USERS()
    new_user.username = "test_1_username"
    new_user.password= "test_1_password"
    new_user.age = 99
    new_user.name = "test_name_1"
    new_user.email = "test_1@gmail.com"
    orm_session.add(new_user)

    # Insert Method 2 ()
    user_2_info = {'username': 'test_2_username',
                   'password': 'test_2_password',
                   'email': 'test_2@gmail.com',
                   'age': 100}

    orm_session.add(USERS(**user_2_info))


    # Insert Method 3 (insert a list of users)
    bulk_lst = []
    for i in range(3, 10):
        temp = {'username': f'test_{i}_username',
                'password': f'test_{i}_password',
                'email': f'test_{i}@gmail.com',
                'age': i}

        bulk_lst.append(USERS(**temp))

    orm_session.bulk_save_objects(bulk_lst)
    orm_session.commit()
    orm_session.close()
    print("Test USERS inserted")


def insert_USER_POSTS_test(session_maker):
    orm_session = session_maker()

    bulk_lst = []
    for i in range(1, 5):
        user_post_info = {'username': f'test_{i}_username',
                          'date_time': datetime.now(),
                          'topic': "Police",
                          'post_header': f"Police Post Header (test_{i})",
                          'post_body': f"Police Post Body (test_{i}). \n Line 2. \n Line 3."}
        bulk_lst.append(USER_POSTS(**user_post_info))

    for i in range(1, 3):
        user_post_info = {'username': f'test_{i}_username',
                          'date_time': datetime.now(),
                          'topic': "Mental Health",
                          'post_header': f"Mental Health Post Header (test_{i})",
                          'post_body': f"Metal Health Post Body. (test_{i}) \n Line 2. \n Line 3."}

        bulk_lst.append(USER_POSTS(**user_post_info))

    orm_session.bulk_save_objects(bulk_lst)
    orm_session.commit()
    orm_session.close()

    print("Test USER_POSTS inserted")


def insert_COMMENTS_test(session_maker):
    orm_session = session_maker()

    bulk_lst = []

    target_post_id = orm_session.query(USER_POSTS.post_id).first()[0]

    for i in range(1,3):

        target_username = orm_session.query(USERS.username).filter(USERS.username.like(f"%{i}%")).first()[0]

        comment_info = {'post_id': target_post_id,
                        'username': target_username,
                        'content': f"comment content from test_{i}",
                        'date_time': datetime.now()}
        bulk_lst.append(COMMENTS(**comment_info))

    orm_session.bulk_save_objects(bulk_lst)
    orm_session.commit()
    orm_session.close()
    print("Test COMMENTS inserted")


def insert_EMERGENCY_CONTACTS_test(session_maker):
    orm_session = session_maker()

    bulk_lst = []
    topics = ['Police','Mental Health', 'Clinic']
    phones = ['123-543-2345', '876-345-1234', '432-253-5432']
    for i in range(len(topics)):
        emergency_contact_info = {'topic': topics[i],
                                  'phone': phones[i],
                                  'email': "test@gmail.com",
                                  'longitude': 180.23454500,
                                  'latitude': -123.543543}

        bulk_lst.append(EMERGENCY_CONTACTS(**emergency_contact_info))


    orm_session.bulk_save_objects(bulk_lst)
    orm_session.commit()
    orm_session.close()

def query_USERS_test(session_maker):
    orm_session = session_maker()

    data = orm_session.query(USERS).filter(USERS.age > 0).all()
    for item in data:
        print(item.username, item.email, item.age)

    # Don't need to commit because no db edits occured
    orm_session.close()


def delete_test_data(session_maker):
    """
    Deletes all test data from USERS, USER_POSTS, COMMENTS, EMERGENCY_CONTACTS
    Data is considered test data if they have "test" in username of (USERS, USER_POSTS, COMMENTS)
    and for EMERGENCY_CONTACTS it is "test" in email
    """

    orm_session = session_maker()
    orm_session.query(USERS).filter(USERS.username.like('%test%')).delete(synchronize_session=False)
    orm_session.query(USER_POSTS).filter(USER_POSTS.username.like('%test%')).delete(synchronize_session=False)
    orm_session.query(COMMENTS).filter(COMMENTS.username.like('%test%')).delete(synchronize_session=False)
    orm_session.query(EMERGENCY_CONTACTS).filter(EMERGENCY_CONTACTS.email.like('%test%')).delete(synchronize_session=False)

    orm_session.commit()
    orm_session.close()
    print("Test Records deleted")

def sql_string_test(session_maker):
    orm_session = session_maker()

    query_string = f"SELECT * FROM USERS WHERE age >= 99"
    data = orm_session.execute(query_string)

    for item in data: # data is an sql object (iterable) but not a list - can't index it
        print(item)
        print(item[2])

        # item looks like ('test_username_1', 'test_password_1', 'test_name_1', 99, 'test_1@gmail.com')
        # Can index it like tuple, but its not a tuple

    orm_session.close()


if __name__ == '__main__':
    session_maker = sessionmaker(engine)
    # orm_session = session_maker()

    delete_test_data(session_maker)
    # Delete test data before we populate in case this file gets re-run multiple times
    # avoids getting error with inserting same primary keys like username multiple times

    insert_USERS_test(session_maker)
    insert_USER_POSTS_test(session_maker)
    insert_COMMENTS_test(session_maker)
    insert_EMERGENCY_CONTACTS_test(session_maker)

    # query_USERS_test(session_maker)
    # sql_string_test(session_maker)  # sample use case of executing raw sql string queries







