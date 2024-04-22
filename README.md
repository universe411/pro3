# CS1520 Project 3

## Goal:
To gain experience using AJAX and JSON by building a website to host and manage
multiple chat rooms.

## High-level description:
You will be writing a website to host and manage chat rooms.

## Specifications:
1. You must build your website using JavaScript, JSON, `fetch`, Python, Flask,
	SQLAlchemy, and the Flask-SQLAlchemy extension.

1. When visiting the page for the first time, users should be given the chance
	to create an account or login

1. Once successfully logged in, the user should be given a list of possible
	chat rooms to join, or a message stating that none currently exist.  The
	user should also have the option to create a new chat room.

1. Once in a chat room, the user should be shown the history of messages for
	that chat room, as well as be kept up to date as messages are sent to the
	chat room. The user should also have the option to post a new message to
	the chat room. The user should further be given a way to leave the chat
	room.

	* Users can be in only one chat room at a time.
	* You must use `fetch` to retrieve update the list of messages posted to the
	  chat room (as JSON), and to post new messages to the chat room.
	* All AJAX chat updates should send only *new* messages to the user.  The
	  user should not receive the full history of all chat messages with every AJAX
	  update as this could grow quite large over time.
	* You must be sure that your application does not display "phantom"
	  messages to the user.
		* I.e., All users in the same chat room should see the same messages in
		  the same order and new messages should always appear at the end of
		  the chat log, never in the middle of the chat log.
	* You should take a polling approach to ensure that new messages are always
	  available to the user. Your application should have a 1 second time
	  between polls.

1. Once a user leaves the chat room, they should again be shown the list of
	potential chat rooms to join (or a message if none exist).

	* The user should also have the option to delete any chat rooms that they
	  created.
		* Any users still in a room when it is deleted should be shown a
		  message informing them that the room was deleted and be again
		  presented with the list of available chat rooms (or a message if none
		  exist).
		  
1. The user should always (on every page) be presented with away to log out
	while they are logged in.

1. All data for your application should be stored in an SQLite database named
	`chat.db` using SQLAlchemy's ORM and the Flask-SQLAlchemy extension.

1. Setup
	* You must setup and run Flask within a virtual environment. A
		`requirements.txt` file has been added to the repository for you to use
		in setting up your virtual environment. This is the same
		`requirements.txt` your TA will use to test your project. *Do not* add
		your virtual environment folder to your repository. I suggest you
		name your virtual environment folder `venv`, as you repo is setup
		to ignore this folder by default (see `.gitignore` for details).

## Submission Guidelines:
* **DO NOT SUBMIT** any IDE package files.

* Do not include `chat.db` in your submitted repository.

* Do not include your Python cache (the `__pycache__` folder) in your submitted
	repository.

* You must name the main flask file for your site `chat.py`, and place it in
  the root directory of your repository.

* You must be able to run your application by setting with `flask --app chat.py run`

* You must be able to initialize your database with `flask --app chat.py initdb`

* You must fill out `info_sheet.txt`.

* Be sure to remember to push the latest copy of your code back to your GitHub
	repository before submitting. To submit, log into GradeScope from Canvas and
	have GradeScope pull your repository from GitHub.

## Additional Notes/Hints:
* You may find the use of profiles
	(https://support.google.com/chrome/answer/2364824) helpful for testing
	multiple users logging in to the chat site at the same time.

* While you are not going to be heavily graded on the style and design of your
	web site, it should be presented in a clear and readable manner.

## Grading Rubric:
| Feature | Points
| ------- | ------:
| User management (account creation/login/logout) works as specified | 10%
| List of available chat rooms shown | 10%
| Leaving a chat room works as specified | 10%
| Posting new messages to a chat room works as specified | 15%
| Polled updates performed as specified | 15%
| AJAX working as specified | 20%
| SQLAlchemy data model quality | 10%
| Clear and readable presentation | 5%
| Submission/info sheet | 5%
