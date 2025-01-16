FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .
RUN conda env create -f environment.yml

# 设置PATH以使用新环境
ENV PATH=/opt/conda/envs/myenv/bin:$PATH

COPY . .

# 使用新环境运行应用
CMD ["python", "app.py"]
