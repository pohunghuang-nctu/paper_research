curl -X POST --header "Content-Type: application/json" \
--data '{
  "service_key": "VHCcJeXPakRfwjdGIHrn5iKif94=",
  "query_requests": [
    {
      "data_source": "QUERY_DATA_SOURCE_USER_DATA",
      "selections": [
        {
          "field": "num_acceptances",
          "name": "total_acceptances",
          "aggregation_function": "QUERY_AGGREGATION_SUM"
        },
        {
          "field": "num_lines_accepted",
          "name": "total_lines",
          "aggregation_function": "QUERY_AGGREGATION_SUM"
        }
      ],
      "filters": [
        {
          "name": "hour",
          "filter": "QUERY_FILTER_GE",
          "value": "2025-07-15"
        },
        {
          "name": "hour",
          "filter": "QUERY_FILTER_LE",
          "value": "2025-08-06"
        }
      ],
      "aggregations": [
        {
          "field": "api_key",
          "name": "user_hash"
        }
      ]
    }
  ]
}' \
https://server.codeium.com/api/v1/Analytics