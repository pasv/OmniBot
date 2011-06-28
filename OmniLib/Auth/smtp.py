import smtplib
import dns.resolver
from email.mime.text import MIMEText

from_email = "OmniBot@yahoo.com" # dont tell them, i assume this is not used tho..

def send_email(email, userstring, genkey):
    try:
	domain = email[email.find("@")+1:]
	servers = dns.resolver.query(domain, 'MX')
    except:
	return -2
    
    msg = MIMEText("User: " + userstring + " has generated this key: " + genkey)
    msg['Subject'] = 'Your OmniBot code has geen generated'
    msg['From'] = from_email
    msg['To'] = email
    our_smtp = servers[0].to_text() # lets use the first response# add more checks later
    our_smtp = our_smtp[our_smtp.find(" ")+1:] # take out the 
 #   try:
    print our_smtp
    
    s = smtplib.SMTP(our_smtp)
    s.sendmail(from_email, [email], msg.as_string())
#    except:
#	return -1 ## lets make some better error catching later
    s.quit()