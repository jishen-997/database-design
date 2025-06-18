import subprocess

def check_mysql_service():
    try:
        command = 'sc query MySQL80'
        result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
        output = result.stdout.decode('utf-8')
        if 'STATE' in output and 'RUNNING' in output:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    if check_mysql_service():
        print('MySQL service is running.')
    else:
        print('MySQL service is not running.')