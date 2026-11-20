# Practical 7 — Flink Watermark Handling — Late Data

Based on the uploaded **BD Practical Journal**. The source text below is kept for reference; the separate code files were extracted from that journal.

## Files

- `latedata.py`

## Step-by-step execution (Windows PowerShell)

1. Install compatible Java/Python/PyFlink versions.
2. Run `python -m pip install apache-flink`.
3. Run `python latedata.py`.
4. Inspect the main window output and side output for late data.

## Expected result

Main output and a separately routed late event, depending on watermark advancement.

## Important note

The code is transcribed from the journal; whether the synthetic late event reaches the side output can depend on the runtime's watermark scheduling.

## Original journal text (reference)

This section preserves the text extracted from the uploaded document. Screenshots/figures are not embedded here.

```text
Practical 7

Q.1 Watermark Handling: Create a stream processor that correctly handles "Late
Data" using watermarks and side outputs.

Create a folder,create a file named latedata.py
Code:

from pyflink.common import Types, WatermarkStrategy, Duration
from pyflink.common.watermark_strategy import TimestampAssigner
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.output_tag import OutputTag
from pyflink.datastream.window import TumblingEventTimeWindows
from pyflink.common.time import Time



class EventTimestampAssigner(TimestampAssigner):
    def extract_timestamp(self, value, record_timestamp):
        return value[1]



env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)    # keeps ordering deterministic for the demo


events = [
    ("Picked up", 1000),
    ("At restaurant", 8000),
    ("Order confirmed", 3000),
    ("Delivered", 22000),
    ("Late scan", 2000),    # arrives after watermark passes 10s -> late
]


data = env.from_collection(
    events,
    type_info=Types.TUPLE([Types.STRING(), Types.LONG()])
)


watermarks = (
    WatermarkStrategy
    .for_bounded_out_of_orderness(Duration.of_seconds(2))
    .with_timestamp_assigner(EventTimestampAssigner())
)


stream = data.assign_timestamps_and_watermarks(watermarks)


late_tag = OutputTag(
    "late_events",
    Types.TUPLE([Types.STRING(), Types.LONG()])
)


main = (
    stream
    .key_by(lambda e: "delivery", key_type=Types.STRING())
    .window(TumblingEventTimeWindows.of(Time.seconds(10)))
    .side_output_late_data(late_tag)
    .reduce(
           lambda a, b: a,
           output_type=Types.TUPLE([Types.STRING(), Types.LONG()])
    )
)


late = main.get_side_output(late_tag)
main.print("main")
late.print("late")


env.execute("Food Delivery Late Data")



In terminal run:
python -m pip install apache-flink
And then run code using: python latedata.py

Output:
```
