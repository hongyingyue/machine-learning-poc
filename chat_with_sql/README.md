# text2sql

## qiuck start
```shell
pip install langchain_community --quiet
pip install "langchain[openai]" --quiet
```

```shell
python text2sql_demo.py
```

**Output**
```text
SELECT "Team" FROM nba_roster WHERE "NAME" = 'Stephen Curry';

[('Golden State Warriors',)]

SELECT "SALARY" FROM nba_roster WHERE "NAME" = 'Stephen Curry';

[('$51,915,615',)]
```
