#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

COMPOSE_CMD="docker compose --env-file .env -f docker-compose.dev.yml"

echo "1) Development"
echo "2) Production"
read -p "Enter: " MODE

if [ "$MODE" = "1" ]; then
    read -p "Are there database/schema updates? [y/N]: " HAS_DB_UPDATES

    echo "Starting DB..."
    $COMPOSE_CMD up -d db

    echo "Waiting for PostgreSQL to be ready..."
    until $COMPOSE_CMD exec db pg_isready -U "${DB_USER:-postgres}" -d "${DB_NAME:-postgres}" > /dev/null 2>&1; do
        sleep 1
    done

    if [[ "$HAS_DB_UPDATES" =~ ^[Yy]$ ]]; then
        echo "Running migrations..."
        $COMPOSE_CMD run --rm app python manage.py makemigrations
        $COMPOSE_CMD run --rm app python manage.py migrate
    fi

    echo "Collecting static files..."
    $COMPOSE_CMD run --rm app python manage.py collectstatic --noinput

    echo "Starting all services (Nginx, 3 Django App instances, DB)..."
    $COMPOSE_CMD up -d --build --force-recreate --scale app=3

    echo "App live at: http://localhost"

elif [ "$MODE" = "2" ]; then
    read -p "Enter branch to push (default: main): " BRANCH
    BRANCH=${BRANCH:-main}
    read -p "Enter commit message: " MSG

    cd ..
    git add .
    git commit -m "$MSG" || echo "No new changes to commit."
    git push origin "$BRANCH"
    echo "Pushed successfully."
else
    echo "Invalid option. Exiting."
    exit 1
fi