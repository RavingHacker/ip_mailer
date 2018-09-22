import requests
import smtplib
import time

smtp_url = "smtp.gmail.com"
smtp_port = 587
usernmae = ""
password = ""
reciever = ""

OPT_LOG = False

ip_log_file_path = "ip_log.txt"
log_file_path = "log_file.txt"

def read_saved_ip(ip_log_file_path):
    with open(ip_log_file_path) as f:
        current_ip = f.readlines()
    current_ip.strip()
    if len(current_ip) < 1:
        current_ip = get_pb_ip()
        write_new_ip(ip_log_file_path, current_ip)

    return current_ip

def write_new_ip(ip_log_file_path, new_ip):

    with open(ip_log_file_path, "w") as f:
        f.write(new_ip)

def write_log(log_message):
    global log_file_path
    with open(log_file_path, "w") as f:
        f.write(log_message)


def get_pb_ip():

    try:
        pb_ip = requests.get(url="https://ipinfo.io/ip")
        return pb_ip.text

    except (requests.exceptions.ConnectionError, TimeoutError, requests.exceptions.Timeout,
                requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
        print("Exception while getting IP: {}".format(e))

def mail_new_ip(new_ip):

    global smtp_url
    global smtp_port
    global username
    global password
    global reciever

    header = 'To:' + reciever + '\n' + 'From: ' + username + '\n' + 'Subject:New Public IP \n'
    message = header + "\n The new Public IP is: " + new_ip + "\n\n"
    smtp_session = smtplib.SMTP_SSL(smtp_url, smtp_port)

    try:
        smtp_session.ehlo()
        smtp_session.starttls()
        smtp_session.ehlo()
        smtp_session.login(username, password)
        smtp_session.sendmail(username, reciever, message)
        smtp_session.quit()

    except Exception as e:
        print("Exception while sending mail: {}".format(e))

def compare_pb_ip(ip_log_file_path):

    saved_ip = read_saved_ip(ip_log_file_path)
    actual_ip = get_pb_ip()

    if saved_ip != actual_ip:
        write_new_ip(log_file_path, actual_ip)
        mail_new_ip(actual_ip)