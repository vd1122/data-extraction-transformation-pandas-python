
```
This tool do data validation/cleanup/conrrection based on config settings give in json format.

This toll give data processing report in json format for further use. 

This tool is extendable for new validation checks and data transformation.

TODO:

- Documenation
- Robust error handling
- Test cases 
```

Below sections cover information about -
```
1. Script run
2. Stdout
3. Project directory structure
``` 

> Script Run
```
python process_data.py
```
> Stdout
```
Please enter dirty data file. default is:  [data/data-dirty.csv]:
--------------------------------------------------------------------------------
Input/Output files
--------------------------------------------------------------------------------
Dirty data file:                    data/data-dirty.csv
Clean data output file:             data/data-clean.csv
Cleanup rules file:                 data_rules/data_cleanup_rules.json
Validation rules file:              data_rules/data_validation_rules.json
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
Pre data cleanup validation report [JSON format]
--------------------------------------------------------------------------------
{
    "fail": [
        {
            "check": "no_dups",
            "msg": "ERROR: Dataset has duplicates."
        },
        {
            "check": "no_nans",
            "msg": "ERROR: Dataset contains NANs."
        },
        {
            "check": "col_no_nans",
            "msg": "ERROR: Column [account_type] has NANs."
        },
        {
            "check": "col_no_nans",
            "msg": "ERROR: Column [age] has NANs."
        },
        {
            "check": "col_valid_values",
            "msg": "ERROR: Column [account_type] has values not matching ^(?:google|facebook|other)$."
        },
        {
            "check": "col_valid_values",
            "msg": "ERROR: Column [age] has values not matching ^[0-9]{1,2}$."
        }
    ],
    "pass": []
}



--------------------------------------------------------------------------------
Post data cleanup validation report [JSON format]
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
Post data cleanup validation report [JSON format]
--------------------------------------------------------------------------------
{
    "fail": [],
    "pass": [
        {
            "check": "no_dups",
            "msg": "OK: Dataset does not contain duplicate reecords."
        },
        {
            "check": "no_nans",
            "msg": "OK: Dataset does not contain NANs."
        },
        {
            "check": "col_no_nans",
            "msg": "OK: Column [account_type] has no NANs."
        },
        {
            "check": "col_no_nans",
            "msg": "OK: Column [age] has no NANs."
        },
        {
            "check": "col_valid_values",
            "msg": "OK: Column [account_type] has all values matching ^(?:google|facebook|other)$."
        },
        {
            "check": "col_valid_values",
            "msg": "OK: Column [age] has all values matching ^[0-9]{1,2}$."
        }
    ]
}


*** Clean data file path is: data/data-clean.csv

```

> Project Directory Structure -
```.
├── README.md
├── data
│   ├── data-clean.csv
│   └── data-dirty.csv
├── data-dirty.csv
├── data_rules
│   ├── data_cleanup_rules.json
│   └── data_validation_rules.json
├── modules
│   ├── data_cleanup.py
│   └── data_validation.py
└── process_data.py

```
