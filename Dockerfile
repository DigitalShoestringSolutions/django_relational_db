FROM python:3.13
# Set environment variables to prevent Python from writing pyc files to disc and buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./code/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt && rm -f /requirements.txt
WORKDIR /app
ADD ./code /app/

# expect to copy extra_requirements.txt use extra_requirements.* to prevent error if not present
COPY --from=solution_config extra_requirements.* /
# pip install if extra_requirements file exists
RUN [ -f "/extra_requirements.txt" ] && pip install -r /extra_requirements.txt && rm -f /extra_requirements.txt || echo "no extra_requirements.txt"

COPY  --from=solution_config django_apps/. /app/
COPY  --from=solution_config module_settings.py /app/module_settings.py
