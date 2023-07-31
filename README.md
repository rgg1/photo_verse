# PhotoVerse

## Description

This is a Django social media project, currently hosted online at "https://photo-verse.com".
This website supports many functionalities, such as making posts with photos and captions, customizing your profile,
following other users, liking and commenting on posts, messaging other users, deleting posts,
deleting your account, searching for other users, changing your timezone, and getting notifications
for any time someone follows you, messages you, likes your post, or comments on your post.

I also integrated the website with AWS, with my static and media files hosted on an S3 bucket,
my database using an RDS PostgreSQL database, hosting on an EC2 instance, and even
using AWS SES to send emails to users with password reset links if they request one.

## Installation

### Prerequisites
- Python
- PostgreSQL
- AWS Credentials (if using AWS services for production)

### Steps
1. Clone the repository: `git clone https://github.com/rgg1/photo_verse.git`
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
4. Install required packages: `pip install -r requirements.txt`
5. Apply database migrations: `python manage.py migrate`
6. Run the server: `python manage.py runserver`

## Local Configuration Guide

To run this project locally or in your own production environment, you'll need to make some changes to the `settings.py` file:

### 1. **Django Secret Key**:
   - Generate a new secret key for Django. You can use [Django's Secret Key Generator](https://djecrety.ir/) or another tool.
   - Add it as an environment variable named `'DJANGO_SECRET_KEY'`, or modify `SECRET_KEY` in `settings.py` directly.

### 2. **Database Configuration**:
   - Set up a local PostgreSQL database, or configure a remote one.
   - Add environment variables for the database connection, including:
      - `'DJANGO_DB_NAME'`: Database name
      - `'DJANGO_DB_USER'`: Database user
      - `'DJANGO_DB_PASSWORD'`: Database password
      - `'DJANGO_DB_HOST'`: Database host
      - `'DJANGO_DB_PORT'`: Database port
   - Alternatively, you can modify the `DATABASES` dictionary in `settings.py` directly.

### 3. **Email Configuration (optional)**:
   - If you want to send emails (exclusively for password resets), configure the email settings with environment variables:
      - `'DJANGO_EMAIL_HOST'`: SMTP server
      - `'DJANGO_EMAIL_PORT'`: Port, default 587
      - `'DJANGO_EMAIL_USE_TLS'`: Use TLS, 'True' or 'False'
      - `'DJANGO_EMAIL_HOST_USER'`: SMTP user
      - `'DJANGO_EMAIL_HOST_PASSWORD'`: SMTP password
      - `'DJANGO_DEFAULT_FROM_EMAIL'`: Default from email address
   - For local development, you might prefer to uncomment the line `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` to send emails to the console instead.

### 4. **AWS Configuration (if not in DEBUG mode)**:
   - If running in production (`DEBUG = False`), configure AWS S3 for static and media file storage.
   - Modify the bucket name to your own bucket name.
   - Ensure appropriate AWS credentials and permissions are set up.

### 5. **Allowed Hosts**:
   - Update the `ALLOWED_HOSTS` list with your domain name, IP address, or other hosts as needed.

By configuring these settings, you should be able to run the project in a local or custom production environment.

Note that the AWS S3 configuration is required for production deployments, so if you're not planning to use S3, you would need to make further changes to how static and media files are served.

## Usage

This section provides a general guide on how to navigate and interact with PhotoVerse.

### Logging In
1. Visit the page at [PhotoVerse](https://photo-verse.com).
2. Register with an email, username, and password or login if you've already made an account
(note: you can easily delete your account and any posts afterwards if you wish).

### Making a Post
1. Click the "New Post" button at the top left of the main page.
2. Upload your photo (might error if photo is too large, supports PNG and JPG).
3. Add a caption to your photo (optional).
4. Click "Post" to post.
5. If you click on "View Profile" at the top of the main page, you can see your posts and delete them if you wish.

### Following Other Users
1. Search for a user by using the search bar (or by finding them in the "Popular Users" section to the right).
2. Visit their profile page.
3. Click the "Follow" button next to their username.
4. After this, you should see any posts they've made in your feed, which you can then like and comment on.

### Messaging Other Users
1. Search for a user by using the search bar (or by finding them in the "Popular Users" section to the right).
2. Visit their profile page.
3. Click the "Message" button next to their username.
4. Send them any message. You can view conversations with the "Messages" button on the main page.

### Editing Your Profile
1. Click the "Edit Profile" button at the top of the main page.
2. Upload a profile photo, change your display name, change your bio, or change your timezone (all optional).
3. The "Delete Account" button is at the bottom left of this page and deletes your account after you confirm on the confirmation page.