FROM python:3.8
ADD app/requirement.txt /requirement.txt
#ADD app/ssh /root/.ssh
WORKDIR /
RUN pip install -r requirement.txt
ADD app /app
WORKDIR /app
EXPOSE 9999
CMD cd /app && python app.py

