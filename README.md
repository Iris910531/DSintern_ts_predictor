# aie_ts_predictor
The time-series predictor for Family Mart after-game prediction


# Known Issue
- use Pandas==1.5.3, newer version will trigger error on sum over datetime64ns
- check IP address for porduction environment
- should disable assert csv written in ts_predictor.py

# user guide
### build container
```shell
docker build -t fami_predictor:latest .
```

### execution
```python
python3 ts_predictor.py  --output_file <OUTPUT_FILE_PATH> --timestamp <10-DIGIT-TIMESTAMP>
```
