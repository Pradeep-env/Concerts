#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "1) Development"
echo "2) Production"
read -p "Enter: " MODE

if [ "$MODE" = "1" ]; then
    read -p "Are there database/schema updates? [y/N]: " HAS_DB_UPDATES

    if [[ "$HAS_DB_UPDATES" =~ ^[Yy]$ ]]; then
        echo "Starting DB..."
        docker compose -f docker-compose.dev.yml up -d db

        echo "Waiting for PostgreSQL to be ready..."
        until docker compose -f docker-compose.dev.yml exec db pg_isready -U clickmart_user -d clickmart_db > /dev/null 2>&1; do
            sleep 1
        done

        echo "Running migrations..."
        docker compose -f docker-compose.dev.yml run --rm app python manage.py makemigrations
        docker compose -f docker-compose.dev.yml run --rm app python manage.py migrate
    fi

    echo "Starting all services (Nginx, 3 Django App instances, DB)..."
    docker compose -f docker-compose.dev.yml up -d --build --scale app=3

    echo "App live at: http://localhost"

elif [ "$MODE" = "2" ]; then
    read -p "Enter branch to push (default: main): " BRANCH
    BRANCH=${BRANCH:-main}
    read -p "Enter commit message: " MSG

    cd ..
    git add .
    # Avoid exiting if there are no changes to commit
    git commit -m "$MSG" || echo "No new changes to commit."
    git push origin "$BRANCH"
    echo "Pushed successfully."
else
    echo "Invalid option. Exiting."
    exit 1
fi
