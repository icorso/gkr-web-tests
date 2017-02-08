import argparse
from datetime import datetime, timedelta
import os

from subprocess import Popen


def configure_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_url", action="store", default="http://10.150.250.73")
    parser.add_argument("--browser", action="store", default="firefox")
    parser.add_argument("--element_wait", action="store", default=10)
    parser.add_argument("--page_load_timeout", action="store", default=30)
    parser.add_argument("--element_init_timeout", action="store", default=0.1)
    parser.add_argument("--mysqlhost", action="store", default="10.150.250.73")
    parser.add_argument("--mysqluser", action="store", default="root")
    parser.add_argument("--mysqlpassword", action="store", default="toor")
    parser.add_argument("--mysqldb", action="store", default="qsystem")

    '''
    Параметр tests_root используется, когда нужно запустить отдельный тест (или модуль) в несколько потоков.
    Пример :
        запуск одного теста "--tests_root tests/auth/test_auth.py::TestAuth::test_not_exist_login"
        запуск модуля "--tests_root tests/auth/test_auth.py"
        запуск отдельного пакета "--tests_root tests/some_package/"
    '''
    parser.add_argument("--tests_root", action="store", dest="tests_root", default='tests')
    parser.add_argument("--timeslot_date", action="store", dest="timeslot_date",
                        default=(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'))
    parser.add_argument("--threads", action="store", dest="threads", type=int, default=1)
    parser.add_argument("--alluredir", action="store")
    parser.add_argument("--python", action="store", dest="python", required=True)
    parser.add_argument("--attempts", action="store", dest="attempts", type=int, default=3)
    parser.add_argument("--failed", action="store_true")
    args = parser.parse_args()
    return args


def main():
    opt = configure_args()
    d = vars(opt)
    args = ''
    for key in d:
        if key not in ('threads', 'python', 'failed'):
            args += '--' + key + ' \"' + str(d[key]) + '\" '

    opt_string = str(opt.python + ' -m pytest %s' % args).replace('\\', '/')
    if opt.failed:
        opt_string += " --failed "

    processes = []
    if '.py' not in opt.tests_root:
        for root, directories, filenames in os.walk(opt.tests_root):
            '''
            в подкаталогах должны отсутствовать файлы с "__", например __init__.py
            '''
            if '__' not in root:
                for filename in filenames:
                    processes.append(opt_string + os.path.join(root, filename))
    else:
        for num in range(0, opt.threads):
            processes.append(opt_string + opt.tests_root)

    launch = [processes[i:i + opt.threads] for i in range(0, len(processes), opt.threads)]

    for l in launch:
        threads = None
        for p in l:
            threads = Popen(p, shell=True)
        threads.communicate()

if __name__ == "__main__":
    main()
