curl -X POST --header "Content-Type: application/json" \
--data '{
  "service_key": "<YOUR_SERVICE_KEY>",
  "query_requests": [
    {
      "data_source": "QUERY_DATA_SOURCE_PCW_DATA",
      "selections": [
        {
          "field": "user_bytes",
          "name": "user_bytes",
          "aggregation_function": "QUERY_AGGREGATION_UNSPECIFIED"
        },
        {
          "field": "total_bytes",
          "name": "total_bytes",
          "aggregation_function": "QUERY_AGGREGATION_UNSPECIFIED"
        }
      ]
    }
  ]
}' \
https://server.codeium.com/api/v1/Analytics
