import subprocess
from croniter import croniter
from datetime import datetime, timedelta
import pytz
from functions.playdb import all_add_tests, update_next_time, get_condition
from concurrent.futures import ThreadPoolExecutor

now = datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S")
now = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")

print(f'\n начало работы {now} \n')

p1 = (datetime.now(pytz.utc) + timedelta(seconds=30)).strftime("%Y-%m-%d %H:%M:%S")  # время now + 30 секунд для сравнения
p1 = datetime.strptime(p1, "%Y-%m-%d %H:%M:%S")

all1 = all_add_tests()

for i in all1:
    id = i[0]
    time = i[1]
    next = i[2]
    condition = int(get_condition(id))
    iter = croniter(time)
    cur_dt = iter.get_next(datetime)
    print(f'просто получил id:{id} time:{time} next_time:{next} condition:{condition}')
    if condition == 2 or not next:
        print(f'я обновил время id: {id}')
        update_next_time(id, cur_dt)

def run_test(command, id):
    print(f'выполнить тест {id}')
    res = subprocess.run(command, shell=True, text=True)
    if res.returncode != 0:
        print(f'ошибка при выполнении теста {id}: {res.stderr}')
    else:
        print(f'тест {id} успешно выполнен')

all2 = all_add_tests()

with ThreadPoolExecutor(max_workers=None) as executor:
    futures = []

    for j in all2:
        id = j[0]
        time = j[1]
        next = j[2]
        condition = int(get_condition(id))

        next_dt = next if next else None
        command = 'python3 ' + j[3]

        print(f'проверка теста {id}: next={next_dt}, now={now}, p1={p1}, condition={condition}')

        if next_dt:
            if (next_dt >= now and next_dt < p1 and condition == 0) or (next_dt < now and condition == 0):
                future = executor.submit(run_test, command, id)
                futures.append(future)
            else:
                print('еще не пришло время')
        else:
            print('нет добавленных тестов')

    for future in futures:
        future.result()
