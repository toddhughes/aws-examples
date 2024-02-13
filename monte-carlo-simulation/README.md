# Monte Carlo Simulation

The following example creates an AWS Cloud Formation Stack to build and run a Monte Carlo Simulation within AWS.

The Monte Carlo Simulation is mathematical technique that predicts possible outcomes of an uncertain or random event. It contains three parts: the input variable(s), the output variable, and the mathematical model.

- Input variables: These are the random variables which we will test against the model.
- Output variable: This is the result of the Monte Carlo analysis.
- Mathematical model: This is the function that will perform the analysis.

## The Model

Is this sample, we will use the well-known [Monte Hall problem](https://en.wikipedia.org/wiki/Monty_Hall_problem) as our mathematical model/function. It's a puzzle based on the television game show Let's Make a Deal which uses conditional probability and reasoning.

If you would like to run the model on your local machine, I've included it in a stand-alone script [here](monte_hall_problem.py).

## The Stack

The main pipeline runs using an AWS Step Function and a Distributed Map Task. Read more [here](https://docs.aws.amazon.com/step-functions/latest/dg/use-dist-map-orchestrate-large-scale-parallel-workloads.html). It allows a maximum concurrency of up to 10,000 executions in parallel. 

For simplicity, we chose an AWS Lambda for processing the model. Alternatively, we could scale out our processing using EC2s or Fargate containers, depending on our needs.

The source and destination data are stored using S3 buckets. The ItemReader of the Distributed Map Task requires the input data to be in one of three formats: multiple CSV files, a single JSON file, or an Amazon S3 inventory list. In our state function, we generate CSV data files using an AWS Lambda. Within this Lambda, we use a combination of static input (from our state function config params) and random data (using the Python random library) to simulate the required input for our model.

The final step in our state machine parses the generated output of the Distributed Map Task into a single, easy-to-read CSV file.

Additionally, we've added a first step to delete all files from the S3 buckets. This allows you to run the pipeline multiple times, having different simulation counts--ensuring the results are not commingled.

## Create the Stack

1. Clone the solution from GitHub to your workstation.
2. In the AWS console, open CloudFormation.
3. Click **Create stack**.
4. Under **Specify template**, select **Upload a template file**.
5. Click **Choose file**.
6. Select the `stack.yaml` file from the cloned repo on your machine, and click **Upload**.
7. Click **Next**.
8. Enter a **Stack name**, e.g., `monte-carlo-stack`
9. Optionally, change the **Parameter** named *Prefix*.
10. Click **Next**.
11. Click **Next**.
12. On the **Review and create** page, check the box at the bottom indicating that an IAM Role will be created.
13. Click **Submit**.

# Run the Application

1. In the AWS console, open Step Functions.
2. Select the pipeline Step Function named similar to the following: `mcs-monte-carlo-pipeline-`.
3. Click **Start execution**.
4. Click **Start execution** again.

The entire pipeline should only take ~20 seconds to run.

### Verify the Results

1. In the AWS console, open S3.
2. Select the S3 bucket prefixed with the following: `mcs-destination-`.
3. Check the `results.csv` file, and click **Download**.

The downloaded file will have the parsed and aggregated results of the simulation, with contents resembling the following. 

```
num_doors,strategy,result
3,switch,won
3,stick,won
3,stick,lost
...
```

There will be one row per simulation.

Each row in the file will contain the static input variable (number of doors), the random input variable (strategy), and the result of the model--won or lost.

# Clean Up

1. In the AWS console, open Step Functions.
2. Select the **State machine** prefixed with the following: `mcs-monte-carlo-delete-data-pipeline-`.
3. Click **Start execution**.  Click **Start execution** again.  
   **NOTE:** This deletes all data from both S3 buckets which allows the stack to be deleted.
4. After execution has completed, in the AWS console, open CloudFormation.
5. Select the stack.
6. Click **Delete**.
