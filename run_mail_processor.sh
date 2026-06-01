#!/bin/bash
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' 

echo -e "${YELLOW}Запуск системы обработки почты...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ОШИБКА: Python 3 не установлен или не добавлен в PATH.${NC}"
    exit 1
fi

INBOX_DIR="inbox"
if [ ! -d "$INBOX_DIR" ]; then
    echo -e "${RED}ОШИБКА: Директория с входящими письмами '$INBOX_DIR' не найдена!${NC}"
    exit 1
fi

OUTPUT_DIR="output"
mkdir -p "$OUTPUT_DIR"

echo -e "Анализ файлов в директории $INBOX_DIR..."

python3 -m src.main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Обработка почты завершена успешно, без критических сбоев.${NC}"
    echo -e "Результаты сохранены в директорию: $OUTPUT_DIR"
else
    echo -e "${RED}КРИТИЧЕСКАЯ ОШИБКА: Python-скрипт завершился аварийно.${NC}"
    exit 1
fi