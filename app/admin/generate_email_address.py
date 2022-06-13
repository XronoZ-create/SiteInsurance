def generate_email_address(email_address):
    domain = email_address.split("@")[1]
    email_address = email_address.replace(f"@{domain}", "@gmail.com")

    f=lambda s:s[11:]and[s[0]+w+x for x in f(s[1:])for w in('.','')]or[s]

    email_address_list = []
    for s in f(email_address):
        if len(s) <= 40 and s.count('.') < 5:
            email_address_list.append(s.replace("@gmail.com", f"@{domain}"))

    return email_address_list

if __name__ == "__main__":
    from app.databases.models_email import Email
    from app.databases.database_email import SessionLocal as SessionLocalEmail

    print(generate_email_address(email_address="test@mardsgovna.xyz"))