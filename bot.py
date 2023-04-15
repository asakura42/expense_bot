import telebot

# create a Bot instance
bot = telebot.TeleBot("token")

# define a list to store numbers
num_list = []

# define a function to write numbers to a file
def write_num_list_to_file():
    with open("numbers.txt", "w") as f:
        for num in num_list:
            f.write("{}\n".format(num))

# define a function to read numbers from a file
def read_num_list_from_file():
    with open("numbers.txt", "r") as f:
        for line in f:
            num_list.append(int(line.strip()))

# define a function to sum all numbers in the list
def sum_num_list():
    return sum(num_list)

# define a function to output the result
def output_result():
    return "Sum of all numbers is: {}".format(sum_num_list())

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hi! I am a bot that records, sums and show your expenses. Type a number to add it to the list, or type '/result' to see the sum of all numbers. Type '/clear' to clear file to start again. Type '/howmuch' to see how much you can spend today.")
    
# Handle '/howmuch'
@bot.message_handler(commands=['howmuch'])
def run_program(message):
    import subprocess
    p = subprocess.Popen('./main | grep "day $(date +%d)"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    line = p.stdout.readline().decode("utf-8")
    output = ""
    while line != '':
        output += line
        line = p.stdout.readline().decode("utf-8")
    bot.reply_to(message, output)

# Handle '/clear'
@bot.message_handler(commands=['clear'])
def clear_num_list(message):
    # read numbers from file
    num_list.clear()
    read_num_list_from_file()
    bot.reply_to(message, output_result())
    # clear numbers.txt file
    open("numbers.txt", "w").close()
    # clear num_list
    num_list.clear()
    bot.reply_to(message, "File cleared!")

# Handle '/result'
@bot.message_handler(commands=['result'])
def output_result_message(message):
    # read numbers from file
    num_list.clear()
    read_num_list_from_file()
    bot.reply_to(message, output_result())

# Handle all other messages with content_type 'text'
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    # read numbers from file
    num_list.clear()
    read_num_list_from_file()
    try:
        num = int(message.text)
        num_list.append(num)
        # write numbers to file
        write_num_list_to_file()
        bot.reply_to(message, "Expense added!")
    except ValueError:
        bot.reply_to(message, "Sorry, I can only take numbers!")

# Run the bot
bot.polling()
