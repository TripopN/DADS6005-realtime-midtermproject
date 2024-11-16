# Kafka Setup with Docker and ksqlDB on AWS EC2

This guide will walk you through the steps to set up Kafka on Docker in an AWS EC2 instance, generate mock data, and process the streams using ksqlDB. By following these instructions, you will have a fully operational Kafka setup for streaming data.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setting Up Docker on AWS EC2](#setting-up-docker-on-aws-ec2)
3. [Configuring Kafka Topics](#configuring-kafka-topics)
4. [Configuring Data Generation](#configuring-data-generation)
5. [Accessing and Using ksqlDB](#accessing-and-using-ksqldb)
6. [Conclusion](#conclusion)

---

## Prerequisites

Before you begin, make sure you have the following:

- An AWS EC2 instance running Ubuntu.
- Docker installed on the EC2 instance.
- Kafka Docker images available (as part of your `docker-compose.yml`).
- Basic knowledge of Docker and Kafka.

---

## Setting Up Docker on AWS EC2

### 1. Copy Docker Compose Files to EC2

Start by copying the `docker-compose.yml` and schema files to your EC2 instance.

```bash
scp -i Tripop_test.pem docker-compose.yml ubuntu@ec2-54-255-209-170.ap-southeast-1.compute.amazonaws.com:/home/ubuntu
scp -i Tripop_test.pem user_page_views_schema.json user_page_views_table.json ubuntu@ec2-54-255-209-170.ap-southeast-1.compute.amazonaws.com:/home/ubuntu

## To be continued.......
