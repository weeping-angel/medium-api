import os
from medium_api import Medium

medium = Medium(os.getenv('RAPIDAPI_KEY'))

user = medium.user(username = 'nishu-jain')

print('Fullname: ', user.fullname) 
print('username: ', user.username)
print('user_id: ', user._id)
print('bio: ', user.bio)
print('followers: ', user.followers_count)
print('following: ', user.following_count)
print('twitter username: ', user.twitter_username)
print('profile image: ', user.image_url)
print('is_writer_program_enrolled: ', user.is_writer_program_enrolled)
