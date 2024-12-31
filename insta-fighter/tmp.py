from ensta import Host as InstaClient
# shimabukurocoder Publ1cPassw0rd
mobile = InstaClient('shimabukurocoder@proton.me', 'Publ1cPassw0rd')
profile = mobile.profile("ethkyiv_ua")
print(profile.full_name)

# import instaloader
# insta = instaloader.Instaloader()
# insta.login('shimabukurocoder', 'Publ1cPassw0rd')