import hashlib
import math
import time as t


def calc_entropy(password):
    # entropy=log2(c^l)
    cardinality = calc_cardinality(password)
    length = len(password)
    sample_space = (cardinality) ** (length)
    entropy = math.log(sample_space,2)
    return entropy



def calc_cardinality(password):

    lower, upper, digits, symbols = 0, 0, 0, 0
    for char in password:
        if char.islower():
            lower = 26
        elif char.isdigit():
            digits = 10
        elif char.isupper():
            upper = 26
        else:
            symbols = 33
    cardinality = lower + digits + upper + symbols

    return cardinality

SINGLE_GUESS = .010
NUM_ATTACKERS = 100 # number of cores guessing in parallel.

SECONDS_PER_GUESS = SINGLE_GUESS / NUM_ATTACKERS

def entropy_to_crack_time(entropy):

    crack_time= (0.5 * math.pow(2, entropy)) * SECONDS_PER_GUESS # average, not total
    return crack_time

def round_to_x_digits(number, digits):

    return round(number * math.pow(10, digits)) / math.pow(10, digits)

def display_time(seconds):

    minute = 60
    hour = minute * 60
    day = hour * 24
    month = day * 31
    year = month * 12
    century = year * 100
    if seconds < minute:
        return 'instant'
    elif seconds < hour:
        return str(1 + math.ceil(seconds / minute)) + " minutes"
    elif seconds < day:
        return str(1 + math.ceil(seconds / hour)) + " hours"
    elif seconds < month:
        return str(1 + math.ceil(seconds / day)) + " days"
    elif seconds < year:
        return str(1 + math.ceil(seconds / month)) + " months"
    elif seconds < century:
        return str(1 + math.ceil(seconds / year)) + " years"
    else:
        return 'centuries'

def crack_time_to_score(seconds):

    if seconds < math.pow(10, 2):
        return "Very Weak" # too guessable: risky password.-very weak
    if seconds < math.pow(10, 4):
        return "Weak" # very guessable-weak
    if seconds < math.pow(10, 6):
        return "Reasonable" # somewhat guessable-reasonable
    if seconds < math.pow(10, 8):
        return "Strong" # safely unguessable-strong
    return "Very Strong" # very unguessable-very strong

def strength(password,flag):
    '''
     This function will return details of user password
     with entropy,crack-time,strength etc
    '''
    entropy=calc_entropy(password)
    if (flag==1): # if the user password exists in the wordlist then by using dictionary_attack we calcualte cracktime
        crack_time, fg = dictionary_attack(hash(password))
    else:
        crack_time = entropy_to_crack_time(entropy)
    return{
        'Password':password,
        'Entropy':round_to_x_digits(entropy,3),
        'Crack time(sec)':round_to_x_digits(crack_time,3),
        'Crack time':display_time(crack_time),
        'Strength':crack_time_to_score(crack_time)
    }

def dictionary_attack(hash):

    startTime = t.time()
    wordlist = 'strength_estimator/wordlist.txt'
    flag = 0
    try:
        pass_file = open(wordlist, 'r')
    except:
        print('no file found')
        quit()
    for word in pass_file:
        enc_wrd = word.encode('utf-8')
        digest = hashlib.sha256(enc_wrd.strip()).hexdigest()
        # print(word+': '+digest)
        if digest == hash:
            # print("(using dictionary attack) Password found: "+word)
            flag = 1
            endTime = t.time()
            elapsedTime = endTime - startTime
            # print(" That took ", elapsedTime, " seconds to crack!")
            return elapsedTime,flag
            break

    if flag == 0:
        # print("Your password not found :(using dictionary attack)")
        time=-1
        return time,flag

def hash(password):
    '''
     This function will generate a sha256 hash for the given password
    '''
    pass_hash = hashlib.sha256((password.strip()).encode('utf-8').strip()).hexdigest()
    return pass_hash
'''
def main():
    password=input("Enter your password:")
    passhash=hash(password)
    et,fg=dictionary_attack(passhash)
    #print(et,fg)
    result=strength(password,fg)
    print(result)

if __name__ == "__main__":
    main()
'''
