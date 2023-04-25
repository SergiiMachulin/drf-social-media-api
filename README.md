# Social Media API
Social Media API backend solution for building social media applications. 
This repository contains a fully functional RESTful API built using DRF and SQLite, 
providing developers with a scalable and efficient way to manage user authentication, profiles, posts, comments and likes. 


# API features

- User Authentication: The API supports user authentication with JWT authentication, 
which allows for secure access to user data and resources.

- User Profiles: The API allows users to create and manage their profiles, 
including their personal information, profile picture, and bio.

- Posts and Comments: Users can create, edit, and delete posts, 
as well as add comments to posts. 
The API provides endpoints to retrieve, update, and delete posts and comments.

- Follow/Unfollow: Users can follow and unfollow other users on the platform, 
and the API provides endpoints to retrieve a user's followers and followers.

- Search: The API allows users to search for other users and posts using keywords.

- Analytics: The API provides analytics for user activities, such as the number 
of likes and comments on posts, as well as user engagement.

# Installation via GitHub

```shell
git clone git@github.com:ZhAlexR/social-media-api.git
cd Cinema-api
python3 -m venv venv
source venv/bin/activete # for linux or macOS
venv\Scripts\activete # for Windows
```

Perform the next commands to create DB:
```shell
python manage.py makemigration
python manage.py migrate
```

Start server:
```shell
python manage.py runserver
```

## Coverage test report of the project
```shell
 
Name                                                                          Stmts   Miss  Cover
-------------------------------------------------------------------------------------------------
follower/admin.py                                                                 5      0   100%
follower/models.py                                                               20      0   100%
follower/serializers.py                                                           6      0   100%
follower/tests.py                                                                86      0   100%
follower/urls.py                                                                  4      0   100%
follower/views.py                                                                61      4    93%
permissions/permissions.py                                                        6      0   100%
posts/admin.py                                                                   33      8    76%
posts/models.py                                                                  23      2    91%
posts/serializers.py                                                             26      0   100%
posts/tests.py                                                                   77      0   100%
posts/urls.py                                                                     7      0   100%
posts/views.py                                                                   82     14    83%
user/admin.py                                                                    26      2    92%
user/models.py                                                                   47     13    72%
user/serializers.py                                                              25      2    92%
user/tests.py                                                                    44      0   100%
user/urls.py                                                                      5      0   100%
user/views.py                                                                    25      0   100%
userprofile/admin.py                                                              6      0   100%
userprofile/models.py                                                             8      0   100%
userprofile/serializers.py                                                        8      0   100%
userprofile/tests.py                                                             56      0   100%
userprofile/urls.py                                                               4      0   100%
userprofile/views.py                                                             46      0   100%
-------------------------------------------------------------------------------------------------
TOTAL                                                                           736     45    95%

```