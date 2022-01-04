import smtplib

server=smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login('threedongscap@gmail.com','th3odor3')

server.sendmail('Three Dongs', '2023083777@tmomail.net', 'Test')