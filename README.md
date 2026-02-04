# steam-download-monitor
Script for monitoring Steam download speed via logs
# Steam Download Monitor

Скрипт отслеживает скорость загрузки игр в Steam через логи клиента.

## Возможности
- Автоматически находит Steam через Windows Registry
- Читает статус загрузки из content_log.txt
- Выводит скорость раз в минуту (5 минут)
- Учитывает паузу загрузки
- Показывает AppID скачиваемой игры

## Ограничение
Steam не всегда пишет скорость в лог во время установки или распаковки файлов.
