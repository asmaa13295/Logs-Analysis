#!/usr/bin/env python2.7

# importing postgre DB

import psycopg2

# creating function


def pop_articles():
    """ a fun to fetch the most 3 popular articles"""

    # making connection to DB
    myConn = psycopg2.connect("dbname = news")

    # creating cursor
    c = myConn.cursor()

    # using cursor to run the query
    c.execute("""
                select title , count(*) as views
                from articles join log
                on log.path = '/article/' || slug
                group by title
                order by views desc limit 3;
                """)

    output = c.fetchall()

    # printing the result of the query
    print " \n the most popular 3 articles of all time are : \n "
    for row in output:
        print ' " ' + (' " - '.join(map(str, row))) + ' views .'

    # end the connection
    myConn.close()


# creating function
def pop_article_authors():
    """ a fun to fetch the most pop article authors """

    # making connection to DB
    myConn = psycopg2.connect("dbname = news")

    # creating cursor
    c = myConn.cursor()

    # using cursor to run the query
    c.execute("""
                select authors.name , count(name)
                from authors join articles
                on articles.author = authors.id join log
                on log.path = '/article/'||articles.slug
                group by authors.name order by count(name) desc;
                """)

    output = c.fetchall()

    # printing the result of the query
    print " \n the most popular article authors of all time are : \n "
    for row in output:
        print (' - '.join(map(str, row))) + ' views .'

    # closing the connection
    myConn.close()


# creating function
def error_days():

    """ a fun to fetch days when error requests are more than 1% """

    # making connection to DB
    myConn = psycopg2.connect("dbname = news")

    # creating cursor
    c = myConn.cursor()

    # using cursor to run the query
    c.execute("""
                select to_char(total_views.date, 'FMMonth DD, YYYY') as date,
                100.0 * errors/total as percentage
                from total_views , error_views
                where total_views.date = error_views.date
                and 100.0 * errors/total > 1
                order by date;
                """)

    output = c.fetchall()
    # printing the result of the query
    print " \n days with more than 1% of error requests: \n "
    for row in output:
        print('{0} - {1:.2f}% errors'.format(row[0], row[1]))

    # ending the connection
    myConn.close()

# calling the 3 functions

pop_articles()
pop_article_authors()
error_days()
