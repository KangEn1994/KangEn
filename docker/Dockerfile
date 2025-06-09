FROM python:1.0
# registry.cn-hangzhou.aliyuncs.com/kang_en/python
ADD app/requirement.txt /requirement.txt
#ADD app/ssh /root/.ssh
WORKDIR /
RUN pip install -r requirement.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
ADD app /app
WORKDIR /app
EXPOSE 9999
CMD cd /app && python app.py