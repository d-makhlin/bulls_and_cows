# bulls_and_cows
## Данный бот позволяет играть в игру "быки и коровы"
Быки и коровы — логическая игра, в ходе которой за несколько попыток игрок должен определить,
что задумал бот. Варианты игры могут зависеть от типа отгадываемой последовательности — это 
могут быть числа или слова. После каждой попытки бот выставляет "оценку", указывая количество
угаданного без совпадения с их позициями (количество "коров") и полных совпадений (количество
"быков"). Угадывающий должен анализировать сделанные попытки и полученные оценки. Бот лишь 
сравнивает очередной вариант с задуманным и выставляет оценку по формальным правилам.


В данной версии реализована игра с числами и словами русского языка.

## Установка
- склонируйте проект с github
- в корне проекта выполните `pip install -r requirements.txt`
- выполните `docker-compose up --build -d pymongo`
- выполните `python ./main.py`

Бот будет доступен как **@bulls_and_cows_game_bot**