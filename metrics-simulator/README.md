# Metrics Simulator

A load testing tool that simulates user behavior and generates metrics for the ShopNexus application.

## Features

- Realistic user behavior simulation
- Concurrent user simulation
- Configurable load percentage
- Configurable error rate
- Detailed logging
- Error simulation with different types:
  - Rate limit errors (40% of errors)
  - Invalid data errors (30% of errors)
  - Server errors (20% of errors)
  - Timeout errors (10% of errors)

## Configuration

The simulator can be configured using environment variables:

- `LOAD_PERCENTAGE`: Controls the number of concurrent users (default: 50%)
- `ERROR_PERCENTAGE`: Controls the error rate (default: 2%)

## Running the Simulator

1. Build the Docker image:
```bash
docker build -t metrics .
```

2. Run the simulator with default settings (50% load, 2% error rate):
```bash
docker run --network shopnexus_shopnexus-net -d --name metrics-simulator metrics
```

3. Run with custom load and error rate:
```bash
docker run --network shopnexus_shopnexus-net -d --name metrics-simulator \
  -e LOAD_PERCENTAGE=75 \
  -e ERROR_PERCENTAGE=5 \
  metrics
```

4. View logs:
```bash
docker logs -f metrics-simulator
```

5. Stop the simulator:
```bash
docker stop metrics-simulator
```

## Simulated Actions

The simulator performs the following actions for each user session:

1. User Operations:
   - Registration (30% chance)
   - Login
   - Profile retrieval

2. Product Operations:
   - Browse products
   - Create product
   - Update product
   - Delete product

## Error Simulation

The simulator includes realistic error scenarios:

- Rate limit errors (40% of errors)
  - Simulates API rate limiting
  - Adds 0.1s delay

- Invalid data errors (30% of errors)
  - Simulates validation failures
  - Returns immediately

- Server errors (20% of errors)
  - Simulates internal server errors
  - Adds 0.2s delay

- Timeout errors (10% of errors)
  - Simulates request timeouts
  - Adds 2s delay

## Metrics Dashboard

The simulator works with the Grafana dashboard to display:

- Request rates
- Average response times
- Error rates
- Total requests

## Best Practices

1. Start with default settings (50% load, 2% error rate)
2. Monitor system performance
3. Adjust load and error rates based on testing needs
4. Use the metrics dashboard to analyze results
5. Check logs for detailed operation information

## Network Requirements

The simulator must be connected to the `shopnexus_shopnexus-net` network to communicate with:
- User service
- Product service
- Prometheus
- Grafana 