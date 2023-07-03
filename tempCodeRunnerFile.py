    SELECT ?path
    WHERE {{
      wd:{start_entity_id} (<>|!<>)* ?path .
      ?path (<>|!<>)* wd:{end_entity_id} .
    }}
    LIMIT {max_hops}