FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml README.md ./
COPY backend ./backend
RUN pip install --no-cache-dir .
RUN useradd --create-home nova && mkdir -p /app/data && chown -R nova:nova /app
USER nova
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
