# Dynamic Fee Model for Uniswap V3

This project implements a dynamic fee model for Uniswap V3 using real-time data from the Ethereum blockchain. It uses machine learning to predict optimal fees based on market conditions.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/chandshantanu/dynamicfeeModel.git
   cd dynamicfeeModel
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Copy `.env.example` to `.env`
   - Fill in the required values in `.env`

## Running the Project

### Using Python directly:

```
python -m src.main
```

### Using Docker:

1. Build the Docker image:
   ```
   docker-compose build
   ```

2. Run the container:
   ```
   docker-compose up -d
   ```

## Running Tests

```
python -m unittest discover tests
```

## Project Structure

- `src/`: Contains the main application code
- `tests/`: Contains unit tests
- `abis/`: Contains ABI files for smart contracts
- `Dockerfile` and `docker-compose.yml`: For containerization
- `requirements.txt`: Python dependencies

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.