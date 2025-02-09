# Research Project

This project is designed for managing and conducting research related to master's studies. It includes various components for setting up Python execution environments, running simulations, and performing numerical computations.

## Project Structure

- **docker-jupyterlab**: This directory contains the setup for a Python execution environment using Docker. It provides a JupyterLab interface for running Python scripts and managing research tasks.
- **googleColabEnv**: This directory includes various subdirectories with programs for numerical computations, simulations, and dispatch models.

## Setting Up the Environment

### Docker JupyterLab

To set up the Python execution environment using Docker, follow these steps:

1. Navigate to the `Research/docker-jupyterlab` directory.
2. Build and start the Docker container:
   ```bash
   docker compose up -d --build
   ```
3. Verify the container is running:
   ```bash
   docker container ls
   ```
4. Connect to the Python environment:
   ```bash
   docker compose exec -it jupyterlab bash
   ```
5. Install Python libraries:
   ```bash
   python -m pip install numpy
   ```
6. Run the sample program:
   ```bash
   python sample.py
   ```
7. Retrieve the JupyterLab token and set it in the `.env` file.
8. Rebuild the Docker container:
   ```bash
   docker compose up -d --build
   ```

Access JupyterLab at [http://localhost:8888](http://localhost:8888).

### Google Colab Environment

The `googleColabEnv` directory contains various programs for different research tasks:

- **/analysis**: Experimental numerical computation programs.
- **/assignmentProblem**: Simulates bike and user assignment, outputting bike distribution.
- **/bikeSharePerMinute**: Simulates taxi data for the first minute.
- **/environmentCheck**: Checks machine specs for numerical computations.
- **/formatLookUpCSV**: Generates CSV mapping location IDs to coordinates.
- **/neighborhoodBasedDispatchModel**: Assigns the nearest bike to users.
- **/optimizationBasedDispatchModel**: Implements objective functions and constraints.
- **/randomBasedDispatchModel**: Randomly assigns bikes as a baseline for comparison.
- **/routingProblem**: Sample program for optimization problems.
- **/withoutStackOptBasedDispatchModel**: Applies optimization model without stacking requests.

## Contributing

Contributions to this project are welcome. Please ensure that any changes are well-documented and tested.
