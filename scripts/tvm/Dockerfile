FROM python:3.10.14
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ECM64.py .
COPY sample2_5.py .
RUN mkdir -p /data
CMD ["bash", "-c", "python ECM64.py docker && python sample2_5.py docker"]

# For apple silicon, you may need to build and run the image for amd64 architecture using the following commands:
# docker build  --platform linux/amd64 -f scripts/tvm/Dockerfile -t tvm-initialization scripts/tvm
# docker run --platform linux/amd64 -v $(pwd):/data tvm-initialization