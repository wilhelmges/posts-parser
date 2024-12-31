import requests
from ensta import Mobile
#import moviepy.editor as mp

# Create a session
session = requests.Session()
# Define your custom headers
custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    # Add any other necessary headers here
}
# Update the session with custom headers
session.headers.update(custom_headers)
#  shimabukurocoder Publ1cPassw0rd
# Use the session in Ensta
mobile = Mobile(username='shimabukurocoder', password='Publ1cPassw0rd') #, session=session)

# Example of fetching profile info
profile = mobile.profile('shimabukurocoder')
print(profile.full_name)
