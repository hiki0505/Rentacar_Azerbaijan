import random


def otp_generator():
    otp = random.randint(999, 9999)
    return otp


# def send_otp(phone):
#     """
#     This is an helper function to send otp to session stored phones or
#     passed phone number as argument.
#     """
#
#     if phone:
#
#         key = otp_generator()
#         phone = str(phone)
#         otp_key = str(key)
#         print('Otp sent to the client...')
#         # link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=fc9e5177-b3e7-11e8-a895-0200cd936042&to={phone}&from=wisfrg&templatename=wisfrags&var1={otp_key}'
#
#         # result = requests.get(link, verify=False)
#
#         return otp_key
#     else:
#         return False

def send_otp(phone, otp_key):
    """
    This is an helper function to send otp to session stored phones or
    passed phone number as argument.
    """

    if phone:

        # key = otp_generator()
        # phone = str(phone)
        # otp_key = str(key)
        # print('Otp sent to the client...')
        # # link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=fc9e5177-b3e7-11e8-a895-0200cd936042&to={phone}&from=wisfrg&templatename=wisfrags&var1={otp_key}'
        #
        # # result = requests.get(link, verify=False)
        print('Otp sent to the client...', otp_key)
        return otp_key
    else:
        return False
