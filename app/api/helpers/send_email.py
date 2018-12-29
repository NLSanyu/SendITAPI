import smtplib
from email.mime.text import MIMEText

me = 'lydiansanyu@yahoo.com'

def send_email(email, which, data):
	if which == 'status':
		message = "The status of your parcel has been updated to " + data

	if which == 'present_location':
		message = "The present location of your parcel has been updated to " + data

	msg = MIMEText(message)

	# me == the sender's email address
	# you == the recipient's email address
	msg['Subject'] = 'SendIT: Updates on parcel'
	msg['From'] = me
	msg['To'] = email

	s = smtplib.SMTP('localhost')
	s.sendmail(me, [email], msg.as_string())
	s.quit()