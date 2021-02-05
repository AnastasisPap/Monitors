def append_to_logs(message):
    with open('logs.txt', 'a') as logs:
        logs.write(message)
