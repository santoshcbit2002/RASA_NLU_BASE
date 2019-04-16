def send_mail(email_address, subject, body):
	print(email_address)
	print(subject)
	print(body)
	return True

if __name__ == '__main__':
	success = send_mail('address', 'subject', 'body')
	print(success)