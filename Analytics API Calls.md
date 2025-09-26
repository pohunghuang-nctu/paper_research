https://server.codeium.com/api/v1/Analytics

{  
 "service\_key": "YOUR\_SERVICE\_KEY",  
 "query\_requests": \[  
   {  
     "data\_source": "QUERY\_DATA\_SOURCE\_CASCADE\_LINES\_ANALYTICS",  
     "selections": \[  
       { "field": "api\_key", "name": "api\_key" },  
       { "field": "email", "name": "email" },  
       { "field": "hour", "name": "hour" },  
{ "field": "lines\_accepted", "name": "lines\_accepted" },  
       { "field": "cascade\_insertions", "name": "cascade\_insertions" }  
     \],  
    "filters": \[  
       {   
         "name": "hour",   
         "filter": "QUERY\_FILTER\_GE",   
         "value": "START\_DATE"   
       },   
       {   
         "name": "hour",   
         "filter": "QUERY\_FILTER\_LE",   
         "value": "END\_DATE"   
       }  
    \]  
   }  
 \]  
}  
