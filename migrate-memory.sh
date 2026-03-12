#!/bin/bash
# migrate-memory.sh — Миграция памяти Claude Code с сервера на локалку
#
# Использование:
#   ./migrate-memory.sh /path/to/allabushka-openclaw /path/to/web-hunter /path/to/sumbawa-openclaw
#
# Или с именованными параметрами:
#   ./migrate-memory.sh --allabushka ~/projects/allabushka --webhunter ~/projects/web-hunter --sumbawa ~/projects/sumbawa
#
# Скрипт:
# 1. Берёт memory-export/ из каждого репо
# 2. Вычисляет правильный путь ~/.claude/projects/<encoded-path>/memory/
# 3. Копирует файлы памяти

set -euo pipefail

CLAUDE_DIR="${HOME}/.claude"

# Encode path for Claude Code memory directory name
# /Users/john/projects/allabushka -> -Users-john-projects-allabushka
encode_path() {
    local path="$1"
    # Resolve to absolute path
    path="$(cd "$path" && pwd)"
    # Replace / with -
    echo "$path" | sed 's|/|-|g'
}

migrate_project() {
    local project_dir="$1"
    local project_name="$2"

    if [ ! -d "$project_dir" ]; then
        echo "SKIP: $project_name — директория $project_dir не найдена"
        return 1
    fi

    local export_dir="$project_dir/memory-export"
    if [ ! -d "$export_dir" ]; then
        echo "SKIP: $project_name — нет memory-export/ в $project_dir"
        return 1
    fi

    local encoded="$(encode_path "$project_dir")"
    local memory_dir="$CLAUDE_DIR/projects/$encoded/memory"

    echo ""
    echo "=== $project_name ==="
    echo "  Источник:  $export_dir"
    echo "  Назначение: $memory_dir"

    mkdir -p "$memory_dir"

    local count=0
    for f in "$export_dir"/*.md; do
        [ -f "$f" ] || continue
        local fname="$(basename "$f")"
        if [ -f "$memory_dir/$fname" ]; then
            echo "  СУЩЕСТВУЕТ: $fname (пропускаю, удали вручную если нужна перезапись)"
        else
            cp "$f" "$memory_dir/$fname"
            echo "  СКОПИРОВАН: $fname"
            count=$((count + 1))
        fi
    done

    echo "  Итого: $count файлов скопировано"
}

# Parse arguments
ALLABUSHKA=""
WEBHUNTER=""
SUMBAWA=""

if [ $# -eq 0 ]; then
    echo "Использование:"
    echo "  $0 /path/to/allabushka /path/to/web-hunter /path/to/sumbawa"
    echo ""
    echo "  $0 --allabushka ~/allabushka --webhunter ~/web-hunter --sumbawa ~/sumbawa"
    echo ""
    echo "Можно указать не все проекты — пропущенные будут проигнорированы."
    exit 1
fi

# Check for named parameters
while [ $# -gt 0 ]; do
    case "$1" in
        --allabushka) ALLABUSHKA="$2"; shift 2 ;;
        --webhunter)  WEBHUNTER="$2"; shift 2 ;;
        --sumbawa)    SUMBAWA="$2"; shift 2 ;;
        *)
            # Positional arguments
            if [ -z "$ALLABUSHKA" ]; then
                ALLABUSHKA="$1"
            elif [ -z "$WEBHUNTER" ]; then
                WEBHUNTER="$1"
            elif [ -z "$SUMBAWA" ]; then
                SUMBAWA="$1"
            fi
            shift
            ;;
    esac
done

echo "Claude Code Memory Migration"
echo "============================="
echo "Claude dir: $CLAUDE_DIR"

[ -n "$ALLABUSHKA" ] && migrate_project "$ALLABUSHKA" "Allabushka"
[ -n "$WEBHUNTER" ]  && migrate_project "$WEBHUNTER"  "Web-Hunter / ForgeSite"
[ -n "$SUMBAWA" ]    && migrate_project "$SUMBAWA"     "Sumbawa OpenClaw"

echo ""
echo "Готово! Память будет подхвачена Claude Code при следующем открытии проекта."
echo ""
echo "Также скопируй глобальный CLAUDE.md (если нужен):"
echo "  scp server:~/.claude/CLAUDE.md ~/.claude/CLAUDE.md"
