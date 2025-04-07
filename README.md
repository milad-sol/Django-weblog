# Weblog Project
A feature-rich blogging platform built with Django and Django REST Framework.
## Project Overview
This is a modern blogging application that includes user authentication, post management, comments, and more. The project features a custom user model, category management, and SEO optimization for blog posts.
## Features
- **User Management**
    - Custom user model with email, phone number, and username fields
    - Profile image and bio support
    - Secure authentication system

- **Blog Management**
    - Post creation and publishing
    - Category organization
    - Rich text content editing with CKEditor
    - Featured images for posts
    - Breaking news designation
    - SEO optimization with meta titles and descriptions
    - Comment system with reply functionality

- **Additional Features**
    - Contact form for visitor inquiries
    - About page content management
    - Static and media file handling

## Tech Stack
- **Framework**: Django
- **API**: Django REST Framework
- **Text Editor**: CKEditor integration
- **Authentication**: Custom user model

## Project Structure
The project consists of the following Django apps:
- **accounts**: User management and authentication
- **posts**: Blog post, category, and comment management
- **home**: Main homepage and site-wide functionality
- **contact**: Contact form handling
- **about**: About page content management

## Models
### User
- Custom user model with phone number as username field
- Profile image and bio support
- Admin/superuser functionality

### Post
- Title, slug, and rich text content
- Featured image support
- Category assignment
- Breaking news designation
- Publication status toggle
- SEO optimization fields

### Category
- Title and slug fields
- Description content
- SEO optimization

### Comment
- Nested reply functionality
- User attribution
- Content management

## Installation and Setup
1. Clone the repository:
``` bash
git clone https://github.com/yourusername/weblog.git
cd weblog
```
1. Create and activate a virtual environment:
``` bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
1. Install dependencies:
``` bash
pip install -r requirements.txt
```
1. Apply migrations:
``` bash
python manage.py migrate
```
1. Create a superuser:
``` bash
python manage.py createsuperuser
```
1. Run the development server:
``` bash
python manage.py runserver
```
1. Access the admin interface at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
