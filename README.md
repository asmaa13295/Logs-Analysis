# Logs-Analysis

0-Introduction :
-----------------

*In this project we use python tools to get data from database using API.
we build an internal reporting tool that uses information from the database.


**First of all we should have Linux-based virtual machin with vagrant running on it
 and python environment also to write API.



**Once you have the data loaded into your database, connect to your database using psql -d news and explore the tables using the \dt and \d table commands and select statements.




**Follow this to run it :

0.1.Open the shel and change the directory to the location of vagrant and database files:

0.2. Run "vagrant up" 
0.3. Run "vagrant ssh".
Wait for awhile to enable the machine downloading requirements after each command.

Now, your machin is ready to read the database file.

*In our project we use a postgre sql and our file is called "newsdata.sql".
for more information about postgresql visit : https://www.postgresql.org/docs/9.5/static/index.html

here you can download the data here "https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip"

**you should unzip the downloaded file and put it into the vagrant directory
the file is called newsdata.sql .

To load the data, use the command" psql -d news -f newsdata.sql."


**Here's what this command does:

psql — the PostgreSQL command line program
-d news — connect to the database named news which has been set up for you
-f newsdata.sql — run the SQL statements in the file newsdata.sql

\dt — display tables — lists the tables that are available in the database.
\d table — (replace table with the name of a table) — shows the database schema for that particular table.


0.3. Connect to the data base using the command:
psql -d news

Here we can copy and past the create view statements specified blew into the console.


0.4. Running the python file using : python mySourceP.py


***************************************************************************


Here my main file is a python one called "mySourceP.py" consists of 3 functions:
 
in each function there are basic common things :

1-Making connection to DB.
2-Creating a cursor.
3-Using the cursor to run the query on DB.
4-Fech the results of the query.
5-Printing the result using for loop to loop records.
6-Ending the connection.

Only the content of line 3 differs from function to another according to the job of it,
and the print line also.



1- The first fun "article_V()" is used to get the most 3 popular article of all time

in this fun I created a view called article_V to get title , concat the col slug with the word "article" to match it in the select 
command with other column.

#Here is the view code : 

		create view article_V as
                select title ,'/article/'||slug as mySlug
                from articles ;

#then the selection of the most pop 3 articles by matching colums between log table and the view :

		select article_V.title , count(log.id)
                from article_V join log 
                on log.path = article_V.mySlug group by path ,
                article_V.title 
                order by count desc limit 3;
				
print statement to print out the result
				
_________________________________________________________________________________________

2-the second function "pop_article_authors()" is used to get the most pop article authors

**In this functon i just wrote a query without making view to get names and count them
but i used join cluase to match 2 tables to shrink the results so that we have only names
that owns articles with the most number of views.

#Here is the query :

		select authors.name , count(name)
                from authors join articles
                on articles.author = authors.id join log
                on log.path = '/article/'||articles.slug
                group by authors.name order by count(name) desc;
				
**Then I wrote a print statement to print out the result
__________________________________________________________________________________________

3- the third function "error_days()" is used to get dayes with error rquests more than 1%:

Using 2 views : 

the first view gets the total accesses per each day:

		create view error_views as
		select date(time) as date,
        count(*) as errors
		from log
		where status != '200 OK'
		group by date(time);
				
the second view get the total errors for each day:


		create view daily_error_percent as
		select to_char(total_views.date, 'mon dd yyyy') as date,
        100.0 * errors/total as percentage
		from total_views, error_views
		where total_views.date = error_views.date
		order by date;



**Then selecting the dayes when the percent of error requsts is more than 1% by matching records from the first abd the second view : 

		select to_char(total_views.date, 'FMMonth DD, YYYY') as date,
        100.0 * errors/total as percentage
		from total_views, error_views
		where total_views.date = error_views.date
		and 100.0 * errors/total > 1
		order by date;
				
**finally printing the results .
_____________________________________________________________________________________________
4-After writing the difinition of the 3 fun we must call them to run , using only their names.
				
				
				
