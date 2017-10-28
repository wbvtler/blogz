Blogz: a blogging app

#### ABOUT ####
- Built off of the Build-A-Blog app
- Integrate User Sign-Up app
- LARGELY borrowing from Get-It-Done app

#### SKELETON ####
- Base HTML for templates
- Login page
- register page
- Blog home (index, all user) page 
- New post page
- View post temp
- Vew Indv. user (singleUser) blog temp
- Logout route (no temp)
- DB w/ User, Blog tables

#### UX OUTLINE ####
- Immediately redirected to blog home
- Nav links at top of page (login, signup, logout, new post)
- See all posts by all pages (ordered?)
    - Title h1, owner p, italics
    - Title links to view post temp
    - owner links to indv. user page
- If not signed in, new post nav link will redirect to login
- Login requires username (not email) and password
    - Errors if field(s) left empty, user doesn't exist (suggest sign-up), password not match db
    - Redirected to New Post page if successful
- New post page taken from Build-A-Blog, redirects to home page 


#### ROUTES ####

# '/':
Template: index.html
For each user of Blogz, add list item with link to '/blog?user={{userId}}'

# '/login':
Template: login.html
Form (no action, method='post')
Formatted as table with username and password inputs and login button
HTML formatted error messages for now
Errors for unregistered user, wrong/mismatched passowrd
Seccess adds username to session, redirects to '/newpost'

# '/signup':
Template: signup.html
Form similar to 'login', but with added verify field
validation pulled from 'User Signup', but username instead of email
Seccess adds username to session, redirects to '/newpost'

# '/logout':
No template
Delete username from session and redirect to '/blog'

# '/blog':
Template: blogs-all.html
For each post by every user, display <h3>title</h3>, <p>text</p> and <h5>owner</h5> (ital)
Owner links to all posts by that user ( '/blog?user={{userId}}' )
Title links to '/viewpost?postId={{postId}}' 

# '/viewpost':
Template: veiwpost.html
<h1>title</h1>, <p>text</p>, <h5>owner</h5> (ital)
Owner links to '/blog?user={{userId}}'
