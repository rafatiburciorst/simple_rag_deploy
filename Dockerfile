FROM public.ecr.aws/lambda/python:3.12

RUN microdnf update -y && microdnf install -y gcc-c++ make

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

COPY DOC-SF238339076816-20230503.pdf ${LAMBDA_TASK_ROOT}/DOC-SF238339076816-20230503.pdf

COPY simple_rag.py ${LAMBDA_TASK_ROOT}

RUN chmod +x simple_rag.py

CMD ["simple_rag.lambda_handler"]