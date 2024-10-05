# Simple RAG

This project is a simple implementation of a Retrieval-Augmented Generation (RAG) model using Python. The project is designed to run on AWS Lambda using a Docker container.

## Project Structure
.gitignore Dockerfile readme.md requirements.txt simple_rag.py vectorstore/ cb12a7c6-c332-4717-845f-002701d34523/ chroma.sqlite3


## Files

- `Dockerfile`: Defines the Docker image for the AWS Lambda function.
- `requirements.txt`: Lists the Python dependencies.
- `simple_rag.py`: The main script for the RAG model.
- `vectorstore/`: Directory containing vector store data.

## Setup

1. **Build the Docker Image:**

    ```sh
    docker build -t simple-rag .
    ```

2. **Run the Docker Container:**

    ```sh
    docker run -p 9000:8080 simple-rag
    ```

3. **Invoke the Lambda Function:**

    You can invoke the Lambda function locally using the AWS CLI:

    ```sh
    aws lambda invoke --function-name simple-rag --endpoint-url http://localhost:9000 --payload '{}' response.json
    ```

## Usage

The main entry point for the Lambda function is the `lambda_handler` function in [`simple_rag.py`](simple_rag.py).

## Dependencies

The dependencies are listed in the [`requirements.txt`](requirements.txt) file and are installed during the Docker build process.

## License

This project is licensed under the MIT License.