FROM python:3.7
WORKDIR /app
COPY requirements.txt requirements.txt
RUN xargs -L 1 pip install < requirements.txt --no-cache-dir
RUN pip install torch==1.8 torchvision==0.9 -f https://download.pytorch.org/whl/cu101/torch_stable.html --no-cache-dir
RUN pip install 'git+https://github.com/facebookresearch/detectron2' --no-cache-dir
EXPOSE 5000
COPY . /app
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]