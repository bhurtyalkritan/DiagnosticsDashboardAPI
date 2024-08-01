# Vehicle Data API

This API provides endpoints for retrieving voltage data, vehicle types, and vehicle specifications for electric vehicles.

## Table of Contents
1. [Base URL](#base-url)
2. [Endpoints](#endpoints)
   - [Get Voltage Data](#1-get-voltage-data)
   - [Get Voltage Data by Timestamp](#2-get-voltage-data-by-timestamp)
   - [Get Voltage Data Range](#3-get-voltage-data-range)
   - [Get Voltage Alerts](#4-get-voltage-alerts)
   - [Get Vehicle Types](#5-get-vehicle-types)
   - [Get Vehicle Specifications](#6-get-vehicle-specifications)
   - [Set Voltage Threshold](#7-set-voltage-threshold)
3. [Error Responses](#error-responses)

## Base URL

`http://127.0.0.1:8001`

## Endpoints

### 1. Get Voltage Data

- **URL:** `/voltage`
- **Method:** GET
- **Query Parameters:** `records` (optional, default: 100)
- **Response:** JSON object with voltage data records

### 2. Get Voltage Data by Timestamp

- **URL:** `/voltage/{timestamp}`
- **Method:** GET
- **URL Parameters:** `timestamp` (ISO format: YYYY-MM-DDTHH:MM:SSZ)
- **Response:** JSON object with voltage data for the specified timestamp

### 3. Get Voltage Data Range

- **URL:** `/voltage/range`
- **Method:** GET
- **Query Parameters:** 
  - `start_time` (ISO format)
  - `end_time` (ISO format)
- **Response:** JSON object with voltage data records within the specified range

### 4. Get Voltage Alerts

- **URL:** `/voltage/alerts`
- **Method:** GET
- **Response:** JSON array of voltage alerts

### 5. Get Vehicle Types

- **URL:** `/vehicle/types`
- **Method:** GET
- **Response:** JSON array of vehicle types and their counts

### 6. Get Vehicle Specifications

- **URL:** `/vehicle/specs`
- **Method:** GET
- **Response:** JSON array of vehicle specifications

### 7. Set Voltage Threshold

- **URL:** `/voltage/threshold`
- **Method:** POST
- **Request Body:** JSON object with `lower_bound` and `upper_bound`
- **Response:** JSON object confirming the new voltage threshold

## Error Responses

- 400 Bad Request: Invalid parameters
- 404 Not Found: Requested resource not found

Error responses include a JSON object with a `detail` field explaining the error.
